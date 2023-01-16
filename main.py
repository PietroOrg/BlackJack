import contextlib
import customtkinter
from PIL import Image
import objects as obj
import itertools
import random
from tkinter import messagebox
import os, sys
from login import LoginPage


class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520
    SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]
    RANKS = ["2", "3", "4", "5", "6", "7", "8",
             "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self, login):
        super().__init__()

        self.title("BlackJack")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.iconbitmap("Assets/Icon/jack_of_spades.ico")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_deck()

        # configure images
        for element in set(self.deck):
            self.card_image_template = f'''self.{element[0].lower()}{element[1].lower()} = customtkinter.CTkImage(dark_image=Image.open("Assets/PNG-cards/{element[1].lower()}_of_{element[0].lower()}.png"), size=(50, 72.6))'''
            exec(self.card_image_template)

        # create delaer and player objects
        self.fiches = int(login.fiches_active)
        self.player = obj.Player(self.deck, self.fiches)
        self.dealer = obj.Dealer(self.deck)

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
        self.configure_frames()

        # configure buttons
        self.hit_button = customtkinter.CTkButton(
            master=self, text="HIT", width=100, height=40, corner_radius=20, font=('', 20), command=self.place_new_hand, state="disabled")
        self.hit_button.grid(row=9, column=1, sticky="nsew")

        self.stand_button = customtkinter.CTkButton(
            master=self, text="STAND", width=100, height=40, corner_radius=20, font=('', 20), command=self.dealer_turn, state="disabled")
        self.stand_button.grid(row=9, column=3, sticky="nsew")

        self.restart_button = customtkinter.CTkButton(
            master=self, text="PLAY\nAGAIN", width=100, height=40, corner_radius=20, font=('', 20), state="disabled", command=self.restart)
        self.restart_button.grid(row=9, column=7, sticky="nsew")

        # configure entries
        self.bet_entry = customtkinter.CTkEntry(
            master=self, width=100, height=40, corner_radius=20, font=('', 20), justify="center")
        self.bet_entry.grid(row=9, column=5, sticky="nsew")
        self.bet_entry.bind("<Return>", self.submit_bet)

        # configure labels
        self.dealerscore_var = customtkinter.StringVar(value="Dealer Score: 0")
        self.dealerscore_label = customtkinter.CTkLabel(
            master=self, textvariable=self.dealerscore_var)
        self.dealerscore_label.grid(
            row=3, column=3, columnspan=3, sticky="nsew")

        self.playerscore_var = customtkinter.StringVar(
            value=f"{login.username_active} Score: 0")
        self.playerscore_label = customtkinter.CTkLabel(
            master=self, textvariable=self.playerscore_var)
        self.playerscore_label.grid(
            row=7, column=3, sticky="nsew")

        self.playerfiches_var = customtkinter.StringVar(value=f"Fiches: {self.player.fiches}")
        self.bet_label = customtkinter.CTkLabel(
            master=self, textvariable=self.playerfiches_var)
        self.bet_label.grid(row=7, column=5, sticky="nsew")
        
    # create deck function: creates a deck of cards
    def create_deck(self) -> None:
        self.deck = list(itertools.product(App.SUITS, App.RANKS))
        self.deck += self.deck
        random.shuffle(self.deck)

    def configure_frames(self) -> None:
        # configure frames
        self.dealer_frame = customtkinter.CTkFrame(
            master=self, width=200, height=120, corner_radius=10, fg_color="#154734")
        self.dealer_frame.grid(row=1, column=1, columnspan=7, sticky="ew")

        self.player_frame = customtkinter.CTkFrame(
            master=self, width=200, height=120, corner_radius=10, fg_color="#154734")
        self.player_frame.grid(row=5, column=1, columnspan=7, sticky="ew")

        # configure frames grid layout (31x3)
        for i in range(0, 15, 2):
            self.player_frame.grid_columnconfigure(i, weight=1)
            self.dealer_frame.grid_columnconfigure(i, weight=1)

        self.player_frame.grid_rowconfigure(1, weight=1)
        self.dealer_frame.grid_rowconfigure(1, weight=1)

    # submit bet function: attached to "enter" command, confirms the bet
    def submit_bet(self, *args) -> None:
        with contextlib.suppress(Exception):
            self.player_bet = int(self.bet_entry.get())
            if self.player_bet <= self.player.fiches and self.player_bet >= 0:
                self.initialize_game()
            else:
                messagebox.showerror("Error", "Invalid bet")

    # initialize game function: initializes player and dealer decks, places bet
    def initialize_game(self) -> None:
        self.player.bet(self.player_bet)
        self.hit_button.configure(state="normal")
        self.stand_button.configure(state="normal")
        self.bet_entry.configure(state="disabled")
        self.place_button_cards('player')
        self.place_dealer_hand()
        self.place_button_cards(entity='player')
        self.playerscore_var.set(f"{login.username_active} Score: {int(self.player)}")
        self.dealerscore_var.set("Dealer Score: X")
        self.playerfiches_var.set(f"Fiches: {self.player.fiches}")

    # place button cards function: places cards on the table
    def place_button_cards(self, entity: str) -> None:
        entity_object = self.player if entity == 'player' else self.dealer
        for index, element in enumerate(entity_object.hand):
            self.add_button_card_template = f'''self.{entity}_card{index} = customtkinter.CTkButton(master=self.{entity}_frame, image=self.{element[0].lower()}{element[1].lower()}, width=50, height=72.6, state="disabled", text="", fg_color="#154734", corner_radius=10)'''
            exec(self.add_button_card_template)
            self.place_button_card_template = f'''self.{entity}_card{index}.grid(row=0, column={index * 2 + 1}, sticky="nsew", pady=20)'''
            exec(self.place_button_card_template)
            
    # place dealer hand function: recalls the last function to place dealer hand
    def place_dealer_hand(self) -> None:
        self.place_button_cards('dealer')
        self.card_back_image = customtkinter.CTkImage(
            dark_image=Image.open("Assets/PNG-cards/back.png"), size=(50, 72.6))
        self.dealer_card1 = customtkinter.CTkButton(
            master=self.dealer_frame, image=self.card_back_image, width=50, height=72.6, state="disabled", text="", fg_color="#154734", corner_radius=10)
        self.dealer_card1.grid(row=0, column=3, sticky="nsew", pady=20)

    # remove cards function: removes every card from a specific entity
    def remove_cards(self, entity: str) -> None:
        entity_object = self.player if entity == 'player' else self.dealer
        for index, element in enumerate(entity_object.hand):
            self.remove_card_template = f'''self.{entity}_card{index}.destroy()'''
            exec(self.remove_card_template)

    # place new hand function: removes every card and replaces with new ones
    def place_new_hand(self) -> None:
        if int(self.player) < 21:
            self.remove_cards(entity='player')
            self.player.draw_card(self.deck)
            self.playerscore_var.set(f"{login.username_active} Score: {int(self.player)}")
            self.place_button_cards('player')
        if int(self.player) > 20:
            self.hit_button.configure(state="disabled")
            self.stand_button.configure(state="disabled")
            self.remove_cards(entity='dealer')
            self.dealer_turn()

    # dealer turn function: draws dealer cards
    def dealer_turn(self) -> None:
        self.hit_button.configure(state="disabled")
        self.stand_button.configure(state="disabled")
        if int(self.dealer) < int(self.player) < 22:
            self.dealer.draw_card(self.deck)
            return self.dealer_turn()
        self.dealerscore_var.set(f"Dealer Score: {int(self.dealer)}")
        self.place_button_cards('dealer')
        self.check_winner()

    # check winner function
    def check_winner(self) -> None:
        if int(self.player) > 21:
            messagebox.showinfo("You Bust!", "You Lose!")
        elif int(self.dealer) > 21:
            messagebox.showinfo("Dealer Busts!", "You Win!")
            self.player.win(self.player_bet)
        elif int(self.player) == int(self.dealer):
            messagebox.showinfo("Tie!", "It's a Tie!")
            self.player.tie(self.player_bet)
        elif int(self.player) > int(self.dealer):
            messagebox.showinfo("You scored more than the dealer!", "You Win!")
            self.player.win(self.player_bet)
        elif int(self.player) < int(self.dealer):
            messagebox.showinfo("You scored less than the dealer!", "You Lose!")
        self.playerfiches_var.set(f"Fiches: {self.player.fiches}")
        self.restart_button.configure(state="normal")
    
    # game restart function
    def restart(self) -> None:
        self.restart_button.configure(state="disabled")
        self.bet_entry.configure(state="normal")
        self.dealer_frame.destroy()
        self.player_frame.destroy()
        self.configure_frames()
        self.playerscore_var.set(f"{login.username_active} Score: 0")
        self.dealerscore_var.set("Dealer Score: 0")
        self.player = obj.Player(self.deck, self.player.fiches)
        self.dealer = obj.Dealer(self.deck)
        self.playerfiches_var.set(f"Fiches: {self.player.fiches}")

    def on_closing(self) -> None:
        login.update_fiches(self.player.fiches)
        self.destroy()
        


if __name__ == "__main__":
    login = LoginPage()
    login.mainloop()

    app = App(login)
    app.mainloop()
