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


#Modular input: get valid input
def get_valid_input():
    if userInput == "quit":
        return "quit"
    elif userInput.isdigit() == False:
        print("Error, please input a positive whole number.")
    else:
        return userInput    
        


    


