# A program that manages shoe inventory: modifies, searches and updates stock.


#=====Formatting Options=====
RED = '\033[31m'
GREEN = '\033[92m'
BLUE = '\033[94m'
PINK = '\033[95m'
CYAN = '\033[96m'
UNDERLINE = '\033[4m'
ENDC = '\033[0m' # Removes all formatting applied.
EM = f"{RED}‼{ENDC}" 
# 'Exclamation Mark' shorthand, preventing repeat code or going over 79char.


class Shoe():
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
    
    def get_cost(self):
        return self.cost
    
    def get_quantity(self):
        return self.quantity
    
    def get_code(self):
        return self.code
    
    def __str__(self):
        output = f"Product code: {self.code}\n"
        output += f"Name: {self.product}\n"
        output += f"Price: £{self.cost}\n"
        output += f"Quantity in stock: {self.quantity}\n"
        output += f"Country of Origin: {self.country}"
        return output 


def read_shoes_data():
    """ Function reads the inventory file and saves the contents to a list.
    Parameters: None
    Returns: None """
    
    first_line = True
    # Boolean value that will change once the first line from file is read.
    try:
        with open('inventory.txt', 'r', encoding='utf-8') as inventory:
            for line in inventory:
                if first_line == True:
                    first_line = False
                    continue
                # Skipping the first line in the file, contains content titles.
                
                line_data = line.strip().split(",")
                shoe = Shoe(line_data[0], line_data[1], line_data[2], 
                                line_data[3], line_data[4])
                shoe_list.append(shoe)
                # Saving each shoe one by one from file to our shoe list.
        print(f"\nInventory loaded {GREEN}successfully{ENDC}.")
    except FileNotFoundError:
        print(f"\n{EM} Inventory file not found.")
    except IndexError:
        print(f"{EM} Inventory file has been {RED}corrupted{ENDC}.",
            f"Please check file contents and try again.")


def capture_shoes():
    """ Function allows user to enter new shoe product to inventory.
    Parameters: None
    Returns: None """
    
    while True:
        try:
            code = input("Enter the product code: ").upper()
            if code[0:3] != "SKU" or len(code) != 8:
                raise Exception(f"'{code}' isn't good format (e.g.'SKU12345')")
            check = int(code.strip('SKU'))
            # If user enters something like 'SKU12w45', the 'check' variable 
            # will trigger "invalid literal for int() with base 10" error.
            break
        except Exception as error:
            print(f"{EM} {error}. Let's try again.")
        # The try except block will make sure user enters a valid SKU code.
    
    for shoe in shoe_list:
        if shoe.code == code:
            print(f"\n{RED}‼ Product code already exists.{ENDC}")
            return
    # If SKU code already on file, it won't add it and will return to menu.
    
    product = input("Enter the product name: ") 
    
    while True:
        try:
            cost = input("Enter the price: ") 
            check = int(cost)
            break
        except ValueError:
            print(f"{EM} Price needs to be a number. Let's try again.")
    
    while True:
        try:
            quantity = input("Enter the stock quantity: ") 
            check = int(quantity)
            break
        except ValueError:
            print(f"{EM} Quantity needs to be a number. Let's try again.")
    
    country = input("Enter the country of origin: ") 
    
    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)
    # Adding the new product to our shoe list.
    
    with open('inventory.txt', 'a', encoding='utf-8') as inventory:
        inventory.write(f"\n{country},{code},{product},{cost},{quantity}")
    # Saving the new shoe product to inventory.


def view_all():
    """ Function will go over the shoes list and print all details of shoes.
    Parameters: None
    Returns: None """
    
    counter = 0
    for shoe in shoe_list:
        counter += 1
        if counter % 2 == 0:
            print(f"\n{CYAN}{shoe}")
        else:
            print(f"\n{BLUE}{shoe}")
    # Displaying all shoes in stock and alternating colours while printing.


def re_stock():
    """ Function will find the shoe object with the lowest quantity, which 
    would need to be restocked, then choosing if they want to restock or not.
    Parameters: None
    Returns: None """
    
    for shoe in shoe_list:
        if shoe == shoe_list[0]:
            # This checks if it's the first object in the list and saves it.
            # We'd need a first value to have something to compare to.
            lowest_quantity = int(shoe.get_quantity())
            lowest_code = shoe.get_code()
        
        if lowest_quantity > int(shoe.get_quantity()):
            lowest_quantity = int(shoe.get_quantity())
            lowest_code = shoe.get_code()
            # Finding the product with the lowest quantity in stock.
    
    lowest_shoe = search_shoe(lowest_code)
    print(f"\nThe product with the lowest quantity in stock:",
            f"{RED}\n{lowest_shoe}{ENDC}\n")
    
    choice = input(f"""Choose stock refill options:
    {CYAN}a. Restock up to max quantity allowed (70 units)
    b. Restock specific quantity
    c. Go back to menu{ENDC}
    Your choice: {CYAN}""").lower().strip('.')
    
    print(f"{ENDC}", end='')
    
    while True:
        if choice == 'a':
            lowest_shoe.quantity = '70'
            # Overriding the object quantity to maximum allowed (70).
            
            print(f"Added {GREEN}{70 - lowest_quantity}{ENDC} units to stock.")
            print(f"New stock total: {GREEN}{lowest_shoe.quantity}{ENDC}")
        
        elif choice == 'b':
            restock = int(input("Enter how many units to add to stock: "))
            # Letting user choose the specific quantity they want to restock.
            
            lowest_shoe.quantity = str(lowest_quantity + restock)
            # Updating the shoe object with the desired quantity.
            
            print(f"Added {GREEN}{restock}{ENDC} units to stock.",
                f"New stock total: {GREEN}{lowest_shoe.quantity}{ENDC}")
        
        elif choice == 'c':
            # Exiting the function, user going back to menu.
            return
        
        else:
            print(f"\n{EM} You have made a wrong choice, please try again.")
            continue
        
        break
    
    # The following code will only run if user chose a. or b.
    
    with open('inventory.txt', 'w', encoding='utf-8') as inventory:
        inventory.write("Country,Code,Product,Cost,Quantity")
        # Writing with 'w' to override previous file.
    
    for shoe in shoe_list:
        shoe_to_add = f"\n{shoe.country},{shoe.code},{shoe.product},"
        shoe_to_add += f"{shoe.cost},{shoe.quantity}"
        
        with open('inventory.txt', 'a', encoding='utf-8') as inventory:
            inventory.write(shoe_to_add)
    # Iterating through the shoe list and adding each shoe object to file.


