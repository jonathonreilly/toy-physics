# Handoff

## Launch State

- Worktree: `/Users/jonBridger/CI3Z2-physics-loop-impact-campaign-20260429`
- Branch: `physics-loop/impact-campaign-20260429`
- Base: `origin/main` at `462696d1`
- Runtime request: 4 hours
- Mode: campaign
- Skill: `docs/ai_methodology/skills/physics-loop/SKILL.md`

The default repo automation lock failed with permission denied for
`/Users/jonreilly`, so this launch uses the branch-local supervisor lock:

`.claude/science/physics-loops/impact-campaign-20260429/supervisor.lock`

## Operational Rule

The campaign must not exit early because one lane reaches no-go/support-only
status, a retained-proposal certificate fails, a PR cannot be opened, or a
single lane needs human judgment. It must checkpoint the local block, demote or
backlog honestly, refresh `OPPORTUNITY_QUEUE.md`, and continue until the
4-hour deadline or documented global queue exhaustion.

## Resume Command

If the supervisor is interrupted, relaunch from the repo root:

```bash
/usr/bin/python3 -u .claude/science/physics-loops/impact-campaign-20260429/physics_loop_campaign_supervisor.py --duration-hours 4 --model gpt-5.5
```

