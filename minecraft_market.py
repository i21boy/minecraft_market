import csv
def add_items():
    item = input("Item Name: ")
    price = input("Item price(coins) :")
    seller = input("Seller name: ")
    with open("market_csv", mode="a",newline="")as file:
        writer= csv.writer(file)
        writer.writerow([item ,price,seller])
    print("Item added\n")

def view_market():
    try:
        with open("market_csv", mode="r", newline="")as file:
            reader = csv.reader(file)
            print("\n---Minecraft Market---")
            print("{:20}{:10}{:<15}".format("item", "price", "seller"))
            print("-"*50)
            for row in reader:
                print("{:<20}{:<10}{:<15}".format(*row))
            print()
    except FileNotFoundError:
        print("Market in empty.\n")

def main():
    while True:
        print("1. Add item for sale")
        print("2. View market")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            add_items()
        elif choice == "2":
            view_market()
        elif choice == "3":
            break
    else:
        print("Invalid choice.\n")

if __name__== "__main__":
    main()

            
