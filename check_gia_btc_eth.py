import ccxt
import time

# Khởi tạo sàn Binance
exchange = ccxt.binance({'enableRateLimit': True})

def check_gia():
    coins = ['BTC/USDT', 'ETH/USDT']
    print(f"\n[{time.strftime('%H:%M:%S')}] --- GIÁ TRÊN BINANCE ---")
    for coin in coins:
        ticker = exchange.fetch_ticker(coin)
        gia = ticker['last']
        thay_doi = ticker['percentage']  # % thay đổi 24h
        cao_nhat = ticker['high']
        thap_nhat = ticker['low']

        dau = "+" if thay_doi >= 0 else ""
        print(f"  {coin:<10} | Giá: ${gia:>12,.2f} | 24h: {dau}{thay_doi:.2f}% | Cao: ${cao_nhat:,.2f} | Thấp: ${thap_nhat:,.2f}")
    print("-" * 75)

# Vòng lặp kiểm tra mỗi 10 giây
while True:
    try:
        check_gia()
        time.sleep(10)
    except Exception as e:
        print(f"Lỗi: {e}")
        time.sleep(5)
