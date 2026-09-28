import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as mpl_plt

from textual.containers import Vertical
from textual_image.widget import Image


class CustomPanelChart(Vertical):
    DEFAULT_CSS = """
    CustomPanelChart {
        border: round rgb(120, 120, 120);
        height: 22;
        width: 1fr;
    }

    CustomPanelChart Image {
        width: 1fr;
        height: 1fr;
    }
    """

    def compose(self):
        yield Image()

    def show_widget(self, widget):
        self.remove_children()
        self.mount(widget)

    def plot_data(self, data, title=""):
        self.remove_children()

        etiquetas = data.index.strftime("%Y").tolist()
        rango = f"{etiquetas[0]} - {etiquetas[-1]}"

        buffer_imagen = self._generar_imagen_grafico(data, title=f"{title} ({rango})", etiquetas=etiquetas)

        imagen_widget = Image(buffer_imagen)
        self.mount(imagen_widget)

    def _generar_imagen_grafico(self, data, title, etiquetas):
        fig, ax = mpl_plt.subplots(figsize=(6, 3), facecolor="black")
        ax.set_facecolor("black")

        ax.plot(etiquetas, data["LTOTALNSA"], label="TOTAL VTAs. NSA", color="orange")
        ax.plot(etiquetas, data["Media Movil"], label="Media Movil", color="yellow", linestyle="dotted")

        promedio = data["LTOTALNSA"].mean()
        ax.axhline(promedio, color="gray", linestyle="--", linewidth=0.8)

        ax.set_title(title, color="white")
        ax.set_xlabel("Año", color="white")
        ax.set_ylabel("Ventas (NSA)", color="white")
        ax.tick_params(colors="white", labelrotation=45)
        ax.legend(facecolor="black", labelcolor="white", fontsize="small")
        ax.grid(True, color="gray", alpha=0.3)

        for spine in ax.spines.values():
            spine.set_color("white")

        buffer = io.BytesIO()
        fig.tight_layout()
        fig.savefig(buffer, format="png", dpi=100)
        mpl_plt.close(fig)
        buffer.seek(0)
        return buffer