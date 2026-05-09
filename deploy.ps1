# Deploy script - uploads files directly to Contabo VPS
param(
    [string]$File,
    [string]$Site = "bin"
)

$KeyPath = "$env:USERPROFILE\.ssh\contabo_key"

if ($Site -eq "bin") {
    $RemotePath = "root@161.97.99.30:/home/binrecipes/htdocs/binrecipes.com/"
} elseif ($Site -eq "ital") {
    $RemotePath = "root@161.97.99.30:/home/italricette/htdocs/italricette.com/"
} else {
    Write-Host "Site must be 'bin' or 'ital'"
    exit 1
}

if ($File) {
    scp -i $KeyPath $File $RemotePath
    Write-Host "Uploaded: $File -> $Site"
} else {
    # Sync entire local directory
    $LocalPath = if ($Site -eq "bin") { "C:\Users\hp\Desktop\MY WEBSITE\MYWEBSITE.github.IO\" } else { "C:\Users\hp\Desktop\NEW SITE\" }
    scp -i $KeyPath -r "${LocalPath}*" $RemotePath
    Write-Host "Synced all files -> $Site"
}
