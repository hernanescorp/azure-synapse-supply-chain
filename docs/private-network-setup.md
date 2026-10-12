# Private Network Connectivity: Azure and Hetzner

## 1. Objective

Provide secure connectivity between an Azure Windows VM
running Self-hosted Integration Runtime (SHIR) and a
PostgreSQL database hosted in Docker on a Hetzner VPS.

The database must not be exposed directly to the Internet.

## 2. Network topology

| Component | Tailscale IP |
|---|---|
| Developer workstation (asus) | 100.127.248.94 |
| Azure VM (vm-graxiano) | 100.96.141.46 |
| Hetzner VPS (graxiano-server) | 100.104.217.36 |

Data connection:

    Azure Synapse
          |
          v
    SHIR (Azure VM)
          |
          | Tailscale / WireGuard
          v
    Hetzner VPS :5432
          |
          | socat TCP proxy
          v
    PostgreSQL Docker container :5432

## 3. PostgreSQL isolation

The PostgreSQL 17 container is named:

    synapse-lab-postgres

Docker network:

    source-system_synapse_lab_network

Current container IP:

    172.19.0.2

The container does not publish port 5432 on the host.

This was verified using:

    sudo docker inspect synapse-lab-postgres \
      --format '{{json .NetworkSettings.Ports}}'

Expected output:

    {"5432/tcp":null}

## 4. Tailscale connectivity

Tailscale provides encrypted connectivity between
the Azure VM and Hetzner VPS.

Verify connectivity from the Azure VM:

    tailscale ping 100.104.217.36

Verify the PostgreSQL TCP endpoint:

    Test-NetConnection 100.104.217.36 -Port 5432

A successful test returns:

    TcpTestSucceeded : True

## 5. PostgreSQL TCP proxy

The proxy is implemented using socat.

It listens on the Hetzner Tailscale IP only:

    100.104.217.36:5432

Connections are restricted to the Azure VM:

    100.96.141.46/32

Traffic is forwarded to the Docker container:

    172.19.0.2:5432

The systemd service definition is versioned at:

    infrastructure/hetzner/systemd/synapse-postgres-proxy.service

## 6. Service management

Check service status:

    sudo systemctl status synapse-postgres-proxy

Restart the service:

    sudo systemctl restart synapse-postgres-proxy

Inspect logs:

    sudo journalctl -u synapse-postgres-proxy -n 50 --no-pager

## 7. Security considerations

- PostgreSQL is not published on a public interface.
- The proxy binds exclusively to the Tailscale IP.
- socat restricts accepted client IPs.
- Tailscale encrypts traffic between peers.
- PostgreSQL SSL is not currently enforced.
- Database credentials must not be stored in Git.
- Network restrictions should also be enforced through
  appropriate host firewall and Tailscale ACL policies.

## 8. Known limitations

The proxy currently uses a fixed Docker container IP.

If Docker recreates the container and assigns another IP,
the proxy configuration must be updated.

A future improvement should use stable service discovery
or an alternative private network architecture.

The proxy also depends on Tailscale being available
when the service starts.

## 9. Validation completed

- Azure VM successfully reached Hetzner via Tailscale.
- TCP connectivity to port 5432 succeeded.
- PostgreSQL Linked Service test succeeded in Synapse.
- systemd proxy service was enabled and started.
- Linked Service connectivity was successfully retested.
