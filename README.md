# TaskFlow - GestÃ£o Inteligente de Tarefas LogÃ­sticas

O **TaskFlow** Ã© uma aplicaÃ§Ã£o web corporativa de gerenciamento de tarefas desenvolvida especificamente para otimizar os fluxos operacionais internos da **TechFlow Solutions**, uma startup focada em soluÃ§Ãµes logÃ­sticas inteligentes de alta performance.

---

## Objetivo

O sistema tem como meta principal servir de ferramenta para acompanhamento de ordens operacionais, permitindo a triagem veloz de gargalos de transporte, controle de frotas e delegaÃ§Ã£o de rotas. Do ponto de vista acadÃªmico, o projeto Ã© um modelo de demonstraÃ§Ã£o prÃ¡tica e integrada de **Engenharia de Software de Alta Maturidade**, aplicando padrÃµes modernos de arquitetura, metodologias Ã¡geis e automaÃ§Ã£o rÃ­gida de esteiras de CI/CD.

---

## Escopo Inicial

O escopo bÃ¡sico contemplava um sistema clÃ¡ssico focado no gerenciamento elementar do ciclo de vida de tarefas:

- **CRUD Operacional:** Cadastro individualizado, ediÃ§Ã£o de dados textuais e remoÃ§Ã£o definitiva de ordens de serviÃ§o.
- **Controle de Estados:** ClassificaÃ§Ã£o estrita de criticidade (Alta, MÃ©dia, Baixa) e fases de entrega (Pendente, Em andamento, ConcluÃ­da).

---

## MudanÃ§a de Escopo no Meio da Sprint

Durante as validaÃ§Ãµes da Sprint 01, identificou-se um gargalo crÃ­tico na usabilidade da plataforma: com um volume massivo de entregas diÃ¡rias, a ausÃªncia de mecanismos rÃ¡pidos de localizaÃ§Ã£o gerava lentidÃ£o cognitiva.

Foi realizada uma adaptaÃ§Ã£o Ã¡gil no backlog do projeto para introduzir os seguintes recursos:

1. **Filtros Multi-CritÃ©rio DinÃ¢micos:** Isolamento instantÃ¢neo de tarefas cruzando sua prioridade com o status atual.
2. **Motor de Busca Textual:** Caixa de pesquisa rÃ¡pida indexando caracteres presentes nos tÃ­tulos e descriÃ§Ãµes das ordens logÃ­sticas.

---

## Metodologia Ãgil

O fluxo de gerenciamento de demandas utilizou a metodologia **Kanban**, implementada nativamente via **GitHub Projects**.

---

## Tecnologias Utilizadas

- **Linguagem Core:** Python 3.11+
- **Framework Web:** Flask 3.0.3 (Arquitetura modular via Blueprints)
- **Mecanismo de Testes:** PyTest 8.2.2
- **EstilizaÃ§Ã£o e UI/UX:** Tailwind CSS
- **Ambiente DevOps:** GitHub Actions

---

## Estrutura do Projeto

```text
taskflow/
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ app.py                 # Application factory
â”‚   â”œâ”€â”€ config.py              # ConfiguraÃ§Ãµes por ambiente
â”‚   â”œâ”€â”€ models/task.py         # Entidade e validaÃ§Ãµes de domÃ­nio
â”‚   â”œâ”€â”€ repositories/          # PersistÃªncia (memÃ³ria)
â”‚   â”œâ”€â”€ services/              # Regras de negÃ³cio (CRUD, busca, filtros)
â”‚   â”œâ”€â”€ routes/
â”‚   â”‚   â”œâ”€â”€ task_routes.py     # Rotas web (HTML)
â”‚   â”‚   â””â”€â”€ api_routes.py      # API REST JSON
â”‚   â”œâ”€â”€ templates/
â”‚   â””â”€â”€ static/
â”œâ”€â”€ tests/
â”œâ”€â”€ requirements.txt
â””â”€â”€ README.md
```

## API REST (`/api`)

| MÃ©todo | Rota | DescriÃ§Ã£o |
|--------|------|-----------|
| GET | `/api/tasks` | Lista tarefas (`?search=&priority=&status=`) |
| GET | `/api/tasks/metadata` | Prioridades e status vÃ¡lidos |
| GET | `/api/tasks/<id>` | Detalhe de uma tarefa |
| POST | `/api/tasks` | Cria tarefa (JSON) |
| PUT/PATCH | `/api/tasks/<id>` | Atualiza tarefa |
| POST/PATCH | `/api/tasks/<id>/complete` | Marca como concluÃ­da |
| DELETE | `/api/tasks/<id>` | Remove tarefa |

---

## Como Executar a AplicaÃ§Ã£o

```bash
cd taskflow
pip install -r requirements.txt
python src/app.py
```

Abra o navegador em: http://localhost:5000

---

## Controle de Qualidade Automatizado

A suÃ­te PyTest cobre modelo, repositÃ³rio, serviÃ§o, rotas web e API REST.

```bash
# Executar todos os testes
python -m pytest

# Com relatÃ³rio de cobertura
python -m pytest --cov=src --cov-report=term-missing
```

Estrutura em `tests/`:

| Arquivo | Escopo |
|---------|--------|
| `test_models.py` | ValidaÃ§Ãµes da entidade `Task` |
| `test_repository.py` | CRUD e filtros em memÃ³ria |
| `test_service.py` | Regras de negÃ³cio |
| `test_app.py` | Rotas web (HTML) |
| `test_api.py` | API REST JSON |

### GitHub Actions

O workflow `.github/workflows/ci.yml` roda automaticamente em `push` e `pull_request` para `main`/`master` e branches `feature/**`, instalando dependÃªncias, executando PyTest e publicando o relatÃ³rio JUnit na aba Checks do PR.

### GitHub Projects (Kanban)

Quadro da Sprint 01 com colunas **To Do**, **In Progress** e **Done**:

```powershell
gh auth login
powershell -ExecutionPolicy Bypass -File scripts/setup-github-kanban.ps1
```

Cards do blueprint: `docs/kanban-cards.md` · ImportaÃ§Ã£o manual: `.github/kanban/IMPORT.md`

---

## LicenÃ§a

Este projeto estÃ¡ licenciado sob a MIT License â€” consulte o arquivo `LICENSE` para detalhes.

