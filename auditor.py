inventory = 0
loop = "continue"
while loop != "quit":
    #loop code
    stockvalue = input("What is the current stock value: ")
    #integer as input
    if stockvalue.isdigit() == False:
        print("Error, please input a number.")
    else:
        stockvalue = int(stockvalue)
        if stockvalue < 0:
            print("Error, please input a positive number")
            


