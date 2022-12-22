#This code will connect to a Cisco device at the specified IP address, set the hostname to "my-router"
#Create a VLAN with ID 10 and name "VLAN10", and add a switchport to the VLAN.
from cisco import CiscoDevice

device = CiscoDevice(host='192.168.1.1', username='admin', password='secret')
device.open()

# Set the hostname of the device
device.set_hostname('my-router')

# Create a VLAN with ID 10 and name 'VLAN10'
device.create_vlan(10, 'VLAN10')

# Add a switchport to VLAN 10
device.create_switchport(10)

# Save the configuration
device.save_config()

# Close the connection to the device
device.close()