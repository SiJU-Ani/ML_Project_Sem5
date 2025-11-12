param(
  [int]$Port = 5500
)

Write-Host "Serving frontend on http://localhost:$Port (Ctrl+C to stop)" -ForegroundColor Cyan
Push-Location $PSScriptRoot
try {
  python -m http.server $Port
}
finally {
  Pop-Location
}
