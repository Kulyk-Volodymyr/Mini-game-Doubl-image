from tkinter import *
from random import shuffle
from PIL import Image, ImageTk

window = Tk()
window['bg'] = '#f0f0f0'
window.title("Double image")
window.geometry('720x600')
window.resizable(width=False, height=False)
window.iconbitmap('icon_di.ico')

images_for_cards = ['images/an_1.png', 'images/an_2.png', 'images/an_3.png', 'images/an_4.png',
                    'images/an_5.png', 'images/an_6.png', 'images/an_7.png', 'images/an_8.png',
                    'images/ca_1.png', 'images/ca_2.png', 'images/ca_3.png', 'images/ca_4.png',
                    'images/ca_5.png', 'images/ca_6.png', 'images/df_1.png', 'images/df_2.png',
                    'images/df_3.png', 'images/df_4.png', 'images/df_5.png', 'images/pl_1.png',
                    'images/pl_2.png', 'images/pl_3.png', 'images/pl_4.png', 'images/pl_5.png',
                    'images/pl_6.png', 'images/pl_7.png', 'images/pl_8.png', 'images/pl_9.png']
hidden_img = 'images/hide.png'  # image that hides the card
sizes = []  # when you start a new game, choose the card sizes and their placement
images = []  # the level of the game determines the list of pictures
cards = []  # a list of cards created from the class 'CreateCard'
first_opened_card = []  # the player opens the first card
second_opened_card = []  # the player opens the second card


class CreateCard:
    """ Create a card.
        Keyword arguments:
            hidden_pic -- image when card is hidden
            opened_pic -- image when card is opened
            lst1 -- a list for first opened card
            lst2 -- a list for second opened card
            lst3 -- a list which is selected when you select the game level. This determines the card size
    """
    def __init__(self, hidden_pic, opened_pic, lst1, lst2, lst3):

        self.hidden_pic = hidden_pic
        self.opened_pic = opened_pic
        self.lst1 = lst1
        self.lst2 = lst2
        self.lst3 = lst3

        self.image1 = Image.open(self.hidden_pic)
        self.img1 = self.image1.resize((lst3[0], lst3[0]))
        self.hidden_image = ImageTk.PhotoImage(self.img1)
        self.image2 = Image.open(self.opened_pic)
        self.img2 = self.image2.resize((lst3[0], lst3[0]))
        self.opened_image = ImageTk.PhotoImage(self.img2)

        self.card = Canvas()
        self.hidden_top = self.hidden_image
        self.card.create_image(self.lst3[0] / 2, self.lst3[0] / 2, image=self.hidden_top)
        self.card.bind('<Button-1>', self.invert_card)

    def invert_card(self, event):
        """ Flipping the card.
            The function changes the image of the card (hidden - open) and passes data to the 'add_card' function. """
        if self.hidden_top == self.hidden_image:
            self.card.delete('all')
            self.card.create_image(self.lst3[0] / 2, self.lst3[0] / 2, image=self.opened_image)
            self.hidden_top = self.opened_image
            self.add_card(self.opened_pic)
        else:
            self.card.delete('all')
            self.card.create_image(self.lst3[0] / 2, self.lst3[0] / 2, image=self.hidden_image)
            self.hidden_top = self.hidden_image
            self.add_card(self.hidden_pic)

    def add_card(self, img):
        """ When you open the first card - it is added into 'first_opened_card'.
            When you click the same card, it is removed from 'first_opened_card'.
            When you open the second card - it is added into 'second_opened_card'
            and the function 'two_opened_cards' starts. """
        if len(self.lst1) == 0:
            if img != self.hidden_pic:
                first_opened_card.append(img)
            else:
                first_opened_card.pop()
        else:
            if len(self.lst2) == 0:
                if img == self.hidden_pic:
                    first_opened_card.pop()
                else:
                    second_opened_card.append(img)
                    two_opened_cards(first_opened_card[0], second_opened_card[0])
            else:
                if img == self.hidden_pic:
                    recover()
                else:
                    second_opened_card.append(img)
                    two_opened_cards(first_opened_card[0], second_opened_card[0])

    def delete_card(self):
        """ Delete a card. It starts when two identical cards are open. """
        self.card.place_forget()

    def hide_card(self):
        """ Hide the card if two different ones are open. """
        self.card.delete('all')
        self.card.create_image(self.lst3[0] / 2, self.lst3[0] / 2, image=self.hidden_image)
        self.hidden_top = self.hidden_image


def place_cards():
    """ Mix pictures for cards, create cards and place them. """
    shuffle(images)
    for pic in images:
        cards.append(CreateCard(hidden_img, pic, first_opened_card, second_opened_card, sizes))
    a = 0
    for r in range(sizes[4]):  # rows
        for c in range(sizes[5]):  # columns
            cards[a].card.place(x=sizes[1] + c * (sizes[0] + sizes[3]), y=sizes[2] + r * (sizes[0] + sizes[3]),
                                anchor="nw", height=sizes[0], width=sizes[0])
            a += 1


