from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from models import User, Cart, Card, Promocode, Order, OrderInfo, Category

# ==================== USERS ====================
async def create_user(db: AsyncSession, data):
    """Создает нового пользователя"""
    user = User(**data.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_tg_id(db: AsyncSession, tg_id: int):
    """Возвращает пользователя по Telegram ID"""
    res = await db.execute(select(User).where(User.tg_id == tg_id))
    return res.scalar_one_or_none()

# ==================== CART ====================
async def add_to_cart(db: AsyncSession, user_id: int, card_id: int):
    """Добавляет товар в корзину"""
    await db.execute(text("INSERT INTO korzina (user_id, card_id) VALUES (:u, :c)"), {"u": user_id, "c": card_id})
    await db.commit()

async def get_cart(db: AsyncSession, user_id: int):
    """Получает корзину пользователя"""
    res = await db.execute(text("""
        SELECT k.id, k.card_id, c.name_card, c.price, c.photo
        FROM korzina k
        JOIN card c ON k.card_id = c.id
        WHERE k.user_id = :u
    """), {"u": user_id})
    return res.mappings().all()

async def remove_from_cart(db: AsyncSession, user_id: int, card_id: int):
    """Удаляет товар из корзины"""
    await db.execute(text("DELETE FROM korzina WHERE user_id = :u AND card_id = :c"), {"u": user_id, "c": card_id})
    await db.commit()

async def clear_cart(db: AsyncSession, user_id: int):
    """Очищает корзину пользователя"""
    await db.execute(text("DELETE FROM korzina WHERE user_id = :u"), {"u": user_id})
    await db.commit()

# ==================== ORDER ====================
async def create_order(db: AsyncSession, user_id: int, promocode_id: int | None, tochka_id: int, total: float):
    """Создает заказ и переносит все позиции из корзины"""
    await db.execute(text("BEGIN"))
    await db.execute(text("""
        INSERT INTO "order" (user_id, promocode_id, tochka_id, total_price)
        VALUES (:u, :p, :t, :total)
    """), {"u": user_id, "p": promocode_id, "t": tochka_id, "total": total})
    await db.execute(text("""
        INSERT INTO order_info (order_id, card_id, order_info_status)
        SELECT last_insert_rowid(), card_id, 'оформлен'
        FROM korzina WHERE user_id = :u
    """), {"u": user_id})
    await db.execute(text("DELETE FROM korzina WHERE user_id = :u"), {"u": user_id})
    await db.execute(text("COMMIT"))

# ==================== ADMIN ====================
async def add_category(db: AsyncSession, name: str):
    """Добавляет категорию"""
    await db.execute(text("INSERT INTO categories (name_category) VALUES (:n)"), {"n": name})
    await db.commit()

async def add_card(db: AsyncSession, name: str, price: float, photo: str | None, category_id: int):
    """Добавляет карточку товара"""
    await db.execute(text("INSERT INTO card (name_card, price, photo, category_id) VALUES (:n, :p, :ph, :c)"),
                     {"n": name, "p": price, "ph": photo, "c": category_id})
    await db.commit()

async def update_order_status(db: AsyncSession, order_info_id: int, status: str):
    """Обновляет статус позиции заказа"""
    await db.execute(text("UPDATE order_info SET order_info_status = :s WHERE id = :id"),
                     {"s": status, "id": order_info_id})
    await db.commit()

async def get_promocode(db: AsyncSession, code: str):
    """Возвращает активный промокод"""
    res = await db.execute(text("SELECT * FROM promocode WHERE code = :c AND is_active = 1"), {"c": code})
    return res.mappings().first()
