from app.infrastructure.database.session import SessionLocal
from app.features.auth.models import User
from app.features.products.service import get_products


def main():
    db = SessionLocal()

    try:
        current_user = db.get(User, 5)

        if current_user is None:
            raise ValueError("Test user not found.")

        test_cases = [
            ("All products", {}),
            ("Samsung products", {"brand": "Samsung"}),
            ("Laptop category", {"category": "Laptop"}),
            (
                "Samsung Laptop",
                {"brand": "Samsung", "category": "laptop"},
            ),
        ]

        for label, filters in test_cases:
            products = get_products(
                db=db,
                current_user=current_user,
                **filters,
            )

            print(f"\n{label}: {len(products)} products")

            for product in products:
                print(
                    product.id,
                    product.name,
                    product.sku,
                    product.brand,
                    product.category,
                )

    finally:
        db.close()


if __name__ == "__main__":
    main()
