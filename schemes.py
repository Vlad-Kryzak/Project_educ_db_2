from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class OrderStatus(str, Enum):
    """Статусы заказа"""
    оформлен = "оформлен"
    выполнен = "выполнен"
    отказан = "отказан"

# ==================== USERS ====================
class UserCreate(BaseModel):
    """Схема для создания пользователя"""
    tg_id: int = Field(..., gt=0, description="Telegram ID пользователя")
    username: str = Field(..., max_length=100, description="Имя пользователя в Telegram")
    first_name: Optional[str] = Field(None, max_length=100, description="Имя пользователя")
    phone: str = Field(..., pattern=r'^\+7\d{10}$', description="Телефон в формате +7XXXXXXXXXX")

class UserResponse(BaseModel):
    """Схема для ответа с данными пользователя"""
    id: int
    tg_id: int
    username: str
    first_name: Optional[str]
    phone: str

# ==================== CART ====================
class CartItemAdd(BaseModel):
    """Добавление товара в корзину"""
    user_tg_id: int
    card_id: int

class CartItem(BaseModel):
    """Товар в корзине"""
    id: int
    card_id: int
    name_card: str
    price: float
    photo: Optional[str]

class CartResponse(BaseModel):
    """Корзина пользователя"""
    user_id: int
    items: List[CartItem]
    total: float

# ==================== ORDER ====================
class OrderCreate(BaseModel):
    """Создание заказа"""
    user_tg_id: int
    tochka_id: int
    promocode: Optional[str] = None
