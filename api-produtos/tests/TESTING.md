# Guia de Testes - Image Checker

Este documento contém todos os comandos necessários para executar os testes do módulo `image_checker`.

## 📋 Índice

- [Pré-requisitos](#pré-requisitos)
- [Comandos Básicos](#comandos-básicos)
- [Testes por Categoria](#testes-por-categoria)
- [Testes por Arquivo](#testes-por-arquivo)
- [Testes Específicos](#testes-específicos)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Níveis de Verbosidade](#níveis-de-verbosidade)
- [Cobertura de Código](#cobertura-de-código)
- [Troubleshooting](#troubleshooting)

---

## Pré-requisitos

### Instalar Dependências

```bash
pip install -r requirements.txt
```

### Configurar Variáveis de Ambiente

Os testes de integração requerem variáveis de ambiente configuradas no arquivo `.env`:

- `REDIS_HOST` - Host do Redis
- `REDIS_PORT` - Porta do Redis
- `REDIS_PASSWORD` - Senha do Redis (opcional)
- `REDIS_DB` - Database do Redis
- `REDIS_SSL` - SSL habilitado (true/false)
- `COPAFER_API_BASE_URL` - URL base da API Copafer
- `COPAFER_AUTH_HEADER` - Header de autenticação
- `COPAFER_AUTH_TOKEN` - Token de autenticação
- `OPENROUTER_API_URL` - URL da API OpenRouter
- `OPENROUTER_API_KEY` - Chave da API OpenRouter
- `OPENROUTER_MODEL` - Modelo a ser usado
- `IMAGE_CACHE_TTL` - TTL do cache (padrão: 259200 segundos = 3 dias)

**Nota**: Os testes unitários não requerem essas variáveis, pois usam mocks.

---

## Comandos Básicos

### Executar Todos os Testes

```bash
pytest
```

### Executar Todos os Testes com Verbosidade

```bash
pytest -v
```

### Executar Todos os Testes com Output Detalhado

```bash
pytest -vv
```

### Executar Todos os Testes e Mostrar Prints

```bash
pytest -s
```

### Executar Todos os Testes com Logs

```bash
pytest --log-cli-level=INFO
```

### Executar Todos os Testes com Logs DEBUG

```bash
pytest -v -s --log-cli-level=DEBUG
```

---

## Testes por Categoria

### Executar Apenas Testes Unitários

Os testes unitários são mockados e não requerem serviços externos:

```bash
pytest -m unit
```

### Executar Apenas Testes de Integração

Os testes de integração requerem serviços externos (Redis, API Copafer, OpenRouter):

```bash
pytest -m integration
```

### Executar Testes de Integração com Verbosidade

```bash
pytest -m integration -v
```

### Executar Testes de Integração com Output Detalhado

```bash
pytest -m integration -vv
```

---

## Testes por Arquivo

### Testes Redis (Unitários)

```bash
pytest tests/test_image_checker_redis.py
```

Com verbosidade:

```bash
pytest tests/test_image_checker_redis.py -v
```

### Testes Copafer (Unitários)

```bash
pytest tests/test_image_checker_copafer.py
```

Com verbosidade:

```bash
pytest tests/test_image_checker_copafer.py -v
```

### Testes OpenRouter (Unitários)

```bash
pytest tests/test_image_checker_openrouter.py
```

Com verbosidade:

```bash
pytest tests/test_image_checker_openrouter.py -v
```

### Testes de Fluxo (Unitários)

```bash
pytest tests/test_image_checker_flow.py
```

Com verbosidade:

```bash
pytest tests/test_image_checker_flow.py -v
```

### Testes de Integração

```bash
pytest tests/test_image_checker_integration.py
```

Com verbosidade:

```bash
pytest tests/test_image_checker_integration.py -v
```

### Testes de Compatibilidade (Integração)

```bash
pytest tests/test_image_checker_compatibility.py
```

Com verbosidade:

```bash
pytest tests/test_image_checker_compatibility.py -v
```

---

## Testes Específicos

### Executar uma Classe de Teste Específica

```bash
pytest tests/test_image_checker_redis.py::TestGetRedisClient
```

### Executar um Teste Específico

```bash
pytest tests/test_image_checker_redis.py::TestGetRedisClient::test_returns_client_when_ping_succeeds
```

### Executar Testes que Contêm um Padrão no Nome

```bash
pytest -k "redis"
```

```bash
pytest -k "cache"
```

```bash
pytest -k "openrouter"
```

---

## Variáveis de Ambiente

### Pular Testes de Redis

Se o Redis não estiver disponível, você pode pular os testes de integração que dependem dele:

```bash
SKIP_REDIS_TESTS=true pytest -m integration
```

No Windows (PowerShell):

```powershell
$env:SKIP_REDIS_TESTS="true"; pytest -m integration
```

No Windows (CMD):

```cmd
set SKIP_REDIS_TESTS=true && pytest -m integration
```

### Pular Testes da API Copafer

```bash
SKIP_COPAFER_TESTS=true pytest -m integration
```

No Windows (PowerShell):

```powershell
$env:SKIP_COPAFER_TESTS="true"; pytest -m integration
```

No Windows (CMD):

```cmd
set SKIP_COPAFER_TESTS=true && pytest -m integration
```

### Pular Testes do OpenRouter

```bash
SKIP_OPENROUTER_TESTS=true pytest -m integration
```

No Windows (PowerShell):

```powershell
$env:SKIP_OPENROUTER_TESTS="true"; pytest -m integration
```

No Windows (CMD):

```cmd
set SKIP_OPENROUTER_TESTS=true && pytest -m integration
```

### Pular Múltiplos Tipos de Testes

```bash
SKIP_REDIS_TESTS=true SKIP_COPAFER_TESTS=true SKIP_OPENROUTER_TESTS=true pytest -m integration
```

No Windows (PowerShell):

```powershell
$env:SKIP_REDIS_TESTS="true"; $env:SKIP_COPAFER_TESTS="true"; $env:SKIP_OPENROUTER_TESTS="true"; pytest -m integration
```

---

## Níveis de Verbosidade

### Modo Silencioso (apenas resultados)

```bash
pytest -q
```

### Modo Normal

```bash
pytest
```

### Modo Verboso (mostra nomes dos testes)

```bash
pytest -v
```

### Modo Muito Verboso (mostra mais detalhes)

```bash
pytest -vv
```

### Modo Muito Muito Verboso (mostra tudo)

```bash
pytest -vvv
```

### Mostrar Prints e Output

```bash
pytest -s
```

### Combinar Verbosidade e Output

```bash
pytest -v -s
```

---

## Cobertura de Código

### Instalar pytest-cov (se ainda não instalado)

```bash
pip install pytest-cov
```

### Executar Testes com Cobertura

```bash
pytest --cov=image_checker --cov-report=term-missing
```

### Gerar Relatório HTML de Cobertura

```bash
pytest --cov=image_checker --cov-report=html
```

O relatório será gerado em `htmlcov/index.html`.

### Cobertura com Limite Mínimo

```bash
pytest --cov=image_checker --cov-report=term-missing --cov-fail-under=80
```

---

## Modo Watch (Desenvolvimento)

### Instalar pytest-watch (se ainda não instalado)

```bash
pip install pytest-watch
```

### Executar Testes em Modo Watch

```bash
ptw
```

### Executar Testes em Modo Watch com Verbosidade

```bash
ptw -v
```

### Executar Apenas Testes Unitários em Modo Watch

```bash
ptw -m unit
```

---

## Executar Testes em Paralelo

### Instalar pytest-xdist (se ainda não instalado)

```bash
pip install pytest-xdist
```

### Executar Testes em Paralelo (4 workers)

```bash
pytest -n 4
```

### Executar Testes em Paralelo (auto-detecta CPUs)

```bash
pytest -n auto
```

**Nota**: Testes de integração podem não funcionar bem em paralelo se compartilharem recursos (ex: Redis).

---

## Troubleshooting

### Testes Falhando com "ModuleNotFoundError"

Certifique-se de estar no diretório raiz do projeto:

```bash
cd /caminho/para/api-produtos
pytest
```

### Testes de Integração Falhando

1. Verifique se as variáveis de ambiente estão configuradas:

```bash
# Linux/Mac
cat .env

# Windows
type .env
```

2. Teste a conexão com Redis manualmente:

```python
import redis
r = redis.Redis(host='seu_host', port=6379)
r.ping()
```

3. Use variáveis de ambiente para pular testes problemáticos:

```bash
SKIP_REDIS_TESTS=true pytest -m integration
```

### Testes Muito Lentos

Execute apenas testes unitários durante desenvolvimento:

```bash
pytest -m unit
```

Execute testes de integração apenas antes de commits:

```bash
pytest -m integration
```

### Ver Logs Detalhados Durante Testes

```bash
pytest -v -s --log-cli-level=DEBUG
```

### Ver Apenas Testes que Falharam

```bash
pytest --lf
```

### Executar Apenas Testes que Falharam na Última Execução

```bash
pytest --ff
```

---

## Comandos Úteis para CI/CD

### Executar Testes e Falhar se Cobertura < 80%

```bash
pytest --cov=image_checker --cov-fail-under=80 --cov-report=term-missing
```

### Executar Testes com JUnit XML (para CI)

```bash
pytest --junitxml=test-results.xml
```

### Executar Testes e Gerar Relatório JSON

```bash
pytest --json-report --json-report-file=test-report.json
```

**Nota**: Requer `pytest-json-report`:

```bash
pip install pytest-json-report
```

---

## Resumo de Comandos Mais Usados

### Desenvolvimento Diário

```bash
# Apenas testes unitários (rápido)
pytest -m unit -v

# Todos os testes (antes de commit)
pytest -v
```

### Antes de Deploy

```bash
# Todos os testes com cobertura
pytest --cov=image_checker --cov-report=term-missing -v

# Testes de integração completos
pytest -m integration -v
```

### Debugging

```bash
# Ver logs detalhados
pytest -v -s --log-cli-level=DEBUG

# Executar teste específico
pytest tests/test_image_checker_redis.py::TestGetRedisClient::test_returns_client_when_ping_succeeds -v -s
```

---

## Estrutura dos Testes

```
tests/
├── conftest.py                          # Fixtures compartilhadas
├── test_image_checker_redis.py         # Testes unitários Redis
├── test_image_checker_copafer.py       # Testes unitários API Copafer
├── test_image_checker_openrouter.py    # Testes unitários OpenRouter
├── test_image_checker_flow.py          # Testes unitários fluxo completo
├── test_image_checker_integration.py   # Testes de integração
└── test_image_checker_compatibility.py # Testes de compatibilidade N8N
```

---

## Referências

- [Documentação pytest](https://docs.pytest.org/)
- [Documentação image_checker](../docs/image_checker.md)
- [Plano de implementação](../.context/plans/image-checker-implementation.md)

