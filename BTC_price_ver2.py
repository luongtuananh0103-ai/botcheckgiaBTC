import ccxt
import time

# Khởi tạo sàn
exchange = ccxt.binance({'enableRateLimit': True})

# 1. Danh sách theo dõi và lưu giá gốc (Mốc so sánh)
watchlist = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
base_prices = {}  # Nơi lưu giá lúc bắt đầu chạy bot

def initialize_prices():
    """Lấy giá khởi điểm cho tất cả coin trong watchlist"""
    print("--- Đang thiết lập giá gốc ---")
    for coin in watchlist:
        try:                                              # ← THÊM
            ticker = exchange.fetch_ticker(coin)
            base_prices[coin] = ticker['last']
            print(f"{coin}: {base_prices[coin]}")
        except ccxt.NetworkError:                         # ← Lỗi mạng
            print(f"Lỗi mạng khi lấy giá {coin}, thử lại...")
            time.sleep(3)
            ticker = exchange.fetch_ticker(coin)          # Thử lại 1 lần
            base_prices[coin] = ticker['last']
        except ccxt.ExchangeError as e:                   # ← Lỗi từ sàn
            print(f"Sàn báo lỗi với {coin}: {e}")
        except Exception as e:                            # ← Lỗi khác
            print(f"Lỗi không xác định với {coin}: {e}")
    print("-" * 30)

def check_alert(symbol, current_price):
    """Hàm tính toán % thay đổi và đưa ra cảnh báo"""
    base_price = base_prices[symbol]
    # Công thức tính % thay đổi: ((Giá mới - Giá cũ) / Giá cũ) * 100
    change_pct = ((current_price - base_price) / base_price) * 100

    if abs(change_pct) >= 3:
        status = "🚀 TĂNG" if change_pct > 0 else "🔥 GIẢM"
        print(f"⚠️ CẢNH BÁO: {symbol} đang {status} {change_pct:.2f}% (Giá gốc: {base_price})")
    else:
        print(f"{symbol}: {current_price} (Biến động: {change_pct:.2f}%)")

# --- CHƯƠNG TRÌNH CHÍNH ---
initialize_prices()
while True:
    try:
        for coin in watchlist:
            ticker = exchange.fetch_ticker(coin)
            current_price = ticker['last']
            check_alert(coin, current_price)

        print("----------------------------")
        time.sleep(10)

    except Exception as e:
        print(f"Lỗi kết nối: {e}")
        time.sleep(5)
