# Khởi động chương trình tính giá BTC
import ccxt
import time
import pandas as pd
import mplfinance as mpf

#Khởi tạo sàn giao dịch
exchange = ccxt.binance({'enableRateLimit': True})
#Danh sách các đồng tiền điện tử cần theo dõi
watchlist = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'AVAX/USDT']
# Lưu giá gốc để làm giá tham chiếu để tính biến động
base_prices = {}

def ve_chart_nen(coin):
    """Lấy 100 nến 15 phút và vẽ chart"""
    ohlcv = exchange.fetch_ohlcv(coin, timeframe='15m', limit=100)
    df = pd.DataFrame(ohlcv, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df.set_index('Date', inplace=True)
    mpf.plot(df, type='candle', style='charles', title=f'{coin} - 15 phút',
             ylabel='Giá (USDT)', volume=True, show_nontrading=False)

def initialize_prizes():
    print('--- Thiết lập giá gốc cho các đồng coin ---')
    for coin in watchlist:
        ticker = exchange.fetch_ticker(coin)
        base_prices[coin] = ticker['last']
    print('--- Đã thiết lập giá gốc ---')

# Vòng lặp chính của chương trình
initialize_prizes()
for coin in watchlist:
    ve_chart_nen(coin)
while True:
    try:
        for coin in watchlist:
            ticker = exchange.fetch_ticker(coin)
            current_price = ticker['last']

            # Tính toán biến động giá
            base_prize = base_prices[coin]
            change_percentage = ((current_price - base_prize) / base_prize) * 100
            if abs(change_percentage) >= 2:
                print(f'⚠️ CẢNH BÁO: {coin} biến động {change_percentage:+.2f}%! Giá gốc: {base_prize}, Giá hiện tại: {current_price}')
                ve_chart_nen(coin)
                # Cập nhật lại giá gốc để tránh cảnh báo liên tục
                base_prices[coin] = current_price
            else:
                print(f'Check {coin}: {current_price} (Biến động: {change_percentage:.2f}%)')
            time.sleep(15)
    except Exception as e:
        print(f'Đã xảy ra lỗi: {e}')
    time.sleep(5)
