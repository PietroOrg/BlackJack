import customtkinter
from PIL import Image
import game_logic_blackjack as glbj  # game logic blowjob


class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("Black Jack")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        self.deck = glbj.create_deck()

        # configure images
        print(len(self.deck))
        for element in set(self.deck):
            self.card_image_template = f'''self.{element[0].lower()}{element[1].lower()} = customtkinter.CTkImage(dark_image=Image.open("PNG-cards/{element[1].lower()}_of_{element[0].lower()}.png"), size=(50, 72.6))'''
            exec(self.card_image_template)

        # create delaer and player objects
        self.player = glbj.Player(self.deck)
        self.dealer = glbj.Dealer(self.deck)

        # configure grid layout (9x11)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(6, weight=1)
        self.grid_columnconfigure(8, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(8, weight=1)
        self.grid_rowconfigure(10, weight=1)

        # configure frames
        self.dealer_frame = customtkinter.CTkFrame(
            master=self, width=200, height=200, corner_radius=10, fg_color="#154734")
        self.dealer_frame.grid(row=1, column=1, columnspan=7, sticky="nsew")

        self.player_frame = customtkinter.CTkFrame(
            master=self, width=200, height=200, corner_radius=10, fg_color="#154734")
        self.player_frame.grid(row=5, column=1, columnspan=7, sticky="nsew")

        # configure frames grid layout (31x3)
        self.dealer_frame.grid_columnconfigure(0, weight=1)
        self.dealer_frame.grid_columnconfigure(2, weight=1)
        self.dealer_frame.grid_columnconfigure(4, weight=1)
        self.dealer_frame.grid_columnconfigure(6, weight=1)
        self.dealer_frame.grid_columnconfigure(8, weight=1)
        self.dealer_frame.grid_columnconfigure(10, weight=1)
        self.dealer_frame.grid_columnconfigure(12, weight=1)
        self.dealer_frame.grid_columnconfigure(14, weight=1)
        self.dealer_frame.grid_columnconfigure(16, weight=1)
        self.dealer_frame.grid_columnconfigure(18, weight=1)
        self.dealer_frame.grid_columnconfigure(20, weight=1)
        self.dealer_frame.grid_columnconfigure(22, weight=1)
        self.dealer_frame.grid_columnconfigure(24, weight=1)
        self.dealer_frame.grid_columnconfigure(26, weight=1)
        self.dealer_frame.grid_columnconfigure(28, weight=1)
        self.dealer_frame.grid_columnconfigure(30, weight=1)

        self.dealer_frame.grid_rowconfigure(0, weight=1)
        self.dealer_frame.grid_rowconfigure(2, weight=1)

        # configure buttons
        self.hit_button = customtkinter.CTkButton(
            master=self, text="HIT", width=100, height=40, corner_radius=10, font=('', 20))
        self.hit_button.grid(row=9, column=1, sticky="nsew")

        self.stand_button = customtkinter.CTkButton(
            master=self, text="STAND", width=100, height=40, corner_radius=10, font=('', 20))
        self.stand_button.grid(row=9, column=3, sticky="nsew")

        self.double_button = customtkinter.CTkButton(
            master=self, text="DOUBLE", width=100, height=40, corner_radius=10, font=('', 20))
        self.double_button.grid(row=9, column=5, sticky="nsew")

        self.split_button = customtkinter.CTkButton(
            master=self, text="SPLIT", width=100, height=40, corner_radius=10, font=('', 20))
        self.split_button.grid(row=9, column=7, sticky="nsew")

        # configure labels
        self.dealerscore_var = customtkinter.StringVar(value="Dealer Score: X")
        self.dealerscore_label = customtkinter.CTkLabel(
            master=self, textvariable=self.dealerscore_var)
        self.dealerscore_label.grid(
            row=3, column=3, columnspan=3, sticky="nsew")

        self.playerscore_var = customtkinter.StringVar(value=f"Player Score: {int(self.player.hand)}")
        self.playerscore_label = customtkinter.CTkLabel(
            master=self, textvariable=self.playerscore_var)
        self.playerscore_label.grid(
            row=7, column=3, columnspan=3, sticky="nsew")

        # generate first hand
        self.start_game()

    def start_game(self):
        for index, element in enumerate(self.player.hand.first_hand):
            self.add_card_template = f'''card{index} = customtkinter.CTkButton(master=self.player_frame, image=self.{element[0].lower()}{element[1].lower()}, width=50, height=72.6, state="disabled", text="", fg_color="#154734", corner_radius=10)'''
            exec(self.add_card_template)
            self.place_card_template = f'''card{index}.grid(row=1, column={index*2+1}, sticky="nsew", pady=20)'''
            exec(self.place_card_template)

    def check_player(self):
        if self.player.hand < 21:
            self.player.hand.draw_card()


if __name__ == "__main__":
    app = App()
    app.mainloop()
