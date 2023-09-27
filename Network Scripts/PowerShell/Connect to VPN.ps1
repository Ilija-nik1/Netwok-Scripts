# Get a list of available VPN connections
$vpnConnections = Get-VpnConnection | Select-Object -Property Name, ServerAddress

# Display the list of VPN connections
Write-Host "Available VPN Connections:"
$vpnConnections | ForEach-Object {
    Write-Host "$($_.Name). $($_.ServerAddress)"
}

# Prompt the user to select a VPN connection
$selectedIndex = Read-Host "Enter the number of the VPN connection you want to connect to"

# Validate the user's input
if (-not [int]::TryParse($selectedIndex, [ref]$null) -or $selectedIndex -lt 1 -or $selectedIndex -gt $vpnConnections.Count) {
    Write-Host "Invalid selection. Please enter a valid number."
    exit 1
}

# Connect to the selected VPN connection
$selectedConnection = $vpnConnections[$selectedIndex - 1].Name
Write-Host "Connecting to $selectedConnection..."
$connectResult = Connect-VpnS2SInterface -Name $selectedConnection -AsJob

# Wait for the connection to complete
$timeout = 60  # Adjust the timeout as needed
try {
    Wait-Job $connectResult -Timeout $timeout | Out-Null
    Receive-Job $connectResult | ForEach-Object {
        if ($_ -match "Connected") {
            Write-Host "Connected to $selectedConnection."
        } else {
            Write-Host "Connection to $selectedConnection failed."
        }
    }
} catch {
    Write-Host "Connection to $selectedConnection failed: $_"
} finally {
    Remove-Job $connectResult
}