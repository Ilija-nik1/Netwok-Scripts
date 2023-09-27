function Get-VPNConnections {
    # Get a list of available VPN connections
    return Get-VpnConnection | Select-Object -Property Name, ServerAddress
}

function Display-VPNConnections($connections) {
    # Display the list of VPN connections with numbers and spacing
    Write-Host "Available VPN Connections:"
    $connections | ForEach-Object {
        $index = [array]::IndexOf($connections, $_) + 1
        $formattedIndex = "{0,-3}" -f $index  # Add spacing for alignment
        Write-Host "$formattedIndex. $($_.Name) - $($_.ServerAddress)"
    }
}

function Connect-To-VPN($connection) {
    # Connect to the selected VPN connection (if available)
    if ($connection) {
        Write-Host "Connecting to $($connection.Name)..."
        $connectResult = Connect-VpnS2SInterface -Name $connection.Name -AsJob

        # Wait for the connection to complete
        $timeout = 60  # Adjust the timeout as needed
        try {
            Wait-Job $connectResult -Timeout $timeout | Out-Null
            $jobOutput = Receive-Job $connectResult -ErrorAction Stop
            if ($jobOutput -match "Connected") {
                Write-Host "Connected to $($connection.Name)."
            } else {
                Write-Host "Connection to $($connection.Name) failed."
            }
        } catch {
            Write-Host "Connection to $($connection.Name) failed: $_"
        } finally {
            Remove-Job $connectResult
        }
    } else {
        Write-Host "Selected VPN connection not found."
    }
}

# Main script logic
$vpnConnections = Get-VPNConnections
Display-VPNConnections $vpnConnections

do {
    $selectedIndex = Read-Host "Enter the number of the VPN connection you want to connect to"

    if (-not [int]::TryParse($selectedIndex, [ref]$null) -or $selectedIndex -lt 1 -or $selectedIndex -gt $vpnConnections.Count) {
        Write-Host "Invalid selection. Please enter a valid number."
    }
} while (-not [int]::TryParse($selectedIndex, [ref]$null) -or $selectedIndex -lt 1 -or $selectedIndex -gt $vpnConnections.Count)

$selectedConnection = $vpnConnections[$selectedIndex - 1]
Connect-To-VPN $selectedConnection