# Deploy da API FastAPI na Fly.io

Este guia completo ensina como fazer o deploy desta aplicação FastAPI na plataforma [Fly.io](https://fly.io), uma plataforma de hospedagem global que permite rodar aplicações próximas dos usuários.

---

## Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação do Fly CLI](#instalação-do-fly-cli)
3. [Autenticação](#autenticação)
4. [Criação do Dockerfile](#criação-do-dockerfile)
5. [Configuração do fly.toml](#configuração-do-flytoml)
6. [Configuração de Variáveis de Ambiente (Secrets)](#configuração-de-variáveis-de-ambiente-secrets)
7. [Deploy da Aplicação](#deploy-da-aplicação)
8. [Comandos Úteis Pós-Deploy](#comandos-úteis-pós-deploy)
9. [Estrutura de Custos](#estrutura-de-custos)
10. [Troubleshooting](#troubleshooting)

---

## Pré-requisitos

Antes de iniciar, certifique-se de ter:

- **Git** instalado
- **Python 3.10+** (para testes locais)
- **Conta no Fly.io** (crie em [fly.io/app/sign-up](https://fly.io/app/sign-up))
- **Variáveis de ambiente** configuradas localmente no `.env`:
  - `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` (Postgres)
  - `OPENAI_API_KEY`, `EMB_MODEL`, `EMB_DIM` (OpenAI)
  - `VTEX_APP_KEY`, `VTEX_APP_TOKEN`, `VTEX_ACCOUNT_HOST` (VTEX)
  - `X_COPAFER_KEY` (Cubo API)

---

## Instalação do Fly CLI

O **flyctl** (ou simplesmente `fly`) é a ferramenta de linha de comando necessária para interagir com a Fly.io.

### Windows (PowerShell)

```powershell
pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

> Se o comando `pwsh` não for encontrado, use `powershell` no lugar.

### macOS (Homebrew)

```bash
brew install flyctl
```

### macOS/Linux (Script de instalação)

```bash
curl -L https://fly.io/install.sh | sh
```

Após a instalação, adicione o diretório do `fly` ao seu PATH (se necessário). Geralmente o instalador mostra instruções específicas.

### Verificar instalação

```bash
fly version
```

Você deve ver algo como: `fly v0.x.x ...`

---

## Autenticação

### Criar conta (se ainda não tem)

```bash
fly auth signup
```

Isso abrirá o navegador para criar sua conta.

### Login (conta existente)

```bash
fly auth login
```

O navegador será aberto para autenticação. Após autorizar, o terminal confirmará o login.

---

## Criação do Dockerfile

Crie um arquivo `Dockerfile` na raiz do projeto com o seguinte conteúdo:

```dockerfile
# =============================================================================
# Dockerfile para FastAPI Search Products API
# =============================================================================

# Imagem base Python
FROM python:3.11-slim-bookworm

# Variáveis de ambiente para otimizar Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema (necessário para psycopg2-binary e outras libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivo de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Expor a porta que a aplicação usa
EXPOSE 8000

# Comando para iniciar a aplicação
# Usamos uvicorn com host 0.0.0.0 para aceitar conexões externas
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Criar arquivo `.dockerignore`

Crie também um `.dockerignore` para evitar copiar arquivos desnecessários:

```plaintext
# Ambiente virtual
venv/
.venv/
env/

# Cache Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Arquivos de ambiente (NÃO incluir secrets no container!)
.env
.env.*
*.env

# Git
.git/
.gitignore

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Arquivos temporários
*.tmp
*.temp
*.log

# Testes
.pytest_cache/
.coverage

# Documentação local
docs-web/

# Arquivos grandes de dados (se houver)
*.csv
!resumido_200.csv
```

---

## Configuração do fly.toml

Você pode criar o arquivo de configuração de duas formas:

### Opção 1: Usando `fly launch` (recomendado para primeira vez)

Execute na raiz do projeto:

```bash
fly launch
```

O comando irá:
1. Detectar automaticamente o Dockerfile
2. Perguntar o nome da aplicação
3. Perguntar a região de deploy
4. Criar o arquivo `fly.toml`

Se preferir **não fazer deploy imediatamente** (para configurar secrets primeiro):

```bash
fly launch --no-deploy
```

### Opção 2: Criar manualmente

Crie o arquivo `fly.toml` na raiz do projeto:

```toml
# =============================================================================
# fly.toml - Configuração de deploy Fly.io
# =============================================================================

# Nome da aplicação (deve ser único globalmente)
app = "search-products-api"

# Região principal (escolha a mais próxima dos seus usuários)
# Algumas opções: gru (São Paulo), iad (Virginia), ewr (New Jersey)
primary_region = "gru"

# =============================================================================
# Configuração de build
# =============================================================================
[build]
  dockerfile = "Dockerfile"

# =============================================================================
# Variáveis de ambiente NÃO sensíveis
# Para variáveis sensíveis, use `fly secrets set`
# =============================================================================
[env]
  # Configurações gerais
  LOG_LEVEL = "info"
  
  # Modelo de embedding (pode ser público)
  EMB_MODEL = "text-embedding-3-small"
  EMB_DIM = "1536"

# =============================================================================
# Configuração do serviço HTTP
# =============================================================================
[http_service]
  # Porta interna que a aplicação escuta
  internal_port = 8000
  
  # Forçar HTTPS
  force_https = true
  
  # Auto-scaling: parar máquinas ociosas para economizar
  auto_stop_machines = "stop"
  auto_start_machines = true
  
  # Mínimo de máquinas rodando (0 = pode parar todas quando ocioso)
  min_machines_running = 0
  
  # Processo que roda este serviço
  processes = ["app"]

# =============================================================================
# Health checks - verificação de saúde da aplicação
# =============================================================================
[[http_service.checks]]
  # Intervalo entre verificações
  interval = "30s"
  
  # Tempo limite para resposta
  timeout = "5s"
  
  # Quantas falhas consecutivas antes de considerar unhealthy
  grace_period = "10s"
  
  # Método e path para verificação
  method = "GET"
  path = "/docs"

# =============================================================================
# Configuração da máquina virtual
# =============================================================================
[[vm]]
  # Tipo de CPU: shared (compartilhada) ou performance (dedicada)
  cpu_kind = "shared"
  
  # Quantidade de CPUs
  cpus = 1
  
  # Memória RAM
  memory = "512mb"
```

### Regiões disponíveis

Algumas regiões populares:

| Código | Localização |
|--------|-------------|
| `gru`  | São Paulo, Brasil |
| `iad`  | Ashburn, Virginia (EUA) |
| `ewr`  | Secaucus, NJ (EUA) |
| `lhr`  | Londres, UK |
| `fra`  | Frankfurt, Alemanha |
| `nrt`  | Tóquio, Japão |
| `syd`  | Sydney, Austrália |

Para listar todas as regiões:

```bash
fly platform regions
```

---

## Configuração de Variáveis de Ambiente (Secrets)

**IMPORTANTE:** Variáveis sensíveis (senhas, API keys, tokens) devem ser configuradas como **secrets** e NÃO no `fly.toml`.

### Configurar todos os secrets necessários

Execute os comandos abaixo, substituindo pelos valores reais:

```bash
# Banco de dados PostgreSQL
fly secrets set DB_HOST="seu-host-postgres.exemplo.com"
fly secrets set DB_PORT="5432"
fly secrets set DB_USER="seu_usuario"
fly secrets set DB_PASSWORD="sua_senha_segura"
fly secrets set DB_NAME="nome_do_banco"

# OpenAI API
fly secrets set OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxx"

# VTEX (se aplicável)
fly secrets set VTEX_APP_KEY="sua_vtex_app_key"
fly secrets set VTEX_APP_TOKEN="seu_vtex_app_token"
fly secrets set VTEX_ACCOUNT_HOST="sua-loja.myvtex.com"

# Cubo API (se aplicável)
fly secrets set X_COPAFER_KEY="sua_chave_copafer"
```

### Configurar múltiplos secrets de uma vez

Você pode configurar vários de uma vez:

```bash
fly secrets set \
  DB_HOST="host" \
  DB_PORT="5432" \
  DB_USER="user" \
  DB_PASSWORD="pass" \
  DB_NAME="dbname"
```

### Verificar secrets configurados

```bash
fly secrets list
```

> **Nota:** Os valores não são exibidos por segurança, apenas os nomes.

### Remover um secret

```bash
fly secrets unset NOME_DA_VARIAVEL
```

---

## Deploy da Aplicação

### Primeiro deploy

Se você usou `fly launch --no-deploy`, agora execute:

```bash
fly deploy
```

### Deploys subsequentes

Sempre que fizer alterações no código:

```bash
fly deploy
```

### O que acontece durante o deploy

1. **Build**: O Dockerfile é construído em um builder remoto da Fly.io
2. **Push**: A imagem é enviada para o registro da Fly.io
3. **Deploy**: Novas máquinas são criadas com a nova imagem
4. **Health check**: Fly.io verifica se a aplicação está saudável
5. **Cutover**: Tráfego é direcionado para as novas máquinas

### Acompanhar o deploy

O progresso é mostrado no terminal. Para ver logs em tempo real:

```bash
fly logs
```

---

## Comandos Úteis Pós-Deploy

### Ver status da aplicação

```bash
fly status
```

### Abrir a aplicação no navegador

```bash
fly open
```

### Ver logs em tempo real

```bash
fly logs
```

### Listar máquinas

```bash
fly machines list
```

### Acessar console SSH na máquina

```bash
fly ssh console
```

### Reiniciar a aplicação

```bash
fly apps restart
```

### Escalar para mais máquinas

```bash
# Escalar para 2 máquinas
fly scale count 2
```

### Escalar recursos (CPU/memória)

```bash
# Ver opções disponíveis
fly scale show

# Mudar para 1GB de RAM
fly scale memory 1024
```

### Ver métricas e monitoramento

```bash
fly dashboard
```

Ou acesse: https://fly.io/apps/NOME-DA-SUA-APP/monitoring

### Destruir a aplicação (cuidado!)

```bash
fly apps destroy nome-da-app
```

---

## Estrutura de Custos

A Fly.io oferece um plano gratuito generoso:

### Plano Gratuito (Hobby)
- **3 VMs compartilhadas** (256MB RAM cada)
- **3GB de armazenamento** persistente
- **160GB de transferência** de saída/mês

### Dicas para economizar

1. **Auto-stop**: Configure `auto_stop_machines = "stop"` para pausar máquinas ociosas
2. **Região única**: Comece com uma região apenas
3. **Memória mínima**: 256MB ou 512MB para APIs simples
4. **CPU compartilhada**: Use `cpu_kind = "shared"` para cargas leves

### Verificar uso

```bash
fly billing
```

Ou acesse: https://fly.io/dashboard/personal/billing

---

## Troubleshooting

### Problema: Deploy falha no build

**Sintoma:** Erro durante `pip install`

**Soluções:**
1. Verifique se `requirements.txt` está correto
2. Adicione dependências de sistema no Dockerfile se necessário

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
```

---

### Problema: Aplicação não inicia

**Sintoma:** Health check falha

**Soluções:**
1. Verifique os logs: `fly logs`
2. Confirme que a porta é 8000 e host é `0.0.0.0`
3. Verifique se todos os secrets estão configurados: `fly secrets list`

---

### Problema: Erro de conexão com banco de dados

**Sintoma:** `Connection refused` ou timeout

**Soluções:**
1. Verifique se o banco permite conexões externas
2. Adicione o IP da Fly.io ao allowlist do banco (se aplicável)
3. Use um banco gerenciado compatível (ex: Supabase, Neon, Railway)

Para ver IPs de saída da Fly.io:

```bash
fly ips list
```

---

### Problema: Variáveis de ambiente não funcionam

**Sintoma:** Aplicação não encontra variáveis

**Soluções:**
1. Use `fly secrets list` para verificar
2. Após adicionar secrets, faça redeploy: `fly deploy`
3. No código, acesse via `os.environ.get("NOME_VARIAVEL")`

---

### Problema: Aplicação muito lenta no primeiro request

**Sintoma:** Cold start demorado

**Causa:** Com `auto_stop_machines = "stop"`, máquinas param quando ociosas

**Soluções:**
1. Configure `min_machines_running = 1` para manter uma máquina sempre ativa
2. Ou aceite o cold start (geralmente 1-3 segundos)

---

### Verificar diagnósticos gerais

```bash
# Status detalhado
fly status --all

# Verificar configuração
fly config show

# Ver releases/versões anteriores
fly releases

# Fazer rollback para versão anterior
fly releases rollback
```

---

## Checklist Rápido para Deploy

```
[ ] Fly CLI instalado (`fly version`)
[ ] Autenticado (`fly auth login`)
[ ] Dockerfile criado e testado localmente
[ ] .dockerignore configurado (sem .env!)
[ ] fly.toml configurado
[ ] Secrets configurados (`fly secrets set ...`)
[ ] Deploy executado (`fly deploy`)
[ ] Aplicação testada (`fly open`)
```

---

## Recursos Adicionais

- **Documentação oficial:** https://fly.io/docs
- **Status da plataforma:** https://status.fly.io
- **Comunidade:** https://community.fly.io
- **Pricing:** https://fly.io/pricing

---

## Exemplo de Script de Deploy Automatizado

Crie um arquivo `deploy.sh` para facilitar deploys:

```bash
#!/bin/bash
# deploy.sh - Script de deploy para Fly.io

set -e

echo "🚀 Iniciando deploy para Fly.io..."

# Verificar se está logado
if ! fly auth whoami > /dev/null 2>&1; then
    echo "❌ Não autenticado. Execute: fly auth login"
    exit 1
fi

# Verificar secrets (opcional - apenas aviso)
echo "📋 Verificando secrets..."
fly secrets list

# Deploy
echo "📦 Executando deploy..."
fly deploy

# Status
echo "✅ Deploy concluído!"
fly status

echo ""
echo "🌐 Acesse sua aplicação:"
fly open --no-browser && echo "URL: https://$(fly status --json | grep -o '"Hostname":"[^"]*"' | cut -d'"' -f4)"
```

Torne executável:

```bash
chmod +x deploy.sh
```

Use:

```bash
./deploy.sh
```

---

**Última atualização:** Dezembro 2024

