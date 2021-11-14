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
telecom = "ORANGE"
electricity = "SUDSTROUM"
employer = "CTG LUXEMBOURG"
payment = "PAYMENT OF VISA|TRANSFER"
loyer = "Loyer"
credit = "NISSAN"
########## END Local variables ######################
def menu_choice(table):
    choice_save = input("\nDo you want to save ? (y/n): ")
    if choice_save == 'y' or choice_save == 'Y':
        dbn.insert_data(table)
        print("Data has been saved...")
    else:
        pass

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
        bankFile.dropna(inplace=True)
        pd.set_option('display.max_columns', None)
        pd.set_option('max_rows', None)
        print(file)
        return bankFile

    def menu(self):
        choice_table = input("Make your choice food, shopping, liesure? (food/shopping/liesure/all): ")

        if choice_table == 'food' or choice_table == 'FOOD':
            menuChoice = input("Go to customer/provider options? (y/n): ")
            if menuChoice == 'y' or menuChoice == 'Y':
                choice = input("Do you want to see company list? (y/n) : ")
                if choice == 'y' or choice == 'Y':
                    print(dbn.sql_queries("food"))
                    dbn.add_delete("food")

                elif choice == 'n' or choice == 'N':
                    dbn.add_delete("food")

            elif menuChoice == 'n' or menuChoice == 'N':
                print("Calculation will start...")
                time.sleep(5)
                print("\nThe amount that you paid for food is: ", dbn.spent('food'))
                menu_choice('nourriture')
                time.sleep(5)
                choice_see_saved = input("Do you want to see previous spendings ? (y/n):")
                if choice_see_saved == 'y' or choice_see_saved == 'Y':
                    dbn.see_saved('nourriture')
                else:

                    print(f'{fore.GREEN}{style.BOLD}What do you want to do ?{style.RESET}')

            else:
                print(" ")

        ##### MENU FOR SHOPPING #####################
        elif choice_table == 'shopping' or choice_table == 'SHOPPING':
            menuChoice = input("Go to customer/provider options? (y/n): ")
            if menuChoice == 'y' or menuChoice == 'Y':
                choice = input("Do you want to see company list? (y/n) : ")
                if choice == 'y' or choice == 'Y':
                    print(dbn.sql_queries("shopping"))
                    dbn.add_delete("shopping")
                elif choice == 'n' or choice == 'N':
                    dbn.add_delete("shopping")


            elif menuChoice == 'n' or menuChoice == 'N':
                print("Calculation will start...")
                time.sleep(5)
                print("\nThe amount that you paid for shopping is: ", dbn.spent('shopping'))
                menu_choice('shopping')
                time.sleep(5)
                choice_see_saved = input("Do you want to see previous spendigns ? (y/n):")
                if choice_see_saved == 'y' or choice_see_saved == 'Y':
                    dbn.see_saved('shopping')
                else:
                    print(f'{fore.GREEN}{style.BOLD}What do you want to do ?{style.RESET}')

            else:
                print(" ")
                logger.warning("{} : no such option.".format(menuChoice))

        ###### MENU FOR LIESURE #######
        ## TO ADD
        ###############################
        elif choice_table == 'all' or choice_table == 'ALL':
            print("\nThe amount that you paid for food is: ", dbn.spent('food'))
            menu_choice('food')
            print("\nThe amount that you paid for shopping is: ", dbn.spent('shopping'))
            menu_choice('shopping')
            others = dbn.spent_liesure_others()
            print("\nThe amount spent in investment: ", dbn.spent_investment())
            menu_choice('investment')
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
            print(f'Income: {fore.GREEN}',monthly[0],f'{style.RESET}'+'-',f'Salary: {fore.GREEN}',*dbn.salary(employer),f'{style.RESET}')
            print(f"Rent: {fore.RED} ", *dbn.rent(loyer),f'{style.RESET}')
            print(f"Credit: {fore.RED} ", *dbn.credit(credit),f'{style.RESET}')
            print(f"Bills (Telecom + electricity): {fore.RED}", dbn.addition(*dbn.telecom_spent(telecom),*dbn.electricity_spent(electricity)),f"{style.RESET}")
            print(f"Total Expenses: {fore.RED}",monthly[2],f"{style.RESET}")
            print(f'Balance: {fore.GREEN}',monthly[1] if monthly[1] >= 0 else f'Balance: {fore.RED}',f'{style.RESET}')
        elif ans == "4":
            print("\n Goodbye")
            conn.close()
            break
        elif ans != "":
            print("\n Not Valid Choice Try again")

    conn.close()

