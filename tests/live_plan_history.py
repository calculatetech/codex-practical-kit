#!/usr/bin/env python3
"""Run one authenticated Codex Plan acceptance check."""

import json
import os
import queue
import subprocess
import tempfile
import threading
import time
from pathlib import Path


class AppServer:
    def __init__(self):
        self.process = subprocess.Popen(
            ["codex", "app-server", "-c", "mcp_servers={}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1,
        )
        self.messages = queue.Queue()
        self.notifications = []
        self.next_id = 1
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        assert self.process.stdout is not None
        for line in self.process.stdout:
            self.messages.put(json.loads(line))

    def send(self, method: str, params: dict) -> dict:
        request_id = self.next_id
        self.next_id += 1
        self._write({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params})
        deadline = time.monotonic() + 120
        while True:
            try:
                message = self.messages.get(timeout=max(0.1, deadline - time.monotonic()))
            except queue.Empty as exc:
                raise RuntimeError(f"Codex app-server timed out during {method}") from exc
            if message.get("id") == request_id:
                if "error" in message:
                    raise RuntimeError(f"Codex app-server {method} failed: {message['error']}")
                return message["result"]
            self.notifications.append(message)

    def notify(self, method: str, params: dict) -> None:
        self._write({"jsonrpc": "2.0", "method": method, "params": params})

    def wait(self, method: str, turn_id: str, event_name: str | None = None) -> dict:
        deadline = time.monotonic() + 300
        while True:
            for index, message in enumerate(self.notifications):
                params = message.get("params", {})
                run = params.get("run", {})
                if message.get("method") == method and (
                    params.get("turn", {}).get("id") == turn_id
                    if event_name is None
                    else params.get("turnId") == turn_id
                    and run.get("eventName") == event_name
                    and run.get("statusMessage") == "Loading practical defaults"
                ):
                    return self.notifications.pop(index)
            try:
                message = self.messages.get(timeout=max(0.1, deadline - time.monotonic()))
            except queue.Empty as exc:
                raise RuntimeError(f"Codex app-server timed out waiting for {method}") from exc
            self.notifications.append(message)

    def _write(self, message: dict) -> None:
        assert self.process.stdin is not None
        self.process.stdin.write(json.dumps(message, separators=(",", ":")) + "\n")
        self.process.stdin.flush()

    def close(self) -> None:
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=10)


def final_response(path: Path, turn_id: str) -> bytes:
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        for line in path.read_text(encoding="utf-8").splitlines():
            record = json.loads(line)
            payload = record.get("payload", {})
            metadata = payload.get("internal_chat_message_metadata_passthrough", {})
            if (
                record.get("type") == "response_item"
                and payload.get("phase") == "final_answer"
                and metadata.get("turn_id") == turn_id
            ):
                return payload["content"][0]["text"].encode()
        time.sleep(0.1)
    raise RuntimeError("Codex did not flush the Plan response to its rollout")


def main() -> None:
    if os.environ.get("CPK_RUN_LIVE_PLAN_HISTORY") != "1":
        raise SystemExit("Set CPK_RUN_LIVE_PLAN_HISTORY=1 to use Codex authentication and model quota.")

    model = os.environ.get("CPK_LIVE_MODEL", "gpt-5.6-luna")
    server = AppServer()
    try:
        server.send(
            "initialize",
            {
                "clientInfo": {"name": "cpk-plan-history", "version": "0.19.1"},
                "capabilities": {"experimentalApi": True},
            },
        )
        server.notify("initialized", {})
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            started = server.send(
                "thread/start",
                {
                    "cwd": str(root),
                    "model": model,
                    "approvalPolicy": "never",
                    "sandbox": "read-only",
                    "ephemeral": False,
                },
            )
            thread = started["thread"]
            settings = {
                "model": model,
                "reasoning_effort": "medium",
                "developer_instructions": None,
            }
            planned = server.send(
                "turn/start",
                {
                    "threadId": thread["id"],
                    "input": [
                        {
                            "type": "text",
                            "text": "Plan one README sentence. Ask no questions. Associate the Plan with no specification.",
                        }
                    ],
                    "collaborationMode": {"mode": "plan", "settings": settings},
                },
            )["turn"]
            server.wait("turn/completed", planned["id"])
            expected = final_response(Path(thread["path"]), planned["id"])

            accepted = server.send(
                "turn/start",
                {
                    "threadId": thread["id"],
                    "input": [{"type": "text", "text": "Implement the plan. Do not use tools."}],
                    "collaborationMode": {"mode": "default", "settings": settings},
                },
            )["turn"]
            server.wait("hook/completed", accepted["id"], "userPromptSubmit")
            records = list((root / ".agent" / "plan-history").glob("*.md"))

            if len(records) != 1 or records[0].read_bytes() != expected:
                raise RuntimeError("acceptance hook did not save the exact Plan before it completed")
            print(f"live Plan acceptance passed with {model}")
    finally:
        server.close()


if __name__ == "__main__":
    main()
