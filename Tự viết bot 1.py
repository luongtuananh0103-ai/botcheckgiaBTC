import ccxt
import time
import pandas as pd # Thư viện xử lý bảng dữ liệu
import os # Thư viện để kiểm tra file đã tồn tại chưa

# Khởi tạo sàn
exchange = ccxt.binance({'enableRateLimit': True})
watchlist = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
base_prices = {}
file_name = "trading_alerts.csv" # Tên file sẽ lưu

def save_to_csv(symbol, price, change):
    """Hàm lưu dữ liệu vào file CSV"""
    data = {
        'Time': [time.strftime('%Y-%m-%d %H:%M:%S')], # Lấy giờ hiện tại
        'Symbol': [symbol],
        'Price': [price],
        'Change (%)': [round(change, 2)]
    }
    df = pd.DataFrame(data)
    
    # Nếu file chưa tồn tại, ghi cả tiêu đề (header). Nếu có rồi, chỉ ghi thêm dòng mới (append)
    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False, mode='w', encoding='utf-8')
    else:
        df.to_csv(file_name, index=False, mode='a', header=False, encoding='utf-8')

def initialize_prices():
    print("--- Thiết lập giá gốc ---")
    for coin in watchlist:
        ticker = exchange.fetch_ticker(coin)
        base_prices[coin] = ticker['last']
    print("Đã xong!")

# --- VÒNG LẶP CHÍNH ---
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
                print(f"Check {coin}: {current_price} ({change_pct:+.2f}%)")

        print("-" * 30)
        time.sleep(15) 
        
    except Exception as e:
        print(f"Lỗi: {e}")
        time.sleep(5)
