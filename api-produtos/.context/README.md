# AI Context - Documentação e Planos

Este diretório contém documentação estruturada e planos de implementação para agentes AI, seguindo o padrão do [ai-coders/context](https://github.com/ai-coders/context).

## Estrutura

```
.context/
├── README.md                    # Este arquivo
├── docs/                        # Documentação técnica (se necessário)
├── agents/                      # Playbooks de agentes (se necessário)
└── plans/                       # Planos de implementação
    └── image-checker-implementation.md
```

## Planos Disponíveis

### image-checker-implementation

**Arquivo**: `plans/image-checker-implementation.md`

**Objetivo**: Implementar funcionalidade de verificação de imagem de produto em Python, substituindo workflow N8N.

**Status**: Planejado

**Fases**:
1. Preparação do Ambiente
2. Implementação do Módulo Core
3. Integração com API
4. Testes e Validação
5. Documentação
6. Deploy e Migração

**Referências**:
- `docs/image_checker.md` - Especificação técnica
- `docs/se_img_existe.md` - Workflow N8N original
- `vtex_shipping.py` - Padrão de módulo

## Como Usar

### Criar um Novo Plano

Seguindo o padrão do ai-coders:

```bash
npx @ai-coders/context plan meu-plano --title "Título" --summary "Objetivo"
```

### Preencher um Plano Existente

```bash
npx @ai-coders/context plan meu-plano --fill -k $API_KEY -r ./
```

### Visualizar sem Modificar

```bash
npx @ai-coders/context plan meu-plano --fill --dry-run
```

## Convenções

- Planos devem estar em `plans/`
- Documentação técnica em `docs/` (ou na raiz `docs/`)
- Playbooks de agentes em `agents/`
- Usar Markdown para todos os documentos
- Seguir estrutura de fases, tarefas e critérios de aceitação

## Referências Externas

- [ai-coders/context](https://github.com/ai-coders/context) - Ferramenta CLI
- Documentação do projeto: `docs/README.md`
- Guia de agentes: `AGENTS.md`

