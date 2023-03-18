import random
import requests

# Constants
MAC_PREFIX = bytes([0x00, 0x16, 0x3e])
MAX_BYTE = 0xff
MAX_GROUP = 0x7f
MAC_API_URL = "https://api.macvendors.com/"

def generate_mac_address() -> str:
    mac_suffix = bytes(random.choices(range(MAX_GROUP + 1), k=3)) + bytes(random.randint(0x00, MAX_BYTE) for _ in range(3))
    mac = MAC_PREFIX + mac_suffix
    mac_address = ":".join(f"{byte:02x}" for byte in mac)
    return mac_address

def validate_mac_address(mac_address: str) -> bool:
    """
    Validate a MAC address.
    """
    mac_address = mac_address.lower().replace("-", ":")
    if not all(c in "0123456789abcdef:" for c in mac_address):
        return False
    octets = mac_address.split(":")
    if len(octets) != 6:
        return False
    for octet in octets:
        if len(octet) != 2:
            return False
        try:
            int(octet, 16)
        except ValueError:
            return False
    return True

def generate_mac_addresses(n: int) -> list:
    """
    Generate n random MAC addresses.
    """
    return [generate_mac_address() for _ in range(n)]

def get_vendor(mac_address: str) -> str:
    """
    Get the vendor information for a MAC address using an API.
    """
    mac_address = mac_address.lower().replace("-", ":")
    try:
        response = requests.get(MAC_API_URL + mac_address)
        return response.text.strip()
    except:
        return "Unknown"

# Generate a random MAC address
print(generate_mac_address())

# Validate a MAC address
print(validate_mac_address("00:16:3E:3C:3F:AB"))

# Generate 10 random MAC addresses
print(generate_mac_addresses(10))

# Get the vendor information for a MAC address
print(get_vendor("00:16:3E:3C:3F:AB"))