# Third-party components and design sources

## Installed components

### Ponytail

- Source: https://github.com/DietrichGebert/ponytail
- Pinned commit: `2ed6c52c9d7e5e56942508591085fd45dea277d3`
- Installed files: `skills/ponytail/SKILL.md`, `LICENSE`
- License: MIT

### SimpleEnglish

- Source: https://github.com/AminBlg/SimpleEnglish
- Pinned commit: `59bf6702197a5aadc96d197ea17f290d8d50dcd3`
- Installed files: the Simple English skill, its two reference files, and `LICENSE`
- License: MIT

### RepoWise

- Source: https://github.com/repowise-dev/repowise
- Pinned runtime version: `0.41.0`
- License: AGPL-3.0-only
- Integration: separate `uvx` process and MCP server
- RepoWise is not copied into or linked with this kit.

## Optional components

### GitHub Spec Kit

- Source: https://github.com/github/spec-kit
- License: MIT
- Status: optional and not installed by default

### Compound Engineering

- Source: https://github.com/EveryInc/compound-engineering-plugin
- Reviewed commit: `05f3b798b0e5fb76c6bb1830bee7cbc84ff6c4c4`
- License: MIT
- Status: optional and not bundled
- Relevant ideas: risk-selected reviewer personas, structured finding synthesis, adversarial code review, adversarial document review

### Superpowers

- Source: https://github.com/obra/superpowers
- Reviewed commit: `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`
- License: MIT
- Status: optional and not bundled
- Relevant ideas: clean-context review packets, fresh task reviewers, design approval before implementation

### Trail of Bits Skills

- Source: https://github.com/trailofbits/skills
- License: CC BY-SA 4.0
- Status: optional and not bundled
- Relevant tools: differential review, property-based testing, spec-to-code compliance, sharp-edge analysis, mutation testing, second opinion

### ADHD

- Source: https://github.com/UditAkhourii/adhd
- License: MIT
- Status: optional and not bundled
- Relevant idea: isolated divergent architecture exploration with trap detection

### NeuroArxiv

- Source: https://github.com/UditAkhourii/neuroarxiv
- License: MIT
- Status: optional and not bundled
- Relevant idea: real arXiv prior-art search with isolated paper reads and one selected path

## Original kit skills

`design-preflight` and `adversarial-review` are original, small Codex skills written for this kit.

They apply general process ideas from the projects above. They do not copy those projects' large skill bodies, helper scripts, or orchestration engines.
