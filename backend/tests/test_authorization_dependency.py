from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from app.features.auth.models import User
from app.shared.security.authorization import require_permission
from app.shared.security.permissions import Permission


app = FastAPI()





client = TestClient(app)


def create_test_user(role):
    return User(
        id=1,
        email=f"{role.value.lower()}@example.com",
        hashed_password="not-used",
        role=role,
        is_active=True,
    )
    

def test_manager_can_create_products():
    from app.shared.enums.roles import UserRole
    from app.shared.security.authentication import get_current_user

    app.dependency_overrides[get_current_user] = (
        lambda: create_test_user(UserRole.MANAGER)
    )

    response = client.get("/test/products/create")

    assert response.status_code == 200
    assert response.json()["message"] == "Product creation allowed"

    app.dependency_overrides.clear()


def test_sales_cannot_create_products():
    from app.shared.enums.roles import UserRole
    from app.shared.security.authentication import get_current_user

    app.dependency_overrides[get_current_user] = (
        lambda: create_test_user(UserRole.SALES)
    )

    response = client.get("/test/products/create")

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have permission to perform this action"
    )

    app.dependency_overrides.clear()