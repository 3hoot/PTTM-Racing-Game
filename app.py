from src import gui, logic


def main() -> None:
    game_gui = gui.Game()
    game_logic = logic.Game(ui=game_gui)
    game_gui.set_logic(game_logic)
    game_gui.run()


if __name__ == "__main__":
    main()
