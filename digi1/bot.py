import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "digi1.settings")
django.setup()
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes)
from asgiref.sync import sync_to_async
from pathlib import Path
from PIL import Image
from io import BytesIO

from shop.models import Category,Product

TOKEN =os.getenv("TELEGRAM_BOT_TOKEN")

@sync_to_async
def get_categories():
    return list(Category.objects.all())

async def show_categories(message):
    categories = await get_categories()

    keyboard = []

    for category in categories:
        keyboard.append([
            InlineKeyboardButton(
                category.name,
                callback_data=f"category_{category.id}"
            )
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await message.reply_text(
        "📂 دسته‌بندی مورد نظر را انتخاب کنید:",
        reply_markup=reply_markup
    )
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await show_categories(update.message)

@sync_to_async
def get_products(category_id):
    return list(Product.objects.filter(category_id=category_id))

async def category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()
    if query.data == "category_all":
        categories = await get_categories()

        keyboard = []

        for category in categories:
            keyboard.append([
                InlineKeyboardButton(
                    category.name,
                    callback_data=f"category_{category.id}"
                )
            ])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.edit_text(
            "📂 دسته‌بندی مورد نظر را انتخاب کنید:",
            reply_markup=reply_markup
        )

        return

    category_id = query.data.split("_")[1]

    products = await get_products(category_id)

    if not products:
        await query.message.reply_text(
            "❌ محصولی در این دسته وجود ندارد."
        )
        return

    keyboard = []

    for product in products:
        if product.is_sale:
            price_text = f"🔥 {product.sale_price:,} تومان"
        else:
            price_text = f"💰 {product.price:,} تومان"

        keyboard.append([
            InlineKeyboardButton(
                f"📱 {product.name}  - {price_text}",
                callback_data=f"product_{product.id}"
            )
        ])
    keyboard.append([
        InlineKeyboardButton(
            "🔙 بازگشت به دسته‌بندی‌ها",
            callback_data="category_all"
        )
        ])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        "🛍 محصولات این دسته را انتخاب کنید:",
        reply_markup=reply_markup
    )

async def product_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    product_id = int(query.data.split("_")[1])

    product = await sync_to_async(
        lambda: Product.objects.select_related("category").get(id=product_id)
    )()

    if product.is_sale:
        text = (
            f"🛍 {product.name}\n\n"
            f"💰 قیمت اصلی: {product.price:,} تومان\n"
            f"🔥 قیمت با تخفیف: {product.sale_price:,} تومان\n"
            f"⭐ امتیاز: {product.star}\n\n"
            f"📝 توضیحات:\n{product.description}"
        )
    else:
        text = (
            f"🛍 {product.name}\n\n"
            f"💰 قیمت: {product.price:,} تومان\n"
            f"⭐ امتیاز: {product.star}\n\n"
            f"📝 توضیحات:\n{product.description}"
        )

    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 افزودن به سبد خرید",
                callback_data=f"add_to_cart_{product.id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 بازگشت به محصولات",
                callback_data=f"category_{product.category.id}"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if product.picture:
        with open(product.picture.path, "rb") as photo:
            await query.message.reply_photo(
                photo=photo,
                caption=text,
                reply_markup=reply_markup
            )
    else:
        await query.message.reply_text(
            text,
            reply_markup=reply_markup
        )
async  def add_to_cart_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    product_id = int(query.data.split("_")[3])
    await query.message.reply_text(
        f"✅ محصول شماره {product_id} به سبد خرید اضافه شد."
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    CallbackQueryHandler(category_callback, pattern="^category_")
)
app.add_handler(
    CallbackQueryHandler(
        product_callback,
        pattern=r"^product_\d+$"
    )
)
app.add_handler(CallbackQueryHandler(add_to_cart_callback, pattern=r"^add_to_cart_\d+$"))

print("Bot is running...")

app.run_polling()

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     categories = await get_categories()
#
#     text = "سلام 👋\nبه فروشگاه Digi1 خوش آمدید.\n\n"
#     text += "📂 دسته‌بندی‌ها:\n\n"
#
#     for category in categories:
#         text += f"🔹 {category.name}\n"
#
#     await update.message.reply_text(text)
#
# app = Application.builder().token(TOKEN).build()
#
# app.add_handler(CommandHandler("start", start))
#
# print("Bot is running...")
#
# app.run_polling()