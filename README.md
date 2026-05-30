# TaskFlow - Gestão Inteligente de Tarefas Logísticas

O *TaskFlow* é uma aplicação web corporativa de gerenciamento de tarefas desenvolvida especificamente para otimizar os fluxos operacionais internos da *TechFlow Solutions*, uma startup focada em soluções logísticas inteligentes de alta performance.

## Objetivo

O sistema tem como meta principal servir de ferramenta para acompanhamento de ordens operacionais, permitindo a triagem veloz de gargalos de transporte, controle de frotas e delegação de rotas. Do ponto de vista acadêmico, o projeto é um modelo de demonstração pratica e integrada de *Engenharia de Software*, aplicando padrões modernos de arquitetura, metodologias ágeis e automação rígida de esteiras de CI/CD.

## Escopo Inicial

O escopo básico contemplava um sistema clássico focado no gerenciamento elementar do ciclo de vida de tarefas:

- *CRUD Operacional:* Cadastro individualizado, edição de dados textuais e remoção definitiva de ordens de serviço.
- *Controle de Estados:* Classificação estrita de criticidade (Alta, Média, Baixa) e fases de entrega (Pendente, em andamento, Concluída).

## Mudança de Escopo no Meio da Sprint

Durante as validações da Sprint 01, identificou-se um gargalo crítico na usabilidade da plataforma: com um volume massivo de entregas diárias, a ausência de mecanismos rápidos de busca dificultava a localização rápida de tarefas.

Foi realizada uma adaptação ágil no backlog do projeto para introduzir os seguintes recursos:

1. *Filtros Multicritério Dinâmicos:* Isolamento instantâneo de tarefas cruzando sua prioridade com o status atual.
2. *Sistema de Busca Textual:* Caixa de pesquisa rápida indexando caracteres presentes nos tí­tulos e descrições das ordens logísticas.

## Metodologia Ágil

O fluxo de gerenciamento de demandas utilizou a metodologia *Kanban*, implementada nativamente via *GitHub Projects*.

## Tecnologias Utilizadas

- *Linguagem Core:* Python 3.11+
- *Framework Web:* Flask 3.0.3 (Arquitetura modular via Blueprints)
- *Mecanismo de Testes:* PyTest 8.2.2
- *Estilização e UI/UX:* Tailwind CSS
- *Ambiente DevOps:* GitHub Actions

## Estrutura do Projeto

```text
taskflow/
├── src/
│   ├── app.py                 # Application factory
│   ├── config.py              # Configurações por ambiente
│   ├── models/
│   │   └── task.py            # Entidade e validações de domínio
│   ├── repositories/          # Persistência em memória
│   ├── services/              # Regras de negócio (CRUD, busca e filtros)
│   ├── routes/
│   │   ├── task_routes.py     # Rotas web (HTML)
│   │   └── api_routes.py      # API REST JSON
│   ├── templates/
│   └── static/
├── tests/
├── docs/
├── requirements.txt
└── README.md
```

```

## API REST (`/api`)

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/tasks` | Lista tarefas (`?search=&priority=&status=`) |
| GET | `/api/tasks/metadata` | Prioridades e status válidos |
| GET | `/api/tasks/<id>` | Detalhe de uma tarefa |
| POST | `/api/tasks` | Cria tarefa (JSON) |
| PUT/PATCH | `/api/tasks/<id>` | Atualiza tarefa |
| POST/PATCH | `/api/tasks/<id>/complete` | Marca como concluída |
| DELETE | `/api/tasks/<id>` | Remove tarefa |

## Como Executar a Aplicação

```bash
cd taskflow
pip install -r requirements.txt
python src/app.py
```

Abra o navegador em: http://localhost:5000

## Controle de Qualidade Automatizado

A suí­te PyTest cobre modelo, repositório, serviços, rotas web e API REST.

```bash
# Executar todos os testes
python -m pytest

# Com relatório de cobertura
python -m pytest --cov=src --cov-report=term-missing
```

Estrutura em `tests/`:

| Arquivo | Escopo |
|---------|--------|
| `test_models.py` | Validações da entidade `Task` |
| `test_repository.py` | CRUD e filtros em memória |
| `test_service.py` | Regras de negócio |
| `test_app.py` | Rotas web (HTML) |
| `test_api.py` | API REST JSON |

### GitHub Actions

O workflow `.github/workflows/ci.yml` roda automaticamente em `push` e `pull_request` para `main`/`master` e branches `feature/**`, instalando dependências, executando PyTest e publicando o relatório JUnit na aba Checks do PR.

### GitHub Projects (Kanban)

O projeto utilizou GitHub Projects para organização das tarefas utilizando metodologia Kanban.

O fluxo foi dividido em:
- Backlog
- Ready
- In Progress
- In Review
- Done

## Licença

Este projeto está licenciado sob a MIT License. Consulte o arquivo `LICENSE` para detalhes.
