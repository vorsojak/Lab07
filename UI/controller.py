import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view._lvout.controls.clear()
        if self._mese == 0:
            self._view._lvout.controls.append(
                ft.Text("Attenzione! Seleziona un mese", color="red")
            )
            self._view.update_page()
            return
        output = self._model.umidita_media(self._mese)
        self._view._lvout.controls.append(
            ft.Text("L'umidità media nel mese selezionato è:")
        )
        for citta, valore in output:
            self._view._lvout.controls.append(ft.Text(f"{citta}: {valore}"))
        self._view.update_page()

    def handle_sequenza(self, e):
        self._view._lvout.controls.clear()
        if self._mese == 0:
            self._view._lvout.controls.append(
                ft.Text("Attenzione! Seleziona un mese", color="red")
            )
            self._view.update_page()
            return
        output = self._model.handle_sequenza(self._mese)
        costo_tot = sum(s.umidita for s in output)
        self._view._lvout.controls.append(
            ft.Text(f"La sequenza ottima ha costo {costo_tot} ed è:")
        )
        for s in output:
            self._view._lvout.controls.append(ft.Text(s))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)
