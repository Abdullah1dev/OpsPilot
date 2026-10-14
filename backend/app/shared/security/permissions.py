
from enum import Enum

from app.shared.enums.roles import UserRole


class Permission(str, Enum):
    VIEW_PRODUCTS = "view_products"
    CREATE_PRODUCTS = "create_products"
    UPDATE_PRODUCTS = "update_products"

    VIEW_INVENTORY = "view_inventory"
    RECORD_INVENTORY_MOVEMENT = "record_inventory_movement"
    VIEW_INVENTORY_MOVEMENTS = "view_inventory_movements"

    MANAGE_USERS = "manage_users"
    ASK_INVENTORY_QUESTIONS = "ask_inventory_questions"


ROLE_PERMISSIONS: dict[UserRole, frozenset[Permission]] = {
    UserRole.ADMIN: frozenset(Permission),

    UserRole.MANAGER: frozenset(
        {
            Permission.VIEW_PRODUCTS,
            Permission.CREATE_PRODUCTS,
            Permission.UPDATE_PRODUCTS,
            Permission.VIEW_INVENTORY,
            Permission.RECORD_INVENTORY_MOVEMENT,
            Permission.VIEW_INVENTORY_MOVEMENTS,
            Permission.ASK_INVENTORY_QUESTIONS,
        }
    ),

    UserRole.SALES: frozenset(
        {
            Permission.VIEW_PRODUCTS,
            Permission.VIEW_INVENTORY,
            Permission.ASK_INVENTORY_QUESTIONS,
        }
    ),

    UserRole.WAREHOUSE: frozenset(
        {
            Permission.VIEW_PRODUCTS,
            Permission.VIEW_INVENTORY,
            Permission.RECORD_INVENTORY_MOVEMENT,
            Permission.VIEW_INVENTORY_MOVEMENTS,
            Permission.ASK_INVENTORY_QUESTIONS,
        }
    ),
}


def has_permission(
    role: UserRole,
    permission: Permission,
) -> bool:
    """Return whether a role is allowed to perform an operation."""
    return permission in ROLE_PERMISSIONS.get(role, frozenset())
