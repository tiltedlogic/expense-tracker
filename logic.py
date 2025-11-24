# started: 11/3/25
#finished : never :(

from datetime import datetime
import json

transactions = [
 #example -
    #{"transaction_type" : "expense",
    #{"category" : "food",
    #"amount" : 11.15,
    # "date" : "11/17/2025"
    # "note" : "...."
    # }
]

def load_data():
    global transactions
    with open("data.json", "r") as file:
        transactions = json.load(file)


def save_data():
    with open("data.json", "w") as file:
        json.dump(transactions, file, indent=4)

def main_menu():
    selection = input("what would you like to do? \n 1. Add transaction \n 2. Review transactions \n 3. Delete transaction \n 4. quit (please respond with 1, 2, 3, or 4)")
    if selection not in {"1", "2", "3", "4"}:
        print("invalid input. Please try again.")
    return selection


def add_transaction():
    transaction_type = input("please input the type of transaction \n 1. Expense \n 2. Income")
    if transaction_type == "1":
        transaction_type = "Expense"
    elif transaction_type == "2":
        transaction_type = "Income"

    category = input("please input the category (i.e. food, gas, electric bill")

    amount_string = input("please input the amount of transaction")
    amount = float(amount_string)

    date = input("please input date like mm/dd/yyyy")
    date_obj = datetime.strptime(date, "%m/%d/%Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")

    note = input("any additional details for personal tracking")

    new_data = {
        "transaction_type": transaction_type,
        "category": category,
        "amount": amount,
        "date": formatted_date,
        "note": note
    }

    transactions.append(new_data)



def review_transaction():
    x = 1
    if not transactions:
        print("you can not view transactions because you have none!")
        return
    for item in transactions:

        print(x,".", f"Transaction Type: {item['transaction_type']} \n Category: {item['category']} \n Amount: {item['amount']} \n Date: {item['date']} \n Note: {item['note']} \n --------------------- ")
        x += 1


def delete_transaction():
    x = 1
    for item in transactions:

        print(x, ".",
              f"Transaction Type: {item['transaction_type']} \n Category: {item['category']} \n Amount: {item['amount']} \n Date: {item['date']} \n Note: {item['note']} \n --------------------- ")
        x += 1
    index_delete = input("please enter the number of the transaction you want to delete")
    index_delete = int(index_delete)
    index_delete = index_delete - 1

    transactions.pop(index_delete)


def run():
   load_data()
   while True:
    selection = main_menu()

    if selection == "1":
        add_transaction()
        save_data()
    if selection == "2":
        review_transaction()

    if selection == "3":
       delete_transaction()
       save_data()
    if selection == "4":
        break


run()


