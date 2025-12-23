from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str]
    first_name: Mapped[str | None]
    phone: Mapped[str]

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name_category: Mapped[str]

class Card(Base):
    __tablename__ = "card"
    id: Mapped[int] = mapped_column(primary_key=True)
    name_card: Mapped[str]
    price: Mapped[float]
    photo: Mapped[str | None]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

class Cart(Base):
    __tablename__ = "korzina"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    card_id: Mapped[int] = mapped_column(ForeignKey("card.id"))

class Promocode(Base):
    __tablename__ = "promocode"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str]
    discount: Mapped[int]
    is_active: Mapped[int]

class Order(Base):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    promocode_id: Mapped[int | None] = mapped_column(ForeignKey("promocode.id"))
    tochka_id: Mapped[int] = mapped_column(ForeignKey("tochka_biz.id"))
    total_price: Mapped[float]

class OrderInfo(Base):
    __tablename__ = "order_info"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    card_id: Mapped[int] = mapped_column(ForeignKey("card.id"))
    order_info_status: Mapped[str]

class TochkaBiz(Base):
    __tablename__ = "tochka_biz"
    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str]
    tochka_addres: Mapped[str]

class Review(Base):
    __tablename__ = "review"
    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("card.id"))
    rating: Mapped[int]
    comment: Mapped[str | None]

class HistoryOrders(Base):
    __tablename__ = "history_orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
