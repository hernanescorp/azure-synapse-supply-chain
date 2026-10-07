# Azure Synapse Supply Chain Data Platform

End-to-end Azure Data Engineering project that simulates a real-world hybrid data platform for an industrial supply chain environment.

The platform integrates an external PostgreSQL operational system and a REST API with Azure services to build an incremental, testable and analytics-ready data pipeline.

## Architecture

External Linux VPS  
→ PostgreSQL operational database  
→ Azure Synapse Pipelines  
→ Azure Data Lake Storage Gen2  
→ Bronze  
→ Synapse Spark / PySpark  
→ Silver  
→ dbt  
→ Gold  
→ Synapse Serverless SQL  
→ Power BI

An external REST API is also ingested through the ingestion layer.

## Technology Stack

- Azure Synapse Analytics
- Azure Data Lake Storage Gen2
- Synapse Pipelines
- Apache Spark / PySpark
- Delta / Parquet
- dbt
- SQL
- Python
- PostgreSQL
- Docker
- Power BI
- Git / GitHub

## Business Scenario

The source system represents a simplified industrial ERP containing:

- Customers
- Materials
- Sales orders
- Sales order lines

The project simulates operational changes such as new orders, updates, cancellations, late-arriving records and invalid data.

## Data Architecture

The analytical platform follows a Medallion Architecture:

### Bronze
Raw source data preserved for traceability and reprocessing.

### Silver
Validated, typed, deduplicated and enriched datasets produced with PySpark.

### Gold
Business-oriented dimensional models designed for analytical consumption.

The initial Gold model will contain:

- `dim_date`
- `dim_customer`
- `dim_material`
- `fct_sales_order_line`

The fact table grain is one row per sales order line.

## Engineering Topics

This project covers:

- Full and incremental ingestion
- Watermark-based extraction
- Idempotent pipelines
- Data quality validation
- Quarantine of invalid records
- PySpark transformations
- Delta / Parquet storage
- Dimensional modelling
- dbt models and tests
- Serverless SQL analytics
- REST API ingestion
- Git-based development
- CI/CD
- Monitoring and observability
- Security and secrets management
- Cost-aware architecture

## Repository Structure

```text
architecture/       Architecture decisions and diagrams
source-system/      External PostgreSQL ERP and data simulator
synapse/            Synapse pipelines and notebooks
dbt/                Transformation models and data tests
sql/                Analytical SQL and exercises
docs/               Technical documentation
powerbi/            Power BI documentation
```

## Project Status

**Phase 0 — Project foundation and architecture**

Current work:

- Repository structure
- Infrastructure assessment
- Architecture design
- Source-system isolation strategy
- Security baseline

## Design Principles

The project prioritizes:

1. Reproducibility
2. Incremental processing
3. Idempotency
4. Data quality
5. Observability
6. Security
7. Cost awareness
8. Clear architectural decisions

## Documentation

Architecture Decision Records (ADRs) are stored under `architecture/decisions/`.

Additional technical documentation is available under `docs/`.

---

Built as a hands-on implementation of production-oriented Azure Data Engineering patterns.
