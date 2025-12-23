from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, init_db
from crud import (create_user, get_user_by_tg_id, add_to_cart, get_cart, clear_cart, 
                  remove_from_cart, create_order, add_category, add_card, update_order_status, get_promocode)
from schemes import UserCreate, CartItemAdd, OrderCreate
import asyncio

app = FastAPI(
    title="Exam MVC Project",
    description="Проект с FastAPI, SQLite и MVC. Документация всех эндпойнтов и моделей",
    version="1.0"
)

# ==================== ИНИЦИАЛИЗАЦИЯ БАЗЫ ====================
asyncio.run(init_db())

# ==================== USERS ====================
user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.post("/", summary="Регистрация пользователя", description="Создает нового пользователя")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Регистрация нового пользователя.
    """
    return await create_user(db, user)

@user_router.get("/{tg_id}", summary="Получить пользователя по tg_id", description="Возвращает данные пользователя по Telegram ID")
async def get_user(tg_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_by_tg_id(db, tg_id)

app.include_router(user_router)

# ==================== CART ====================
cart_router = APIRouter(prefix="/cart", tags=["Cart"])

@cart_router.post("/", summary="Добавить товар в корзину")
async def add_item(item: CartItemAdd, db: AsyncSession = Depends(get_db)):
    await add_to_cart(db, item.user_tg_id, item.card_id)
    return {"status": "added"}

@cart_router.get("/{user_id}", summary="Получить корзину пользователя")
async def get_items(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_cart(db, user_id)

@cart_router.delete("/{user_id}", summary="Очистить корзину пользователя")
async def clear(user_id: int, db: AsyncSession = Depends(get_db)):
    await clear_cart(db, user_id)
    return {"status": "cleared"}

@cart_router.delete("/{user_id}/{card_id}", summary="Удалить товар из корзины")
async def remove_item(user_id: int, card_id: int, db: AsyncSession = Depends(get_db)):
    await remove_from_cart(db, user_id, card_id)
    return {"status": "removed"}

app.include_router(cart_router)

# ==================== ORDER ====================
order_router = APIRouter(prefix="/orders", tags=["Orders"])

@order_router.post("/", summary="Создать заказ")
async def create_order_endpoint(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    await create_order(db, order.user_tg_id, None, order.tochka_id, 0)
    return {"status": "order created"}

app.include_router(order_router)

# ==================== ADMIN ====================
admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.post("/category", summary="Добавить категорию")
async def category(name: str, db: AsyncSession = Depends(get_db)):
    await add_category(db, name)
    return {"status": "ok"}

@admin_router.post("/card", summary="Добавить карточку товара")
async def card(name: str, price: float, photo: str | None, category_id: int, db: AsyncSession = Depends(get_db)):
    await add_card(db, name, price, photo, category_id)
    return {"status": "ok"}

@admin_router.put("/order-status", summary="Обновить статус заказа")
async def status(order_info_id: int, status: str, db: AsyncSession = Depends(get_db)):
    await update_order_status(db, order_info_id, status)
    return {"status": "updated"}

@admin_router.get("/promocode/{code}", summary="Получить промокод")
async def promocode(code: str, db: AsyncSession = Depends(get_db)):
    return await get_promocode(db, code)

app.include_router(admin_router)
