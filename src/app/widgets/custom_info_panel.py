from textual.widgets import Static, Label


class CustomInfoPanel(Static):

    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)

        self.__title = title

    def compose(self):
        yield Label(self.__title, id="panel-title")
        yield Static("", id="panel-content")

    def show_widget(self, widget):
        content = self.query_one("#panel-content", Static)
        content.remove_children()
        content.mount(widget)
