inventory = 0
loop = "continue"
rejectedentries = 0
while loop != "quit" or inventory > 500:
    #loop code
    stockvalue = input("What is the current stock value: ")
    #integer as input
    if stockvalue.isdigit() == False:
        print("Error, please input a number.")
        rejectedentries += 1
    elif int(stockvalue) < 0:
        print("Error, please input a positive number")
        rejectedentries += 1
    else:
        inventory += stockvalue 
    print("Your current inventory is:" + inventory)
    loop = ("Continue? Type "continue" or "quit": ")
if inventory > 500:
    print("Current inventory is above 500.")

    



