# TaskFlow — Quadro Kanban (GitHub Projects)

Simulação do backlog da **Sprint 01** conforme o blueprint TechFlow Solutions.

## Colunas

| Coluna | Descrição |
|--------|-----------|
| **To Do** | Demandas planejadas |
| **In Progress** | Em execução ativa |
| **Done** | Concluídas e validadas pelo CI |

## Cards

| ID | Título | Escopo | Coluna | Atribuído | Notas |
|----|--------|--------|--------|-----------|-------|
| TF-01 | Desenhar Diagrama de Caso de Uso e Classes | Modelagem UML | Done | Arquiteto de Software | Aprovado no repositório |
| TF-02 | Inicializar Arquitetura Estrutural Base Flask | Infra/Core | Done | Engenheiro de Software | Blueprints mapeados |
| TF-03 | Codificar Modelos e Regras de Negócio de Tarefas | Desenvolvimento | Done | Dev Backend | Validações de domínio inclusas |
| TF-04 | Criar Rotas e Controladores Web do Core CRUD | Desenvolvimento | Done | Dev Backend | Redirecionamentos funcionais |
| TF-05 | Desenvolver Interface Responsiva Moderna | UI/UX Frontend | Done | Dev Frontend | Acabamento em Tailwind CSS |
| TF-06 | Escrever Suite de Testes Automatizados Core | Automação/Qualidade | Done | Engenheiro de QA | Cobertura CRUD validada |
| TF-07 | Configurar Pipeline Remoto CI/CD | CI/CD | Done | Engenheiro de DevOps | Executando a cada Push |
| TF-08 | MUDANÇA DE ESCOPO: Implementar Filtros Dinâmicos | Evolutivo | Done | Sênior Full Stack | Adicionado pós-reunião |
| TF-09 | MUDANÇA DE ESCOPO: Desenvolver Motor de Busca Interno | Evolutivo | Done | Sênior Full Stack | Query params indexadas |
| TF-10 | Consolidar Relatórios e Artigos de Engenharia | Documentação | In Progress | Tech Writer / Aluno | Ajustes finais da ABNT |

## Configuração automática

Na raiz do projeto, após `gh auth login`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup-github-kanban.ps1
```
