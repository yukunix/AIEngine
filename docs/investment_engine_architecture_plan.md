# Investment Data Analysis & Decision Engine Architecture Plan (AWS-first, GCP option)

## 1) Goal and scope
Design a cloud-native platform that continuously ingests market and alternative data (exchange announcements, news wires, broker/terminal feeds, Yahoo Finance, price/volume, and open web sources), transforms it into a normalized research dataset, and produces:
- General market insights.
- Strategy-specific insights (factor, value, momentum, event-driven, etc.).
- Portfolio-aware recommendations (alerts, risk, rebalancing candidates) for user-defined holdings and constraints.

---

## 2) Core design principles
1. **Event-driven + batch hybrid**: support both low-latency alerts and end-of-day research jobs.
2. **Data contracts first**: enforce canonical schemas for instruments, events, fundamentals, and news.
3. **Model/feature reproducibility**: version all data, features, models, and prompts.
4. **Multi-tenant security**: isolate user/portfolio data and provide audit trails for recommendations.
5. **Explainability by default**: every insight includes provenance, confidence, and rationale.

---

## 3) High-level architecture (logical layers)

### A. Source & ingestion layer
**Typical sources**
- Exchange announcements (ASX, NYSE/Nasdaq feeds, regulatory filings).
- News providers/APIs (Bloomberg, IBKR, Yahoo Finance, Reuters-like feeds where licensed).
- Market data (OHLCV, corporate actions, fundamentals, estimates).
- Alternative data (public news portals such as Sydney Morning Herald, social sentiment, macro calendars).

**AWS services**
- Managed connectors: **AWS Glue connectors**, partner integrations, API Gateway + Lambda for custom pulls.
- Streaming ingestion: **Amazon Kinesis Data Streams** (or MSK/Kafka).
- Batch ingestion/scheduling: **AWS Step Functions + EventBridge + Lambda/ECS jobs**.
- Raw landing zone: **Amazon S3 (Data Lake, Bronze tier)**.

**GCP equivalents**
- API ingestion via Cloud Functions/Cloud Run + Cloud Scheduler.
- Streaming via Pub/Sub or Kafka on Confluent.
- Raw lake on Cloud Storage.

### B. Storage & data modeling layer
- **Bronze (raw immutable)**: source payloads, original timestamps, source IDs.
- **Silver (cleaned/normalized)**: canonical schemas for symbol master, company master, events, news, prices.
- **Gold (analytics-ready)**: factor tables, strategy signals, portfolio snapshots.

**AWS services**
- Data lake: **S3 + AWS Lake Formation + Glue Data Catalog**.
- Table format: **Apache Iceberg/Hudi/Delta** (Iceberg preferred for ACID + time travel).
- Query engines: **Athena**, **Redshift Serverless** for BI/SQL workloads.
- Time-series store (optional): **Timestream** for intraday metrics.
- Search store: **OpenSearch** for full-text/news retrieval.

**GCP equivalents**
- Cloud Storage + Dataplex/Data Catalog.
- BigQuery (lakehouse style) + BigLake tables.
- Vertex AI Feature Store / AlloyDB / OpenSearch-compatible option.

### C. Processing, enrichment, and feature layer
- Parsing and normalization (entity mapping, ticker normalization, timezone alignment).
- NLP enrichment (NER, sentiment, topic/event extraction, summarization).
- Market enrichment (returns, volatility, exposures, factor scores).
- Portfolio context enrichment (holdings overlap, concentration, risk budget impact).

**AWS services**
- ETL/ELT: **AWS Glue (Spark)**, **EMR**, or **EKS** for custom pipelines.
- Workflow orchestration: **Step Functions** (or MWAA/Airflow).
- ML feature pipelines: **SageMaker Processing + Feature Store**.

### D. Intelligence layer (signals + recommendations)
1. **Rule engine**: deterministic checks (e.g., earnings downgrade + high leverage + weak price action).
2. **ML models**: forecasting, anomaly detection, event impact scoring, ranking models.
3. **LLM insight generation**: create human-readable investment notes from structured evidence.
4. **Portfolio decision engine**: map signals to actions given mandate, constraints, and risk model.

**AWS services**
- Modeling and MLOps: **SageMaker** pipelines, model registry, endpoints/batch inference.
- LLM orchestration: **Amazon Bedrock** with retrieval from curated knowledge index.
- Online decision API: **ECS/EKS/Lambda + API Gateway**.

**GCP equivalents**
- Vertex AI Pipelines/Model Registry/Endpoints.
- Gemini/Vertex for LLM summarization + retrieval.
- Cloud Run / GKE + API Gateway.

### E. Serving, experience, and integration layer
- Analyst dashboard (web app), alert center, and portfolio cockpit.
- Channels: email, Slack/Teams, webhook, mobile push.
- External integration: OMS/PMS, broker APIs, internal research tools.

**AWS services**
- Frontend hosting: **CloudFront + S3/Amplify**.
- Application backend: **AppSync/GraphQL** or API Gateway + ECS.
- Notifications: **SNS, SES, EventBridge**.

### F. Governance, security, and compliance layer
- IAM least privilege and tenant isolation.
- Encryption at rest/in transit (KMS, TLS).
- Data lineage and audit of recommendations.
- Licensing controls for premium data (field-level entitlements, access logging).
- Compliance workflows (model approvals, recommendation disclaimers).

**AWS services**
- IAM, KMS, CloudTrail, GuardDuty, Security Hub, Macie.
- Lake Formation permissions + row/column-level governance.

---

