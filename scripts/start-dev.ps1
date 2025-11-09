# ===============================
# Script: scripts/start-dev.ps1
# ===============================
param(
    [string]$Rede = "192.168.0.0"  # Rede padrão (pode ser alterada)
)

Write-Host "Verificando se o Docker Desktop está rodando..."

try {
    docker info > $null 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Docker não está ativo"
    }
    Write-Host "Docker já está em execução."
} catch {
    Write-Host "Iniciando o Docker Desktop..."
    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    
    Write-Host "⏳ Aguardando o Docker iniciar..."
    $tentativas = 0
    while ($tentativas -lt 30) {
        Start-Sleep -Seconds 5
        docker info > $null 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Docker iniciado com sucesso!"
            break
        }
        $tentativas++
        Write-Host "Aguardando ($tentativas/30)..."
    }
}

# Adiciona a regra de firewall
# Write-Host "Configurando regra de firewall para porta 8080..."
# $ruleName = "Allow 8080 TCP LAN"
# if (-not (Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue)) {
#     New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -LocalPort 8080 -Protocol TCP -RemoteAddress "$Rede/24" -Action Allow
#     Write-Host "Regra de firewall criada para $Rede/24."
# } else {
#     Write-Host "ℹRegra de firewall já existente."
# }

# Sobe o container a partir da raiz do projeto
Write-Host "Subindo container em modo desenvolvimento..."
docker compose -f container/docker-compose-dev.yml up -d

# Mostra logs do container principal
Write-Host "Mostrando últimos logs..."
docker logs --tail 100 -f api-flask-csv-container
