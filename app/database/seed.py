from decimal import Decimal, ROUND_HALF_UP
import random

from sqlalchemy import func, select

from app.database.database import SessionLocal
from app.models.category import Category
from app.models.product import Product


def _money(value: float) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def seed_database_if_empty() -> None:
    """Populate initial data only when the database has no categories and products."""
    db = SessionLocal()
    try:
        category_count = int(db.scalar(select(func.count(Category.id))) or 0)
        product_count = int(db.scalar(select(func.count(Product.id))) or 0)
        if category_count > 0 or product_count > 0:
            return

        random.seed(42)

        category_names = [
            ("Electronics", "Devices and consumer gadgets"),
            ("Home & Kitchen", "Appliances and household essentials"),
            ("Office", "Office supplies and productivity tools"),
            ("Sports", "Fitness gear and sporting goods"),
            ("Personal Care", "Health and personal care products"),
        ]

        categories: list[Category] = []
        for name, description in category_names:
            category = Category(name=name, description=description)
            db.add(category)
            categories.append(category)

        db.flush()

        products_per_category = 5
        for category in categories:
            prefix = "".join(part[0].upper() for part in category.name.replace("&", " ").split())
            for index in range(1, products_per_category + 1):
                base_cost = _money(random.uniform(5.0, 350.0))
                margin_multiplier = Decimal(str(random.uniform(1.15, 1.85)))
                sale_price = (base_cost * margin_multiplier).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
                stock_quantity = random.randint(5, 180)
                sku = f"{prefix}-{index:03d}"

                product = Product(
                    category_id=category.id,
                    name=f"{category.name} Product {index}",
                    sku=sku,
                    stock_quantity=stock_quantity,
                    cost=base_cost,
                    sale_price=sale_price,
                )
                db.add(product)

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
