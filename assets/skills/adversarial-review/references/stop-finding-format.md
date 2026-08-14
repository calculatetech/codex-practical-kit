# Stop finding format

Render every validated stop finding as a separate block. Preserve reviewer order. Do not combine findings into one decision handoff.

```markdown
### Finding <id> — <severity> — <title>

Location: <source locations>

Decision

<The decision that requires human direction.>

Term

<Optional. Define one unfamiliar term. Remove this label when no definition is necessary.>

Trigger

<The supported normal-use trigger.>

Likelihood

<already present | likely | unlikely | unknown>. <Evidence.>

Current exposure

<yes | no | unknown>. <One factual reason.>

Options

1. <Option.>

   Effect: <Result of this option.>

2. <Option.>

   Effect: <Result of this option.>

Recommendation

<One option and its reason.>

Question

<One exact question for this finding.>
```

Repeat the complete block for each finding. Do not use cumulative `Trigger`, `Options`, `Recommendation`, or `Question` sections.
