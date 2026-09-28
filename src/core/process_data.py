from pathlib import Path

from pandas import read_excel


class ProcessData:
    def __init__(self):
        self.__path_dir = Path(__file__).resolve().parents[2] /"data"/"LTOTALNSA.xlsx"
        self.__data = read_excel(self.__path_dir, sheet_name="Monthly")

    def get_indicator(self):

        # Obtener la suma total de ventas por año
        df_annually = self.__data.resample(rule="YE", on="observation_date").sum()

        # Obtener la diferencia de ventas totales entre el años
        df_annually["Anual Difference"] = df_annually["LTOTALNSA"].diff().fillna(0.0)

        # Obtener la diferencia porcentual de ventas totales por año
        df_annually["Annual PCT Change"] = df_annually["LTOTALNSA"].pct_change().fillna(0.0)

        # Obtener la media movil de ventas totales
        df_annually["Media Movil"] = df_annually["LTOTALNSA"].rolling(window=2).mean().fillna(0.0)

        return df_annually
