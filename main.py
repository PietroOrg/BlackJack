import customtkinter
import game_logic_blackjack as glbj  # game logic blowjob


class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("Black Jack")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        self.player = glbj.Player(glbj.deck)
        self.dealer = glbj.Dealer(glbj.deck)

        # configure grid layout (11x9)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(8, weight=1)
        self.grid_rowconfigure(10, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(6, weight=1)
        self.grid_columnconfigure(8, weight=1)

        # configure frames
        


if __name__ == "__main__":
    app = App()
    app.mainloop()
