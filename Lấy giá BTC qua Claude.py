import ccxt
import time

# 1. Khởi tạo sàn giao dịch (Binance)
exchange = ccxt.binance()

def get_crypto_price(symbol):
    try:
        # 2. Lấy thông tin thị trường (ticker) của cặp tiền
        ticker = exchange.fetch_ticker(symbol)
        
        # 3. Trích xuất giá hiện tại (last price)
        current_price = ticker['last']
        timestamp = ticker['datetime']
        
        return current_price, timestamp
    except Exception as e:
        return None, str(e)

# 4. Vòng lặp chạy bot để theo dõi giá
symbol = 'BTC/USDT'
print(f"--- Đang theo dõi giá {symbol} ---")

while True:
    price, info = get_crypto_price(symbol)
    if price:
        print(f"[{info}] Giá {symbol}: {price} USDT")
    else:
        print(f"Lỗi: {info}")
    
    time.sleep(2) # Nghỉ 2 giây trước khi lấy giá mới
