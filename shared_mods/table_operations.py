class update:
    def __init__(self,action,table=None,t_date=None,column=None,ex_data=None,ch_data=None):
        self.table = table
        self.action = action
        self.t_date = t_date
        self.column = column
        self.ex_data = ex_data
        self.ch_data = ch_data

    def questions(self):
        self.table = input("Please choose table: ")
        self.column = input("Please choose column to change: ")
        self.ex_data = input("Existing data: ")
        self.ch_data = input("Value to change: ")
        return self.table,self.column, self.ex_data,self.ch_data

    def find_id(self):
        if 'customer' in self.table:
            query = "select id_customer from table_{} where t_{} like '{}'".format(self.table,self.column,self.ex_data)
        else:
            query = "select id_table from table_{} where t_{} = {}".format(self.table,self.column,self.ex_data)
        return query

    def data_update(self,id_table=None):
        if 'customer' in self.table:
            query_update = "update table_{} set t_{} = '{}' where id_customer = {}".format(self.table,self.column,self.ch_data,id_table)
        else:
            query_update = "update table_{} set t_{} = {} where id_table = {}".format(self.table,self.column,self.ch_data,id_table)
        return query_update

    def tables(self):
        crt_statment_tdate = "create table '{}' ('id_table' INTEGER NOT NULL UNIQUE," \
                       "'t_date' NUMERIC NOT NULL," \
                       "'t_spent' NUMERIC NOT NULL, PRIMARY KEY('id_table' AUTOINCREMENT))".format('table_'+self.table)
        crt_cust_statment = "create table '{}' ('id_customer' INTEGER NOT NULL UNIQUE," \
                            "'t_customer' TEXT UNIQUE, PRIMARY KEY('id_customer' AUTOINCREMENT))".format('table_customer_'+self.table)
        table_names_delete = ['table_{}'.format(self.table),'table_{}_{}'.format('customer',self.table)]
        return crt_statment_tdate, crt_cust_statment, table_names_delete
