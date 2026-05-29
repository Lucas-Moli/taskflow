from flask import Blueprint, redirect, render_template, request, url_for

from src.repositories.task_repository import task_repository
from src.services.task_service import task_service

tasks_bp = Blueprint("tasks", __name__)


def _build_stats(tasks: list) -> dict:
    return {
        "total": len(tasks),
        "pendente": sum(1 for t in tasks if t.status == "Pendente"),
        "em_andamento": sum(1 for t in tasks if t.status == "Em andamento"),
        "concluida": sum(1 for t in tasks if t.status == "ConcluÃ­da"),
        "alta": sum(1 for t in tasks if t.priority == "Alta"),
    }


@tasks_bp.route("/")
def index():
    all_tasks = task_repository.get_all()
    return render_template(
        "index.html",
        tasks=all_tasks,
        search="",
        priority="",
        status="",
        stats=_build_stats(all_tasks),
        filtered_count=len(all_tasks),
        has_filters=False,
    )


@tasks_bp.route("/task/create", methods=["POST"])
def create():
    try:
        task_service.create_task(
            title=request.form.get("title", ""),
            description=request.form.get("description", ""),
            priority=request.form.get("priority", "MÃ©dia"),
        )
    except ValueError as e:
        print(f"Erro ao criar tarefa: {e}")
    return redirect(url_for("tasks.index"))


@tasks_bp.route("/task/update/<int:task_id>", methods=["POST"])
def update(task_id):
    if not task_service.get_task(task_id):
        return redirect(url_for("tasks.index"))
    try:
        task_service.update_task(
            task_id=task_id,
            title=request.form.get("title", ""),
            description=request.form.get("description", ""),
            priority=request.form.get("priority", "MÃ©dia"),
            status=request.form.get("status", "Pendente"),
        )
    except ValueError as e:
        print(f"Erro ao atualizar tarefa: {e}")
    return redirect(url_for("tasks.index"))


@tasks_bp.route("/task/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    task_service.complete_task(task_id)
    return redirect(url_for("tasks.index"))


@tasks_bp.route("/task/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    task_service.delete_task(task_id)
    return redirect(url_for("tasks.index"))
