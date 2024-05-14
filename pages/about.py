import customtkinter as ctk
from widgets.image import ImageWidget


def AboutPage(win):
    page = ctk.CTkFrame(master=win, width=1280, height=720)
    win.title("Urban Utopia - About Us")

    canvas = ctk.CTkCanvas(
        master=page, width=1280, height=720, borderwidth=0, highlightthickness=0
    )
    canvas.place(x=0, y=0)

    ImageWidget(canvas, "./assets/about_page.png", (1280, 720), anchor="nw")

    back = ctk.CTkButton(
        master=canvas,
        text="< Back",
        font=("Merriweather", 15),
        width=100,
        height=35,
        command=lambda: win.nav.navigate_to("welcome"),
        bg_color="#EAC7C5",
        fg_color="#f95959",
        hover_color="#e15151",
        background_corner_colors=("#EAC7C5",)*4
    )
    back.place(relx=0.01, rely=0.02, anchor="nw")


    return "about", page
