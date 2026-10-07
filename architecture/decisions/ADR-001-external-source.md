# ADR-001: External PostgreSQL Operational Source

## Status

Accepted

## Context

This project requires an operational source system located outside Azure in order to reproduce a realistic data integration scenario.

The source system represents a simplified industrial ERP containing customers, materials, sales orders and sales order lines.

A Linux VPS is already available and runs Docker workloads. The existing workloads must remain isolated and unaffected by this project.

## Decision

The operational source system will be implemented using PostgreSQL 17 running in a dedicated Docker container on the external Linux VPS.

The Azure Supply Chain project will use:

- A dedicated Docker Compose configuration
- A dedicated Docker network
- A dedicated PostgreSQL container
- A dedicated persistent Docker volume
- Explicit resource limits where appropriate
- Separate environment configuration and credentials

The database will not share containers, networks, volumes or credentials with unrelated workloads running on the VPS.

## Rationale

This approach provides:

- A persistent operational database outside Azure
- Clear separation between the source system and analytical platform
- Reproducible infrastructure through Docker Compose
- Controlled resource consumption
- An environment suitable for testing full and incremental ingestion
- A realistic network boundary between source and cloud platform

PostgreSQL also provides a suitable relational source for practising SQL-based extraction, watermark strategies and change processing.

## Important Distinction

The Linux VPS is not a literal on-premises environment.

It is used to simulate an operational system running outside Azure and therefore provides a useful environment for practising hybrid data integration patterns.

A real private on-premises source could require additional connectivity components such as a Self-hosted Integration Runtime, VPN or private networking depending on the architecture.

## Alternatives Considered

### Local PostgreSQL

Rejected as the primary source because it would depend on a developer workstation being available and running.

### Azure Database for PostgreSQL

Not selected because placing both the operational source and analytical platform inside Azure would remove part of the external-source integration scenario.

### Existing PostgreSQL Container

Rejected because the VPS already hosts an unrelated application database. Sharing that database would create unnecessary coupling and operational risk.

## Consequences

### Positive

- Strong workload isolation
- Reproducible source environment
- Persistent operational data
- Independent lifecycle
- Suitable for incremental ingestion testing

### Negative

- Additional resource consumption on a small VPS
- External connectivity must be designed securely
- The environment does not reproduce every characteristic of a true private on-premises network

## Security

The PostgreSQL service must not be exposed publicly unless required by the selected Azure connectivity architecture.

Credentials and connection strings must never be committed to Git.

Secrets will be stored outside the repository and represented only by placeholders in `.env.example`.

## Next Steps

1. Define the PostgreSQL source schema.
2. Create the isolated Docker Compose configuration.
3. Implement deterministic seed data.
4. Implement the ERP change simulator.
5. Design secure connectivity between the external source and Azure.
