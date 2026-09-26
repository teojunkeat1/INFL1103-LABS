maxcapacity = 500
taxrate = 0.1 


def load_inventory():
    try: 
        file = open('inventory.txt', 'r')
    except:
        file = open('inventory.txt', 'w+')
    inventory = file.read()
    print(inventory)
    file.close()

def store_valid_transaction(inventory_list, inventory):
    inventory_list.append(inventory)

def save_inventory(inventory,inventory_list):
    file = open('inventory.txt', 'w+')
    file.write(str(inventory))
    file.write("\n")
    file.writelines(str(inventory_list))
    file.close()


#Opening previous inventory

#Modular input: get valid input
def get_valid_input():
    userInput = input("What is the current stock value: ")
    if userInput == "quit":
        return "quit"
    elif userInput.isdigit() == False:
        print("Error, please input a positive whole number.")
        return None 

    elif int(userInput) >= maxcapacity:
        print("Error, please input a valid number: ")
        return None
    else:
        return int(userInput)    

#Process delivery
def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total

#Calculate tax
def calculate_tax(amount):
    tax = amount * taxrate
    return tax 

#Generate report
def generate_report(total_units, failed_attempts):
    print("The total units delivered is: " + str(total_units))
    print("The total failed entries is: " + str(failed_attempts))

def main():

    inventory = 0
    tax_amount = 0
    failed_attempts = 0 
    inventory_list = [] 
    exit_program = False

    load_inventory()

    while not exit_program:

        userInput = get_valid_input()

        if userInput == "quit":
            generate_report(inventory, failed_attempts)
            save_inventory(inventory, inventory_list)
            exit_program = True 

        elif userInput == None:
            failed_attempts += 1

        elif inventory > maxcapacity:
            print("Error, delivery would exceed max capacity.")
            generate_report(inventory, failed_attempts)
            save_inventory(inventory, inventory_list)
            exit_program = True

        else:
            inventory = process_delivery(inventory, userInput)
            tax_amount = calculate_tax(userInput)
            store_valid_transaction(inventory_list, userInput)
            print("Delivery successful, tax is:" + str(tax_amount))
            print(inventory_list)
main()



    


