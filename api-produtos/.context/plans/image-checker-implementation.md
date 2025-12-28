# Plano de Implementação: Image Checker

## Objetivo

Implementar a funcionalidade de verificação de imagem de produto em Python, substituindo o workflow N8N atual (`se_img_existe`). A funcionalidade deve verificar se existe uma imagem adequada para um produto, utilizando cache Redis para otimização e inteligência artificial (OpenRouter/GPT-5) para selecionar a melhor imagem entre múltiplas opções.

## Contexto

- **Workflow N8N atual**: `docs-dev/se_img_existe.json`
- **Documentação de referência**: `docs/se_img_existe.md`
- **Especificação técnica**: `docs/image_checker.md`
- **Padrões do projeto**: Seguir estrutura de `vtex_shipping.py` e `api.py`

## Fases de Implementação

### Fase 1: Preparação do Ambiente

#### 1.1 Atualizar Dependências
- [x] Adicionar `redis` ao `requirements.txt`
- [x] Verificar se `openai` está atualizado
- [x] Executar `pip install -r requirements.txt`

**Artefatos**:
- `requirements.txt` atualizado

**Referências**:
- `docs/image_checker.md` - Seção "Dependências Necessárias"

---

#### 1.2 Configurar Variáveis de Ambiente
- [x] Adicionar variáveis Redis ao `.env`:
  - `REDIS_HOST`
  - `REDIS_PORT`
  - `REDIS_PASSWORD` (opcional)
  - `REDIS_DB`
- [x] Adicionar variáveis API Copafer:
  - `COPAFER_API_BASE_URL`
  - `COPAFER_AUTH_HEADER`
  - `COPAFER_AUTH_TOKEN`
- [x] Adicionar variáveis OpenRouter:
  - `OPENROUTER_API_URL`
  - `OPENROUTER_API_KEY`
  - `OPENROUTER_MODEL`
- [x] Adicionar `IMAGE_CACHE_TTL`

**Artefatos**:
- `.env` atualizado (ou `.env.example` se não existir)

**Referências**:
- `docs/image_checker.md` - Seção "Configuração (.env)"
- `vtex_shipping.py` - Padrão de configuração via dotenv

---

### Fase 2: Implementação do Módulo Core

#### 2.1 Criar Arquivo `image_checker.py`
- [x] Criar arquivo na raiz do projeto
- [x] Implementar imports e configuração inicial
- [x] Seguir padrão de `vtex_shipping.py` para estrutura

**Artefatos**:
- `image_checker.py` criado

**Referências**:
- `docs/image_checker.md` - Seção "Estrutura do Código"
- `vtex_shipping.py` - Exemplo de estrutura de módulo

---

#### 2.2 Implementar Cliente Redis
- [x] Implementar função `get_redis_client()`
- [x] Implementar função `get_cached_image(produto_id)`
- [x] Implementar função `set_cached_image(produto_id, base64_value, ttl)`
- [x] Adicionar tratamento de erros (Redis indisponível)
- [x] Adicionar timeouts apropriados

**Artefatos**:
- Funções Redis implementadas em `image_checker.py`

**Referências**:
- `docs/image_checker.md` - Seção "2. Cliente Redis"
- Biblioteca `redis` para Python

**Testes**:
- Testar com Redis disponível
- Testar com Redis indisponível (deve continuar funcionando)

---

#### 2.3 Implementar Busca de Imagens (API Copafer)
- [x] Implementar função `fetch_product_images(produto_id)`
- [x] Configurar headers de autenticação
- [x] Implementar tratamento de erros HTTP
- [x] Validar estrutura de resposta
- [x] Extrair array de imagens com base64

**Artefatos**:
- Função `fetch_product_images` implementada

**Referências**:
- `docs/image_checker.md` - Seção "3. Busca de Imagens na API Copafer"
- `vtex_shipping.py` - Padrão de chamadas HTTP com `requests`

**Testes**:
- Testar com produto que tem imagens
- Testar com produto sem imagens
- Testar com API indisponível

---

#### 2.4 Implementar Integração OpenRouter
- [x] Implementar função `prepare_openrouter_payload(images)`
- [x] Implementar função `call_openrouter(payload)`
- [x] Configurar schema JSON strict
- [x] Implementar parsing da resposta
- [x] Tratar código especial `932042349`

**Artefatos**:
- Funções OpenRouter implementadas

**Referências**:
- `docs/image_checker.md` - Seção "4. Preparação e Chamada ao OpenRouter"
- Documentação OpenRouter API

