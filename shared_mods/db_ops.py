
from shared_mods.connection_module import conn,cur
from script import mainscript
from shared_mods.logger_module import logger

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
        sub.append(b)

## SQL QUERIES FOR SHOPPING ##

sql_sub_sh = "select t_customer from table_customer_shopping"

sub_check_sh = cur.execute(sql_sub_sh)

sub_fetch_sh = sub_check_sh.fetchall()

sub_list_sh = [list(i) for i in sub_fetch_sh]
sub_sh = []
for a in sub_list_sh:

    for b in a:
        sub_sh.append(b)



def insert_data():

    dt = bankFile["Value Date"].tail(1)

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

    data = bankFile.sort_values("Operation")
    LIST = []

    for i in sub:
        operation_Name = data[data['Operation'].str.contains(i)]
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


#### SHOPPING FUNCTIONS ###################



def insert_data_shopping():

    dt = bankFile["Value Date"].tail(1)

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

    data = bankFile.sort_values("Operation")
    LIST = []

    for i in sub_sh:
        operation_Name = data[data['Operation'].str.contains(i)]
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

##### Liesure and others #################

def spent_liesure_others():
    value_all=['PURCHASE']


    data = bankFile.sort_values("Operation")
    LISTe = []

    for imm in value_all:
        operation_Namer = data[data['Operation'].str.contains(imm)]
        amounts = operation_Namer["Amount"]

        for row in amounts:

            LISTe.append(row)

    global amountTotal_all
    amountTotal_all=round(sum(LISTe),2)


    amount_spent_lieure_other=(-(amountTotal_all-amountTotal_shopping-amountTotal_food))
    print("\nThe amount that you paid for liesure and others is: ", -amount_spent_lieure_other)


