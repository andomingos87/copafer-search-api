# requirements.txt

## O que é?

Este arquivo lista todas as **dependências Python** necessárias para executar o projeto.

---

## Dependências

| Pacote | Versão | Uso |
|--------|--------|-----|
| fastapi | latest | Framework web para a API |
| uvicorn[standard] | latest | Servidor ASGI para rodar FastAPI |
| psycopg2-binary | latest | Driver PostgreSQL para Python |
| python-dotenv | latest | Carregar variáveis de ambiente do .env |
| openai | latest | Gerar embeddings para busca vetorial |
| cohere | latest | Alternativa para embeddings (não usado atualmente) |
| tiktoken | latest | Contar tokens para chunking |
| requests | latest | Fazer requisições HTTP para VTEX/Cubo |
| pandas | latest | Processamento de CSV |
| tqdm | latest | Barras de progresso |

---

## Como Instalar

```bash
# Criar ambiente virtual (recomendado)
python -m venv .venv

# Ativar ambiente
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

---

## Detalhes dos Pacotes

### fastapi
Framework web moderno e rápido para construir APIs. Usa type hints do Python para validação automática.

### uvicorn[standard]
Servidor ASGI de alta performance. O `[standard]` inclui dependências extras para melhor performance.

### psycopg2-binary
Driver PostgreSQL. A versão `binary` não requer compilação, facilitando a instalação.

### python-dotenv
Carrega variáveis de um arquivo `.env` para `os.environ`. Essencial para configuração.

### openai
SDK oficial da OpenAI. Usado para gerar embeddings dos produtos.

### tiktoken
Tokenizador da OpenAI. Usado para dividir textos longos em chunks respeitando o limite de tokens.

### requests
Biblioteca HTTP simples. Usada para integração com VTEX e API do Cubo.

### pandas
Biblioteca de análise de dados. Usada para leitura robusta de CSVs.

### tqdm
Barras de progresso. Mostra andamento durante ingestão de muitos produtos.

---

## Atualizando Dependências

```bash
# Atualizar todas
pip install --upgrade -r requirements.txt

# Verificar desatualizadas
pip list --outdated
```