**Testes**:
- Testar com múltiplas imagens
- Testar quando modelo retorna código especial
- Testar com erro na API

---

#### 2.5 Implementar Função Principal
- [x] Implementar função `check_image_exists(produto_id)`
- [x] Implementar fluxo completo:
  1. Verificar cache
  2. Buscar imagens se não houver cache
  3. Analisar com IA se houver imagens
  4. Armazenar resultado no cache
  5. Retornar resposta
- [x] Implementar todas as validações
- [x] Tratar todos os casos de erro

**Artefatos**:
- Função principal implementada

**Referências**:
- `docs/image_checker.md` - Seção "5. Função Principal"
- `docs/se_img_existe.md` - Fluxo do workflow N8N

**Testes**:
- Testar fluxo completo com cache hit
- Testar fluxo completo com cache miss
- Testar produto sem imagens
- Testar produto com imagens inadequadas

---

#### 2.6 Implementar Modelos Pydantic
- [x] Criar classe `ImageCheckRequest`
- [x] Criar classe `ImageCheckResponse`
- [x] Adicionar docstrings apropriadas

**Artefatos**:
- Modelos Pydantic implementados

**Referências**:
- `docs/image_checker.md` - Seção "Modelos Pydantic"
- `vtex_shipping.py` - Exemplo de modelos Pydantic

---

### Fase 3: Integração com API

#### 3.1 Adicionar Endpoint no `api.py`
- [x] Importar `ImageCheckRequest`, `ImageCheckResponse`, `check_image_exists`
- [x] Adicionar endpoint `POST /is-image-exists`
- [x] Adicionar docstring do endpoint
- [x] Configurar response_model

**Artefatos**:
- Endpoint adicionado em `api.py`

**Referências**:
- `docs/image_checker.md` - Seção "Integração no api.py"
- `api.py` - Padrão de endpoints existentes

**Testes**:
- Testar endpoint via curl/Postman
- Verificar formato de resposta
- Verificar status codes

---

### Fase 4: Testes e Validação

#### 4.1 Testes Unitários
- [x] Testar funções Redis isoladamente
- [x] Testar busca de imagens (mock da API)
- [x] Testar integração OpenRouter (mock da API)
- [x] Testar função principal com diferentes cenários

**Artefatos**:
- Testes unitários criados em `tests/test_image_checker_redis.py`
- Testes unitários criados em `tests/test_image_checker_copafer.py`
- Testes unitários criados em `tests/test_image_checker_openrouter.py`
- Testes unitários criados em `tests/test_image_checker_flow.py`

**Referências**:
- `docs/image_checker.md` - Seção "Testes"

---

#### 4.2 Testes de Integração
- [x] Testar fluxo completo com Redis disponível
- [x] Testar fluxo completo com Redis indisponível
- [x] Testar com diferentes produtos (com/sem imagens)
- [x] Validar formato de resposta
- [x] Validar cache (TTL, chaves)

**Artefatos**:
- Testes de integração criados em `tests/test_image_checker_integration.py`
- Testes podem ser executados com `pytest -m integration`
- Testes podem ser pulados com variáveis de ambiente (SKIP_REDIS_TESTS, SKIP_COPAFER_TESTS, SKIP_OPENROUTER_TESTS)

**Referências**:
- `docs/image_checker.md` - Seção "Testes"

---

#### 4.3 Validação de Compatibilidade
- [x] Comparar request/response com workflow N8N
- [x] Validar chaves Redis (mesmo formato)
- [x] Validar TTL (3 dias)
- [x] Validar código especial `932042349`

**Artefatos**:
- Testes de compatibilidade criados em `tests/test_image_checker_compatibility.py`
- Todos os cenários do workflow N8N foram validados
- Formato de request/response é idêntico ao N8N
- Chaves Redis seguem padrão `best_image_for_{{ produto_id }}`
- TTL de 3 dias (259200 segundos) validado
- Código especial 932042349 validado

**Referências**:
- `docs/se_img_existe.md` - Especificação do workflow N8N
- `docs/image_checker.md` - Seção "Migração do N8N"

---

### Fase 5: Documentação

#### 5.1 Atualizar Documentação
- [x] Verificar se `docs/image_checker.md` está completo
- [x] Adicionar exemplos de uso
- [x] Documentar casos de erro
- [x] Adicionar troubleshooting

**Artefatos**:
- Documentação atualizada com exemplos completos (API, Python, JavaScript)
- Seção de casos de erro detalhada
- Seção de troubleshooting com soluções práticas

