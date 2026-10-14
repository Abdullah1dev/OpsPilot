from app.shared.enums.roles import UserRole
from app.shared.security.permissions import Permission, has_permission


def test_admin_permissions():
    for permission in Permission:
        assert has_permission(UserRole.ADMIN, permission) is True


def test_manager_permissions():
    assert has_permission(UserRole.MANAGER, Permission.VIEW_PRODUCTS)
    assert has_permission(UserRole.MANAGER, Permission.CREATE_PRODUCTS)
    assert has_permission(UserRole.MANAGER, Permission.UPDATE_PRODUCTS)
    assert has_permission(UserRole.MANAGER, Permission.VIEW_INVENTORY)
    assert has_permission(
        UserRole.MANAGER,
        Permission.RECORD_INVENTORY_MOVEMENT,
    )
    assert has_permission(
        UserRole.MANAGER,
        Permission.VIEW_INVENTORY_MOVEMENTS,
    )
    assert has_permission(
        UserRole.MANAGER,
        Permission.ASK_INVENTORY_QUESTIONS,
    )

    assert not has_permission(UserRole.MANAGER, Permission.MANAGE_USERS)


def test_sales_permissions():
    assert has_permission(UserRole.SALES, Permission.VIEW_PRODUCTS)
    assert has_permission(UserRole.SALES, Permission.VIEW_INVENTORY)
    assert has_permission(
        UserRole.SALES,
        Permission.ASK_INVENTORY_QUESTIONS,
    )

    assert not has_permission(UserRole.SALES, Permission.CREATE_PRODUCTS)
    assert not has_permission(UserRole.SALES, Permission.UPDATE_PRODUCTS)
    assert not has_permission(
        UserRole.SALES,
        Permission.RECORD_INVENTORY_MOVEMENT,
    )
    assert not has_permission(
        UserRole.SALES,
        Permission.VIEW_INVENTORY_MOVEMENTS,
    )
    assert not has_permission(UserRole.SALES, Permission.MANAGE_USERS)


def test_warehouse_permissions():
    assert has_permission(UserRole.WAREHOUSE, Permission.VIEW_PRODUCTS)
    assert has_permission(UserRole.WAREHOUSE, Permission.VIEW_INVENTORY)
    assert has_permission(
        UserRole.WAREHOUSE,
        Permission.RECORD_INVENTORY_MOVEMENT,
    )
    assert has_permission(
        UserRole.WAREHOUSE,
        Permission.VIEW_INVENTORY_MOVEMENTS,
    )
    assert has_permission(
        UserRole.WAREHOUSE,
        Permission.ASK_INVENTORY_QUESTIONS,
    )

    assert not has_permission(UserRole.WAREHOUSE, Permission.CREATE_PRODUCTS)
    assert not has_permission(UserRole.WAREHOUSE, Permission.UPDATE_PRODUCTS)
    assert not has_permission(UserRole.WAREHOUSE, Permission.MANAGE_USERS)


if __name__ == "__main__":
    test_admin_permissions()
    test_manager_permissions()
    test_sales_permissions()
    test_warehouse_permissions()

    print("All authorization policy tests passed.")