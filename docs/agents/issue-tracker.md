# Issue tracker: GitHub

Issues and specs for this repository live as GitHub issues. Use the `gh` CLI for all operations.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`.
- **Read an issue**: `gh issue view <number> --comments`, including its labels.
- **List issues**: `gh issue list --state open` with appropriate label and state filters.
- **Comment on an issue**: `gh issue comment <number> --body "..."`.
- **Apply or remove labels**: `gh issue edit <number> --add-label "..."` or `--remove-label "..."`.
- **Close an issue**: `gh issue close <number> --comment "..."`.

Infer the repository from `origin`; `gh` does this automatically when run inside the repository.

## Pull requests as a triage surface

**PRs as a request surface: no.**

When a skill says "publish to the issue tracker", create a GitHub issue. When it says "fetch the relevant ticket", run `gh issue view <number> --comments`.
