"""Smoke tests: imports, rotas, templates e assets estáticos."""

import pytest

from src.app import create_app


@pytest.fixture
def app():
    return create_app("testing")


def test_all_modules_import():
    """Garante que o pacote src importa sem erros."""
    import src.app  # noqa: F401
    import src.config  # noqa: F401
    import src.models.task  # noqa: F401
    import src.repositories.task_repository  # noqa: F401
    import src.services.task_service  # noqa: F401
    import src.routes.api_routes  # noqa: F401
    import src.routes.task_routes  # noqa: F401


def test_registered_routes(app):
    rules = {str(rule) for rule in app.url_map.iter_rules()}
    expected = {
        "/",
        "/task/create",
        "/task/update/<int:task_id>",
        "/task/complete/<int:task_id>",
        "/task/delete/<int:task_id>",
        "/api/tasks",
        "/api/tasks/metadata",
        "/api/tasks/<int:task_id>",
        "/api/tasks/<int:task_id>/complete",
    }
    assert expected.issubset(rules)


def test_index_renders_without_template_error(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.content_type.startswith("text/html")


def test_static_js_available(client):
    response = client.get("/static/js/app.js")
    assert response.status_code == 200
    assert b"toggleModal" in response.data


def test_api_metadata_route_not_treated_as_task_id(client):
    """'/api/tasks/metadata' não deve ser capturado por task_id=int."""
    response = client.get("/api/tasks/metadata")
    assert response.status_code == 200
    assert response.is_json
    assert "priorities" in response.get_json()


def test_web_post_only_routes_reject_get(client):
    assert client.get("/task/create").status_code == 405
    assert client.post("/task/update/999").status_code == 302
