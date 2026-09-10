inventory = 0
loop = "continue"
rejectedentries = 0
while loop != "quit" or inventory > 500:
    #loop code
    stockvalue = input("What is the current stock value: ")
    #integer as input
    if stockvalue.isdigit() == False:
        print("Error, please input a positive whole number.")
        rejectedentries += 1
    else:
        stockvalue = int(stockvalue)
        inventory += stockvalue 
    print("Your current inventory is:" + str(inventory))
    loop = input("Continue? Type continue or quit: ")
if inventory > 500:
    print("Current inventory is above 500.")
elif loop == "quit":
    print("Total Units processed: " + str(inventory))
    print ("Total rejected units: " + str(rejectedentries))
    
    



