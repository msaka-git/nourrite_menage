import script
from shared_mods.connection_module import conn,cur
from shared_mods.logger_module import logger
import re
from script import mainscript




amountTotal_food=float(0)
amountTotal_shopping=float(0)

ins=mainscript()

f=ins.root_win()
bankFile=ins.file_select(f)
## SQL QUERIES FOR FOOD ##

sql_sub = "select t_customer from table_customer_food"

sub_check = cur.execute(sql_sub)

sub_fetch = sub_check.fetchall()

sub_list = [list(i) for i in sub_fetch]

sub = []
for a in sub_list:
    for b in a:
        sub.append(b.lower()) # converts provider name from database to lower case.

## SQL QUERIES FOR SHOPPING ##

sql_sub_sh = "select t_customer from table_customer_shopping"

sub_check_sh = cur.execute(sql_sub_sh)

sub_fetch_sh = sub_check_sh.fetchall()

sub_list_sh = [list(i) for i in sub_fetch_sh]
sub_sh = []
for a in sub_list_sh:

    for b in a:
        sub_sh.append(b.lower()) #converts provider name from database to lower case.

dt = bankFile["Value Date"].tail(1)
data = bankFile.sort_values("Operation")

def amount_retriever(func):
    '''
    Retrieve the amount of a given row.
    Ex: you want to retrieve the amount of 'orange' telecom expense.
    '''

    def wrapper(argument):
        islem = func(argument)
        expense_data = data[data['Operation'].str.contains(islem,flags=re.IGNORECASE)]
        expense_amount = [float(i) for i in expense_data['Amount']]

        return expense_amount
    return wrapper

def insert_data():

    for a in dt:
        sql1 = "insert into table_nourriture values(NULL,'{}','{}')".format(a, amountTotal_food)

        cur.execute(sql1)
        conn.commit()


def insert_customer():
    sql2 = "insert into table_customer_food values(NULL,'{}')".format(sub_input)
    cur.execute(sql2)
    conn.commit()


def delete_customer():
    sql3 = "delete from table_customer_food where t_customer = '{}'".format(choice_del)
    cur.execute(sql3)
    conn.commit()


def see_saved():
    sql4 = "select t_date,t_spent from table_nourriture"
    data = cur.execute(sql4)
    for i in data.fetchall():
        print(', '.join(map(str, i)))


def add_delete():
    in1 = input("Do you want to add or delete company? (add/delete/n): ")

    if in1 == 'add' or in1 == 'ADD':
        global sub_input
        sub_input = input("Company to add: ")
        insert_customer()


    elif in1 == 'delete' or in1 == 'DELETE':
        print('\n', sub, '\n')
        global choice_del
        choice_del = input("Company to delete: ")
        delete_customer()

    elif in1 == 'n' or in1 == 'N':
        spent()

    else:
        logger.warning("Operation not found. Program quits...")


def spent():

    LIST = []

    for i in sub:
        operation_Name = data[data['Operation'].str.contains(i,flags=re.IGNORECASE)] # flags= ignore case sensitivity in excel file.
        amounts = operation_Name["Amount"]

        for row in amounts:
            LIST.append(row)


    global amountTotal_food
    amountTotal_food = round(sum(LIST), 2)
    print("\nThe amount that you paid for food is: ", amountTotal_food)

    choice_save = input("\nDo you want to save ? (y/n): ")
    if choice_save == 'y' or choice_save == 'Y':
        insert_data()
        print("Data has been saved...")
    else:
        pass
    return amountTotal_food

#### SHOPPING FUNCTIONS ###################

def insert_data_shopping():

    for a in dt:
        sql1 = "insert into table_shopping values(NULL,'{}','{}')".format(a, amountTotal_shopping)

        cur.execute(sql1)
        conn.commit()

def insert_customer_shopping():
    sql2 = "insert into table_customer_shopping values(NULL,'{}')".format(sub_input)
    cur.execute(sql2)
    conn.commit()

