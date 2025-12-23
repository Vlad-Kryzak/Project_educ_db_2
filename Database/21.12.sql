CREATE TABLE IF NOT EXISTS "user" (
	"id" INTEGER,
	"tg_id" INTEGER NOT NULL UNIQUE,
	"username" VARCHAR,
	"first_name" VARCHAR,
	"phone" VARCHAR UNIQUE,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "categories" (
	"id" INTEGER,
	"name_category" VARCHAR NOT NULL UNIQUE,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "card" (
	"id" INTEGER,
	"name_card" VARCHAR NOT NULL,
	"price" REAL NOT NULL CHECK("price" >= 0),
	"photo" VARCHAR,
	"category_id" INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("category_id") REFERENCES "categories"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "korzina" (
	"id" INTEGER,
	"user_id" INTEGER NOT NULL,
	"card_id" INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("user_id") REFERENCES "user"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("card_id") REFERENCES "card"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "promocode" (
	"id" INTEGER,
	"code" VARCHAR NOT NULL UNIQUE,
	"discount" INTEGER NOT NULL CHECK("discount" >= 1 AND "discount" <= 100),
	"is_active" INTEGER DEFAULT 1 CHECK("is_active" IN 0 AND 1),
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "tochka_biz" (
	"id" INTEGER,
	"city" VARCHAR NOT NULL,
	"tochka_addres" VARCHAR NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "order" (
	"id" INTEGER,
	"user_id" INTEGER NOT NULL,
	"promocode_id" INTEGER,
	"tochka_id" INTEGER NOT NULL,
	"total_price" REAL NOT NULL CHECK("total_price" >= 0),
	PRIMARY KEY("id"),
	FOREIGN KEY ("user_id") REFERENCES "user"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("promocode_id") REFERENCES "promocode"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("tochka_id") REFERENCES "tochka_biz"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "order_info" (
	"id" INTEGER,
	"order_id" INTEGER NOT NULL,
	"card_id" INTEGER NOT NULL,
	"order_info_status" VARCHAR,
	PRIMARY KEY("id"),
	FOREIGN KEY ("order_id") REFERENCES "order"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("id") REFERENCES "card"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "review" (
	"id" INTEGER,
	"card_id" INTEGER NOT NULL,
	"rating" INTEGER NOT NULL CHECK("rating" >= 1 AND "rating" <= 5),
	PRIMARY KEY("id"),
	FOREIGN KEY ("card_id") REFERENCES "card"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "history_orders" (
	"id" INTEGER NOT NULL UNIQUE,
	"user_id" INTEGER NOT NULL,
	"order_id" INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("user_id") REFERENCES "user"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("order_id") REFERENCES "order"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
