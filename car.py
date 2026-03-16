class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
    def drive(self):
       print(f"Bạn đang lái chiếc xe {self.make} {self.model} Model năm {self.year}")
        
Mercedes = Car("Mercedes", "C300", 2020)
Mercedes.drive() 