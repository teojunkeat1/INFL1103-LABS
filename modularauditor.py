inventory = 0
rejectedentries = 0
while True:
    #loop code
    stockvalue = input("What is the current stock value: ")
    if stockvalue == "quit":
        print("Total processed units: " + str(inventory))
        print("Total rejected units: " + str(rejectedentries))
        break 
    #integer as input
    elif stockvalue.isdigit() == False:
        print("Error, please input a positive whole number.")
        rejectedentries += 1
    else:
        inventory += int(stockvalue)
    print("Your current inventory is:" + str(inventory))
    if inventory > 500:
        print("Current inventory is above 500.")
        break 

maxcapacity = 500
taxrate = 0.1 
failed_attempts = 0

#Modular input: get valid input
def get_valid_input():
    userInput = input("What is the current stock value: ")
    if userInput == "quit":
        return "quit"
    elif userInput.isdigit() == False:
        print("Error, please input a positive whole number.")
        failed_attempts += 1
    else:
        return userInput    

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
    print("The total failed entries is: " + str(failed_attempts)))





    


