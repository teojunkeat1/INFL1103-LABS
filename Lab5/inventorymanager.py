import json 

def menu():
    print("========================================\nINVENTORY MANAGEMENT SYSTEM\n========================================")

menu()

def add_product(id, name, stock, cost):
    product = {"ID: ":id, "Name: ":name, "Stock: ":stock, "Cost: ":cost}
    with open("data.json", "a", encoding="utf-8") as f:
        json.dump(product, f, indent=2)
    print(product)

add_product(1001,10,10,100)
add_product(2222,22,22,22)






