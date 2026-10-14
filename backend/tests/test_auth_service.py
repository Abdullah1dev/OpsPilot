from fastapi import HTTPException

from app.features.auth.schemas import UserLogin, UserRegister
from app.features.auth.service import register_user, login_user
from app.infrastructure.database.session import SessionLocal
from app.shared.enums.roles import UserRole


test_email = "auth-service-test@example.com"

with SessionLocal() as db:
    try:
        # Clean up a leftover test user if an earlier run failed.
        from sqlalchemy import select
        from app.features.auth.models import User

        existing = db.scalar(
            select(User).where(User.email == test_email)
        )
        if existing:
            db.delete(existing)
            db.commit()

        # 1. Register a user.
        user = register_user(
            db,
            UserRegister(
                email=test_email,
                password="Temporary-Test-Password-123!",
            ),
        )
        print("Registration:", user.email)
        print("Default role:", user.role.value)
        print("Password hashed:", user.hashed_password != "Temporary-Test-Password-123!")

        # 2. Log in with the correct password.
        result = login_user(
            db,
            UserLogin(
                email=test_email,
                password="Temporary-Test-Password-123!",
            ),
        )
        print("Login returned access token:", bool(result["access_token"]))
        print("Token type:", result["token_type"])

        # 3. Duplicate registration should fail.
        try:
            register_user(
                db,
                UserRegister(
                    email=test_email,
                    password="Another-Temporary-Password-123!",
                ),
            )
            print("Duplicate registration: FAILED (unexpected)")
        except HTTPException as exc:
            print("Duplicate registration:", exc.status_code)

    finally:
        # Remove the test user.
        from sqlalchemy import select
        from app.features.auth.models import User

        test_user = db.scalar(
            select(User).where(User.email == test_email)
        )
        if test_user:
            db.delete(test_user)
            db.commit()
        print("Test user cleaned up.")
