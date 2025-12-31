# started: 11/3/25
#finished : never :(

from datetime import datetime
import json
import sqlite3


conn = sqlite3.connect("transactions.db")
c = conn.cursor()


def create_trans_table():
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS transactions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT,
                category TEXT,
                bucket TEXT,
                amount REAL,
                date TEXT,
                note TEXT
        )""")

def create_cat_table():
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS income_categories(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT UNIQUE
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS expense_categories(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT UNIQUE
        )""")

    try:
        income_cats = [
            ("Income",),
            ("Investments",),
            ("Refund",)
        ]
        with conn:
            c.executemany("INSERT INTO income_categories (category) VALUES (?)",
                        income_cats)

            expense_cats = [
                ("gas",),
                ("food",),
                ("lifestyle",),
                ("personal hygiene",)
            ]
            c.executemany("INSERT INTO expense_categories(category) VALUES (?)",
                        expense_cats)
    except sqlite3.IntegrityError:
        pass # defaults already exist


def insert_transaction(transaction_type, category, bucket, amount, formatted_date, note):
    new_data = (transaction_type, category, bucket, amount, formatted_date, note)
    with conn:
        c.execute("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?)", new_data)

#c.execute("SELECT * FROM transactions")
#print(c.fetchall())

conn.commit()


def load_transaction_data():
    with open("transaction_data.json", "r") as file:

        return json.load(file)


def save_transaction_data(transaction_list):
    with open("transaction_data.json", "w") as file:
        json.dump(transaction_list, file, indent=4)


def load_categories():
    with open("categories.json", "r") as file:
        data = json.load(file)

    return data["income"], data["expense"]


def save_categories():
    with open("categories.json", "w") as file:
        data = {
            "income": income_categories,
            "expense": expense_categories
        }
        json.dump(data, file, indent=4)


def main_menu():
    selection = input("what would you like to do? "
                      "\n 1. Add transaction "
                      "\n 2. Review transactions "
                      "\n 3. Delete transaction "
                      "\n 4. Edit transaction "
                      "\n 5. Quit "
                      "(please respond with 1, 2, 3, 4, or 5)"
    )

    if selection not in {"1", "2", "3", "4", "5"}:
        print("Invalid input. Please try again.")

    return selection

def category_selection(transaction_type, income_list, expense_list):
    if transaction_type == "expense":
        category = expense_list
    elif transaction_type == "income":
        category = income_list

    for index, cat_name in enumerate(category, start=1):
        print(f"{index}. {cat_name}")

    last_option = len(category) + 1
    print(f"{last_option}. Create new category")

    category_input_selection = input("please enter the number value of category you"
                                     " want to use for this transaction, or create a"
                                     " new one(last option in selection of categories)."
    )

    category_input = int(category_input_selection)

    if category_input == last_option:
        new_category = input("please input new category name")

        category.append(new_category)
        return new_category
    else:
        return category[category_input - 1]


def add_transaction(transaction_type, category, bucket, amount, formatted_date, note, income_list, expense_list):
    bucket = ''

    transaction_type = input("please input the type of transaction "
                             "\n 1. Expense "
                             "\n 2. Income"
    )

    if transaction_type == "1":
        transaction_type = "expense"
    elif transaction_type == "2":
        transaction_type = "income"
    else:
        print("Invalid transaction type. Please Try again.")
        return

    category = category_selection(transaction_type, income_list, expense_list)

    amount_string = input("please input the amount of transaction")
    amount = float(amount_string)

    date = input("please input date like mm/dd/yyyy")
    date_obj = datetime.strptime(date, "%m/%d/%Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")

    note = input("any additional details for personal tracking")

    if transaction_type == "expense":
        raw = input("What is this transaction?"
                    "\n 1. Need"
                    "\n 2. Want"
                    "\n 3. Savings"
        )

        if raw == "1":
            bucket = "needs"
        if raw == "2":
            bucket = "wants"
        if raw == "3":
            bucket = "savings"

        add_transaction(transaction_type, category, bucket, amount, formatted_date, note, income_list, expense_list)

    else:
        bucket = "income"
        add_transaction(transaction_type, category, bucket, amount, formatted_date, note, income_list, expense_list)



