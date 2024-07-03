from database.DB_connect import DBConnect
from model.stato import Stato


class DAO():

    @staticmethod
    def getShape(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct shape
                from sighting s 
                where year(s.`datetime`)=%s
                order by s.shape 
                """

        cursor.execute(query,(anno,))

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getStates():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select s.*
                from state s
                    """

        cursor.execute(query,)

        for row in cursor:
            result.append(Stato(**row))

        cursor.close()
        conn.close()
        return result



    @staticmethod
    def getNeighbors():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select n.*
                from neighbor n  """

        cursor.execute(query, )

        for row in cursor:
            result.append((row["state1"],row["state2"]))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getPeso(uid,vid,anno,forma):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select count(s.id) as peso
                from sighting s
                where(s.state = %s or s.state = %s) and year(s.`datetime`) = %s and s.shape = %s"""

        cursor.execute(query,(uid.lower(),vid.lower(),anno,forma,) )

        for row in cursor:
            result.append(row["peso"])

        cursor.close()
        conn.close()
        return result
