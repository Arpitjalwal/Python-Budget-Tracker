class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({
            "amount": amount,
            "description": description
        })

    def withdraw(self, amount, description=""):
        if not self.check_funds(amount):
            return False
        self.ledger.append({
            "amount": -amount,
            "description": description
        })
        return True

    def get_balance(self):
        total = 0
        for item in self.ledger:
            total += item["amount"]
        return total

    def transfer(self, amount, category):
        if not self.check_funds(amount):
            return False
        self.withdraw(amount, f"Transfer to {category.name}")
        category.deposit(amount, f"Transfer from {self.name}")
        return True

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = self.name.center(30, "*") + "\n"
        items = ""
        for entry in self.ledger:
            desc = entry["description"][:23]
            amt = f"{entry['amount']:.2f}"
            items += f"{desc:<23}{amt:>7}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    # Title
    chart = "Percentage spent by category\n"

    # Calculate total withdrawals
    withdrawals = []
    total = 0
    for cat in categories:
        spent = 0
        for item in cat.ledger:
            if item["amount"] < 0:
                spent += -item["amount"]
        withdrawals.append(spent)
        total += spent

    # Calculate percentages rounded down to nearest 10
    percentages = []
    for w in withdrawals:
        percent = int((w / total) * 100) // 10 * 10
        percentages.append(percent)

    # Chart bars
    for i in range(100, -1, -10):
        line = f"{i:>3}|"
        for p in percentages:
            if p >= i:
                line += " o "
            else:
                line += "   "
        line += " "
        chart += line + "\n"

    # Bottom line
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # Vertical names
        # Vertical names
    max_len = max(len(cat.name) for cat in categories)
    for i in range(max_len):
        line = "     "
        for cat in categories:
            if i < len(cat.name):
                line += cat.name[i] + "  "
            else:
                line += "   "
        chart += line + "\n"

    return chart.rstrip("\n")

# --- Testing Code ---
food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more")

clothing = Category("Clothing")
clothing.deposit(500, "initial deposit")
food.transfer(50, clothing)
clothing.withdraw(25.55, "t-shirt")

auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(150, "fuel")

print(food)
print(clothing)
print(create_spend_chart([food, clothing, auto]))