phone_book = open("phone_book.txt", "r", encoding="utf-8")
for person in phone_book:
    print(person.replace("\n", ""))

phone_book.close()

# Them dữ liệu vào file .txt trong phone_book
phone_book = open("new_phone_book.txt", "a", encoding="utf-8")
phone_book.write("Nguyễn Văn A -- 01234566543\n")
phone_book.write("Trần Thị B -- 0987654321\n")
phone_book.close()
