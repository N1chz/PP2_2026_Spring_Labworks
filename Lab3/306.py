class Shape:
    pass

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

def main():
    l, w = map(int, input().split())
    rect = Rectangle(l, w)
    print(rect.area())

if __name__ == "__main__":
    main()