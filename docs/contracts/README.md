# Phase 0 - Step 1: Canonical Schemas & Data Contracts

This folder executes the first roadmap step from `docs/investment_engine_architecture_plan.md`:

- **Define canonical schemas and data contracts**.

## What is included

1. `data_contract_standard.md`
   - Contract metadata requirements.
   - Schema lifecycle and versioning rules.
   - Data quality gates for Bronze/Silver/Gold transitions.

2. `schemas/*.schema.json`
   - JSON Schemas for the canonical entities defined in the architecture plan:
     - instrument master
     - corporate events
     - news events
     - market bars
     - fundamentals
     - portfolio snapshots
     - signals
     - recommendations

## Intended usage

- Producers validate payloads at publish time.
- Consumers validate payloads at ingest and before Silver promotion.
- Contract versions are immutable once published.
- Breaking changes require a major version bump.

## Branching note
- Current implementation branch is intended to be merged into `master` via pull request.
