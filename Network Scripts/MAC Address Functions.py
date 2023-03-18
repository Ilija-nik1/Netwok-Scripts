import random
import requests

# Constants
MAC_PREFIX = bytes([0x00, 0x16, 0x3e])
MAX_BYTE = 0xff
MAX_GROUP = 0x7f
MAC_API_URL = "https://api.macvendors.com/"

def generate_mac() -> str:
    """
    Generate a random MAC address.
    """
    mac_suffix = bytes(random.choices(range(MAX_GROUP + 1), k=3)) + bytes(random.randint(0x00, MAX_BYTE) for _ in range(3))
    mac = MAC_PREFIX + mac_suffix
    mac_address = ":".join(f"{byte:02x}" for byte in mac)
    return mac_address

def validate_mac(mac_address: str) -> bool:
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

def is_multicast(mac_address: str) -> bool:
    """
    Check if a MAC address is a multicast address.
    """
    mac_address = mac_address.lower().replace("-", ":")
    octets = mac_address.split(":")
    return bool(int(octets[0], 16) & 1)

def is_unicast(mac_address: str) -> bool:
    """
    Check if a MAC address is a unicast address.
    """
    return not is_multicast(mac_address)

def generate_mac_with_prefix(n: int, prefix: str) -> list:
    """
    Generate n random MAC addresses with the given vendor prefix.
    """
    prefix = prefix.lower().replace("-", ":").replace(".", ":")
    prefix_bytes = bytes.fromhex(prefix)
    if len(prefix_bytes) != 3:
        raise ValueError("Invalid prefix")
    mac_suffixes = [bytes(random.randint(0x00, MAX_BYTE) for _ in range(3)) for _ in range(n)]
    mac_addresses = [MAC_PREFIX + prefix_bytes + suffix for suffix in mac_suffixes]
    return [":".join(f"{byte:02x}" for byte in mac) for mac in mac_addresses]

def get_vendor(mac_address: str) -> str:
    """
    Get the vendor information for a MAC address using an API.
    """
    mac_address = mac_address.lower().replace("-", ":")
    try:
        response = requests.get(MAC_API_URL + mac_address)
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException:
        raise ValueError("Could not retrieve vendor information")

def get_prefix(mac_address: str) -> str:
    """
    Get the vendor prefix of a MAC address.
    """
    mac_address = mac_address.lower().replace("-", ":")
    octets = mac_address.split(":")
    if len(octets) != 6:
        raise ValueError("Invalid MAC address")
    prefix_bytes = bytes.fromhex("".join(octets[:3]))
    return ":".join(f"{byte:02x}" for byte in prefix_bytes)

def get_organization_name(prefix: str) -> str:
    """
    Get the organization name associated with a vendor prefix.
    """
    prefix = prefix.lower().replace("-", ":").replace(".", ":")
    prefix_bytes = bytes.fromhex(prefix)
    if len(prefix_bytes) != 3:
        raise ValueError("Invalid prefix")
    try:
        response = requests.get(MAC_API_URL + prefix)
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException:
        return "Unknown"