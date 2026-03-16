import ccxt
import time
from datetime import datetime

# ─── 1. KHỞI TẠO SÀN ────────────────────────────────────────
exchange = ccxt.binance()

# ─── 2. HÀM LẤY GIÁ (giữ nguyên logic của bạn, thêm chi tiết) ──
def get_crypto_price(symbol):
    try:
        ticker = exchange.fetch_ticker(symbol)
        return {
            "price":   ticker["last"],           # Giá hiện tại
            "high":    ticker["high"],            # Cao nhất 24h
            "low":     ticker["low"],             # Thấp nhất 24h
            "change":  ticker["percentage"],      # % thay đổi 24h
            "volume":  ticker["baseVolume"],      # Volume 24h
            "time":    ticker["datetime"]
        }
    except Exception as e:
        return None

# ─── 3. HÀM PHÁT HIỆN TÍN HIỆU ĐƠN GIẢN ────────────────────
price_history = []   # Lưu lịch sử giá để so sánh

def get_signal(price):
    price_history.append(price)
    if len(price_history) < 5:
        return "⏳ CHỜTHÊM DỮ LIỆU"

    recent = price_history[-5:]       # 5 giá gần nhất
    avg    = sum(recent) / len(recent)

    if price > avg * 1.002:           # Giá > MA5 + 0.2%
        return "🟢 BUY SIGNAL"
    elif price < avg * 0.998:         # Giá < MA5 - 0.2%
        return "🔴 SELL SIGNAL"
    else:
        return "⚪ HOLD"

# ─── 4. FORMAT HIỂN THỊ ĐẸP HƠN ────────────────────────────
def format_display(symbol, data, signal, prev_price):
    now    = datetime.now().strftime("%H:%M:%S")
    price  = data["price"]
    change = data["change"] or 0

    # So sánh với giá trước để hiện mũi tên
    if prev_price is None:
        arrow = "  "
    elif price > prev_price:
        arrow = "▲"
    elif price < prev_price:
        arrow = "▼"
    else:
        arrow = "─"

    print(f"""
┌─────────────────────────────────────────┐
│  🤖 BOT GIÁ  │  {now}  │  {symbol}
├─────────────────────────────────────────┤
│  Giá hiện tại : {arrow} ${price:>12,.2f} USDT
│  Thay đổi 24h : {change:>+.2f}%
│  Cao / Thấp   : ${data['high']:,.2f} / ${data['low']:,.2f}
│  Volume 24h   : {data['volume']:,.2f} BTC
├─────────────────────────────────────────┤
│  Tín hiệu     : {signal}
└─────────────────────────────────────────┘""")

# ─── 5. VÒNG LẶP CHÍNH ──────────────────────────────────────
symbol     = "BTC/USDT"
prev_price = None
interval   = 2      # Giây giữa mỗi lần lấy giá
count      = 0

print(f"🚀 Bot khởi động — Đang theo dõi {symbol}...")
print("   Nhấn Ctrl+C để dừng\n")

while True:
    try:
        data = get_crypto_price(symbol)

        if data:
            count += 1
            signal = get_signal(data["price"])
            format_display(symbol, data, signal, prev_price)
            prev_price = data["price"]
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  Không lấy được giá, thử lại...")

        time.sleep(interval)

    except KeyboardInterrupt:
        print(f"\n\n✅ Bot dừng sau {count} lần lấy giá. Tạm biệt!")
        break
    except ccxt.NetworkError as e:
        print(f"⚠️  Lỗi mạng: {e} — thử lại sau 5s...")
        time.sleep(5)
    except ccxt.ExchangeError as e:
        print(f"⚠️  Lỗi sàn: {e}")
        time.sleep(5)