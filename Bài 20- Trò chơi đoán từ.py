secret_word = "python"
hint = "Đây là một ngôn ngữ lập trình phổ biến"
guess = ""
guess_count = 0
guess_limit = 3

while guess != secret_word:
    if guess_count < guess_limit:
        guess = input("Hãy đoán từ gì ")
        guess_count +=1
    else:
        break 

if guess == secret_word:
    print(" CHÚC MỪNG BẠN ĐÃ ĐOÁN ĐÚNG")
else:
    print("Rất tiếc, bạn đã đoán sai")
