# Troubleshooting and Lessons Learned

## 1. Tailscale disconnects after Windows RDP login

### Symptoms

The Azure VM initially connected to Tailscale but
became unreachable shortly after an RDP login.

The Windows Tailscale service remained running,
while the client reported a logged-out state.

### Investigation

Windows service logs showed:

- A user session connecting to Tailscale.
- An attempt to migrate legacy profile preferences.
- Tailscale transitioning from Running to NoState.
- WantRunning=false.
- The client entering NeedsLogin.

### Resolution tested

1. Identified a Tailscale shortcut in the Windows
   common Startup folder.
2. Disabled the shortcut without disabling the
   Tailscale Windows service.
3. Reauthenticated Tailscale in unattended mode
   using a one-time authentication key.
4. Verified connectivity after an RDP login.
5. Verified connectivity after a Windows restart.
6. Verified authentication following VM deallocation
   and subsequent startup.

The workaround was successful in our tests.
The underlying Windows profile interaction was not
conclusively established as the root cause.

### Security

Authentication keys were not committed to Git.
Azure Key Vault was used during recovery.

## 2. Azure VM deallocation delay

### Symptoms

The Azure VM remained in a Deallocating state
longer than expected.

### Investigation

Azure Activity Log reported the deallocation operation.
The VM eventually reached PowerState/deallocated.

### Validation command

    az vm get-instance-view \
      --resource-group rg-graxiano-prod \
      --name vm-graxiano \
      --query "instanceView.statuses[].{code:code,displayStatus:displayStatus,time:time}" \
      --output table

### Lesson learned

Distinguish between stopping the guest operating
system and deallocating Azure compute resources.

VM compute charges stop after deallocation,
although storage and other resources may still incur costs.

## 3. Tailscale connectivity timeout

### Symptoms

The workstation initially failed to ping the Azure VM.

### Investigation

- Tailscale service was Running and Automatic.
- The VM retained its Tailscale identity.
- The VM could ping the workstation through DERP.
- UDP connectivity was available.
- A subsequent workstation ping succeeded directly.

### Outcome

Connectivity recovered without generating a new key.

A single timeout was insufficient evidence
of lost authentication.

## 4. PostgreSQL SSL connection error in VS Code

### Symptoms

    server does not support SSL, but SSL was required

### Cause

The PostgreSQL client required SSL, while the
laboratory PostgreSQL server did not offer it.

### Resolution

Configured SSL Mode = Disable for the local
VS Code Remote SSH connection to the Docker network.

This is a laboratory configuration, not a
recommended production security baseline.

## 5. Docker permission denied

### Symptoms

The Linux user could not access:

    /var/run/docker.sock

### Resolution

Used sudo for Docker inspection commands.

No changes to Docker group membership were required.

## 6. PostgreSQL inaccessible from Azure

### Cause

The PostgreSQL container had no published host port.

### Resolution

Configured a socat TCP proxy listening exclusively
on the Hetzner Tailscale IP and restricting clients
to the Azure VM Tailscale IP.

The proxy was deployed as a systemd service.

### Validation

- Test-NetConnection returned TcpTestSucceeded=True.
- Synapse PostgreSQL Linked Service connection succeeded.
- Connectivity was retested after enabling systemd.

## 7. Remaining technical debt

- Replace the hardcoded Docker container IP.
- Enforce PostgreSQL TLS where appropriate.
- Review host firewall and Tailscale ACL policies.
- Reduce temporary Key Vault permissions.
- Disable or remove obsolete authentication secrets.
- Automate infrastructure provisioning and validation.
- Add monitoring and backup/recovery procedures.
