# TaskFlow — cria GitHub Project (Kanban) e os 10 cards do blueprint.
# Pré-requisito: gh auth login

$ErrorActionPreference = "Stop"
$Owner = "Lucas-Moli"
$Repo = "taskflow"
$ProjectTitle = "TaskFlow - Sprint 01 Kanban"

$Cards = @(
    @{
        Id = "TF-01"
        Title = "Desenhar Diagrama de Caso de Uso e Classes"
        Scope = "Modelagem UML"
        Status = "Done"
        Assignee = "Arquiteto de Software"
        Notes = "Aprovado no repositório."
    },
    @{
        Id = "TF-02"
        Title = "Inicializar Arquitetura Estrutural Base Flask"
        Scope = "Infra/Core"
        Status = "Done"
        Assignee = "Engenheiro de Software"
        Notes = "Blueprints mapeados."
    },
    @{
        Id = "TF-03"
        Title = "Codificar Modelos e Regras de Negócio de Tarefas"
        Scope = "Desenvolvimento"
        Status = "Done"
        Assignee = "Dev Backend"
        Notes = "Validações de domínio inclusas."
    },
    @{
        Id = "TF-04"
        Title = "Criar Rotas e Controladores Web do Core CRUD"
        Scope = "Desenvolvimento"
        Status = "Done"
        Assignee = "Dev Backend"
        Notes = "Redirecionamentos funcionais."
    },
    @{
        Id = "TF-05"
        Title = "Desenvolver Interface Responsiva Moderna"
        Scope = "UI/UX Frontend"
        Status = "Done"
        Assignee = "Dev Frontend"
        Notes = "Acabamento em Tailwind CSS."
    },
    @{
        Id = "TF-06"
        Title = "Escrever Suite de Testes Automatizados Core"
        Scope = "Automação/Qualidade"
        Status = "Done"
        Assignee = "Engenheiro de QA"
        Notes = "Cobertura CRUD validada."
    },
    @{
        Id = "TF-07"
        Title = "Configurar Pipeline Remoto CI/CD"
        Scope = "CI/CD"
        Status = "Done"
        Assignee = "Engenheiro de DevOps"
        Notes = "Executando a cada Push (GitHub Actions)."
    },
    @{
        Id = "TF-08"
        Title = "MUDANÇA DE ESCOPO: Implementar Filtros Dinâmicos"
        Scope = "Evolutivo"
        Status = "Done"
        Assignee = "Sênior Full Stack"
        Notes = "Adicionado pós-reunião de escopo."
    },
    @{
        Id = "TF-09"
        Title = "MUDANÇA DE ESCOPO: Desenvolver Motor de Busca Interno"
        Scope = "Evolutivo"
        Status = "Done"
        Assignee = "Sênior Full Stack"
        Notes = "Query params indexadas."
    },
    @{
        Id = "TF-10"
        Title = "Consolidar Relatórios e Artigos de Engenharia"
        Scope = "Documentação"
        Status = "In Progress"
        Assignee = "Tech Writer / Aluno"
        Notes = "Ajustes finais da ABNT."
    }
)

function Get-Gh {
    $gh = Get-Command gh -ErrorAction SilentlyContinue
    if (-not $gh) {
        throw "GitHub CLI (gh) não encontrado. Instale com: winget install GitHub.cli"
    }
    return $gh.Source
}

function Ensure-GhAuth {
    $gh = Get-Gh
    & $gh auth status 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Execute primeiro: gh auth login"
    }
}

function Build-Body($card) {
    @"
## $($card.Id) — $($card.Title)

| Campo | Valor |
|-------|-------|
| **Escopo** | $($card.Scope) |
| **Atribuído** | $($card.Assignee) |
| **Status Kanban** | $($card.Status) |

### Notas de sprint
$($card.Notes)

---
_TaskFlow · TechFlow Solutions · Blueprint acadêmico_
"@
}

function Map-StatusOption($options, $desired) {
    $normalized = @{
        "To Do" = @("Todo", "To do", "To Do", "Backlog")
        "In Progress" = @("In progress", "In Progress", "Doing")
        "Done" = @("Done", "Concluído", "Complete")
    }
    $aliases = $normalized[$desired]
    if (-not $aliases) { $aliases = @($desired) }
    foreach ($opt in $options) {
        foreach ($alias in $aliases) {
            if ($opt.name -eq $alias) { return $opt.id }
        }
    }
    return $null
}

Ensure-GhAuth
$gh = Get-Gh

Write-Host "Criando projeto: $ProjectTitle" -ForegroundColor Cyan
$projectJson = & $gh project create --owner $Owner --title $ProjectTitle --format json | ConvertFrom-Json
$projectNumber = $projectJson.number
$projectId = $projectJson.id
Write-Host "Projeto #$projectNumber criado (id: $projectId)"

Write-Host "Vinculando repositório $Owner/$Repo ..."
& $gh project link $projectNumber --owner $Owner --repo "$Owner/$Repo" | Out-Null

Write-Host "Obtendo campo Status ..."
$fieldQuery = @'
query($login: String!, $number: Int!) {
  user(login: $login) {
    projectV2(number: $number) {
      field(name: "Status") {
        ... on ProjectV2SingleSelectField {
          id
          options { id name }
        }
      }
    }
  }
}
'@
$fieldResp = & $gh api graphql -f query=$fieldQuery -f login=$Owner -F number=$projectNumber | ConvertFrom-Json
$statusField = $fieldResp.data.user.projectV2.field
$statusFieldId = $statusField.id
$statusOptions = $statusField.options

$statusMap = @{
    "To Do" = (Map-StatusOption $statusOptions "To Do")
    "In Progress" = (Map-StatusOption $statusOptions "In Progress")
    "Done" = (Map-StatusOption $statusOptions "Done")
}

foreach ($key in @("To Do", "In Progress", "Done")) {
    if (-not $statusMap[$key]) {
        Write-Warning "Opção de status '$key' não encontrada. Opções disponíveis: $($statusOptions.name -join ', ')"
    }
}

foreach ($card in $Cards) {
    $fullTitle = "$($card.Id): $($card.Title)"
    $body = Build-Body $card
    $bodyFile = [System.IO.Path]::GetTempFileName()
    Set-Content -Path $bodyFile -Value $body -Encoding UTF8

    Write-Host "  + $fullTitle" -ForegroundColor Green
    $itemJson = & $gh project item-create $projectNumber --owner $Owner --title $fullTitle --body-file $bodyFile --format json | ConvertFrom-Json
    Remove-Item $bodyFile -Force

    $kanbanColumn = switch ($card.Status) {
        "Done" { "Done" }
        "In Progress" { "In Progress" }
        default { "To Do" }
    }
    $optionId = $statusMap[$kanbanColumn]
    if ($optionId) {
        & $gh project item-edit --project-id $projectId --id $itemJson.id --field-id $statusFieldId --single-select-option-id $optionId | Out-Null
    }
}

$projectUrl = "https://github.com/users/$Owner/projects/$projectNumber"
Write-Host ""
Write-Host "Kanban criado com sucesso!" -ForegroundColor Green
Write-Host "URL: $projectUrl"
Write-Host ""
Write-Host "No GitHub: Project settings > Layout > Board view (colunas To Do / In Progress / Done)."