def delete_customer_shopping():
    sql3 = "delete from table_customer_shopping where t_customer = '{}'".format(choice_del)
    cur.execute(sql3)
    conn.commit()

def see_saved_shopping():
    sql4 = "select t_date,t_spent from table_shopping"
    data = cur.execute(sql4)
    for i in data.fetchall():
        print(', '.join(map(str, i)))


def add_delete_shopping():
    in1 = input("Do you want to add or delete company? (add/delete/n): ")

    if in1 == 'add' or in1 == 'ADD':
        global sub_input
        sub_input = input("Company to add: ")
        insert_customer_shopping()


    elif in1 == 'delete' or in1 == 'DELETE':
        print('\n', sub_sh, '\n')
        global choice_del
        choice_del = input("Company to delete: ")
        delete_customer_shopping()

    elif in1 == 'n' or in1 == 'N':
        spent_shopping()

    else:
        logger.warning("Operation not found. Program quits...")


def spent_shopping():

    LIST = []

    for i in sub_sh:
        operation_Name = data[data['Operation'].str.contains(i,flags=re.IGNORECASE)] # flags= ignore case sensitivity in excel file.)]
        amounts = operation_Name["Amount"]

        for row in amounts:
            LIST.append(row)

    global amountTotal_shopping
    amountTotal_shopping = round(sum(LIST), 2)

    print("\nThe amount that you paid for shopping is: ", amountTotal_shopping)

    choice_save = input("\nDo you want to save ? (y/n): ")
    if choice_save == 'y' or choice_save == 'Y':
        insert_data_shopping()
        print("Data has been saved...")
    else:
        pass
    return amountTotal_shopping

##### Liesure and others #################

def spent_liesure_others():
    value_all=['PURCHASE']
    LISTe = []
################ Start investment amount

    invest=data[data['Operation'].str.contains('ING ARIA',flags=re.IGNORECASE)] # flags= ignore case sensitivity in excel file.)] # selects row with item

    amount_invest=[0] if invest.empty else invest["Amount"]
    amount_invest=[i for i in amount_invest]

    ind=len(amount_invest)

    global fl_amount_invest
    for _ in range(ind): fl_amount_invest = float(sum(amount_invest))

########### END investment amount

    global operation_Namer
    global operation_Namer_creditCard
    global amounts
    purchase_count=data[data['Operation'].str.contains('purchase',flags=re.IGNORECASE)].count()
    if purchase_count['Operation'] > 0:
        for imm in value_all: operation_Namer = data[data['Operation'].str.contains(imm,flags=re.IGNORECASE)] # flags= ignore case sensitivity in excel file.)]
        amounts=operation_Namer["Amount"]
    else:
        operation_Namer_creditCard=data[data['Operation'].str.contains("PAYMENT OF VISA|TRANSFER")==False]
        amounts=operation_Namer_creditCard['Amount']

    for row in amounts: LISTe.append(row)

    global amountTotal_all
    amountTotal_all=round(sum(LISTe),2)

    amount_spent_lieure_other=(-(amountTotal_all-amountTotal_shopping-amountTotal_food-fl_amount_invest))

    print("\nThe amount spent in investment: ", round(fl_amount_invest, 2))
    print("\nThe amount that you paid for liesure and others is: ", -round(amount_spent_lieure_other,2))
    return -round(amount_spent_lieure_other,2)

########## Income /exp balance

@amount_retriever
def salary(salary):
    return salary

@amount_retriever
def telecom_spent(telecom):
    return telecom

@amount_retriever
def rent(amount):
    return amount

def monthly_spent():
    '''
    return only expenses. Without investment amount.
    '''
    expenses_food = spent()
    expenses_shopping = spent_shopping()
    expenses_liesure_other = spent_liesure_others()
    expenses_rent = sum(rent(script.loyer))
    expenses_telecom = sum(telecom_spent(script.telecom))
    income = sum(salary(script.employer))

    expenses_total = expenses_shopping + expenses_food + expenses_liesure_other + expenses_rent + expenses_telecom
    print(expenses_total)
    balance = round(income - (-expenses_total),2)
    print(balance)


