from configparser import ConfigParser
import time
import logging
import db_nourriture as dbn

#### Setup configparser and config file #############
config=ConfigParser()
config.read('config.ini')
column=config['excel_options']['column']
rowsa=config['excel_options']['rowsa']
DBfile=config['db_file']['file']

########## END Configuration ########################


###### LOGGING CONSTRUCTOR #####################
logger = logging.getLogger()

#############################################


class mainscript:


    def menu(self):
        menuChoice=input("Go to customer/provider options? (y/n): ")
        if menuChoice == 'y' or menuChoice == 'Y':
            choice = input("Do you want to see company list? (y/n) : ")
            if choice == 'y' or choice == 'Y':
                print(dbn.sub)
                dbn.add_delete()

            elif choice == 'n' or choice == 'N':
                dbn.add_delete()



        elif menuChoice == 'n' or menuChoice == 'N':
            print("Calculation will start...")
            time.sleep(5)
            dbn.spent()
            time.sleep(5)
            choice_see_saved=input("Do you want to see previous spendigns ? (y/n):")
            if choice_see_saved == 'y' or choice_see_saved =='Y':
                dbn.see_saved()
            else:
                exit(0)



if __name__ == '__main__':

    sc=mainscript()

    sc.menu()
    dbn.conn.close()


