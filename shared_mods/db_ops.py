import script
from shared_mods.connection_module import conn,cur
from shared_mods.logger_module import logger
from shared_mods.table_operations import update
import re
from script import mainscript

ins=mainscript()

f=ins.root_win()
bankFile=ins.file_select(f)

dt = bankFile["Value Date"].tail(1)
data = bankFile.sort_values("Operation")

## SQL QUERIES FOR CUSTOMERS OR PROVIDERS + SQL requests ##
def sql_queries(object_):
    '''
    To see customers inside t_customer column of table_customer
    object = FOOD or SHOPPING or INVESTMENT
    '''

    sql_sub = "select t_customer from table_customer_{}".format(object_)
    sub_check = cur.execute(sql_sub)
    sub_fetch = sub_check.fetchall()
    sub_list = [list(i) for i in sub_fetch]
    sub = []
    for a in sub_list:
        for b in a:
            sub.append(b.lower()) # converts provider name from database to lower case.
    return sub

def insert_data(table,income=None,salary=None,rent=None,credit=None,credit_card=None,bills=None,insurance=None,
                balance=None,total_expense=None,investment=None):

    sql1="insert into table_{} values(NULL,'{}','{}')"
    for a in dt:
        query = "select count(*) from table_{} where t_date='{}' and t_spent='{}'".format(table,a,amountTotal)
        res_data = cur.execute(query)
        res = [i for i in res_data.fetchall()[0]]
        if res[0] >= 1:
            print("Data already exist in DB")
        else:
            if table == 'balance_yearly':
                sql_balance = "insert into table_{} values(NULL,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"\
                    .format(table,a,income,salary,rent,credit,credit_card,bills,insurance,total_expense,investment,balance)
                cur.execute(sql_balance)
            elif table == 'bills':
                sql1=sql1.format(table,a,
                            round(addition(spent('telecom'),spent('electricity'))))
                cur.execute(sql1)
            elif table == 'credit_card':
                sql1 = sql1.format(table,a,
                                   round(addition(*amount_catch(script.credit_card_no)),2))
                cur.execute(sql1)
            else:
                sql1 = sql1.format(table,a, income if table == 'liesure' else amountTotal)
                cur.execute(sql1)
            print("Data has been saved...")
            conn.commit()

def table_ops(table,action,t_date=None):
    '''
    table: from script.py
    req[0-2] returns query statements.
    '''
    if action.lower() == 'create':
        req = update('create',table=table)
        req_ = req.tables()
        if t_date.lower() == 'yes':
            cur.execute(req_[0])
        else:
            cur.execute(req_[1])
    if action.lower() == 'delete':
        req = update('delete', table=table)
        req_ = req.tables()
        for i in req_[2]:
            delete_statement = "drop table if exists {}".format(i)
            cur.execute(delete_statement)
    if action.lower() == 'update':
        req = update('delete', table=table)
        req.questions()
        update_query = req.find_id()
        query = cur.execute(update_query)
        update_id = [i for i in query.fetchall()[0]] # update_id[0] gives id_table number.
        update_statement = req.data_update(id_table=update_id[0])
        cur.execute(update_statement)
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