def two_opened_cards(first, second):
    """ When two cards are open. If they are the same, remove them and check if there are more cards.
        If they are different, turn them over. """
    if first == second:
        for card in cards:
            if card.opened_pic == first:
                card.delete_card()
                global final_cards_quantity
                final_cards_quantity -= 1
                if final_cards_quantity == 0:
                    finish()
        first_opened_card.pop()
        second_opened_card.pop()
        for card in cards:
            card.hide_card()
    else:
        if len(second_opened_card) == 1:
            pass
        else:
            for card in cards:
                card.hide_card()
            first_opened_card.pop()
            second_opened_card.pop()
            second_opened_card.pop()


def recover():
    """ One card is already open. The player opens a second one. When he closes the second,
        the first one also closes. """
    for card in cards:
        card.hide_card()
    first_opened_card.pop()
    second_opened_card.pop()


def select_level():
    """ This is a window to select the game level.
        There are 9 buttons which select the number of cards for the game. """
    new_game_label.place_forget()
    new_game_button.place_forget()
    srb = [("12 pics", 1), ("16 pics", 2), ("20 pics", 3),  # srb - start radiobutton data
           ("24 pics", 4), ("30 pics", 5), ("36 pics", 6),
           ("42 pics", 7), ("48 pics", 8), ("56 pics", 9)]
    select_level_label = Label(window, text="START NEW GAME", font="Arial 36", bg='#f0f0f0')
    select_level_label.place(anchor="c", relx=0.5, rely=0.25)
    start_value = IntVar()
    start_buttons = []

    def select():
        """ This function transmits the value of the selected radiobutton and starts the game."""
        global sizes
        sizes = []
        shuffle(images_for_cards)
        global images
        images = []
        if start_value.get() == 1:  # 12 pics, 3 rows, 4 columns
            sizes = [100,  # image's size
                     115,  # distance between card and left(or right) border
                     120,  # distance between card and top(or bottom) border
                     30,  # distance between cards
                     3,  # quantity of rows
                     4,  # quantity of columns
                     ]
            images = images_for_cards[:6] * 2
        if start_value.get() == 2:  # 16 pics, 4 rows, 4 columns
            sizes = [100, 115, 55, 30, 4, 4, ]
            images = images_for_cards[:8] * 2
        if start_value.get() == 3:  # 20 pics, 4 rows, 5 columns
            sizes = [100, 50, 55, 30, 4, 5, ]
            images = images_for_cards[:10] * 2
        if start_value.get() == 4:  # 24 pics, 4 rows, 6 columns
            sizes = [84, 33, 87, 30, 4, 6, ]
            images = images_for_cards[:12] * 2
        if start_value.get() == 5:   # 30 pics, 5 rows, 6 columns
            sizes = [84, 33, 30, 30, 5, 6, ]
            images = images_for_cards[:15] * 2
        if start_value.get() == 6:  # 36 pics, 6 rows, 6 columns
            sizes = [74, 78, 18, 24, 6, 6, ]
            images = images_for_cards[:18] * 2
        if start_value.get() == 7:  # 42 pics, 6 rows, 7 columns
            sizes = [74, 29, 18, 24, 6, 7, ]
            images = images_for_cards[:21] * 2
        if start_value.get() == 8:  # 48 pics, 6 rows, 8 columns
            sizes = [64, 27, 53, 22, 6, 8, ]
            images = images_for_cards[:24] * 2
        if start_value.get() == 9:  # 56 pics, 7 rows, 8 columns
            sizes = [64, 27, 10, 22, 7, 8, ]
            images = images_for_cards[:28] * 2

        select_level_label.place_forget()
        for item in start_buttons:
            item.place_forget()
        new_game_label.place_forget()
        new_game_button.place_forget()

        global cards
        cards = []
        place_cards()
        global final_cards_quantity
        final_cards_quantity = len(cards)

    for k in srb:  # a list of buttons for selecting game level
        start_buttons.append(
            Radiobutton(window, text=k[0], value=k[1], variable=start_value, command=select,
                        indicatoron=0, font="Arial 24"))
    for i in range(3):  # place the game level buttons
        for j in range(3):
            start_buttons[i * 3 + j].place(anchor="c", relx=0.28 + j * 0.22, rely=0.4 + i * 0.15)


new_game_label = Label(window, text="GAME OVER", font="Arial 36", bg='#f0f0f0')
new_game_button = Button(window, text="NEW GAME", font="Arial 18", command=select_level)


def finish():
    """ A message about the end of the game and a 'start' button for a new one. """
    new_game_label.place(anchor="c", relx=0.5, rely=0.35)
    new_game_button.place(anchor="c", relx=0.5, rely=0.55)


select_level()

window.mainloop()
