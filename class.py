class Cat:
    name = None
    age = None
    isHappy = None
    def __init__(self = None, name = None, age = None, isHappy = None):
        self.set_data(name, age, isHappy)
        self.get_data()
    def set_data(self, name = None, age = None, isHappy = None):

        self.name = name
        self.age = age
        self.isHappy = isHappy
    def get_data(self):

        print(self.name, "age:", self.age, "is happy:", self.isHappy)

cat1 = Cat('Murka', 5, True)
cat1.set_data('Murka', 5, False)
cat2 = Cat('Vaska', 3, False)