def amount_retriever(func):
    '''
    Retrieve the amount of a given row.
    Ex: you want to retrieve the amount of 'orange' telecom expense.
    islem[0] = 'Operation', islem[1]='SALE', fetch all amounts under Operation column having SALE pattern in rows.
    '''

    def wrapper(*args):
        islem = func(*args)
        #print("islem 0: ",islem[0])
        #print("islem 1: ", islem[1])
        expense_data = data[data['{}'.format(islem[0])].str.contains(islem[1],flags=re.IGNORECASE, na=False,regex=True)]
        expense_amount = [float(i) for i in expense_data['Amount']]
        return expense_amount
    return wrapper

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
    Object must be food, shopping, liesure or all.
    Telecom and others expenses can be calculated as well.
    Ex: spent("telecom"), will calculate telecom expenses according to existing customers in DB, related customer table.
    Value or pattern must be present in DB
    '''

    LIST = []

    for i in sql_queries(object_):
        operation_Name = data[data['Operation'].str.contains(i,flags=re.IGNORECASE)] # flags= ignore case sensitivity in excel file.
        #print("operation name: ",operation_Name)
        amounts = operation_Name["Amount"]

        for row in amounts:
            LIST.append(row)


    global amountTotal
    amountTotal = round(sum(LIST), 2)
    return amountTotal

##### Liesure and others #################

def all_purchases():
    '''
    Total purchased amounts

    '''
    value_all = ['PURCHASE']
    LISTe = float(0)  # all amount was spent

    for i in value_all:
        all_spent_amounts = data[data['Operation'].str.contains(i, flags=re.IGNORECASE)]
        LISTe = round(sum(all_spent_amounts['Amount']),2)  # All purchases, "purchased tag in excel file"
    #print(LISTe)
    return LISTe

def sp_liesure():
    spent_liesure = spent('liesure')
    #print(spent_liesure)
    return spent_liesure

def sp_food():
    spent_food = spent('food')
    #print(spent_food)
    return spent_food

def sp_shopping():
    spent_shopping = spent('shopping')
    #print(spent_shopping)
    return spent_shopping

def sp_telecom():
    '''
    Spent for fix internet and mobile lines

    '''
    spent_telecom = spent('telecom')
    #print(spent_telecom)
    return spent_telecom

def sp_electricty():
    spent_electricity = spent('electricity')
    #print(spent_electricity)
    return spent_electricity

def sp_insurance():
    spent_insurance = spent('insurance')
    #print(spent_insurance)
    return spent_insurance

def sp_investment():
    """
    sql_spent calculates iNG ARIA funds. String Returned from DB.
    sql_investment_other is any other investments such as bought shares in stock exchange.
    """
    sql_spent = spent('investment')
    spent_investment_other = sum(sale('purchase\s.*[^ARIA]\sW[0-9]{10}$'))
    res = sql_spent + spent_investment_other
    return res

def sp_atm_withdrawls():
    spent_withdrawls = amount_pattern('WITHDRAWAL')
    #print(sum(spent_withdrawls))
    return sum(spent_withdrawls)

def sp_others():
    '''

    :return: Other amounts inside purchases, not included yet in DB
    '''
    all_purchase = all_purchases()
    food = sp_food()
    shopping = sp_shopping()
    liesure = sp_liesure()
    spent_all = addition(food,shopping,liesure)
    spent_others = round(addition(-all_purchase,spent_all),2) # - at the beginin is to convert negaitve amount to positive.
    return -spent_others,all_purchase,food,liesure,spent_all # returning with - at the begining o mark it's an expense. Other values are used in all_expenses function.

def sp_credit():
    spent_credit = sum(amount_catch(script.credit))
    return spent_credit

def sp_credit_card():
    spent_credit_card = sum(amount_catch(script.credit_card_no))
    return spent_credit_card

def all_expenses():
    '''

    :return: All expenses; purchases, bills, rents, investment, credits, credit cards etc.
    '''
    expenses = addition(sp_others()[4],sp_others()[0]) # Expenses food, shopping,liesure, others
    expenses_total = addition(expenses,rent_income(script.loyer)[0],sp_investment(),sp_telecom(),sp_electricty(),sp_insurance(),sp_atm_withdrawls(),
                              sp_credit(),sp_credit_card())
    #print(expenses_total)
    return expenses_total

########## Income /exp balance
@amount_retriever
def amount_pattern(pattern):
    '''

    :param pattern: Anything yoy want to search under operations column
    :return: operation name, amount
    '''
    res = 'Operation'
    return res, pattern
@amount_retriever
def sale(sale_data='SALE'):
    '''
    Returns benefits of sold shares
    '''
    res = 'Operation'
    return res,sale_data

@amount_retriever
def amount_catch(item_):
    if item_ == script.credit_card_no:
        res = 'Beneficiary Account'
    else:
        res = 'Operation'
    return res,item_

def rent_income(item_):
     if item_ == script.loyer:
         rent=data[data['Operation'].str.contains('Loyer .*charges',flags=re.IGNORECASE,regex=True)]
         state_help=data[data['Operation'].str.contains("European Transfer TRESORERIE DE L'ETAT.*",flags=re.IGNORECASE,regex=True)]
         res_rent=addition(sum(rent['Amount']))
         res_help_state=addition(sum(state_help['Amount']))
         return res_rent,res_help_state

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
    income = sum(amount_catch(script.employer)) + sum(sale('SALE')) + rent_income(script.loyer)[1] + sum(amount_catch(script.remobourse_cns))
    income = round(income,2)
    balance = round(income - (-all_expenses()),2) # all_expenses has - to convert negative value to positive.

    return income,balance

