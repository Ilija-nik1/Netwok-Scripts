import paramiko
import base64
from Crypto.Cipher import AES

# RouterOS credentials
router_ip = "192.168.1.1"
router_username = "admin"
router_password = "your_router_password"

# Function to encrypt the password for secure transmission
def encrypt_password(password, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_password = password + ' ' * (16 - len(password) % 16)
    encrypted_password = cipher.encrypt(padded_password.encode())
    return base64.b64encode(encrypted_password).decode()

# Function to connect to the RouterOS and send commands
def send_command(session, command):
    session.exec_command(command)
    return session.recv(8192).decode()

# Function to run multiple commands in sequence
def run_commands(session, commands):
    for cmd in commands:
        result = send_command(session, cmd)
        print(result.strip())  # Print the command result

# Function to configure VLAN interfaces
def configure_vlans(session, vlan_id, interface):
    cmd = f"/interface vlan add name=vlan{vlan_id} interface={interface} vlan-id={vlan_id}"
    return send_command(session, cmd)

# Function to create firewall address lists
def create_firewall_address_list(session, list_name, addresses):
    cmd = f"/ip firewall address-list add list={list_name} address={addresses}"
    return send_command(session, cmd)

# Function to configure NAT rules
def configure_nat(session, nat_type, dst_address, to_address):
    cmd = f"/ip firewall nat add chain=srcnat action={nat_type} src-address={dst_address} to-address={to_address}"
    return send_command(session, cmd)

# Function to configure DHCP server
def configure_dhcp_server(session, interface, dhcp_pool, gateway, dns_servers):
    cmd = f"/ip dhcp-server add interface={interface}"
    run_commands(session, [cmd])

    cmd = f"/ip dhcp-server network add address={dhcp_pool} gateway={gateway} dns-server={dns_servers}"
    return send_command(session, cmd)

# Function to configure PPPoE server
def configure_pppoe_server(session, interface, service_name, authentication_type, username, password):
    cmd = f"/interface pppoe-server server add interface={interface} service-name={service_name}"
    run_commands(session, [cmd])

    cmd = f"/interface pppoe-server server profile add name=default local-address=\
        192.168.1.1 remote-address=pppoe-pool use-encryption=yes only-one=default use-mpls=default\
        use-compression=default use-vj-compression=default dns-server=8.8.8.8,8.8.4.4"
    run_commands(session, [cmd])

    cmd = f"/ppp secret add name={username} password={password} service=pppoe profile=default\
        local-address=192.168.1.1 remote-address=pppoe-pool use-mpls=default use-compression=default\
        use-vj-compression=default"
    return send_command(session, cmd)

# Function to add static routes
def add_static_route(session, destination, gateway):
    cmd = f"/ip route add dst-address={destination} gateway={gateway}"
    return send_command(session, cmd)

if __name__ == "__main__":
    # Establish SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(router_ip, username=router_username, password=router_password)

    # Encrypt the password for secure transmission
    encrypted_password = encrypt_password(router_password, b"0123456789ABCDEF")  # Change the key if needed

    # Send basic configuration commands
    commands = [
        f"/ip address add address=192.168.1.1/24 interface=ether1",
        f"/ip dhcp-client add dhcp-options=hostname,clientid disabled=no interface=ether1",
        f"/ip firewall filter add chain=input action=accept connection-state=established,related",
        f"/ip firewall filter add chain=input action=drop",
        f"/ip firewall filter add chain=forward action=accept connection-state=established,related",
        f"/ip firewall filter add chain=forward action=drop",
        f"/ip service set telnet disabled=yes",
        f"/user set 0 password={encrypted_password}",
    ]

    run_commands(ssh, commands)

    # Example: Configure VLANs
    configure_vlans(ssh, 10, "ether2")
    configure_vlans(ssh, 20, "ether3")

    # Example: Create Firewall Address Lists
    create_firewall_address_list(ssh, "allowed_clients", "192.168.1.100,192.168.1.101")

    # Example: Configure NAT Rules
    configure_nat(ssh, "src-nat", "192.168.1.0/24", "203.0.113.10")

    # Example: Configure DHCP Server
    configure_dhcp_server(ssh, "ether1", "192.168.1.100-192.168.1.200", "192.168.1.1", "8.8.8.8,8.8.4.4")

    # Example: Configure PPPoE Server
    configure_pppoe_server(ssh, "ether2", "MyPPPoEService", "chap", "pppoe_user", "pppoe_password")

    # Example: Add Static Route
    add_static_route(ssh, "10.0.0.0/24", "192.168.1.254")

    ssh.close()