from textual.widgets import DataTable


class CustomDataTable(DataTable):
    DEFAULT_CSS = """
               CustomDataTable {
                   height: 1fr;
                   border: round rgb(120, 120, 120);
                   scrollbar-background: rgb(120, 120, 120);
                   scrollbar-gutter: stable;
                   scrollbar-color: $accent;
                   scrollbar-color-hover: rgb(255, 221, 97);
                   scrollbar-background-hover: rgb(120, 120, 120);
                   scrollbar-background-active: rgb(120, 120, 120);
                   scrollbar-color-active: rgb(252, 192, 0);
               }

               CustomDataTable > .datatable--header {
                  color: $accent;
               }
               """

    def __init__(self, rows, columns, **kwargs):
        super().__init__(**kwargs)

        self.__initial_rows = rows
        self.__initial_columns = columns

    def on_mount(self):
        self.add_columns(*self.__initial_columns)
        self.add_rows(self.__initial_rows)