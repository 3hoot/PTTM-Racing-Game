from actions import GuiActions


class Game:
    def __init__(self, ui: GuiActions) -> None:
        self.ui = ui

    def option_1(self) -> None:
        self.ui.show_status("Option 1 selected")

    def option_2(self) -> None:
        self.ui.show_status("Option 2 selected")