## 4) Canonical data model (minimum viable)
1. **Instrument master**: ISIN, ticker, exchange, currency, sector.
2. **Corporate events**: announcements, filings, dividends, splits, earnings.
3. **News events**: source, timestamp, entities, sentiment, relevance score.
4. **Market bars**: OHLCV + adjusted prices + liquidity metrics.
5. **Fundamentals**: statements, ratios, estimates, revisions.
6. **Portfolio snapshots**: holdings, cost basis, exposures, constraints.
7. **Signals**: feature vector, model version, confidence, decay.
8. **Recommendations**: action, rationale, risk impact, timestamp, approval status.

Use immutable event IDs and time-travelable tables to reproduce any recommendation historically.

---

## 5) End-to-end data flow
1. **Ingest** source payloads into Bronze S3 with metadata (source, schema version, retrieval timestamp).
2. **Validate/clean** with data quality checks (nulls, outliers, schema drift).
3. **Normalize** into Silver canonical entities (security, issuer, event, news, bar).
4. **Enrich** with NLP + factor calculations + cross-source deduplication.
5. **Persist features/signals** in Gold + Feature Store.
6. **Run decision policies** per strategy and per portfolio.
7. **Publish insights** to APIs/dashboard/alerts, storing explanation artifacts.
8. **Monitor** data freshness, model performance, and recommendation outcomes.

---

## 6) Strategy & portfolio personalization framework

### Strategy definitions
Represent strategy logic as versioned configuration:
- Universe filters (region, cap, sector, liquidity).
- Signal blend (quality/value/momentum/event weights).
- Risk constraints (max position size, sector caps, turnover).
- Execution preferences (rebalance frequency, slippage assumptions).

### Portfolio-aware engine
For each portfolio:
- Compute current exposures and active bets.
- Score candidate actions by expected return, risk contribution, and constraint fit.
- Generate ranked actions: **add / reduce / hold / watchlist**, each with confidence and “why now”.

---

## 7) MLOps + LLMOps blueprint
1. **Feature/version management**: point-in-time correct joins; feature registry.
2. **Training cadence**: daily/weekly retraining by strategy class.
3. **Validation**: walk-forward and regime-based backtests.
4. **Deployment**: shadow mode → canary → full rollout.
5. **Monitoring**: drift, precision/recall for events, PnL attribution stability.
6. **LLM safety**:
   - Retrieval only from licensed + approved indexed content.
   - Guardrails to avoid unsupported claims.
   - Always attach source snippets and confidence score.

---

## 8) Reliability and operational SLOs
- **Freshness SLO**: e.g., news ingestion < 2 minutes from receipt.
- **Availability SLO**: insight API 99.9% monthly.
- **Backfill capability**: replay pipelines for 1–5 years historical recomputation.
- **Disaster recovery**: multi-AZ, optional cross-region replication for critical datasets.

Operational tooling:
- CloudWatch dashboards, alarms, tracing.
- Dead-letter queues and replay tools.
- Runbooks for vendor outage and schema breakage.

---

## 9) Security, legal, and licensing considerations
- Ensure contractual rights for each feed (Bloomberg/IBKR/news portals) before storage and redistribution.
- Separate raw licensed content from derived analytics outputs.
- Implement per-tenant and per-license entitlements in API and query layers.
- Keep immutable audit logs for all recommendation generation and user delivery.
- Add jurisdiction-specific disclaimers: insights are research support, not personalized financial advice unless licensed accordingly.

---

## 10) AWS reference deployment (recommended)
- **Networking**: multi-account setup (data, ml, prod), VPC per environment, private subnets.
- **Data**: S3 + Iceberg + Glue Catalog + Lake Formation.
- **Compute**: Glue/EMR for heavy ETL; Lambda for lightweight ingestion; ECS for APIs.
- **Streaming**: Kinesis + Firehose.
- **AI/ML**: SageMaker + Bedrock + OpenSearch vector/full-text index.
- **Serving**: API Gateway + ECS/AppSync + CloudFront frontend.
- **Ops/Sec**: CloudWatch, CloudTrail, GuardDuty, KMS, Secrets Manager.

---

## 11) Phased implementation roadmap

### Phase 0 (2–4 weeks): foundation
- Define canonical schemas and data contracts.
- Set up landing zone, IAM model, CI/CD, observability baseline.

### Phase 1 (6–10 weeks): core data + insights MVP
- Ingest 3–5 key sources (prices, corporate filings, one premium/one public news source).
- Build Bronze/Silver/Gold transformations.
- Deliver baseline insights: event summaries + sentiment + simple ranking.
- Launch dashboard + alerting.

### Phase 2 (8–12 weeks): strategy personalization
- Strategy config service + portfolio ingestion.
- Risk model integration and portfolio-aware recommendation engine.
- Backtesting and paper-trading loop.

### Phase 3 (ongoing): scaling + optimization
- Expand source universe and geographies.
- Improve model ensemble and LLM explainability.
- Add execution analytics and post-trade feedback loop.

---

## 12) KPI framework
- Data quality: completeness, freshness, dedup ratio.
- Model quality: hit rate, information coefficient, calibration.
- Business impact: user engagement with alerts, decision turnaround time, strategy alpha vs benchmark.
- Trust: explainability coverage, source citation rate, audit pass rate.

---

## 13) Suggested first build choices
If you want to start quickly on AWS:
1. S3 + Glue Catalog + Athena + Lake Formation.
2. Step Functions + Lambda for ingestion orchestration.
3. OpenSearch for searchable news/event corpus.
4. SageMaker for event-impact model + ranking model.
5. Bedrock for narrative insight generation grounded on retrieved evidence.
6. Simple React dashboard with API Gateway + ECS backend.

This gives a practical path from raw ingestion to explainable investment recommendations while keeping an upgrade path to advanced portfolio optimization and execution integration.

---

## 14) Execution status
- **Completed**: Phase 0, Step 1 (define canonical schemas and data contracts).
- Deliverables are stored under `docs/contracts/`.
