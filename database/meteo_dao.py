from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao:
    @staticmethod
    def get_all_situazioni(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s
                        where month(Data) = %s
                        ORDER BY s.Data ASC"""
            cursor.execute(query, (mese,))
            for row in cursor:
                result.append(Situazione(row["Localita"], row["Data"], row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    @classmethod
    def getUmiditaMedia(cls, mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """select Localita, (sum(Umidita) / count(Umidita)) as umiditaMedia
                        from situazione s 
                        where month(Data) = %s
                        group by Localita"""
            cursor.execute(query, (mese,))
            for row in cursor:
                result.append(row)
            cursor.close()
            cnx.close()
        return result
