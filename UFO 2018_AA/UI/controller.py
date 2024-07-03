import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    # def fillDD(self):
    #     for year in range(1910,2015):
    #         self._view.ddyear.options.append(ft.dropdown.Option(year))
    #
    #     forme = self._model.shapes
    #     for shape in forme:
    #          self._view.ddshape.options.append(ft.dropdown.Option(shape))
    #
    #     self._view.update_page()


    def handle_selezione(self, e):
        anno = self._view._txtAnno.value
        if anno =="" or anno == None:
            return self._view.create_alert("INSERIRE UN ANNO")
        anno = int(self._view._txtAnno.value)
        if anno<1904 or anno >2014:
            return self._view.create_alert("ANNO DEVE ESSERE COMPRESO TRA 1910 E 2014")

        forme= self._model.fillDD(anno)
        for f in forme:
            self._view.ddshape.options.append(ft.dropdown.Option(f))

        self._view.update_page()



    def handle_graph(self, e):
        if self._view.ddshape.value == "" or self._view.ddshape.value == None:
            return self._view.create_alert("ERRORE SELEZIONARE UNA FORMA")
        anno = int(self._view._txtAnno.value)
        forma = self._view.ddshape.value
        self._model.buildGraph(anno,forma)
        nodi, archi = self._model.graphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"GRAFO CREATO CORRETTAMENTE CON {nodi} NODI E {archi} ARCHI "))

        lista = self._model.adiacenze()
        for ee in lista:
            self._view.txt_result.controls.append(ft.Text(f"{ee[0].Name}--con somma {ee[1]}"))

        self._view.update_page()

    def handle_path(self,e):
        percorso,distanza = self._model.getPath()
        self._view.txt_result.controls.append(ft.Text(f"DISTANZA MASSIMA: {distanza}"))
        for p in range(0,len(percorso)-1):
            self._view.txt_result.controls.append(ft.Text(f"Arco tra {percorso[p]} e {percorso[p+1]} con distanza {self._model.distanzaGeo(percorso[p],percorso[p+1])}"))

        self._view.update_page()



