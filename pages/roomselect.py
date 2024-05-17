import customtkinter as ctk
from sql.api import fetch_rooms
from widgets.image import load_image_ctk


def RoomSelectPage(win):
    page = ctk.CTkFrame(master=win, width=1280, height=720)

    def onmount():
        win.title("Urban Utopia - Select Room")
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


        def room(uid):
            win.room_id = uid
            win.nav.navigate_to("styleselect")

        img.bind("<Button-1>", command=lambda _,x=uid:room(x))

        col += 1

        if col > 2:
            row += 1
            col = 1
    
    back = ctk.CTkButton(
        master=page,
        text="< Back",
        font=("Merriweather", 15),
        width=100,
        height=35,
        corner_radius=0,
        command=lambda: win.nav.navigate_to("welcome"),
        bg_color="#EAC7C5",
        fg_color="#f95959",
        hover_color="#e15151",
        background_corner_colors=("#EAC7C5",) * 4,
    )
    back.place(relx=0.98, rely=0.04, anchor="e")

    return "roomselect", page, onmount, lambda: None
