import ccxt
import time
import pandas as pd
import os
# Khởi tạo sàn giao dịch
exchange = ccxt.binance({'enableRateLimit': True})
# Danh sách cặp tiền tệ cần theo dõi
watchlist = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
#Lưu giá gốc để làm giá tham chiếu và tính biến động
base_prices = {}
def initialize_prices():
    print("--- Thiết lập giá gốc ---")
    for coin in watchlist:
        ticker = exchange.fetch_ticker(coin)
        base_prices[coin] = ticker['last']
    print("Đã xong!")
    # Vòng lặp chính
    initialize_prices()
while True:
    try:
        for coin in watchlist:
            ticker = exchange.fetch_ticker(coin)
            current_price = ticker['last']
            # Tính toán biến động
            base_price = base_prices[coin]
            change_pct = ((current_price - base_price) / base_price) * 100
            if abs(change_pct) >= 3:
                print(f"⚠️ CẢNH BÁO: {coin} biến động {change_pct:.2f}%! Đang lưu...")
                # GỌI HÀM LƯU FILE
                save_to_csv(coin, current_price, change_pct)
                # Cập nhật lại giá gốc để tránh lưu trùng lặp liên tục
                base_prices[coin] = current_price 
            else:
                print(f"Check {coin}: {current_price} ({change_pct:.2f}%)")
        print("-" * 30)
        time.sleep(15)
    except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")
            time.sleep(15)

