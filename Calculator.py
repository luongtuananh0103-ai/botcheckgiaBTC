num1 = float(input("Nhập số thứ nhất: "))
num2 = float(input("Nhập số thứ hai: "))
operator = input("Nhập phép toán (+, -, *, /): ")

try:
    if operator == "+":
        print(num1 + num2)
    elif operator == "-":
        print(num1 - num2)
    elif operator == "*":
        print(num1 * num2)
    elif operator == "/":
        if num2 != 0:
            print(num1 / num2)
        else:
            print("Lỗi: Không thể chia cho 0")
    else:
        print("Phép toán không hợp lệ")

except ValueError:
    print("Lỗi: Phải nhập số, không nhập chữ!")

except Exception as e:
    print(f"Lỗi không xác định: {e}")