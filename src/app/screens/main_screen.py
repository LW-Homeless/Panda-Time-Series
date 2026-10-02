from math import ceil

from textual.widgets import Footer, Header
from textual.screen import Screen
from textual.containers import Horizontal, Vertical, Grid, ScrollableContainer

from src.app.widgets.custom_info_panel import CustomInfoPanel
from src.app.widgets.custom_panel_chart import CustomPanelChart
from src.app.widgets.custom_loading_indicator import CustomLoadingIndicator
from src.app.widgets.custom_data_table import CustomDataTable

from src.core.process_data import ProcessData


class MainScreen(Screen):
    BINDINGS = [
        ("q", "quit", "Cerrar Applicación")
    ]

    def __init__(self):
        super().__init__()

        self.title = "Análisis Ventas NSA x Año"
        self.__data = None

    def compose(self):
        yield Header()
        with Horizontal(id="main_layout"):
            with Vertical(id="left-panel"):
                yield CustomInfoPanel("Datos Originales", id="panel-data")
                yield CustomInfoPanel("Diferencia ventas x año", id="panel-sales-diff")
                yield CustomInfoPanel("Diferencia Porcentual x año", id="panel-percent-diff")
                yield CustomInfoPanel("Media movil", id="panel-media-movil")
            with Grid(id="charts-container"):
                yield CustomPanelChart(id="panel-chart-1")
                yield CustomPanelChart(id="panel-chart-2")
                yield CustomPanelChart(id="panel-chart-3")
                yield CustomPanelChart(id="panel-chart-4")
                yield CustomPanelChart(id="panel-chart-5")
        yield Footer()

    def on_mount(self):
        # Cargo en cada CustomInfoPanel y CustomPanelChart un widget LoadingIndicator.
        for panel in self.query_one("#left-panel", Vertical).query_children(CustomInfoPanel):
            panel.show_widget(CustomLoadingIndicator())

        for chart_panel in self.query_one("#charts-container", Grid).query_children(CustomPanelChart):
            chart_panel.show_widget(CustomLoadingIndicator())

        # cargar los diferente indicadores en los paneles de informacion CustomInfoPanel

        self.__data = ProcessData().get_indicator()
        self.__data.index = self.__data.index.strftime("%Y-%m-%d")
        self.load_data_panel_data(self.__data)

    def load_data_panel_data(self, data):

        self.query_one("#panel-data", CustomInfoPanel).show_widget(
            CustomDataTable(columns=["Fecha", "TOTAL VTAs. NSA"], rows=data["LTOTALNSA"].items())
        )

        self.set_timer(3, self.load_data_panel_sales_diff)

    def load_data_panel_sales_diff(self):
        self.query_one("#panel-sales-diff", CustomInfoPanel).show_widget(
            CustomDataTable(columns=["Fecha", "TOTAL VTAs. NSA", "Diferencia Anual"],
                            rows=self.__data[["LTOTALNSA", "Anual Difference"]].itertuples()
                            )
        )
        self.set_timer(3, self.load_data_panel_percent_diff)

    def load_data_panel_percent_diff(self):
        self.query_one("#panel-percent-diff", CustomInfoPanel).show_widget(
            CustomDataTable(
                columns=["Fecha", "TOTAL VTAs. NSA", "Diferencia x Año", "% de Cambio Anual"],
                rows=self.__data[["LTOTALNSA", "Anual Difference", "Annual PCT Change"]].itertuples())
        )
        self.set_timer(3, self.load_data_panel_media_movil)

    def load_data_panel_media_movil(self):
        self.query_one("#panel-media-movil", CustomInfoPanel).show_widget(
            CustomDataTable(columns=["Fecha", "TOTAL VTAs. NSA", "Media Movil"],
                            rows=self.__data[["LTOTALNSA", "Media Movil"]].itertuples())
        )
        self.set_timer(3, self.load_charts)

    def load_charts(self):
        cantidad_graficos = 5
        total = len(self.__data)
        tamano_grupo = ceil(total / cantidad_graficos)

        for i in range(cantidad_graficos):
            inicio = i * tamano_grupo
            fin = min(inicio + tamano_grupo, total)
            subconjunto = self.__data.iloc[inicio:fin]

            if subconjunto.empty:
                continue

            panel_id = f"#panel-chart-{i + 1}"
            self.query_one(panel_id, CustomPanelChart).plot_data(
                data=subconjunto,
                title="TOTAL VTAs. NSA vs Media Móvil"
            )