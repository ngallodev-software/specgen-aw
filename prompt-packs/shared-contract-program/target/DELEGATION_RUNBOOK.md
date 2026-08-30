# Delegation runbook

Use Agent-Workflow's public prompt-pack and delegation surfaces. SpecGen does not launch workers or own lifecycle state.

Before delegation, verify the pack, source baseline when present, dependencies, result schemas, and evaluation plan.
If a generated target cannot represent the canonical specification faithfully, return to SpecGen rather than patching execution artifacts by hand.
