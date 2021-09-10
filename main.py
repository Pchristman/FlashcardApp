from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
timer = None

# ------------------------ CREATE FLASHCARDS -------------------------------
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
    current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(language_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)


# -------------------------- FLIP FLASHCARDS --------------------------------
def flip_card():
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")


# --------------------------- SAVE PROGRESS --------------------------------
def is_known():
    to_learn.remove(current_card)
    data_frame = pd.DataFrame(to_learn)
    data_frame.to_csv('data/words_to_learn.csv', index=False)
    next_card()


# ------------------------------ UI SETUP ---------------------------------
# Window
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Images
card_back_img = PhotoImage(file="images/card_back.png")
card_front_img = PhotoImage(file="images/card_front.png")
right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")

# Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas_image = canvas.create_image(400, 263, image=card_front_img)
language_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
right_button = Button(image=right_img, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

wrong_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()

window.mainloop()
