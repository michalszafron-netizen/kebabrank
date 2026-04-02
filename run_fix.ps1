# PowerShell script to fix NULL place_ids
param(
    [Parameter(Mandatory=$true)]
    [string]$DatabaseUrl
)

# Get database URL from .env
$envPath = ".\.env"
if (Test-Path $envPath) {
    $envContent = Get-Content $envPath
    $DatabaseUrl = ($envContent | Select-String -Pattern "DATABASE_URL=(.+)").Matches[0].Groups[1].Value
} else {
    Write-Error "Could not find .env file"
    exit 1
}

Write-Host "Fixing NULL place_ids in database..."
Write-Host "Database URL: $DatabaseUrl"

# Execute SQL fix
try {
    $result = psql $DatabaseUrl -f fix_null_place_ids.sql
    
    if ($result -match "Fixed") {
        Write-Host "✅ Successfully fixed NULL place_ids!"
        Write-Host "Fixed count: $($result | Select-String -Pattern 'Fixed (\d+) records').Matches[0].Groups[1].Value)"
    } else {
        Write-Host "❌ Fix failed: $result"
        Write-Host "Error details: $($result | Out-String)"
    }
} catch {
    Write-Host "❌ Database connection failed: $($_.Exception.Message)"
    Write-Host "Error details: $($_.Exception.ToString())"
}
