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

dt = bankFile["Value Date"].tail(1)
data = bankFile.sort_values("Operation")

## SQL QUERIES FOR FOOD ##
def sql_queries(object_):
    '''
    object = FOOD or SHOPPING
    '''

    sql_sub = "select t_customer from table_customer_{}".format(object_)
    #print(sql_sub)

    sub_check = cur.execute(sql_sub)

    sub_fetch = sub_check.fetchall()

    sub_list = [list(i) for i in sub_fetch]

    sub = []
    for a in sub_list:
        for b in a:
            sub.append(b.lower()) # converts provider name from database to lower case.
    return sub

def amount_retriever(func):
    '''
    Retrieve the amount of a given row.
    Ex: you want to retrieve the amount of 'orange' telecom expense.
    '''

    def wrapper(*args):
        islem = func(*args)
        expense_data = data[data['Operation'].str.contains(islem,flags=re.IGNORECASE)]
        expense_amount = [float(i) for i in expense_data['Amount']]
        #print("Expense amount:", expense_amount)
        return expense_amount
    return wrapper

def insert_data(table):

    for a in dt:
        sql1 = "insert into table_{} values(NULL,'{}','{}')".format(table,a, amountTotal)

        cur.execute(sql1)
        conn.commit()


def insert_customer(table):
    sql2 = "insert into table_customer_{} values(NULL,'{}')".format(table,sub_input)
    cur.execute(sql2)
    conn.commit()


def delete_customer(table):
    sql3 = "delete from table_customer_{} where t_customer = '{}'".format(table,choice_del)
    cur.execute(sql3)
    conn.commit()


def see_saved(table):
    sql4 = "select t_date,t_spent from table_{} order by t_date".format(table)
    data = cur.execute(sql4)
    for i in data.fetchall():
        print(', '.join(map(str, i)))


def add_delete(object_):
    in1 = input("Do you want to add or delete company? (add/delete/n): ")

    if in1 == 'add' or in1 == 'ADD':
        global sub_input
        sub_input = input("Company to add: ")
        insert_customer(object_)


    elif in1 == 'delete' or in1 == 'DELETE':
        #print('\n', sql_queries(object_), '\n')
        global choice_del
        choice_del = input("Company to delete: ")
        delete_customer(object_)

    elif in1 == 'n' or in1 == 'N':
        print("The amount that you have paid for '{}' is:".format(object_) ,spent(object_))


    else:
        logger.warning("Operation not found. Program quits...")


def spent(object_):
    '''
    object must be food, shopping, liesure or all
    '''

    LIST = []

    for i in sql_queries(object_):
        operation_Name = data[data['Operation'].str.contains(i,flags=re.IGNORECASE)] # flags= ignore case sensitivity in excel file.
        amounts = operation_Name["Amount"]

        for row in amounts:
            LIST.append(row)


    global amountTotal
    amountTotal = round(sum(LIST), 2)

    return amountTotal

##### Liesure and others #################
#@amount_retriever
def spent_investment():
    # amount_fl_invest = investment
    invest=data[data['Operation'].str.contains('PURCHASE ING ARIA',flags=re.IGNORECASE)]
    amount_invest=[0] if invest.empty else invest["Amount"]
    amount_invest=[i for i in amount_invest]
    ind=len(amount_invest)

    global fl_amount_invest
    for _ in range(ind): fl_amount_invest = float(sum(amount_invest))
    return fl_amount_invest

def spent_liesure_others():
    # amount_spent_li_ot=others
    value_all=['PURCHASE']
    LISTe = float(0) # all amount was spent
    for i in value_all:
        all_spent_amounts = data[data['Operation'].str.contains(i,flags=re.IGNORECASE)]
        LISTe = sum(all_spent_amounts['Amount'])

    expenses_total = addition(spent("food"),spent("shopping")) # excluding bills
    amount_spent_li_ot = round(LISTe - expenses_total,2)

    return amount_spent_li_ot

########## Income /exp balance
@amount_retriever
def sale(sale_data='SALE'):
    '''
    Returns benefits of sold shares
    '''

    return sale_data

@amount_retriever
def salary(salary):
    return salary

@amount_retriever
def telecom_spent(telecom):
    return telecom

@amount_retriever
def electricity_spent(electricity):
    return electricity

@amount_retriever
def rent(amount):
    return amount

@amount_retriever
def credit(credit):
    return credit

def addition(*args):
    '''
    Sum of any numbers.
    Especially used to sum expenses.
    '''
    res = 0
    for i in args:
        res += i

    return res

def monthly_spent():
    '''
    return only expenses. Without investment amount.
    others = all PURCHASEd items - (shopping + food)
    '''
    others = spent_liesure_others()
    expenses_total = round(addition(spent("food"),spent("shopping"),others,sum(rent(script.loyer)),sum(telecom_spent(script.telecom)),sum(electricity_spent(script.electricity)),
                                    sum(credit(script.credit))),2)
    income = sum(salary(script.employer)) + sum(sale('SALE'))
    balance = round(income - (-expenses_total),2)
    return income,balance,expenses_total




