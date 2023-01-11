#!/usr/bin/python3
import os

# anssi ssh recommendation
recommendations = {
    "Protocol": "2",
    "PermitRootLogin": "no",
    "PermitEmptyPasswords": "no",
    "PasswordAuthentication": "no",
    "UsePrivilegeSeparation": "yes",
    "PermitUserEnvironment": "no",
    "Ciphers": "chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr",
    "UsePAM" : "yes",
    "X11Forwarding": "no",
    "AllowTcpForwarding": "no",
    "AllowAgentForwarding": "no",
    "MaxAuthTries" : "3",
    "ClientAliveInterval" : "900",
    "ClientAliveCountMax" : "0",
    "IgnoreRhosts": "yes",
    "HostKeyAlgorithms": "ssh-rsa,ssh-dss,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521",
    "KexAlgorithms": "diffie-hellman-group-exchange-sha256,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,diffie-hellman-group-exchange-sha1",
    "Macs": "hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha1-etm@openssh.com",
    "Banner": "/etc/issue.net",
    "MaxSessions" : "10",
}

with open("/etc/ssh/sshd_config", "r") as f:
    ssh_config = f.readlines()
    ssh_config = [x.strip() for x in ssh_config]

# Initialize variables
compliant_settings = {}
non_compliant_settings = {}
missing_settings = []

# Iterate through config file and compare
line_number = 0
for line in ssh_config:
    line_number += 1
    if line.startswith("#") or line == "":
        continue
    setting = line.split()[0]
    value = line.split()[1]
    if setting in recommendations:
        if value != recommendations[setting]:
            non_compliant_settings[setting] = (line_number, line, value)
        else:
            compliant_settings[setting] = (line_number, line, value)

#missing settings
missing_settings = [s for s in recommendations if s not in compliant_settings and s not in non_compliant_settings]

# Print results
if missing_settings:
    print("Missing settings:")
    for setting in missing_settings:
        print(setting)
if compliant_settings:
    print("\nCompliant settings:")
    for setting, (line_number, line, value) in compliant_settings.items():
        print(f"Line {line_number}: {line}")
if non_compliant_settings:
    print("\nNon-compliant settings:")
    for setting, (line_number, line, value) in non_compliant_settings.items():
        print(f"Line {line_number}: {line} (should be {setting} {recommendations[setting]})")
