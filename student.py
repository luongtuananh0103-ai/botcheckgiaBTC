class student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade
        pass
    def study(self):
        print(f"{self.name} đang học bài")
    def play(self):
        print(f"{self.name} đang chơi")
student1 = student("Nguyen Van A", 20, "A")
student2= student("Nguyen Van B", 17, "A")
student1.study()
student2.play()

class coin:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    def update_price(self, new_price):
        self.price = new_price
        print(f"Giá của {self.name} đã được cập nhật: {self.price}")
BTC = coin("Bitcoin", 50000)
BTC.update_price(55000)

