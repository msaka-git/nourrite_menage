import datetime
import pandas as pd
import sqlite3
from sqlite3 import Error
import time
import tkinter as tk
from tkinter import filedialog
import logging

root=tk.Tk()

root.withdraw()

file_path = filedialog.askopenfilename(title="Select a file !!")

print(file_path)

bankFile=pd.read_excel(r'{}'.format(file_path),usecols='C,E,G',skiprows=[0,1,2,3,4,5])
bankFile.dropna(inplace=True)
pd.set_option('display.max_columns',None)

pd.set_option('max_rows',None)



""" create a database connection to a SQLite database """
conn = None
try:
    conn = sqlite3.connect("database.db")

except Error as e:
    print(e)
cur=conn.cursor()


sql_sub="select t_customer from table_customer"
sub_check=conn.execute(sql_sub)

sub_fetch=sub_check.fetchall()

sub_list=[list(i) for i in sub_fetch]
sub=[]
for a in sub_list:

    for b in a:

        sub.append(b)

###### LOGGING CONSTRUCTOR #####################
logger = logging.getLogger()

#############################################


def insert_data():

    dt = bankFile["Value Date"].tail(1)

    for a in dt:
        sql1="insert into table_nourriture values(NULL,'{}','{}')".format(a,amountTotal)

        cur.execute(sql1)
        conn.commit()

def insert_customer():
    sql2="insert into table_customer values(NULL,'{}')".format(sub_input)
    conn.execute(sql2)
    conn.commit()

def delete_customer():
    sql3="delete from table_customer where t_customer = '{}'".format(choice_del)
    conn.execute(sql3)
    conn.commit()

def see_saved():
    sql4="select t_date,t_spent from table_nourriture"
    data=conn.execute(sql4)
    for i in data.fetchall():

        print(', '.join(map(str,i)))


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
        logger.warning("Islem bulunamadi. Cikis yapiliyor...")

def spent():



    data=bankFile.sort_values("Operation")
    LIST=[]



    for i in sub:
        operation_Name=data[data['Operation'].str.contains(i)]
        amounts=operation_Name["Amount"]


        for row in amounts:
            LIST.append(row)

    global amountTotal
    amountTotal=round(sum(LIST),2)
    print("\nThe amount that you paid for food is: ",amountTotal)


    choice_save=input("\nDo you want to save ? (y/n): ")
    if choice_save == 'y' or choice_save == 'Y':
        insert_data()
        print("Data has been saved...")
    else:
        pass


def menu():
    menuChoice=input("Go to customer/provider options? (y/n): ")
    if menuChoice == 'y' or menuChoice == 'Y':
        choice = input("Do you want to see company list? (y/n) : ")
        if choice == 'y' or choice == 'Y':
            print(sub)
            add_delete()

        elif choice == 'n' or choice == 'N':
            add_delete()



    elif menuChoice == 'n' or menuChoice == 'N':
        print("Calculation will start...")
        time.sleep(5)
        spent()
        time.sleep(5)
        choice_see_saved=input("Do you want to see previous spendigns ? (y/n):")
        if choice_see_saved == 'y' or choice_see_saved =='Y':
            see_saved()
        else:
            exit(0)






if __name__ == '__main__':
    menu()

    conn.close()

