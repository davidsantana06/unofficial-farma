**Unofficial Farma** é um conjunto de serviços para gestão de fármacos, empresas fornecedoras (laboratórios) e avaliações de clientes, servido por três serviços web REST e exposto a uma IA pelo protocolo MCP. O cliente é um chat LibreChat com suporte a Gemini, que conversa com os servidores MCP; são eles que intermediam o acesso aos serviços.

## 🧩 Módulos

A ordem abaixo é também a ordem de subida. Os servidores MCP dependem da rede e dos serviços criados pelo primeiro módulo, e o cliente depende dos servidores MCP.

### ⚙️ `unofficial-farma-services/`

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

São três aplicações FastAPI independentes, cada uma no seu container e na sua porta, todas ligadas à mesma instância do PostgreSQL 16. O `init.sql` cria as tabelas e popula o banco na primeira vez que o volume sobe.

| Serviço    | Porta | Responsabilidade                                         |
| ---------- | ----- | -------------------------------------------------------- |
| `company/` | 8001  | Laboratórios farmacêuticos                               |
| `product/` | 8002  | Medicamentos, cada um vinculado a um laboratório         |
| `comment/` | 8003  | Avaliações que os clientes escrevem sobre um medicamento |

O `product` é o único que conversa com outro serviço. Ao criar um medicamento, ou ao trocar o `company_id` de um que já existe, ele consulta o `company` e devolve `400` se o laboratório não existir.

Por dentro, os três seguem o mesmo layout de arquivos.

| Arquivo          | Responsabilidade                                            |
| ---------------- | ----------------------------------------------------------- |
| `__main__.py`    | Monta o app FastAPI e sobe o uvicorn na porta do serviço    |
| `database.py`    | Cria a engine a partir de `DATABASE_URL` e fornece a sessão |
| `schemas.py`     | Modelos para entrada de dados                               |
| `models.py`      | Mapeamento das tabelas no banco em modelos (entidades)      |
| `controllers.py` | Rotas HTTP do recurso                                       |

As rotas também são as mesmas nos três, mudando só o nome do recurso (`/companies`, `/products`, `/comments`).

| Rota                     | Descrição                                                 |
| ------------------------ | --------------------------------------------------------- |
| `GET /health`            | Retorna o estado do serviço                               |
| `POST /{recurso}`        | Cria um registro e devolve `201`                          |
| `GET /{recurso}`         | Lista com `limit` (padrão 50) e `offset` (padrão 0)       |
| `GET /{recurso}/search`  | Filtra por campo, com `ILIKE` parcial nos campos de texto |
| `GET /{recurso}/{id}`    | Busca por ID, ou `404`                                    |
| `PATCH /{recurso}/{id}`  | Atualiza os campos enviados e o `updated_at`              |
| `DELETE /{recurso}/{id}` | Remove o registro e devolve `204`                         |

---

### 🔌 `unofficial-farma-mcp-servers/`

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MCP](https://img.shields.io/badge/mcp-%23000000.svg?style=for-the-badge&logo=modelcontextprotocol&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

Cada servidor usa FastMCP com transporte `streamable-http`, escuta na sua própria porta e traduz chamadas de ferramenta em requisições HTTP para o serviço correspondente. Só as operações de leitura viraram ferramenta, então a IA consulta o catálogo sem poder alterá-lo.

| Servidor   | Porta | Ferramentas                                                          |
| ---------- | ----- | -------------------------------------------------------------------- |
| `company/` | 9001  | `check_company_service_health`, `list_companies`, `search_companies` |
| `product/` | 9002  | `check_product_service_health`, `list_products`, `search_products`   |
| `comment/` | 9003  | `check_comment_service_health`, `list_comments`, `search_comments`   |

O layout interno se repete nos três.

| Arquivo       | Responsabilidade                                                               |
| ------------- | ------------------------------------------------------------------------------ |
| `__main__.py` | Registra as ferramentas no FastMCP e sobe o transporte HTTP                    |
| `client.py`   | Chama o serviço com httpx e converte falha de rede ou erro HTTP em `ToolError` |
| `models.py`   | Modelo Pydantic do recurso devolvido                                           |
| `tools.py`    | As ferramentas, cujas docstrings a IA lê como documentação                     |

O compose deste módulo declara a rede `unofficial-farma-network` como externa, por isso os serviços precisam estar de pé antes.

---

### 💬 `unofficial-farma-client/`

![Gemini](https://img.shields.io/badge/gemini-%238E75B2.svg?style=for-the-badge&logo=googlegemini&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

O LibreChat sobe com um MongoDB só dele. No `librechat.yaml` ficam registrados os três servidores MCP, em `host.docker.internal`, nas portas 9001, 9002 e 9003. A interface fica acessível em `http://localhost:3080`.

## 🛠️ Instalação e execução

### 1️⃣ Pré-requisitos

Sistema operacional Linux, macOS ou Windows com WSL, além de Docker com o plugin Compose. Os dois módulos de backend constroem a própria imagem a partir de `python:3.12-slim` e instalam o `requirements.txt` no build, então não é preciso ter Python no host.

As portas 3080, 5432, 8001-8003 e 9001-9003 precisam estar livres. Se alguma estiver ocupada, o compose falha na subida.

### 2️⃣ Subir serviços

```bash
cd unofficial-farma-services
docker compose up -d --build
cd ..
```

O comando cria a rede `unofficial-farma-network` e sobe o PostgreSQL junto com os serviços. O `init.sql` só roda quando o volume `pgdata` está vazio. Para repovoar o banco, apague o volume com `docker compose down -v`.

Antes de seguir, chame o `/health` de cada um.

```bash
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
```

Todos devem responder `{"status":"ok","service":"..."}`.

### 3️⃣ Subir servidores MCP

```bash
cd unofficial-farma-mcp-servers
docker compose up -d --build
cd ..
```

### 4️⃣ Preencher `.env` do cliente

O LibreChat lê as credenciais de `unofficial-farma-client/.env`. Copie o template `.env.example` e preencha o seu.

```bash
cd unofficial-farma-client
cp .env.example .env
```

São cinco campos.

| Campo                | Descrição                                                         |
| -------------------- | ----------------------------------------------------------------- |
| `GOOGLE_KEY`         | Chave do Google AI Studio, que habilita o endpoint Google no chat |
| `JWT_SECRET`         | Segredo de assinatura do token de sessão                          |
| `JWT_REFRESH_SECRET` | Segredo de assinatura do token de renovação                       |
| `CREDS_KEY`          | Chave de criptografia das credenciais salvas                      |
| `CREDS_IV`           | Vetor de inicialização dessa criptografia                         |

A chave deve ser obtida através do [Google AI Studio](https://aistudio.google.com/apikey). Os demais valores podem ser gerados com `openssl rand`:

```bash
openssl rand -hex 32   # JWT_SECRET, JWT_REFRESH_SECRET e CREDS_KEY
openssl rand -hex 16   # CREDS_IV
```

### 5️⃣ Subir cliente

```bash
docker compose up -d
```

Abra `http://localhost:3080` e crie uma conta, já que o registro está aberto no compose. Escolha o endpoint Google e ative as ferramentas dos servidores `company`, `product` e `comment` na conversa. Feito isso, é só usar o chat e se divertir 😎👍.
