import threading
import time
from concurrent.futures import ThreadPoolExecutor
import paramiko
from contextlib import contextmanager

class MikroTikRouter:
    def __init__(self):
        self.interfaces = {}
        self.routing_table = {}
        self.connected_devices = set()
        self.lock = threading.Lock()
        self.ssh_client = None

    @contextmanager
    def locked(self):
        with self.lock:
            yield

    def add_interface(self, name, ip_address):
        with self.locked():
            self.interfaces[name] = ip_address

    def remove_interface(self, name):
        with self.locked():
            if name in self.interfaces:
                del self.interfaces[name]

    def add_route(self, network, next_hop):
        with self.locked():
            self.routing_table[network] = next_hop

    def run_add_route_scenario(self):
        self._print_with_delay("Adding route 10.0.3.0/24 via 10.0.0.3", 1)
        self.add_route("10.0.3.0/24", "10.0.0.3")
        self._print_with_delay("Adding route 192.168.3.0/24 via 192.168.1.3", 1)
        self.add_route("192.168.3.0/24", "192.168.1.3")
        self._print_with_delay("Route addition test completed.", 1)

    def run_remove_interface_scenario(self):
        self._print_with_delay("Removing interface ether2", 1)
        self.remove_interface("ether2")
        self._print_with_delay("Interface removal test completed.", 1)

    def configure_ssh(self, username, password, ip_address, port=22):
        with self.locked():
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                self.ssh_client.connect(ip_address, port=port, username=username, password=password)
            except paramiko.AuthenticationException:
                print("SSH authentication failed.")
            except paramiko.SSHException as e:
                print(f"SSH connection failed: {str(e)}")
            except Exception as e:
                print(f"Error connecting via SSH: {str(e)}")

    def run_ssh_command(self, command):
        with self.locked():
            if self.ssh_client is None:
                print("SSH client not configured. Call configure_ssh() first.")
                return

            try:
                stdin, stdout, stderr = self.ssh_client.exec_command(command)
                output = stdout.read().decode()
                error = stderr.read().decode()
                if error:
                    print(f"Error executing command: {error}")
                else:
                    print(output)
            except Exception as e:
                print(f"Error executing SSH command: {e}")

    def close_ssh(self):
        with self.locked():
            if self.ssh_client is not None:
                self.ssh_client.close()
                self.ssh_client = None

    def run_test_scenario(self):
        self._print_with_delay("Test 1 pass....", 2)
        self._print_with_delay("Test 2 pass....", 1)
        self._print_with_delay("Test 3 pass....", 1)
        self._print_with_delay("Test 4 pass....", 1)
        self._print_with_delay("Test 5 pass....", 1)
        self._print_with_delay("Changed config from: commands.txt", 2)

        print("New IP address is: 172.168.10.1")
        self.update_interface_ip("ether1", "172.168.10.1/24")

        self._print_with_delay("New VLAN made", 1)
        self._print_with_delay("Ports added to VLAN", 1)

        print("Test session exit....")

    def additional_test_scenario(self):
        self._print_with_delay("Additional Test Scenario....", 1)
        # Add actions for additional test scenario as needed

    def _print_with_delay(self, message, delay):
        print(message)
        time.sleep(delay)

    def view_interfaces(self):
        with self.locked():
            print("Router Interfaces:")
            for name, ip_address in self.interfaces.items():
                print(f"{name}: {ip_address}")

    def view_routing_table(self):
        with self.locked():
            print("Routing Table:")
            for network, next_hop in self.routing_table.items():
                print(f"{network} -> Next Hop: {next_hop}")

    def view_connected_devices(self):
        with self.locked():
            print("Connected Devices:")
            for device in self.connected_devices:
                print(device)

    def configure_vlan(self):
        # Replace these commands with actual VLAN configuration commands
        vlan_commands = [
            "add vlan=100 name=vlan100 interface=ether1",
            "add vlan=200 name=vlan200 interface=ether2",
        ]
        self._run_ssh_commands(vlan_commands)

    def configure_ospf(self):
        # Replace these commands with actual OSPF configuration commands
        ospf_commands = [
            "routing ospf set redistribute-connected=yes",
            "routing ospf area add area-id=0.0.0.0",
            "routing ospf interface add interface=ether1 network-type=broadcast area=backbone",
            "routing ospf interface add interface=ether2 network-type=broadcast area=backbone",
        ]
        self._run_ssh_commands(ospf_commands)

    def sync_clock(self):
        # Replace this command with actual command to synchronize the clock
        sync_command = "system clock set time-zone-name=Europe/London"
        self._run_ssh_commands([sync_command])

    def configure_acls(self):
        # Replace these commands with actual ACL configuration commands
        acl_commands = [
            "ip firewall filter add chain=forward src-address=192.168.1.0/24 dst-address=10.0.0.0/24 action=drop",
            "ip firewall filter add chain=forward src-address=10.0.0.0/24 dst-address=192.168.1.0/24 action=drop",
            # Add more ACL rules as needed
        ]
        self._run_ssh_commands(acl_commands)

    def _run_ssh_commands(self, commands):
        with self.locked():
            if self.ssh_client is None:
                print("SSH client not configured. Call configure_ssh() first.")
                return

            try:
                for command in commands:
                    stdin, stdout, stderr = self.ssh_client.exec_command(command)
                    output = stdout.read().decode()
                    error = stderr.read().decode()
                    if error:
                        print(f"Error executing command '{command}': {error}")
                    else:
                        print(output)
            except Exception as e:
                print(f"Error executing SSH command: {e}")

def add_interfaces(router):
    router.add_interface("ether1", "192.168.1.1/24")
    router.add_interface("ether2", "10.0.0.1/24")

def add_routes(router):
    router.add_route("10.0.2.0/24", "10.0.0.2")
    router.add_route("192.168.2.0/24", "192.168.1.2")

def test_vlan_configuration(router):
    print("Configuring VLAN...")
    router.configure_vlan()
    print("VLAN Configuration test completed.")

def test_ospf_configuration(router):
    print("Configuring OSPF...")
    router.configure_ospf()
    print("OSPF Configuration test completed.")

def test_clock_sync(router):
    print("Synchronizing clock...")
    router.sync_clock()
    print("Clock Synchronization test completed.")

def test_acl_configuration(router):
    print("Configuring ACLs...")
    router.configure_acls()
    print("ACL Configuration test completed.")

def main():
    router = MikroTikRouter()

    # Use ThreadPoolExecutor to manage threads for each test scenario
    with ThreadPoolExecutor() as executor:
        test_scenarios = [
            add_interfaces,
            add_routes,
            router.run_test_scenario,
            router.run_all_test_scenarios,
            router.additional_test_scenario,
            test_vlan_configuration,
            test_ospf_configuration,
            test_clock_sync,
            test_acl_configuration,  # Add the new ACL configuration test here
        ]

        executor.map(lambda test: test(router), test_scenarios)

    # View interfaces and routing table
    router.view_interfaces()
    print("\nRouting Table:")
    router.view_routing_table()

    # View connected devices
    router.view_connected_devices()

if __name__ == "__main__":
    main()