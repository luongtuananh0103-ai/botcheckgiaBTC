# bot.py
import ccxt
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ─── CONFIG ──────────────────────────────────────────────────
load_dotenv()
TOKEN   = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

exchange = ccxt.binance()

# ─── LƯU TRẠNG THÁI BOT ─────────────────────────────────────
state = {
    "is_running":    False,
    "symbol":        "BTC/USDT",
    "interval":      10,
    "alert_pct":     2.0,
    "price_history": [],
    "last_price":    None,
    "task":          None,
}

# ─── HÀM LẤY GIÁ ────────────────────────────────────────────
def get_ticker(symbol):
    try:
        t = exchange.fetch_ticker(symbol)
        return {
            "price":  t["last"],
            "high":   t["high"],
            "low":    t["low"],
            "change": t["percentage"] or 0,
            "volume": t["baseVolume"],
        }
    except Exception as e:
        return None

# ─── HÀM TÍN HIỆU MA5 ───────────────────────────────────────
def get_signal(price):
    state["price_history"].append(price)
    if len(state["price_history"]) > 100:
        state["price_history"].pop(0)

    history = state["price_history"]
    if len(history) < 5:
        return "Chua du du lieu"

    avg = sum(history[-5:]) / 5
    if price > avg * 1.002:
        return "BUY SIGNAL"
    elif price < avg * 0.998:
        return "SELL SIGNAL"
    return "HOLD"

# ─── FORMAT TIN NHẮN ─────────────────────────────────────────
def format_message(data, signal):
    symbol = state["symbol"]
    arrow  = "🔺" if data["change"] >= 0 else "🔻"
    now    = datetime.now().strftime("%H:%M:%S %d/%m/%Y")

    return (
        f"🤖 *BTC PRICE BOT*\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"💰 *{symbol}*: `${data['price']:,.2f}`\n"
        f"{arrow} Thay doi 24h: `{data['change']:+.2f}%`\n"
        f"📈 Cao nhat: `${data['high']:,.2f}`\n"
        f"📉 Thap nhat: `${data['low']:,.2f}`\n"
        f"📦 Volume: `{data['volume']:,.0f} BTC`\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📊 Tin hieu: {signal}\n"
        f"🕐 `{now}`"
    )

# ─── COMMANDS ────────────────────────────────────────────────
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🤖 BTC Price Bot\n\n"
        "/price — Lay gia BTC ngay\n"
        "/start_auto — Tu dong gui gia moi 10 giay\n"
        "/stop_auto — Dung theo doi tu dong\n"
        "/symbol ETH/USDT — Doi sang coin khac\n"
        "/alert 3 — Alert khi gia thay doi >= 3%\n"
        "/status — Xem trang thai bot\n"
        "/help — Hien menu nay"
    )
    await update.message.reply_text(msg)

async def cmd_price(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Dang lay gia...")
    data = get_ticker(state["symbol"])
    if data:
        signal = get_signal(data["price"])
        await update.message.reply_text(
            format_message(data, signal),
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("Khong lay duoc gia, thu lai sau!")

async def cmd_start_auto(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if state["is_running"]:
        await update.message.reply_text("Bot dang chay roi! Dung /stop_auto de dung.")
        return

    state["is_running"] = True
    await update.message.reply_text(
        f"Bot bat dau theo doi {state['symbol']}\n"
        f"Cap nhat moi {state['interval']} giay"
    )
    state["task"] = asyncio.create_task(auto_loop(ctx))

async def cmd_stop_auto(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not state["is_running"]:
        await update.message.reply_text("Bot chua chay.")
        return

    state["is_running"] = False
    if state["task"]:
        state["task"].cancel()
    await update.message.reply_text("Bot da dung.")

async def cmd_symbol(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Dung: /symbol ETH/USDT")
        return

    new_symbol = ctx.args[0].upper()
    try:
        exchange.fetch_ticker(new_symbol)
        state["symbol"] = new_symbol
        state["price_history"].clear()
        await update.message.reply_text(f"Da chuyen sang {new_symbol}")
    except Exception:
        await update.message.reply_text(f"Symbol {new_symbol} khong hop le!")

async def cmd_alert(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Dung: /alert 3")
        return
    try:
        pct = float(ctx.args[0])
        state["alert_pct"] = pct
        await update.message.reply_text(f"Alert dat: {pct}%")
    except ValueError:
        await update.message.reply_text("Nhap so, vi du: /alert 2.5")

async def cmd_status(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    status = "Dang chay" if state["is_running"] else "Da dung"
    last   = f"${state['last_price']:,.2f}" if state["last_price"] else "chua co"
    await update.message.reply_text(
        f"TRANG THAI BOT\n"
        f"Trang thai : {status}\n"
        f"Symbol     : {state['symbol']}\n"
        f"Interval   : {state['interval']}s\n"
        f"Alert      : >= {state['alert_pct']}%\n"
        f"Gia cuoi   : {last}"
    )

# ─── VÒNG LẶP TỰ ĐỘNG ───────────────────────────────────────
async def auto_loop(ctx: ContextTypes.DEFAULT_TYPE):
    bot = ctx.bot
    prev_price = None

    while state["is_running"]:
        try:
            data = get_ticker(state["symbol"])

            if data:
                price = data["price"]
                state["last_price"] = price
                signal = get_signal(price)

                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=format_message(data, signal),
                    parse_mode="Markdown"
                )

                # Gửi alert riêng nếu giá thay đổi mạnh
                if prev_price:
                    pct_change = abs(price - prev_price) / prev_price * 100
                    if pct_change >= state["alert_pct"]:
                        direction = "TANG MANH" if price > prev_price else "GIAM MANH"
                        await bot.send_message(
                            chat_id=CHAT_ID,
                            text=(
                                f"PRICE ALERT!\n"
                                f"{direction}: {pct_change:+.2f}%\n"
                                f"Gia: ${price:,.2f}"
                            )
                        )
                prev_price = price

        except asyncio.CancelledError:
            break
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"Loi: {e}")

        await asyncio.sleep(state["interval"])

# ─── KHỞI CHẠY ───────────────────────────────────────────────
def main():
    print("Bot dang khoi dong...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start",      cmd_start))
    app.add_handler(CommandHandler("price",      cmd_price))
    app.add_handler(CommandHandler("start_auto", cmd_start_auto))
    app.add_handler(CommandHandler("stop_auto",  cmd_stop_auto))
    app.add_handler(CommandHandler("symbol",     cmd_symbol))
    app.add_handler(CommandHandler("alert",      cmd_alert))
    app.add_handler(CommandHandler("status",     cmd_status))
    app.add_handler(CommandHandler("help",       cmd_start))

    print("Bot san sang! Mo Telegram va go /start")
    app.run_polling()

if __name__ == "__main__":
    main()