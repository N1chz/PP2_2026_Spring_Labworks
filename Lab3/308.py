class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

def main():
    B, W = map(int, input().split())
    acc = Account("Unknown", B)
    if acc.withdraw(W):
        print(acc.balance)
    else:
        print("Insufficient Funds")

if __name__ == "__main__":
    main()