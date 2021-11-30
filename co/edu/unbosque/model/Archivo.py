import psycopg2
from pyjavaproperties import Properties

class Archivo:
    def __init__(self):
        self.p = Properties()
        self.p.load(open('C:/Users/jvtp0/PycharmProjects/ClinicaVeterinariaMVC/Data/CaracteristicaBases.properties'))

    def realizarSQL(self, sql):
        all_values = ""
        try:
            connection = psycopg2.connect(
                host=self.p.getProperty("host"),
                user=self.p.getProperty("user"),
                password=self.p.getProperty("password"),
                database=self.p.getProperty("database")
            )
            cursor = connection.cursor()
            cursor.execute(sql)

            all_values = cursor.fetchall()
            cursor.close()
            connection.close()
        except Exception as e:
            print(e)
            all_values = "Ocurrio un error"
        return all_values

    def realizarInsertSQL(self, sql):
        all_values = "OK"
        try:
            connection = psycopg2.connect(
                host=self.p.getProperty("host"),
                user=self.p.getProperty("user"),
                password=self.p.getProperty("password"),
                database=self.p.getProperty("database")
            )
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            print(e)
            all_values = ["Ocurrio un error",e]
        return all_values
