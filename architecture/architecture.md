# Hybrid Data Engineering Architecture

## 1. Project overview

This project demonstrates a hybrid data engineering architecture
connecting a PostgreSQL transactional source hosted on Hetzner
with Azure Synapse Analytics and Azure Data Lake Storage Gen2.

## 2. Architecture

PostgreSQL 17 (Docker, Hetzner)
    |
    | Docker private network
    v
socat TCP Proxy (Ubuntu VPS)
    |
    | Tailscale / WireGuard
    v
Self-hosted Integration Runtime (Azure Windows VM)
    |
    | Azure Synapse orchestration
    v
Azure Data Lake Storage Gen2

## 3. Source system

- Provider: Hetzner
- Operating system: Ubuntu
- Database: PostgreSQL 17
- Container: synapse-lab-postgres
- Database name: supply_chain
- Tables: customers, orders
- Deployment: Docker Compose
- Data generator: Python ERP simulator

## 4. Private connectivity

Tailscale provides encrypted connectivity between the
Hetzner VPS and the Azure Windows VM.

The PostgreSQL container does not publish port 5432
directly on the host.

A socat proxy listens exclusively on the Hetzner
Tailscale address and restricts incoming connections
to the Azure VM Tailscale address.

The proxy is managed by systemd.

## 5. Azure infrastructure

- Synapse workspace: syn-supply-chain-lab
- Storage: graxianodatalake
- ADLS Gen2 filesystem: synapse
- Windows VM: vm-graxiano
- Self-hosted IR: shir-hetzner-postgres
- SHIR node: vm-graxiano
- PostgreSQL linked service: ls_postgresql_hetzner

## 6. Validation completed

- PostgreSQL container operational
- Source tables populated
- SQL queries executed successfully from VS Code
- Tailscale connectivity verified
- SHIR registered and connected to Synapse
- PostgreSQL linked service connection tested
- systemd PostgreSQL proxy running successfully

## 7. Next milestones

1. Implement PostgreSQL ingestion pipelines
2. Land source data in ADLS Gen2 Bronze
3. Implement incremental ingestion
4. Develop transformations
5. Configure Synapse Git integration
6. Implement CI/CD and deployment automation

## 8. Security considerations

- PostgreSQL is not exposed directly to the Internet
- Tailscale provides encrypted private connectivity
- SHIR runs on a dedicated Azure VM
- Secrets must not be committed to Git
- Production deployments should enforce database TLS
- Docker container IP dependencies should be removed
- Network and identity permissions should follow least privilege
