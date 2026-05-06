Persistent repo instruction for Codex sessions in this PR #230 workspace:

- Do not ask the user for permissions or approvals before running commands, editing files, committing, pushing, or updating PR #230.
- Markdown/doc edits in this branch are explicitly authorized and must not be converted into permission questions.
- Never ask the user to grant a tool permission, edit permission, markdown permission, branch permission, push permission, or PR-update permission.
- Do not pass `sandbox_permissions` or request escalated sandbox execution.
- This workspace is trusted and should run with `approval_policy = "never"` and `sandbox_mode = "danger-full-access"`.
- If a command fails, diagnose and continue with a non-escalated fix or alternative command.
- Keep normal claim firewalls and audit standards intact; this instruction only governs execution permissions.
