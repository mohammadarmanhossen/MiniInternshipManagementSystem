from abc import ABC, abstractmethod

# -------------------------
# Abstraction - Base Class
# -------------------------
class Account(ABC):
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance  # Encapsulation - private variable

    @abstractmethod
    def account_type(self):
        pass

    # Encapsulation - Access balance safely
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"{amount} Tk deposited. New balance: {self.__balance} Tk")
        else:
            print("Invalid deposit amount!")

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
            print(f"{amount} Tk withdrawn. New balance: {self.__balance} Tk")
        else:
            print("Insufficient balance!")

    def get_balance(self):
        return self.__balance

# -------------------------
# Inheritance - Child Classes
# -------------------------
class SavingsAccount(Account):
    def account_type(self):
        print("This is a Savings Account.")

    # Polymorphism - override withdraw
    def withdraw(self, amount):
        if amount > 50000:
            print("Cannot withdraw more than 50,000 Tk at once from Savings Account!")
        else:
            super().withdraw(amount)

class CurrentAccount(Account):
    def account_type(self):
        print("This is a Current Account.")

# -------------------------
# Main Program
# -------------------------
def main():
    # Create accounts
    s_acc = SavingsAccount("Arman", 100000)
    c_acc = CurrentAccount("Rahim", 200000)

    accounts = [s_acc, c_acc]

    # Show account info and transactions
    for acc in accounts:
        print(f"\nOwner: {acc.owner}")
        acc.account_type()
        acc.deposit(10000)
        acc.withdraw(60000)  # Polymorphism effect
        print(f"Final balance: {acc.get_balance()} Tk")

if __name__ == "__main__":
    main()
