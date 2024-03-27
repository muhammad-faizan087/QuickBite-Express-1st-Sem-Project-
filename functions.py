import time


# Making a signup function to take and save user details in a userdata.txt file.
def signup(users):
    with open("userdata.txt", "a") as f:
        firstname = input("Enter your 1st name:").replace(" ", "")
        if firstname == "":  # Ensuring that 1st and lastname shouldn't be empty.
            while True:
                print("It should not ne empty,rewrite it!!.")
                firstname = input("Enter your 1st name:").replace(" ", "")
                if firstname != "":
                    break
        lastname = input("Enter your last name:").replace(
            " ", ""
        )  # Ensuring that 1st and lastname shouldn't contain spaces.
        if lastname == "":
            while True:
                print("It should not ne empty,rewrite it!!.")
                lastname = input("Enter your last name:").replace(" ", "")
                if lastname != "":
                    break
        username = input("Enter your username(Without any space's):")
        if " " in username:
            while True:
                print("Username should not contain spaces.")
                username = input("Enter your username(Without any space's):")
                if " " not in username:
                    break

        password = input("Set a password(Atleast 7 characters):")
        if len(password) < 7:  # Checking password criteria.
            while True:
                print("Password length should be atleast 7 digits.")
                password = input("Set a password(Atleast 7 characters):")
                if len(password) >= 7:
                    break

        for user in users:  # Checking if this username already have an account or not.
            if user["username"] == username:
                print("Username already exist,login or create a new account.")
                break
        else:
            f.write(
                f"{firstname} {lastname} {username} {password}\n"
            )  # Writing details to file.
            print("Your account is created login to continue.")


# Making a options function to display and implement all options of the application.
def options_func(username, fast_food_menu, cart):
    while True:
        options = "\n1. View Menu\n2. Add products to cart\n3. Remove products from cart\n4. View cart\n5. View shopping history\n6. Checkout\n7. Move to Home Page\n"
        print(options)
        while True:
            try:
                option = int(input("Select Any Option Mentioned Above:"))
                break
            except:
                print("Option should be choosen numeric.")
        if option == 1:  # Displaying menu.
            print("Welcome!!!,We Offer Following Saviour's:")
            for key, val in fast_food_menu.items():
                print(key, end="  ")
                for a, b in val.items():
                    print(f"({a} : Rs{b})")
        elif option == 2:  # Adding item's to cart.
            selection = input("Select any item from menu:").lower().strip()
            if selection in fast_food_menu:
                while True:
                    try:
                        quantity = int(input("How Many:"))
                        break
                    except:
                        print("Quantity should be numeric.")
                if quantity < 0:  # Ensuring that item quantity shouldn't be negative.
                    print("Quantity should be a positive number,add item again.")
                else:
                    price = quantity * fast_food_menu[selection]["price"]
                    cart[selection] = price
                    want_more(
                        fast_food_menu, cart
                    )  # Calling want_more function if user needs more item's.
            else:
                print("Item not available,check menu.")
        elif option == 3:  # Removing items from cart.
            to_remove = input("What you want to remove from cart?:")
            if to_remove in cart:  # Checking whether the item present in cart or not.
                quantity = int(input("How Many:"))
                if quantity * fast_food_menu[to_remove]["price"] == cart[to_remove]:
                    cart.pop(to_remove)
                    print(f"{to_remove} is being removed from cart.")
                elif quantity * fast_food_menu[to_remove]["price"] < cart[to_remove]:
                    cart[to_remove] = (
                        cart[to_remove] - quantity * fast_food_menu[to_remove]["price"]
                    )
                    print(f"{quantity} {to_remove} is being removed from cart.")
                else:
                    print("You enter quantity greater than the existing one,view cart.")
            else:
                print("Item is already not present there.")
        elif option == 4:  # Displaying Cart.
            if cart:
                print(f"Your cart is:")
                for key, val in cart.items():
                    items = val / (fast_food_menu[key]["price"])
                    print(f"{key.capitalize()} ({items} items) :Rs{val}")
            else:
                print("Cart is empty,add products first.")
        elif option == 5:
            view_history(username)  # Calling view_history() to display user's history.
        elif option == 6:
            if cart:  # If user added items then proceeding to checkout.
                address = input("Enter your current address:")
                if address == "":
                    while True:
                        print("Address should not be empty.")
                        address = input("Enter your current address:")
                values = []
                for i in cart.values():
                    values.append(i)
                total = sum(values)
                print(f"Your cart is:{cart}\nYour total bill is:{total}")
                print(
                    f"Thanks for shopping!!!\nYour order will be delivered to {address} in 30 minutes."
                )
                save_history(
                    username, cart
                )  # Calling save_history() to save user's order history.
                cart.clear()  # Making cart empty to add items again.
            else:
                print("Your cart is empty,please select some items first.")

        elif option == 7:  # Logingout back to the homepage.
            print("Welcome To QuickBite Express\n1. LOGIN\n2. SIGNUP\n3. EXIT")
            break


# Making a function to allow user to add as much items as desired.
def want_more(fast_food_menu, cart):
    while True:
        decision = input("Do you want to add other item's(Y/N):")
        if decision == "n" or decision == "N":
            break
        elif decision == "Y" or decision == "y":
            order(fast_food_menu, cart)  # Calling order() to take details of item.
        else:
            print("Please choose between(Y/N).")


# Making a order function to take details of the further items.
def order(fast_food_menu, cart):
    selection = input("What do you want?:")
    if selection in fast_food_menu:  # Ensuring that items present in menu or not.
        while True:
            try:
                quantity = int(input("How Many:"))
                break
            except:
                print("Quantity should be numeric.")
        if quantity < 0:
            print("Quantity should be a positive number,add item again.")
        elif selection in cart:
            # quantity = int(input("How Many:"))
            amount = quantity * fast_food_menu[selection]["price"]
            print(amount)
            cart[selection] += amount
        else:
            price = quantity * fast_food_menu[selection]["price"]
            cart[selection] = price
    else:
        print("Item not available,check menu.")


# Making a function to save user's order history if ordered something.
def save_history(username, cart):
    order_time = time.ctime(time.time())  # Retrieving current time using time library.
    with open(f"{username}_history.txt", "a") as f:
        f.write(
            f"Order Details: {cart} | {order_time}\n"
        )  # Writing user's order details in a user_history file.


# Making a function to read and display user's order details from user_history file.
def view_history(username):
    with open(f"{username}_history.txt", "r") as f:
        content = f.read()
        if content:
            print(f"Order History for {username}:\n{content}")
        else:
            print(f"No order history found for {username}.")
