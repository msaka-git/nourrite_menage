#!/usr/bin/env python
import logging
import sys
from configparser import ConfigParser
from colored import back, style, fore
import time
import shared_mods.db_ops as dbn
import shared_mods.table_operations as tbops
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from shared_mods.connection_module import conn
from shared_mods.logger_module import logger

#### Setup configparser and config file #############
config = ConfigParser()
config.read('config.ini')
column = config['excel_options']['column']
rowsa = config['excel_options']['rowsa']
credit_card_no = config['personal_data']['credit_card_no']

########## END Configuration ########################

########## LOCAL VARIABLES ##########################
#employer = "CTG LUXEMBOURG"
employer = "PROXIMUS LUXEMBOURG SA"
remobourse_cns = "CNS-MALADIE REMBOURSEMENT"
loyer = "Loyer"
credit = "NISSAN"

########## END Local variables ######################
def print_text(message, fonction=None):
    print("\nAmount spent for {}: ".format(message), fonction)

def print_colorfull(color,message,style_=None,fonction=None):
    colors = { 'green':f"{fore.GREEN}",
               'bold':f"{style.BOLD}",
               'dark_green':f"{fore.DARK_GREEN}",
               'red':f"{fore.RED}"
    }
    if color and style_ == 'BOLD':
        print(colors[color]+colors['bold']+'{}'.format(message),f'{style.RESET}')
    if color and not style_ and not fonction:
        print(colors[color]+'{}'.format(message),f'{style.RESET}')
    if color and fonction:
        print('{}'.format(message)+colors[color],fonction,f"{style.RESET}")

def menu_save(table,*args):
    choice_save = input("\nDo you want to save ? (y/n): ")
    if choice_save == 'y' or choice_save == 'Y':
        dbn.insert_data(table,*args)
    elif choice_save == 'n' or choice_save == 'N':
        print_colorfull('red',"Not saved.")
    else:
        logging.warning("{}: No such option.".format(choice_save))

def db_menu():
    print('Operations are: \n'
          '1.Create table for expense savings\n'
          '2.Create customer table\n'
          '3.Delete table\n'
          '4.Update data\n'
          '5.Back\n')
    ans = input('Answer: ')
    if ans == '1':
        t_name = input("Table to create: ")
        dbn.table_ops(t_name,'create',t_date='Yes')
        print_colorfull('green','Table {} created.'.format('table_'+t_name))
    if ans == '2':
        t_name = input("Table to create: ")
        dbn.table_ops(t_name,'create',t_date='No')
        print_colorfull('green','Table {} created.'.format('table_customer_'+t_name))
    if ans == '3':
        t_name = input("Table to delete: ")
        dbn.table_ops(t_name,'delete')
        print_colorfull('green', 'All tables related to {} deleted'.format(t_name))
    if ans == '4':
        dbn.table_ops(table=None,action='update')
        print_colorfull('green', 'Data updated.')
    if ans == '5':
        mainscript()

def menu_choice(choice_,ch_table):
    '''
    choice: choice of parameters; food, liesure, shopping, all
    '''
    menuChoice = input("Go to customer/provider options? (y/n): ")
    if menuChoice == 'y' or menuChoice == 'Y':
        choice = input("Do you want to see company list? (y/n) : ")
        if choice == 'y' or choice == 'Y':
            print(dbn.sql_queries("{}".format(choice_)))
            dbn.add_delete("{}".format(choice_))

        elif choice == 'n' or choice == 'N':
            dbn.add_delete("{}".format(choice_))

    elif menuChoice == 'n' or menuChoice == 'N':
        print("Calculation will start...")
        time.sleep(5)
        print("\nThe amount that you paid for {} is: ".format(choice_), dbn.spent('{}'.format(choice_)))
        menu_save('{}'.format(ch_table))
        time.sleep(5)
        choice_see_saved = input("Do you want to see previous spendings ? (y/n):")
        if choice_see_saved == 'y' or choice_see_saved == 'Y':
            dbn.see_saved('{}'.format(ch_table))
        else:

            print(f'{fore.GREEN}{style.BOLD}What do you want to do ?{style.RESET}')
    else:
        logger.warning("\n{} : no such option.".format(menuChoice))

