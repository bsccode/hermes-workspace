# Spawn Ali Quickly

This is the fastest path for creating a new Ali node from a vanilla Hermes installation.

## File

- `ali/spawn-ali.sh`

This single file embeds:
- current baseline Hermes config
- a public non-secret bootstrap env template
- the Ali operating skill
- the Ali architecture doc
- the new-node prompt

## Use

1. Install Hermes on the new machine.
2. Copy or download `ali/spawn-ali.sh`.
3. Run:

```bash
bash spawn-ali.sh
```

4. Start Ali:

```bash
hermes --profile ali-$(hostname -s | tr '[:upper:]' '[:lower:]') -s ali-operating-model
```

5. Paste the contents of:

```text
~/hermes-workspace/ali/NEW-NODE-PROMPT.md
```

## Notes

- If you want git credential bootstrapping, fill values in `~/hermes-workspace/ali/bootstrap/ali-secrets.local.env` after running the script.
- Hermes-specific OAuth and provider auth can be configured separately in Hermes itself.
