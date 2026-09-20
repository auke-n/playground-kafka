# Repository Working Agreement

## Language

- Communicate with the user in Ukrainian.
- Write all source code, configuration, documentation content, and code comments in English.

## Context-driven development

Before making a material change, read `docs/context/PROJECT_CONTEXT.md` and the relevant documents in `docs/`.
After a material change, update the context and any affected requirements, backlog items, ADRs, or runbooks in the same change set.

A material change includes an architectural decision, a new capability, a changed deployment or security assumption, a completed backlog item, or a newly discovered constraint. Do not create history-only updates when nothing has changed.

## Engineering workflow

- Keep infrastructure reproducible and reviewable as Terraform plus versioned configuration.
- Keep local development independent from AWS where possible.
- Treat the EC2 deployment as a learning/demo environment, not production.
- Add an ADR before or with an irreversible or consequential technical decision.
- Trace implemented work to a backlog item and functional requirement where applicable.
- Validate changes with the narrowest relevant automated checks and record important operational steps in runbooks.

## Safety

- Never commit credentials, private keys, Terraform state, or real AWS account identifiers.
- Use `.env.example` files for non-secret configuration examples.
- Prefer least-privilege security groups and private service ports.
