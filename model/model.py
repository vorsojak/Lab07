import copy

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self.ultima_citta = None
        self.risultato = None
        self.giorno = 1
        self.dati = []
        self._soluzione = []
        self.costo = 0
        self.MeteoDao = MeteoDao

    def umidita_media(self, mese):
        self.MeteoDao.get_all_situazioni(mese)
        return self.MeteoDao.getUmiditaMedia(mese)

    def handle_sequenza(self, mese):
        self.dati = self.MeteoDao.get_all_situazioni(mese)
        res = self.ricorsione(self.giorno, [], self.dati, self.ultima_citta, 0, 0)
        return res

    def ricorsione(self, giorno, parziale, rimanenti, ultima_citta, min_3_gg, max_6_gg):
        if giorno == 16:
            return copy.deepcopy(parziale)
            # pass
        else:
            situazioni_oggi = [s for s in rimanenti if s.data.day == giorno]
            rimanenti_futuri = [s for s in rimanenti if s.data.day > giorno]
            situazioni_oggi.sort(key=lambda x: x.umidita)

            for sit in situazioni_oggi:
                if (
                    ultima_citta is not None
                    and sit.localita != ultima_citta
                    and min_3_gg < 3
                ):
                    continue
                if (
                    ultima_citta is not None
                    and sit.localita == ultima_citta
                    and max_6_gg >= 6
                ):
                    continue
                nuovo_min = (min_3_gg + 1) if sit.localita == ultima_citta else 1
                nuovo_max = (max_6_gg + 1) if sit.localita == ultima_citta else 1

                # ultima_citta = sit.localita
                parziale.append(sit)
                res = self.ricorsione(
                    giorno + 1,
                    parziale,
                    rimanenti_futuri,
                    sit.localita,
                    nuovo_min,
                    nuovo_max,
                )
                if res:
                    return res
                parziale.pop()