def search_shoe(code_to_search):
    """ Function will search for a shoe from the list using the shoe code.
    Parameters: None
    Returns: shoe (object) if found; or 'code not found' (str) """
    
    for shoe in shoe_list:
        if shoe.code == code_to_search:
            return shoe
    
    return f"{RED}‼ '{code_to_search}' not found.{ENDC}"
    # If loop finished without returning 'shoe', it will return 'not found'.


def value_per_item():
    """ Function will calculate the total value for each item and print it.
    Parameters: None
    Returns: None """
    
    total_money = 0
    print(f"\n{PINK}{UNDERLINE}The values of each stock item{ENDC}\n")
    
    for shoe in shoe_list:
        value = int(shoe.get_cost()) * int(shoe.get_quantity())
        total_money += value
        # Calculating the total value of entire stock as well.
        print(f"{shoe.code} ({shoe.product}) value: {CYAN}£{value}{ENDC}")
    
    print(f"\nTotal stock worth: {GREEN}£{total_money}{ENDC}")


def highest_qty():
    """ Function determines the product with the highest quantity and prints 
    this shoe as being for sale.
    Parameters: None
    Returns: None """
    
    for shoe in shoe_list:
        if shoe == shoe_list[0]:
            # This checks if it's the first object in the list and saves it.
            # We'd need a first value to have something to compare to.
            highest_quantity = int(shoe.quantity)
            highest_code = shoe.code
        
        if highest_quantity < int(shoe.quantity):
            highest_quantity = int(shoe.quantity)
            highest_code = shoe.code
    
    highest_shoe = search_shoe(highest_code)
    print(f"\nThis shoe has the highest quantity in stock:\n\n" +
            f"{CYAN}{highest_shoe}\n{ENDC}\nIt's going on {GREEN}SALE{ENDC}!")


#==========Main Menu=============

shoe_list = []
# The list will be used to store the objects of shoes.

inventory_opened = False
# Boolean variable that will confirm if inventory was accessed and saved.


while True:
    menu = input(f'''
    {PINK}╔{'═'*45}╗
    ║{ENDC} Please select one of the following options: {PINK}║
    ║ ♦{CYAN} 1 {ENDC}- Load the inventory file {PINK}{' '*14}║
    ║ ♦{CYAN} 2 {ENDC}- Enter new product to inventory {PINK}{' '*7}║
    ║ ♦{CYAN} 3 {ENDC}- View all products {PINK}{' '*20}║
    ║ ♦{CYAN} 4 {ENDC}- Re-stock {PINK}{' '*29}║
    ║ ♦{CYAN} 5 {ENDC}- Search for a product {PINK}{' '*17}║
    ║ ♦{CYAN} 6 {ENDC}- Values of each stock item{PINK}{' '*13}║
    ║ ♦{CYAN} 7 {ENDC}- Find product for SALE {PINK}{' '*16}║
    ║ ♦{RED} 8 {ENDC}- {UNDERLINE}Exit{ENDC}{PINK}{' '*34}║
    ╚{'═'*45}╝
    {ENDC}  Your selection: {CYAN}''').lower()
    
    print(f"{ENDC}", end='') # Resetting the colour formatting. 
    
    if menu == '1':
        # Loading the inventory file to list.
        read_shoes_data()
        
        inventory_opened = True
        # Boolean variable confirming shoe inventory saved to list. 
    
    elif menu == '2':
        # Entering a new product to inventory and to list.
        if inventory_opened == False:
            print(f"\n{EM} You need to load the inventory file first.")
            continue
        capture_shoes()
    
    elif menu == '3':
        # Displays all products on the screen.
        if inventory_opened == False:
            print(f"\n{EM} You need to load the inventory file first.")
            continue
        view_all()
    
    elif menu == '4':
        # Restocks product.
        if inventory_opened == False:
            print(f"\n{EM} You need to load the inventory file first.")
            continue
        re_stock()
    
    elif menu == '5':
        # Searches for a product by product code.
        if inventory_opened == False:
            print(f"\n{EM} You need to load the inventory file first.")
            continue
        
        product_code = input("Enter the SKU code you want to search: ").upper()
        print(f"\n{GREEN}{search_shoe(product_code)}{ENDC}")
    
    elif menu == '6':
        # Displays values of each stock item.
        if inventory_opened == False:
            print(f"\n{EM} You need to load the inventory file first.")
            continue
        value_per_item()
    
    elif menu == '7':
        # Finds the highest quantity product and display it as for sale.
        if inventory_opened == False:
            print(f"\n{EM} You need to load the inventory file first.")
            continue
        highest_qty()
    
    elif menu == '8':
        # Exit program.
        print(f"{CYAN}Goodbye!{ENDC}")
        break
    
    else:
        print(f"\n{EM} You have made a wrong choice, please try again.")