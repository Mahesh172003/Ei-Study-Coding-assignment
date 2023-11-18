# Define the Product class with attributes for name, price, and availability
class Product:
    def __init__(self, name, price, available=True):
        self._name = name
        self._price = price
        self._available = available

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def available(self):
        return self._available

    # Method to clone a product instance, used in the Cart for adding products
    def clone(self):
        return Product(self._name, self._price, self._available)

# Cart class to manage shopping cart operations
class Cart:
    def __init__(self):
        self.items = {}  # Stores cart items

    # Add a product to the cart with optional quantity, defaulting to 1
    def add_product(self, product, quantity=1):
        if not product.available:
            raise ValueError(f"Product {product.name} is not available.")
        self.items[product.name] = self.items.get(product.name, {'product': product.clone(), 'quantity': 0})
        self.items[product.name]['quantity'] += quantity

    # Remove a product from the cart by its name
    def remove_product(self, product_name):
        if product_name in self.items:
            del self.items[product_name]

    # Update the quantity of a product in the cart
    def update_quantity(self, product_name, quantity):
        if product_name in self.items:
            self.items[product_name]['quantity'] = quantity

    # Calculate the total price of all items in the cart
    def calculate_total(self):
        return sum(item['product'].price * item['quantity'] for item in self.items.values())

    # Display all items in the cart
    def display_cart(self):
        for product_name, item in self.items.items():
            print(f"{item['quantity']} x {product_name} (Price: {item['product'].price} each)")

# Base class for discount strategies
class DiscountStrategy:
    def apply_discount(self, cart):
        pass

# Discount strategy that applies a percentage off the total
class PercentageOffDiscount(DiscountStrategy):
    def __init__(self, percentage):
        self.percentage = percentage

    def apply_discount(self, cart):
        total = cart.calculate_total()
        return total - (total * self.percentage / 100)

# Function to get product details from the user input
def get_product_input():
    name = input("Enter product name: ")
    price = float(input("Enter product price: "))
    available = input("Is the product available (yes/no)? ").lower() == 'yes'
    return Product(name, price, available)

# Main function to run the e-commerce cart application
def main():
    cart = Cart()
    discount_strategy = PercentageOffDiscount(10)  # Example: 10% off

    while True:
        # User input for selecting the action
        action = input("Choose action (add/view/update/remove/checkout): ").lower()

        # Add product to the cart
        if action == "add":
            product = get_product_input()
            quantity = int(input("Enter quantity: "))
            cart.add_product(product, quantity)

        # View cart contents
        elif action == "view":
            if not cart.items:
                print("Whoops!! The cart is empty. Please add the items.")
            else:
                cart.display_cart()

        # Update product quantity in the cart
        elif action == "update":
            product_name = input("Enter product name to update: ")
            if product_name not in cart.items:
                print(f"Product '{product_name}' not in cart.")
                print("Please enter valid item from your cart")
                continue
            new_quantity = int(input("Enter new quantity: "))
            cart.update_quantity(product_name, new_quantity)

        # Remove a product from the cart
        elif action == "remove":
            product_name = input("Enter product name to remove: ")
            if product_name not in cart.items:
                print(f"Product '{product_name}' not in cart.")
                print("Please enter valid item from your cart")
                continue
            cart.remove_product(product_name)

        # Checkout and display the total bill after discount
        elif action == "checkout":
            total = cart.calculate_total()
            total_after_discount = discount_strategy.apply_discount(cart)
            cart.display_cart()
            print(f"Total Bill: ${total}")
            print(f"Total after Discount: ${total_after_discount}")
            break

        # Handle invalid action input
        else:
            print("Invalid action. Please choose a valid option.")

# Entry point for the program
if __name__ == "__main__":
    main()
