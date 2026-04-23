# Ali Architecture

Goal: one assistant identity across many computers without turning all machine-local observations into one polluted memory soup.

## 1. Shared layer: the parts that make Ali feel like the same assistant everywhere

Keep these shared in git:
- identity docs
- shared skills
- playbooks and operating procedures
- stable knowledge notes
- cross-node lessons that have been deliberately promoted from a local journal into shared knowledge

In practice, this `ali/` folder is the seed of that shared layer.

## 2. Local layer: the machine brain

Every node gets its own Hermes profile, for example:
- `~/.hermes/profiles/ali-mac-studio/`
- `~/.hermes/profiles/ali-r730/`
- `~/.hermes/profiles/ali-cosmos/`

Each profile keeps its own:
- sessions
- memory
- local config deltas
- machine-specific skills
- local environment secrets

This is the machine body and autobiographical memory for that node.

## 3. Shared adventures, separate journals

Do not merge every raw memory into one global store.

Instead, journal by node, for example:
- `ali/journal/mac-studio/`
- `ali/journal/r730/`
- `ali/journal/cosmos/`

Recommended promotion flow:
1. Node experiences something locally.
2. The event gets summarized into that node's journal.
3. If the lesson is machine-specific, it stays there.
4. If the lesson is reusable, promote it into:
   - a shared skill,
   - a playbook,
   - or a stable knowledge note.

## 4. Skills policy

Shared skills:
- portable workflows
- repo conventions
- cross-node operating procedures
- the Ali identity/operating model

Local-only skills:
- hardware quirks
- service restart specifics for one machine
- path conventions unique to one node
- GPU/runtime oddities that should not be generalized

## 5. What makes Ali "the same assistant"

Shared identity comes from:
- common personality docs
- common operating skill(s)
- common repo and notes
- common conventions about memory promotion

Separate identity drift is prevented by:
- keeping local memories local,
- journaling per node,
- and only promoting reusable lessons into the shared layer.

## 6. Recommended repo conventions

Suggested structure:

```text
ali/
  README.md
  ALI-ARCHITECTURE.md
  NEW-NODE-BOOTSTRAP.md
  NEW-NODE-PROMPT.md
  bootstrap-node.sh
  bootstrap/
    ali-secrets.local.env        # local only, gitignored
    config.current.yaml          # local only, gitignored
  shared/
    skills/
      ali-operating-model/
        SKILL.md
  journal/
    <node-name>/
  knowledge/
  playbooks/
  nodes/
    <node-name>/
      README.md
```

## 7. Operational rule of thumb

Promote facts according to stability:
- transient/local fact -> local memory or local node journal
- repeatable workflow -> shared skill
- stable cross-node fact -> shared knowledge note
- user preference/personality -> shared identity docs, not node memory

## 8. Bootstrapping rule

A new machine should be able to go from vanilla Hermes to Ali by doing three things:
1. get credentials and baseline config,
2. clone the shared repo,
3. create a dedicated `ali-<node-name>` profile and install the Ali operating skill into that profile.

The provided `bootstrap-node.sh` automates exactly that.
