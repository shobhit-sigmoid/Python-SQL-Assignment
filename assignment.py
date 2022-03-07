import pandas as pd
import logging
from connection import create_connection

logging.basicConfig(filename='logs.log', level=logging.INFO,
                    format='%(asctime)s: %(levelname)s --> %(funcName)s() --> %(message)s')

user = "shobhitchaurasiya"
database = "postgres"
password = "none"
host = "localhost"
port = "5432"


class Employee:
    def __init__(self):
        pass

    # Query-1
    def list_of_employees(self):
        connection = create_connection.get_connection(self, database=database, user=user, password=password,
                                                      host=host, port=port)
        cur = connection.cursor()
        data = cur.execute(
            "SELECT t1.empno as EmployeeNumber, t1.ename as EmployeeName, t2.ename as Manager FROM emp t1, "
            "emp t2 WHERE t1.mgr=t2.empno;")
        rows = cur.fetchall()
        EMP_Number, Name, Manager = ([] for i in range(3))

        for row in rows:
            temp_list = list(row)
            EMP_Number.append(temp_list[0])
            Name.append(temp_list[1])
            Manager.append(temp_list[2])

        df = pd.DataFrame({'EMP_Number': EMP_Number, 'Name': Name, 'Manager': Manager})
        print(df.head())
        final_data = pd.ExcelWriter('ques1.xlsx')
        df.to_excel(final_data, sheet_name='ques1', index=False)
        final_data.save()
        connection.close()
        logging.info("Connection Close")

    # Query-2

    def total_compensation(self):
        connection = create_connection.get_connection(self, database=database, user=user, password=password,
                                                      host=host, port=port)
        cur = connection.cursor()
        cur.execute("UPDATE jobhist SET enddate=CURRENT_DATE WHERE enddate IS NULL;")
        data = cur.execute(
            "SELECT emp.ename, "
            "jh.empno, dept.dname, jh.deptno, "
            "ROUND((jh.enddate-jh.startdate)/30*jh.sal,0) "
            "AS total_compensation, ROUND((jh.enddate-jh.startdate)/30,0) as months_spent FROM "
            "jobhist as jh INNER JOIN dept ON jh.deptno=dept.deptno INNER JOIN emp ON jh.empno=emp.empno;")
        rows = cur.fetchall()
        Employee_Name, Employee_No, Dept_Name, Dept_Number, Dept_Number, Total_Compensation, Months_Spent = ([] for i in
                                                                                                             range(7))

        for row in rows:
            temp_list = list(row)
            Employee_Name.append(temp_list[0])
            Employee_No.append(temp_list[1])
            Dept_Name.append(temp_list[2])
            Dept_Number.append(temp_list[3])
            Total_Compensation.append(temp_list[4])
            Months_Spent.append(temp_list[5])
        df = pd.DataFrame(
            {'Employee_Name': Employee_Name, 'Employee_No': Employee_No, 'Dept_Name': Dept_Name,
             'Dept_Number': Dept_Number, 'Total_Compensation': Total_Compensation, 'Months_Spent': Months_Spent})
        print("\n\n", df.head())
        writer = pd.ExcelWriter('ques2.xlsx')
        df.to_excel(writer, sheet_name='Q2', index=False)
        writer.save()
        connection.close()
        logging.info("Connection Close")

    # Query-3
    def file_to_query(self, data, file):
        engine = create_connection.get_engine(self, user=user, password=password, host=host,
                                              port=port, database=database)
        try:
            if data == 'Q2':
                df = pd.read_excel(file, 'Q2')
                df.to_sql(name='total_compensation', con=engine, if_exists='append', index=False)
        except:
            logging.info("Query Execution Unsuccessful")
        finally:
            logging.info("Table Creation Successful.")

    def file_to_table(self):
        with pd.ExcelFile('ques2.xlsx') as xls1:
            for sheet_name in xls1.sheet_names:
                obj.file_to_query(sheet_name, xls1)

    # Query-4
    def read_sheets(self, data, file):
        try:
            if data == 'Q2':
                df = pd.read_excel(file, 'Q2')
                print("\n\n", df.head())
                return df
        except:
            logging.info("Execution Unsuccessful")
        finally:
            logging.info("Execution Successful.")

    def compensation_at_dept_level(self):
        with pd.ExcelFile('ques2.xlsx') as xls2:
            for sheet_name in xls2.sheet_names:
                new_df = obj.read_sheets(sheet_name, xls2)

        temp1_df = new_df.groupby(['Dept_Name', 'Dept_Number']).agg(
            Total_Compensation=pd.NamedAgg(column='Total_Compensation', aggfunc="sum")).reset_index()

        final_data = pd.ExcelWriter('ques4.xlsx')
        temp1_df.to_excel(final_data, sheet_name='Excel_file_Q4', index=False)
        final_data.save()


obj = Employee()
# q1
obj.list_of_employees()
# q2
obj.total_compensation()
# q3
obj.file_to_table()
# q4
obj.compensation_at_dept_level()
