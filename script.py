#!/usr/bin/env python
from configparser import ConfigParser
from colored import back, style, fore
import time
import shared_mods.db_ops as dbn
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
########## END Configuration ########################

########## LOCAL VARIABLES ##########################
employer = "CTG LUXEMBOURG"
loyer = "Loyer"
credit = "NISSAN"
credit_card_no = "LU030141471040210000"
########## END Local variables ######################

def menu_save(table):
    choice_save = input("\nDo you want to save ? (y/n): ")
    if choice_save == 'y' or choice_save == 'Y':
        dbn.insert_data(table)
    else:
        pass

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
        #menu_save('nourriture')
        menu_save('{}'.format(ch_table))
        time.sleep(5)
        choice_see_saved = input("Do you want to see previous spendings ? (y/n):")
        if choice_see_saved == 'y' or choice_see_saved == 'Y':
            #dbn.see_saved('nourriture')
            dbn.see_saved('{}'.format(ch_table))
        else:

            print(f'{fore.GREEN}{style.BOLD}What do you want to do ?{style.RESET}')
    else:
        print(" ")
        logger.warning("{} : no such option.".format(menuChoice))

class mainscript:
    """ Mainscript to run select window
        And process Actions """

    def root_win(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(title="Select a file !!!")
        return file_path

    def file_select(self, file):
        bankFile = pd.read_excel(r'{}'.format(file), usecols='{}'.format(column), skiprows=[0,1,2,3,4,5])
        bankFile.dropna(inplace=False)
        pd.set_option('display.max_columns', None)
        pd.set_option('max_rows', None)

        print(file)
        return bankFile

    def menu(self):
        choice_table = input("Make your choice food, shopping, liesure? (food/shopping/liesure/all): ")

        if choice_table == 'food' or choice_table == 'FOOD':
            menu_choice('food','nourriture')

        ##### MENU FOR SHOPPING #####################
        elif choice_table == 'shopping' or choice_table == 'SHOPPING':
            menu_choice('shopping','shopping')

        ###### MENU FOR LIESURE #######
        ## TO ADD
        ###############################
        elif choice_table == 'all' or choice_table == 'ALL':
            print("\nThe amount that you paid for food is: ", dbn.spent('food'))
            menu_save('food')
            print("\nThe amount that you paid for shopping is: ", dbn.spent('shopping'))
            menu_save('shopping')
            others = dbn.spent_liesure_others()
            print("\nThe amount spent in investment: ", dbn.spent_investment())
            menu_save('investment')
            print("\nThe amount that you paid for liesure and others is: ", others)

        else:
            print("There is no such option...")


if __name__ == '__main__':
    sc = mainscript()
    while True:
        print("""
       1.Go to Script
       2.Check saved data
       3.Check income / exp balance
       4.Exit/Quit
       """)
        ans = input("What would you like to do? ")
        if ans == "1":
            sc.menu()
        elif ans == "2":
            print(f'{fore.DARK_GREEN}{style.BOLD}### Old data for shopping ###{style.RESET}')
            dbn.see_saved('shopping')
            print(" ")
            print(f'{fore.DARK_GREEN}{style.BOLD}### Old data for food ###{style.RESET}')
            dbn.see_saved('nourriture')
        elif ans == "3":
            monthly=dbn.monthly_spent()
            print(f'Income: {fore.GREEN}',monthly[0],f'{style.RESET}'+'-',f'Salary: {fore.GREEN}',*dbn.amount_catch(employer),dbn.rent_income(loyer)[1],f'{style.RESET}')
            print(f"Rent: {fore.RED} ", dbn.rent_income(loyer)[0],f'{style.RESET}')
            print(f"Credit: {fore.RED} ", *dbn.amount_catch(credit),f'{style.RESET}')
            print(f"Credit Card Repayment: {fore.RED} ", *dbn.amount_catch(credit_card_no),f'{style.RESET}')
            print(f"Bills (Telecom + electricity): {fore.RED}", dbn.addition(*dbn.amount_catch(*dbn.sql_queries("telecom")),*dbn.amount_catch(*dbn.sql_queries("electricity")))
                  ,f"{style.RESET}")
            print(f"Total Expenses: {fore.RED}",monthly[2],f"{style.RESET}")
            print(f'Balance: {fore.GREEN}',monthly[1] if monthly[1] >= 0 else f'Balance: {fore.RED}',f'{style.RESET}')
        elif ans == "4":
            print("\n Goodbye")
            conn.close()
            break
        elif ans != "":
            print("\n Not Valid Choice Try again")

    conn.close()

