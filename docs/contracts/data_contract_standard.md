# Data Contract Standard (v1)

## 1. Scope
This standard defines how data producers and consumers exchange canonical investment data within the platform.

Applies to:
- Ingestion payloads entering Bronze.
- Canonical normalized records in Silver.
- Analytics-ready records in Gold.

## 2. Contract metadata (required)
Every dataset must declare:
- `contract_name` (stable identifier)
- `owner_team` (responsible team)
- `domain` (`market_data`, `events`, `news`, `portfolio`, `signals`)
- `schema_version` (semantic version `MAJOR.MINOR.PATCH`)
- `classification` (`public`, `internal`, `licensed`, `restricted`)
- `source_system`
- `refresh_mode` (`streaming`, `batch`, `micro_batch`)
- `sla_freshness_minutes`
- `primary_keys`
- `event_time_field`
- `pii_present` (`true`/`false`)

## 3. Schema evolution rules
- Additive, backward-compatible fields: **minor** bump.
- Documentation-only clarifications: **patch** bump.
- Field removal/type changes/semantic shifts: **major** bump.
- A published schema version is immutable.

## 4. Required technical fields
All canonical records must include:
- `event_id` (UUID)
- `as_of_time` (UTC timestamp)
- `ingested_at` (UTC timestamp)
- `source_name`
- `source_record_id`
- `schema_version`

## 5. Data quality gates
Minimum checks for Bronze -> Silver promotion:
1. Schema validation pass rate >= 99.5%
2. Primary key uniqueness violations = 0
3. Required field null rate <= 0.5%
4. Event timestamp parse success = 100%
5. Duplicate ratio below contract-defined threshold

Minimum checks for Silver -> Gold promotion:
1. Reference integrity (instrument keys resolvable) >= 99.9%
2. Freshness within SLA for contract
3. Derived metric sanity checks pass

## 6. Retention and reproducibility
- Bronze raw immutable retention: 7 years (default).
- Silver/Gold support time-travel snapshots for backtesting and audit.
- Derived artifacts (features/signals/recommendations) must store source lineage references.

## 7. Access and licensing controls
- `licensed` and `restricted` contracts require explicit entitlement checks.
- Redistribution is controlled by source license terms.
- All access must be auditable.

## 8. Validation integration pattern
- Producer-side: validate before publishing.
- Ingestion-side: validate before Bronze write where feasible.
- Transform-side: revalidate before Silver/Gold write.
- Failures route to dead-letter storage with reason codes.
