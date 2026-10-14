
from fastapi import HTTPException
from app.infrastructure.database.session import SessionLocal
from app.features.auth.models import User
from app.shared.enums.roles import UserRole
from app.shared.security.hashing import hash_password
from app.shared.security.jwt import create_access_token
from app.shared.security.authentication import get_current_user

with SessionLocal() as db:
    test_user = User(
        email="jwt-test@opspilot.local",
        hashed_password=hash_password("Temporary-Test-Password-123!"),
        role=UserRole.SALES,
        is_active=True,
    )

    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    try:
        token = create_access_token(str(test_user.id))
        authenticated_user = get_current_user(token=token, db=db)

        print("Authenticated user:", authenticated_user.email)
        print("User ID:", authenticated_user.id)
        print("Role:", authenticated_user.role.value)
    finally:
        db.delete(test_user)
        db.commit()
        print("Temporary test user deleted.")
