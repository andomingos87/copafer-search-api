# Plano (ai-coders): Testes automatizados do `image_checker.py`

## Título
**Testes automatizados para `image_checker.py` (Redis + API Copafer + OpenRouter)**

## Resumo / Objetivo
Criar uma suíte de testes automatizados para validar o comportamento do módulo `image_checker.py` com foco em:
- Garantir compatibilidade com o fluxo do N8N (`/is-image-exists`)
- Cobrir cenários de cache (Redis), ausência de imagens (API Copafer) e decisão do modelo (OpenRouter)
- Tornar o desenvolvimento seguro para evoluções na Fase 3 (endpoint no `api.py`) e além

## Contexto e referências
- **Especificação técnica**: `docs/image_checker.md`
- **Workflow N8N (fonte de verdade do fluxo/compatibilidade)**: `docs/se_img_existe.md`
- **Módulo alvo**: `image_checker.py`

## Escopo
### Dentro do escopo
- Testes **unitários** com mocks (sem depender de Redis/API externa reais)
- Testes do fluxo principal `check_image_exists(produto_id)` cobrindo:
  - cache hit (base64 e `"null"`)
  - cache miss + API sem imagens
  - cache miss + API com imagens + OpenRouter escolhe índice válido
  - OpenRouter retorna código especial `932042349`
  - falhas de Redis / API Copafer / OpenRouter
- Validações de payload e parsing:
  - `prepare_openrouter_payload`
  - `call_openrouter` (parse de `choices[0].message.content`)
- Testes mínimos dos modelos Pydantic (`ImageCheckRequest`, `ImageCheckResponse`)

### Fora do escopo (por enquanto)
- Testes E2E do endpoint FastAPI (`api.py`) — isso entra na Fase 3
- Teste com chamadas reais ao OpenRouter (custo + flakiness). Só opcional via marcação “manual/integration”.
- Performance tests / load tests

## Estratégia de testes
### Ferramentas
- `pytest` como test runner
- `pytest-mock` (ou `unittest.mock`) para mocks
- `fakeredis` **opcional** (se quisermos simular Redis com comportamento realista)

### Pirâmide de testes
- **Unitário (principal)**: 90%+ dos casos, totalmente mockado
- **Integração (opcional)**: poucos casos, executados sob flag/marker

## Design dos testes (casos alvo)
### Redis
- `get_redis_client`
  - retorna cliente quando `ping()` funciona
  - retorna `None` quando falha ao conectar/pingar
- `get_cached_image`
  - retorna valor quando existe
  - retorna `None` quando Redis indisponível / erro
- `set_cached_image`
  - grava base64 com `setex` e TTL
  - grava `"null"` quando `base64_value is None`
  - retorna `False` quando Redis indisponível / erro

### API Copafer (requests.get)
- resposta ok com `images=[{"base64": "..."}]` -> `ok=True` e lista filtrada
- resposta ok sem `images` ou `images` inválido -> `ok=False`
- `HTTPError` / timeout -> `ok=False` e mensagem de erro

### OpenRouter (requests.post)
- resposta ok com `choices[0].message.content` JSON válido -> parse correto
- conteúdo vazio / choices vazio -> `ok=False`
- JSON inválido -> `ok=False` com erro de parse
- `HTTPError` / timeout -> `ok=False`

### Função principal `check_image_exists`
- **cache hit base64** -> `imageExists=True`
- **cache hit "null"** -> `imageExists=False`
- **cache miss + API sem imagens** -> `imageExists=False` e grava cache `"null"`
- **cache miss + API com imagens + IA escolhe índice válido** -> `imageExists=True` e grava base64 escolhido
- **cache miss + IA retorna `932042349`** -> `imageExists=False` e grava `"null"`
- **IA falha** -> `imageExists=False` e grava `"null"` (conforme doc)
- **Copafer falha** -> `imageExists=False` (decidir se grava cache negativo — alinhar com doc; atualmente grava)

## Estrutura de arquivos proposta
- `tests/`
  - `test_image_checker_redis.py`
  - `test_image_checker_copafer.py`
  - `test_image_checker_openrouter.py`
  - `test_image_checker_flow.py`
  - `conftest.py` (fixtures comuns)

## Tarefas (checklist executável)
### Preparação
- [x] Adicionar dependências de teste (`pytest`, `pytest-mock`, opcional `fakeredis`) no `requirements.txt`
- [x] Criar pasta `tests/` com estrutura proposta
- [x] Adicionar `pytest.ini` (ou config equivalente) com markers: `unit`, `integration`

### Implementação dos testes
- [x] Fixtures em `conftest.py`:
  - imagens base64 dummy (sem conteúdo real, apenas string)
  - respostas mockadas de Copafer e OpenRouter
- [x] Testes unitários de Redis (mocks ou fakeredis)
- [x] Testes unitários de `fetch_product_images` (mock `requests.get`)
- [x] Testes unitários de `prepare_openrouter_payload` (estrutura do payload + remoção de quebras de linha)
- [x] Testes unitários de `call_openrouter` (mock `requests.post`)
- [x] Testes de fluxo de `check_image_exists` (mockar funções internas: cache/fetch/IA/set)

### Integração opcional (apenas se desejado)
- [ ] Marker `@pytest.mark.integration` para:
  - Redis real (se existir no ambiente)
  - chamada real para Copafer (se token disponível)
  - **não** chamar OpenRouter por padrão (manual)
  
**Nota**: Testes de integração foram deixados de fora do escopo inicial conforme o plano. Todos os testes unitários foram implementados e estão passando (52 testes, ~0.5s de execução).

## Critérios de aceitação
- **Cobertura funcional**: todos os cenários listados em “Design dos testes” passam
- **Determinismo**: testes unitários não dependem de rede/Redis real
- **Compatibilidade**: validações cobrem chave Redis `best_image_for_{produto_id}`, TTL padrão e código especial `932042349`
- **Execução**: `pytest` roda localmente em < 10s (meta) sem serviços externos

## Comandos de execução (dev)
- Rodar tudo:
  - `pytest -q`
- Rodar só unitários:
  - `pytest -q -m unit`
- Rodar integração (quando habilitado):
  - `pytest -q -m integration`

## Riscos / Notas
- **Ambiente Windows**: preferir executar `python -m pytest` usando o Python do `.venv`.
- **Variáveis de ambiente**: testes devem usar `monkeypatch` para não depender de `.env`.
- **Decisões de cache negativo**: alinhar comportamento esperado com `docs/image_checker.md` vs implementação atual (hoje grava `"null"` em mais cenários).


