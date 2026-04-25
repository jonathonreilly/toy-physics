# Codex Machine Dump

**Capture date:** 2026-04-25

**Capture workspace:** `/Users/jonreilly/Projects/Physics`

**Codex home:** `/Users/jonreilly/.codex`

This file is a raw machine-side inventory for the Codex/OpenAI half of the
workflow. It is intentionally machine-local and unsanitized.

---

## 1. Top-level Codex state objects

```text
/Users/jonreilly/.codex/desktop.sqlite
TYPE file SIZE 0
/Users/jonreilly/.codex/logs_2.sqlite
TYPE file SIZE 553996288
/Users/jonreilly/.codex/.codex-global-state.json
TYPE file SIZE 89072
/Users/jonreilly/.codex/AGENTS.md
TYPE file SIZE 0
/Users/jonreilly/.codex/archived_sessions
TYPE dir FILES 1253
/Users/jonreilly/.codex/sessions
TYPE dir FILES 1010
/Users/jonreilly/.codex/state
TYPE dir FILES 3
/Users/jonreilly/.codex/plugins/cache
TYPE dir FILES 190
```

## 2. Representative `.codex` file inventory

First visible file inventory from `find /Users/jonreilly/.codex -maxdepth 2`:

```text
/Users/jonreilly/.codex/.codex-global-state.json
/Users/jonreilly/.codex/.codex-global-state.json.bak
/Users/jonreilly/.codex/.personality_migration
/Users/jonreilly/.codex/.tmp/app-server-remote-plugin-sync-v1
/Users/jonreilly/.codex/.tmp/plugins.sha
/Users/jonreilly/.codex/AGENTS.md
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-05T15-03-57-019cbf99-8dd5-7861-a03d-482d17520ca9.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-05T17-39-02-019cc027-8857-7cc0-8870-d246a6a39e19.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-05T18-58-39-019cc070-5a09-7102-b683-350155774be7.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-07T16-56-03-019cca4c-e72a-7710-b214-17f5e2673c8d.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-07T17-20-27-019cca63-3c29-7d13-adb2-f35692a21703.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-07T18-18-41-019cca98-8bd6-7562-81bf-0f5e293d9153.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-07T21-41-50-019ccb52-864f-7491-8987-970c52632f46.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-08T07-31-25-019ccd37-63f6-73f0-bd75-67601b8658b6.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-08T07-33-45-019ccd39-88ed-7bf3-a2c2-98409ab29dc5.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-08T11-00-04-019ccdf6-5697-7670-ba7d-14764d7dc6c1.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-08T12-47-29-019cce58-bf2d-7f40-9262-aaecddf2237a.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-11T13-16-57-019cdde6-d017-7523-b934-e1c5721ebfb4.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-13T07-50-04-019ce708-43df-74f2-b270-949389d45a14.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-14T09-05-06-019cec73-5074-7d63-b279-0c6b61d4099f.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-21T09-02-37-019d107d-9195-7881-b046-841310be49d2.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-21T10-02-54-019d10b4-befe-7662-946f-86697382cffa.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-21T11-02-55-019d10eb-b33c-78b1-9b9f-e6e452a7cd05.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-21T12-02-54-019d1122-9e59-7a70-8a5e-4fa48db71d02.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-21T13-02-55-019d1159-8f2a-7363-82fb-18d738704a8c.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-21T14-02-56-019d1190-83df-72e0-a34e-368e01ca1ef5.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-21T15-02-56-019d11c7-729a-7432-b62f-b24385a8ea71.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-21T16-02-58-019d11fe-66cb-70e1-89e0-ee333d3889bc.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-21T17-02-59-019d1235-5826-7632-b7f8-bee1b6c2fab4.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-21T18-02-59-019d126c-4937-7412-8b10-a618b7904b69.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-21T19-07-26-019d12a7-4840-7a02-ae2b-6cc40fa8003e.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-21T20-07-25-019d12de-3420-7c31-bfa5-7da1ae0dd24c.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-21T21-07-26-019d1315-2702-7b20-bd1f-460609a0d84e.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-21T22-07-27-019d134c-1aee-7d03-b422-4f8849ea0af2.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-21T23-14-39-019d1389-9f3b-7ba3-b4d1-91a06c4aaa7a.jsonl
/Users/jonreilly/.codex/archived_sessions/rollout-2026-03-22T00-14-37-019d13c0-852f-7400-a0c3-7a477a6191ac.jsonl
... many more omitted in this first raw pass ...
```

## 3. Physics-scoped session store examples

Representative physics-scoped session files observed under
`/Users/jonreilly/.codex/sessions/2026/04/25/`:

```text
/Users/jonreilly/.codex/sessions/2026/04/25/rollout-2026-04-25T09-14-37-019dc4c7-1e77-77b1-a3e4-4179a92cf5a8.jsonl
/Users/jonreilly/.codex/sessions/2026/04/25/rollout-2026-04-25T09-22-23-019dc4ce-3d97-7e21-8497-df48c0db194b.jsonl
/Users/jonreilly/.codex/sessions/2026/04/25/rollout-2026-04-25T09-22-24-019dc4ce-3e5b-7421-b20d-cf083ae74c10.jsonl
/Users/jonreilly/.codex/sessions/2026/04/25/rollout-2026-04-25T09-22-24-019dc4ce-3f3d-7f90-8c88-52427e262679.jsonl
```

These four files already show one top-level Codex orchestration thread plus
three spawned subagents.

## 4. Current-day Codex worktree target in raw session capture

Representative current worktree path used in Codex raw session capture:

```text
/Users/jonreilly/.codex/worktrees/8805/CL3Z3 new work
```

This path appears directly in the raw session JSONL as the working directory
for the April 25 multi-agent exploration thread.
