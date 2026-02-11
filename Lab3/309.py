class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        pi = 3.14159
        return pi * self.radius * self.radius

def main():
    r = int(input().strip())
    circle = Circle(r)
    area = circle.area()
    print(f"{area:.2f}")

if __name__ == "__main__":
    main()