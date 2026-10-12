# Azure VM and Self-hosted Integration Runtime Deployment

## 1. Objective

Deploy a Windows Server virtual machine in Microsoft Azure
to host a Self-hosted Integration Runtime (SHIR).

The SHIR enables Azure Synapse Analytics to connect to
a PostgreSQL database hosted externally on Hetzner.

## 2. Azure resources

| Resource | Configuration |
|---|---|
| Resource group | rg-graxiano-prod |
| Virtual machine | vm-graxiano |
| Region | West Europe |
| Operating system | Windows Server 2022 |
| VM size | Standard D2s v3 |
| vCPUs | 2 |
| RAM | 8 GiB |
| Synapse workspace | syn-supply-chain-lab |
| Integration Runtime | shir-hetzner-postgres |

## 3. Private connectivity

Tailscale is installed on the Windows Server VM.

The VM uses the following private Tailscale address:

100.96.141.46

Remote Desktop access is performed through Tailscale,
without exposing RDP port 3389 publicly.

## 4. SHIR installation

1. Open the Azure Windows VM through Remote Desktop.
2. Download Microsoft Integration Runtime from Microsoft.
3. Install the 64-bit Integration Runtime.
4. Open Microsoft Integration Runtime Configuration Manager.
5. Open Synapse Studio.
6. Navigate to Manage > Integration runtimes.
7. Select shir-hetzner-postgres.
8. Obtain a registration key.
9. Register the Windows VM as a SHIR node.
10. Verify that the runtime is connected.

Registration keys must never be stored in Git.

## 5. PostgreSQL linked service

| Setting | Value |
|---|---|
| Name | ls_postgresql_hetzner |
| Integration Runtime | shir-hetzner-postgres |
| Server | 100.104.217.36 |
| Port | 5432 |
| Database | supply_chain |
| Username | synapse_lab |

Credentials are configured securely in Synapse
and must not be committed to the repository.

## 6. Validation

The following checks were completed successfully:

- Tailscale connectivity between Azure and Hetzner
- TCP connectivity to PostgreSQL port 5432
- SHIR registration in Azure Synapse
- PostgreSQL Linked Service connection test

## 7. Operational considerations

The Azure VM has an automatic shutdown schedule
to reduce infrastructure costs.

After starting the VM, verify:

1. VM power state is Running.
2. Tailscale service is running.
3. Private connectivity to Hetzner works.
4. SHIR is online in Synapse.
5. PostgreSQL Linked Service connection succeeds.

Stopping the VM with deallocation avoids ongoing
VM compute charges, although other Azure resources
may continue generating costs.

## 8. Security

- No public inbound RDP access is required.
- PostgreSQL is accessed through Tailscale.
- SHIR registration keys must remain confidential.
- Access to Azure Key Vault should follow least privilege.
- Production deployments should use appropriate
  secret management, monitoring and recovery procedures.
