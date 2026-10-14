from fastapi import Depends, HTTPException, status

from app.features.auth.models import User
from app.shared.enums.roles import UserRole
from app.shared.security.authentication import get_current_user
from app.shared.security.permissions import Permission, has_permission

def require_roles(*allowed_roles: UserRole):
    """
    Allow access only to authenticated users with an approved role.
    """

    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )

        return current_user

    return role_checker




def require_permission(permission: Permission):
    """
    Allow access only to authenticated users
    whose role has the required permission.
    """

    def permission_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if not has_permission(current_user.role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )

        return current_user

    return permission_checker
