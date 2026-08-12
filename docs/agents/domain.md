# Domain docs

How engineering skills should consume this repository's domain documentation.

## Before exploring

- Read `CONTEXT.md` at the repository root when it exists.
- Read relevant decisions in `docs/adr/`.

If these files do not exist, proceed silently. Create them only when domain terms or architectural decisions are actually resolved.

## Layout

This is a single-context repository:

```text
/
├── CONTEXT.md
├── docs/
│   └── adr/
└── src/
```

## Vocabulary and decisions

Use terms as defined in `CONTEXT.md`. If a needed concept is missing, reconsider whether the repository already uses a different term or record the gap for domain modelling. Surface any conflict with an existing ADR instead of silently overriding it.
