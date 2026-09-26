import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
AVIASALES_MARKER = "YOUR_MARKER"
BOOKING_AFF_ID = "YOUR_BOOKING_ID"

MAIN_MENU, FLIGHT_FROM, FLIGHT_TO, FLIGHT_DATE, FLIGHT_RETURN, FLIGHT_PASSENGERS, HOTEL_CITY, HOTEL_CHECKIN, HOTEL_CHECKOUT, HOTEL_GUESTS = range(10)

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("✈️ Flight Search", callback_data="flight")],[InlineKeyboardButton("🏨 Hotel Search", callback_data="hotel")]]
    await update.effective_message.reply_text("🌍 *Welcome to FlyMatraBot!*\n\nFlights aur Hotels best prices par!", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return MAIN_MENU

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "flight":
        await query.edit_message_text("✈️ Kahan se jaana hai?\n(City ya Airport Code, e.g. Karachi ya KHI)")
        return FLIGHT_FROM
    elif query.data == "hotel":
        await query.edit_message_text("🏨 Kis city mein hotel chahiye?\n(e.g. Dubai, London)")
        return HOTEL_CITY

async def flight_from(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["from"] = update.message.text
    await update.message.reply_text("📍 Kahan jaana hai? (e.g. Dubai ya DXB)")
    return FLIGHT_TO

async def flight_to(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["to"] = update.message.text
    await update.message.reply_text("📅 Jaane ki date? (DD-MM-YYYY)")
    return FLIGHT_DATE

async def flight_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["date"] = update.message.text
    await update.message.reply_text("👥 Kitne passengers?")
    return FLIGHT_PASSENGERS

async def flight_passengers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ud = context.user_data
    origin = ud.get("from","KHI")
    dest = ud.get("to","DXB")
    date = ud.get("date","")
    pax = update.message.text.strip()
    url = f"https://www.aviasales.com/search/{origin.upper()}{dest.upper()}?marker={AVIASALES_MARKER}"
    sky = f"https://www.skyscanner.net/transport/flights/{origin.lower()[:3]}/{dest.lower()[:3]}/?adults={pax}"
    keyboard = [[InlineKeyboardButton("🔍 Aviasales", url=url)],[InlineKeyboardButton("🔍 Skyscanner", url=sky)],[InlineKeyboardButton("🏠 Main Menu", callback_data="main")]]
    await update.message.reply_text(f"✈️ *Flight Results*\n🛫 From: {origin}\n🛬 To: {dest}\n📅 Date: {date}\n👥 Passengers: {pax}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return MAIN_MENU

async def hotel_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["city"] = update.message.text
    await update.message.reply_text("📅 Check-in date? (DD-MM-YYYY)")
    return HOTEL_CHECKIN

async def hotel_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["checkin"] = update.message.text
    await update.message.reply_text("📅 Check-out date? (DD-MM-YYYY)")
    return HOTEL_CHECKOUT

async def hotel_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["checkout"] = update.message.text
    await update.message.reply_text("👥 Kitne guests?")
    return HOTEL_GUESTS

async def hotel_guests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ud = context.user_data
    city = ud.get("city","Dubai")
    checkin = ud.get("checkin","")
    checkout = ud.get("checkout","")
    url = f"https://www.booking.com/searchresults.html?ss={city}&aid={BOOKING_AFF_ID}"
    keyboard = [[InlineKeyboardButton("🏨 Booking.com", url=url)],[InlineKeyboardButton("🏠 Main Menu", callback_data="main")]]
    await update.message.reply_text(f"🏨 *Hotel Results*\n📍 City: {city}\n📅 Check-in: {checkin}\n📅 Check-out: {checkout}", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    return MAIN_MENU

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(update, context)
    return MAIN_MENU

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start), CallbackQueryHandler(menu_callback, pattern="^(flight|hotel)$")],
        states={
            MAIN_MENU: [CallbackQueryHandler(menu_callback, pattern="^(flight|hotel)$"), CallbackQueryHandler(main_menu, pattern="^main$")],
            FLIGHT_FROM: [MessageHandler(filters.TEXT & ~filters.COMMAND, flight_from)],
            FLIGHT_TO: [MessageHan
