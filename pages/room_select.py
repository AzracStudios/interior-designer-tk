import customtkinter as ctk
from sql.api import fetch_rooms
from widgets.image import load_image_ctk


def RoomSelectPage(win):
    page = ctk.CTkFrame(master=win, width=1280, height=720)

    rooms = fetch_rooms()

    row = 1
    col = 1

    for uid, room_name, _, room_card in rooms:
        card = ctk.CTkFrame(master=page, width=640, height=360)
        img = ctk.CTkLabel(
            master=card,
            text=room_name.upper(),
            image=load_image_ctk(room_card, (640, 360)),
            width=640,
            height=360,
            text_color="white",
            font=("Merriweather", 40, "bold")
        )
        card.uid = uid
        img.place(relx=0, rely=0, anchor="nw")

        card.grid(row=row, column=col)

        col += 1

        if col > 2:
            row += 1
            col = 1

    return "roomselect", page
