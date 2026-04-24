# Ali session sync

Goal: keep shared state as current as possible at session start and end without blindly mutating `main`.

## Policy

At session start:
- always `fetch --all --prune`
- fast-forward pull the current branch only when the working tree is clean and non-diverged
- inspect current-node WIP state
- automatically clear the current node's remote WIP branch when it is already merged into the default branch

At session end:
- if the tree is clean, push the current branch when it is only ahead
- if the tree is dirty, checkpoint the entire working tree onto `wip/<node>`
- write `ali/WIP/<node>/STATUS.md` with a compact summary of the unfinished work
- push that WIP branch so other nodes can inspect it if needed

## Why this model

This keeps everyone updated where it is safe to do so:
- clean work stays on the normal branch
- unfinished work stays visible and recoverable
- `main` is not polluted with half-finished commits
- WIP stays node-scoped

## Files and branches

- `ali/session-sync.sh` — implements `start`, `end`, `status`, and `clear`
- `ali/run-ali.sh` — wrapper that runs sync at session start and end around Hermes itself
- `ali/WIP/<node>/STATUS.md` — latest node-scoped WIP summary, committed on the WIP branch
- `wip/<node>` — remote branch holding the current checkpoint for unfinished work on that node

## Recommended use

Start Ali through:

```bash
~/hermes-workspace/ali/run-ali.sh
```

Or run sync manually:

```bash
~/hermes-workspace/ali/session-sync.sh start
~/hermes-workspace/ali/session-sync.sh end
```

## Notes

- WIP branches are automatically deleted only after they are fully merged into the default branch.
- If a branch has diverged, sync reports the state and refuses to auto-merge it.
- If the tree is dirty at start, sync fetches and reports state but skips pull.
