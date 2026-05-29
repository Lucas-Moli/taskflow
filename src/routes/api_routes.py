from flask import Blueprint, jsonify, request

from src.services.task_service import task_service

api_bp = Blueprint("api", __name__, url_prefix="/api")

# Rotas estáticas (/tasks/metadata) devem ser registradas antes de /tasks/<int:task_id>


@api_bp.route("/tasks/metadata", methods=["GET"])
def task_metadata():
    return jsonify(task_service.metadata())


@api_bp.route("/tasks", methods=["GET"])
def list_tasks():
    tasks = task_service.list_tasks(
        search=request.args.get("search", ""),
        priority=request.args.get("priority", ""),
        status=request.args.get("status", ""),
    )
    return jsonify([t.to_dict() for t in tasks])


@api_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}
    try:
        task = task_service.create_task(
            title=data.get("title", ""),
            description=data.get("description", ""),
            priority=data.get("priority", "Média"),
            status=data.get("status", "Pendente"),
        )
        return jsonify(task.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = task_service.get_task(task_id)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    return jsonify(task.to_dict())


@api_bp.route("/tasks/<int:task_id>", methods=["PUT", "PATCH"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    existing = task_service.get_task(task_id)
    if not existing:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    try:
        task = task_service.update_task(
            task_id=task_id,
            title=data.get("title", existing.title),
            description=data.get("description", existing.description),
            priority=data.get("priority", existing.priority),
            status=data.get("status", existing.status),
        )
        if not task:
            return jsonify({"error": "Tarefa não encontrada"}), 404
        return jsonify(task.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/tasks/<int:task_id>/complete", methods=["POST", "PATCH"])
def complete_task(task_id):
    task = task_service.complete_task(task_id)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    return jsonify(task.to_dict())


@api_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if not task_service.delete_task(task_id):
        return jsonify({"error": "Tarefa não encontrada"}), 404
    return "", 204