**Referências**:
- `docs/image_checker.md`
- `docs/vtex_shipping.md` - Formato de documentação

---

#### 5.2 Atualizar README
- [x] Verificar se README já foi atualizado (já feito)
- [x] Adicionar exemplo de uso do endpoint
- [x] Adicionar variáveis de ambiente ao README

**Artefatos**:
- `docs/README.md` atualizado com exemplo de uso do endpoint
- `README.md` principal atualizado com descrição do `image_checker.py` e variáveis de ambiente

---

### Fase 6: Deploy e Migração

#### 6.1 Preparação para Deploy
- [ ] Verificar se Redis está disponível no ambiente de produção
- [ ] Configurar variáveis de ambiente no servidor
- [ ] Testar conexão Redis em produção
- [ ] Testar chamadas às APIs externas

**Artefatos**:
- Ambiente de produção configurado

**Referências**:
- `docs/deploy-fly-io.md` (se aplicável)

---

#### 6.2 Deploy Gradual
- [ ] Deploy da nova funcionalidade
- [ ] Manter workflow N8N ativo inicialmente
- [ ] Monitorar logs e métricas
- [ ] Comparar resultados N8N vs Python

**Artefatos**:
- Deploy realizado
- Logs de monitoramento

**Referências**:
- `docs/image_checker.md` - Seção "Migração do N8N"

---

#### 6.3 Desativação do N8N
- [ ] Validar que resultados são idênticos
- [ ] Desabilitar workflow N8N (não deletar)
- [ ] Monitorar por alguns dias
- [ ] Remover workflow N8N após confirmação

**Artefatos**:
- Workflow N8N desativado
- Migração concluída

---

## Critérios de Aceitação

### Funcionalidade
- [ ] Endpoint `/is-image-exists` responde corretamente
- [ ] Cache Redis funciona (hit/miss)
- [ ] Busca de imagens na API Copafer funciona
- [ ] Integração com OpenRouter funciona
- [ ] Resposta tem formato compatível com N8N

### Performance
- [ ] Cache hit: resposta < 100ms
- [ ] Cache miss: resposta < 5s (incluindo IA)
- [ ] Redis não bloqueia se indisponível

### Confiabilidade
- [ ] Tratamento de erros em todas as chamadas externas
- [ ] Sistema continua funcionando sem Redis
- [ ] Timeouts apropriados configurados
- [ ] Logs adequados para debugging

### Compatibilidade
- [ ] Request/Response compatível com N8N
- [ ] Chaves Redis no mesmo formato
- [ ] TTL de 3 dias mantido
- [ ] Código especial `932042349` mantido

---

## Riscos e Mitigações

### Risco: Redis Indisponível
**Mitigação**: Sistema continua funcionando sem cache (performance reduzida)

### Risco: API Copafer Indisponível
**Mitigação**: Retorna `imageExists: false`, não armazena cache negativo

### Risco: OpenRouter Indisponível
**Mitigação**: Retorna `imageExists: false`, marca como `null` no cache

### Risco: Incompatibilidade com N8N
**Mitigação**: Validação extensiva antes de desativar N8N

---

## Recursos Necessários

### Dependências Externas
- Redis (servidor ou instância)
- API Copafer (já existente)
- OpenRouter API (já configurada)

### Credenciais
- Token API Copafer
- Bearer Token OpenRouter
- Configuração Redis (host, port, password)

### Tempo Estimado
- Fase 1: 30 minutos
- Fase 2: 4-6 horas
- Fase 3: 30 minutos
- Fase 4: 2-3 horas
- Fase 5: 1 hora
- Fase 6: 2-3 horas (com monitoramento)

**Total**: ~10-14 horas

---

## Referências

### Documentação
- `docs/image_checker.md` - Especificação técnica completa
- `docs/se_img_existe.md` - Documentação do workflow N8N
- `docs/vtex_shipping.md` - Exemplo de módulo similar

### Código de Referência
- `vtex_shipping.py` - Padrão de estrutura de módulo
- `api.py` - Padrão de endpoints FastAPI
- `docs-dev/se_img_existe.json` - Workflow N8N original

### APIs Externas
- OpenRouter API Documentation
- Redis Python Client Documentation
- FastAPI Documentation

---

## Notas de Implementação

- Manter compatibilidade total com workflow N8N durante migração
- Implementar logging adequado para debugging
- Considerar métricas de performance (cache hit rate, tempo de resposta)
- Documentar todos os casos de erro e como tratá-los
- Seguir padrões de código do projeto (Pydantic, dotenv, tratamento de erros)

