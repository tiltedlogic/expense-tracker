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

income_categories = []
expense_categories = []


def load_transaction_data():
    global transactions
    with open("transaction_data.json", "r") as file:
        transactions = json.load(file)


def save_transaction_data():
    with open("transaction_data.json", "w") as file:
        json.dump(transactions, file, indent=4)


def load_categories():
    global income_categories
    global expense_categories
    with open("categories.json", "r") as file:
        data = json.load(file)

    income_categories = data["income"]
    expense_categories = data["expense"]

def save_categories():
    with open("categories.json", "w") as file:
        data = {
            "income": income_categories,
            "expense": expense_categories
        }
        json.dump(data, file, indent=4)


def main_menu():
    selection = input("what would you like to do? \n 1. Add transaction \n 2. Review transactions \n 3. Delete transaction \n 4. Edit transaction \n 5. quit (please respond with 1, 2, 3, 4, or 5)")
    if selection not in {"1", "2", "3", "4", "5"}:
        print("invalid input. Please try again.")
    return selection


def category_selection(transaction_type, category):
    global expense_categories
    global income_categories
    print(transaction_type)
    if transaction_type == "Expense":
        category = expense_categories
    elif transaction_type == "Income":
        category = income_categories
    else:
        print("an error has occurred please try again.")
        run()

    print(category)
    for index, cat_name in enumerate(category, start = 1):
        print(f"{index}. {cat_name}")
    print(len(category))
    last_option = len(category) +1


    print(f"{last_option}.create new category")
    category_input_selection = input("please enter the number value of category you want to use for this transaction, or create a new one(last option in selection of categories).")
    category_input = int(category_input_selection)
    print(category_input)
    print(last_option)
    if category_input == last_option:
         new_category = input("please input new category name")
         category.append(new_category)
         category = new_category
         return category
    else:
        category = category[category_input - 1]
        return category




def add_transaction():
    transaction_type = input("please input the type of transaction \n 1. Expense \n 2. Income")
    if transaction_type == "1":
        transaction_type = "Expense"
    elif transaction_type == "2":
        transaction_type = "Income"


    category = ''

    category = category_selection(transaction_type, category)

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

        print(x, ".", f"Transaction Type: {item['transaction_type']} \n Category: {item['category']} \n Amount: {item['amount']} \n Date: {item['date']} \n Note: {item['note']} \n --------------------- ")
        x += 1


def delete_transaction():
    review_transaction()

    index_delete = input("Please enter the number of the transaction you want to delete")
    index_delete = int(index_delete)
    index_delete = index_delete - 1

    transactions.pop(index_delete)


def edit_transaction():
   global transactions




   while True:
    review_transaction()
    edit_index_input = input("please input the # of transaction to edit")
    index_edit = int(edit_index_input) - 1

    data_change = input( "What would you like to edit? \n 1. Transaction Type \n 2. Category \n 3. Amount \n 4. Date \n 5. Note")

    if data_change == "1":
        current_type = transactions[index_edit]["transaction_type"]
        confirm_edit = input(f"This transaction is currently labeled as {current_type}. Would you like to switch it to the other type? (y or n)")
        if confirm_edit == "n":
            print("so.... You didn't have anything to change then?")
            break
        if confirm_edit == "y" and current_type == "income":
            edit = "expense"
            transactions[index_edit]["transaction_type"] = edit
        elif confirm_edit == "y" and current_type == "expense":
            edit = "income"
            transactions[index_edit]["transaction_type"] = edit

    if data_change == "2":

        category = ''
        transaction_type = transactions[index_edit]["transaction_type"]
        print(transaction_type)
        category = category_selection(transaction_type, category)
        transactions[index_edit]["category"] = category

    if data_change == "3":
        amount_string = input("please input the amount of transaction")
        amount = float(amount_string)

        transactions[index_edit]["amount"] = amount

    if data_change == "4":
        date = input("please input date like mm/dd/yyyy")
        date_obj = datetime.strptime(date, "%m/%d/%Y")
        formatted_date = date_obj.strftime("%Y-%m-%d")

        transactions[index_edit]["date"] = formatted_date

    if data_change == "5":
        note = input("please input new note")
        transactions[index_edit]["note"] = note



    edit_more = input("Is there more you would like to edit? (y or n)")

    if edit_more == "n":
        break





def run():
   load_transaction_data()
   load_categories()
   while True:
    selection = main_menu()

    if selection == "1":
        add_transaction()
        save_transaction_data()
        save_categories()
    if selection == "2":
        review_transaction()

    if selection == "3":
       delete_transaction()
       save_transaction_data()

    if selection == "4":
        edit_transaction()
        save_transaction_data()
        save_categories()

    if selection == "5":
        save_transaction_data()
        save_categories()
        break


run()