class mainscript:
    """ Mainscript to run select window
        And process Actions """

    def root_win(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(title="Select a file !!!")
        return file_path

    def file_select(self, file):
        try:

            bankFile = pd.read_excel(r'{}'.format(file), usecols='{}'.format(column), skiprows=[0,1,2,3,4,5])
            bankFile.dropna(inplace=False)
            pd.set_option('display.max_columns', None)
            pd.set_option('max_rows', None)

            print(file)
            return bankFile
        except FileNotFoundError:
            print("You cancelled the operation")
            sys.exit(0)

    def menu(self):
        choice_table = input("Make your choice food, shopping, all? (food/shopping/all): ")

        if choice_table == 'food' or choice_table == 'FOOD':
            menu_choice('food','food')

        elif choice_table == 'shopping' or choice_table == 'SHOPPING':
            menu_choice('shopping','shopping')

        elif choice_table == 'all' or choice_table == 'ALL':
            print_text('food',dbn.spent('food'))
            menu_save('food')
            print_text('shopping',dbn.spent('shopping'))
            menu_save('shopping')
            print_text('investment',dbn.spent_investment())
            menu_save('investment')
            print_text('Credit card repayment: ',round(dbn.addition(*dbn.amount_catch(credit_card_no)),2))
            menu_save('credit_card')
            print_text('Bills: ',round(dbn.addition(dbn.spent('telecom'),dbn.spent('electricity')))) # telecom + electricty
            menu_save('bills')
            print_text('insurances',dbn.spent('insurance')) # Put a save menu
            menu_save('insurance')
            others = dbn.spent_liesure_others()
            print_text('liesure and others',others)
            menu_save('liesure',others) # positional argument of 'income' parameter. To save the amount 'others' into DB.

        else:
            logger.warning("\n{} : no such option.".format(choice_table))

if __name__ == '__main__':
    sc = mainscript()
    while True:
        print("""
       1.Go to Script
       2.Check saved data
       3.Check income / exp balance
       4.DB operations
       5.Exit/Quit
       """)
        ans = input("What would you like to do? ")
        if ans == "1":
            sc.menu()
        elif ans == "2":
            print_colorfull('dark_green','### Old data for shopping ###',style_='BOLD')
            dbn.see_saved('shopping')
            print(" ")
            print_colorfull('dark_green',"### Old data for food ###", style_='BOLD')
            dbn.see_saved('food')
            print_colorfull('dark_green', '### Old data for investment ###', style_='BOLD')
            dbn.see_saved('investment')
            print(" ")
            print_colorfull('dark_green', '### Old data for insurance ###', style_='BOLD')
            dbn.see_saved('insurance')
            print(" ")
            print_colorfull('dark_green', '### Old data for liesure ###', style_='BOLD')
            dbn.see_saved('liesure')
            print(" ")
        elif ans == "3":
            monthly=dbn.monthly_spent()
            print(f'Income: {fore.GREEN}',monthly[0],f'{style.RESET}'+'-',f'Salary: {fore.GREEN}',sum(dbn.amount_catch(employer)),
                  'Earned amounts: ',*dbn.amount_catch(employer),dbn.rent_income(loyer)[1],f'{style.RESET}')
            print_colorfull('red',"Rent: ",fonction=dbn.rent_income(loyer)[0])
            print(f"Credit Total: {fore.RED} ",round(dbn.addition(*dbn.amount_catch(credit)),2),f'{style.RESET}',
                f'{fore.RED}',*dbn.amount_catch(credit),f'{style.RESET}')
            print(f"Credit Card Repayment: {fore.RED} ", round(dbn.addition(*dbn.amount_catch(credit_card_no)),2),f'{style.RESET}',
                  f'{fore.RED}',*dbn.amount_catch(credit_card_no),f'{style.RESET}')
            print(f"Bills (Telecom + electricity): {fore.RED}", dbn.addition(*dbn.amount_catch(*dbn.sql_queries("telecom")),*dbn.amount_catch(*dbn.sql_queries("electricity")))
                  ,f"{style.RESET}")
            print_colorfull('red',"Insurance: ",fonction=dbn.spent('insurance'))
            print_colorfull('red',"Total Expenses: ",fonction=monthly[2])
            print(f'Balance: {fore.GREEN}',monthly[1] if monthly[1] >= 0 else f'{fore.RED}'"{}".format(monthly[1]),f'{style.RESET}')
            menu_save('balance_yearly',monthly[0],sum(dbn.amount_catch(employer)),dbn.rent_income(loyer)[0],
                      round(dbn.addition(*dbn.amount_catch(credit)),2),round(dbn.addition(*dbn.amount_catch(credit_card_no)),2),
                      round(dbn.addition(dbn.spent('telecom'),dbn.spent('electricity'))),dbn.spent('insurance'),monthly[1],monthly[2])
        elif ans == "4":
            db_menu()
        elif ans == "5":
            print("\n Goodbye")
            conn.close()
            break
        elif ans != "":
            print("\n Not Valid Choice Try again")

    conn.close()

