param(
    [string]$Platform = "StandaloneWindows64",
    [string]$ConfigPath = "",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

function Resolve-RepoRoot {
    $scriptDir = Split-Path -Parent $PSCommandPath
    return (Resolve-Path (Join-Path $scriptDir "../..")).Path
}

function Read-UploadConfig {
    param([string]$Path)

    if ([string]::IsNullOrWhiteSpace($Path)) {
        $Path = Join-Path (Split-Path -Parent $PSCommandPath) "AAUploadData.json"
    }
    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Upload config not found: $Path. Copy upload-addressables.temp.json to AAUploadData.json and fill server info."
    }

    return Get-Content -Raw -Encoding UTF8 -LiteralPath $Path | ConvertFrom-Json
}

function Assert-Config {
    param($Config)

    foreach ($field in @("host", "user", "remoteRoot")) {
        if ([string]::IsNullOrWhiteSpace($Config.$field)) {
            throw "Upload config missing field: $field"
        }
    }
    if (-not $Config.port) {
        $Config | Add-Member -NotePropertyName port -NotePropertyValue 22 -Force
    }
}

function Resolve-ConfigText {
    param(
        $Config,
        [string]$Value
    )

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return $Value
    }
    return "$Value".Replace("{host}", "$($Config.host)")
}

function New-SshArguments {
    param($Config)

    $args = @(
        "-p", "$($Config.port)",
        "-o", "BatchMode=yes",
        "-o", "ConnectTimeout=30",
        "-o", "StrictHostKeyChecking=accept-new"
    )
    if (-not [string]::IsNullOrWhiteSpace($Config.privateKey)) {
        $args += @("-i", "$($Config.privateKey)")
    }
    return $args
}

function New-ScpArguments {
    param($Config)

    $args = @(
        "-P", "$($Config.port)",
        "-o", "BatchMode=yes",
        "-o", "ConnectTimeout=30",
        "-o", "StrictHostKeyChecking=accept-new"
    )
    if (-not [string]::IsNullOrWhiteSpace($Config.privateKey)) {
        $args += @("-i", "$($Config.privateKey)")
    }
    return $args
}

$repoRoot = Resolve-RepoRoot
$config = Read-UploadConfig -Path $ConfigPath
Assert-Config -Config $config

$localPath = Join-Path $repoRoot "ServerData/$Platform"
if (-not (Test-Path -LiteralPath $localPath)) {
    throw "Local Addressables directory not found: $localPath. Build Addressables in Unity first."
}

$remoteRoot = (Resolve-ConfigText -Config $config -Value "$($config.remoteRoot)").TrimEnd("/")
$remotePath = "$remoteRoot/$Platform"
$remoteTarget = "$($config.user)@$($config.host)"
$sshArgs = New-SshArguments -Config $config
$scpArgs = New-ScpArguments -Config $config
$remoteCommand = "rm -rf '$remotePath' && mkdir -p '$remotePath'"

Write-Host "Local path: $localPath"
Write-Host "Remote path: ${remoteTarget}:$remotePath"

if ($DryRun) {
    Write-Host "[DryRun] ssh $($sshArgs -join ' ') $remoteTarget $remoteCommand"
    Write-Host "[DryRun] scp $($scpArgs -join ' ') -r $localPath/* ${remoteTarget}:$remotePath/"
    return
}

ssh @sshArgs $remoteTarget $remoteCommand
if ($LASTEXITCODE -ne 0) {
    throw "Failed to prepare remote directory."
}

scp @scpArgs -r "$localPath/*" "${remoteTarget}:$remotePath/"
if ($LASTEXITCODE -ne 0) {
    throw "Failed to upload Addressables."
}

if (-not [string]::IsNullOrWhiteSpace($config.publicBaseUrl)) {
    $baseUrl = (Resolve-ConfigText -Config $config -Value "$($config.publicBaseUrl)").TrimEnd("/")
    Write-Host "Upload completed: $baseUrl/$Platform/"
} else {
    Write-Host "Upload completed."
}
