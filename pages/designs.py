import customtkinter as ctk
from sql.api import fetch_room_by_id, fetch_style_by_id


def DesignPage(win):
    page = ctk.CTkFrame(master=win, width=1280, height=720)

    def onmount():
        win.title("Urban Utopia - Designs")
        room_name = fetch_room_by_id(win.room_id)[1]
        style_name = fetch_style_by_id(win.style_id)[1]
        title.configure(text=f"{style_name} {room_name}")

    title = ctk.CTkLabel(master=page, text="", font=("Merriweather", 25))
    title.place(relx=0.5, rely=0.04, anchor="center")

    return "designs", page, onmount, lambda: None
