# New Node Bootstrap

This file is the human-readable version of the Ali onboarding process.

## Outcome

After running the bootstrap, the target machine will have:
- a dedicated Hermes profile named `ali-<node-name>`
- the current baseline config copied from the source machine snapshot
- the current `.env` secrets copied into the node profile
- git credentials configured for GitHub access
- the shared workspace repo cloned or updated
- the `ali-operating-model` skill installed into that node profile
- a node-specific journal and node README scaffold inside the repo

## Files used by the bootstrap

- `ali/bootstrap/ali-secrets.local.env`
- `ali/bootstrap/config.current.yaml`
- `ali/shared/skills/ali-operating-model/SKILL.md`
- `ali/bootstrap-node.sh`

## Fast path on a new machine

1. Install Hermes normally.
2. Copy the full `ali/` folder from the source machine, or clone the repo if credentials are already available.
3. On the new machine, run:

   ```bash
   cd ~/hermes-workspace/ali
   bash bootstrap-node.sh
   ```

4. Start Ali on that machine:

   ```bash
   hermes --profile ali-$(hostname -s) -s ali-operating-model
   ```

5. Feed the contents of `NEW-NODE-PROMPT.md` into the first session.

## Security note

`ali/bootstrap/ali-secrets.local.env` contains real credentials from the source machine and is intentionally gitignored. Do not commit it.
