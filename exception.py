try:
    num1 = int(input("Nhập số thứ nhất: "))
    num2 = int(input("Nhập số thứ hai: "))
    result = num1/num2
    print(f"Thương của phép chia là: {result}")
except ZeroDivisionError:
    print("Lỗi: Không thể chia cho 0!")
except ValueError:
    print("Lỗi: Vui lòng nhập một số hợp lệ là số nguyên!")
except:
    print("Đã xảy ra lỗi không xác định! Vui lòng liên hệ bộ phận hỗ trợ.")
    