def review_transaction(transaction_list):
    if not transaction_list:
        print("you can not view transactions because you have none!")


    for x, item in enumerate(transaction_list, 1):
        print(x, ".", f"Transaction Type: {item['transaction_type']} \n Category: {item['category']} \n Bucket: {item['bucket']} \n Amount: {item['amount']} \n Date: {item['date']} \n Note: {item['note']} \n --------------------- ")


def delete_transaction(transaction_list):
    review_transaction(transaction_list)

    index_delete = input("Please enter the number of the transaction you want to delete")
    index_delete = int(index_delete)
    index_delete = index_delete - 1
    transaction_list.pop(index_delete)


def edit_transaction(transaction_list, income_list, expense_list):
    review_transaction(transaction_list)

    edit_index_input = input("please input the # of transaction to edit")
    index_edit = int(edit_index_input) - 1

    data_change = input( "What would you like to edit? "
                         "\n 1. Transaction Type "
                         "\n 2. Category "
                         "\n 3. Bucket "
                         "\n 4. Amount "
                         "\n 5. Date "
                         "\n 6. Note"
    )

    if data_change == "1":
        current_type = transaction_list[index_edit]["transaction_type"]

        confirm_edit = input(f"This transaction is currently labeled as "
                             f"{current_type}. Would you like to switch it to the other type? (y or n)"
        )

        if confirm_edit == "n":
            print("so.... You didn't have anything to change then?")
            return

        if confirm_edit == "y" and current_type == "income":
            edit = "expense"

            bucket_input = input("What bucked should this transaction go under?"
                                 "\n 1. Need "
                                 "\n 2. Want "
                                 "\n 3. Savings"
            )

            if bucket_input == "1":
                bucket = "needs"
            if bucket_input == "2":
                bucket = "wants"
            if bucket_input == "3":
                bucket = "savings"

            transaction_list[index_edit]["transaction_type"] = edit

            transaction_list[index_edit]["bucket"] = bucket

        elif confirm_edit == "y" and current_type == "expense":
            edit = "income"
            bucket = "income"

            transaction_list[index_edit]["transaction_type"] = edit

            transaction_list[index_edit]["bucket"] = bucket

    if data_change == "2":
        transaction_type = transaction_list[index_edit]["transaction_type"]

        category = category_selection(transaction_type,income_list, expense_list,)
        transaction_list[index_edit]["category"] = category

    if data_change == "3":
        if transaction_list[index_edit]["transaction_type"] == "expense":
            options = ["needs", "wants", "savings"]
            current = transaction_list[index_edit]["bucket"]
            options.remove(current)

            bucket = input(
                f"This transaction is currently labeled as {current}. What would you like to change it to? "
                f"\n 1. {options[0]} "
                f"\n 2. {options[1]} "
                f"\n 3. Cancel"
            )

            if bucket == "3":
                return
            elif bucket == "1":
                transaction_list[index_edit]["bucket"] = options[0]
            elif bucket == "2":
                transaction_list[index_edit]["bucket"] = options[1]

        else:
            print("You can not change bucket type on income transactions "
                  "as they don't have a specific bucket besides income"
            )

    if data_change == "4":
        amount_string = input("please input the amount of transaction")
        amount = float(amount_string)

        transaction_list[index_edit]["amount"] = amount

    if data_change == "5":
        date = input("please input date like mm/dd/yyyy")
        date_obj = datetime.strptime(date, "%m/%d/%Y")
        formatted_date = date_obj.strftime("%Y-%m-%d")

        transaction_list[index_edit]["date"] = formatted_date

    if data_change == "6":
        note = input("please input new note")
        transaction_list[index_edit]["note"] = note


def run(transaction_list, income_list, expense_list):
    create_trans_table()
    create_cat_table()
    while True:
        selection = main_menu()

        if selection == "1":
            add_transaction(transaction_list, income_list, expense_list)
            save_transaction_data(transaction_list)
            save_categories()

        elif selection == "2":
            review_transaction(transaction_list)

        elif selection == "3":
            delete_transaction(transaction_list)
            save_transaction_data(transaction_list)

        elif selection == "4":
            edit_transaction(transaction_list, income_list, expense_list)
            save_transaction_data(transaction_list)
            save_categories()

        elif selection == "5":
            save_transaction_data(transaction_list)
            save_categories()
            conn.close()
            break


transaction_list = load_transaction_data()

income_categories, expense_categories = load_categories()


run(transaction_list, income_categories, expense_categories)