import customtkinter
import game_logic_blackjack as glb

class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("Black Jack")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")        