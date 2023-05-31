import ipaddress

# Get user input for network address and subnet mask
network = input("Enter the network address: ")
subnet_mask = input("Enter the subnet mask: ")

# Create an IPv4Network object
network_address = ipaddress.IPv4Network(f"{network}/{subnet_mask}", strict=False)

# Print the network details
print("Network address:", network_address.network_address)
print("Netmask:", network_address.netmask)
print("Wildcard mask:", network_address.hostmask)
print("Broadcast address:", network_address.broadcast_address)
print("Number of hosts:", network_address.num_addresses - 2) # Subtract 2 to exclude network and broadcast addresses