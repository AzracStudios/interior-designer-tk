import customtkinter as ctk
from sql.api import fetch_room_by_id, fetch_styles, fetch_style_card
from widgets.image import load_image_ctk


def StyleSelectPage(win):
    page = ctk.CTkFrame(master=win, width=1280, height=720)

    def on_mount():
        win.title("Urban Utopia - Select Style")
        uid, name, banner, card = fetch_room_by_id(win.room_id)
        banner_img.configure(text=name.upper(), image=load_image_ctk(banner, (1280, 0)))

        # styles
        fetched_styles = fetch_styles()
        row = 2
        col = 2

        styles = ctk.CTkFrame(master=page, width=1280, height=510)
        styles.columnconfigure(1, minsize=20)
        styles.rowconfigure(1, minsize=20)

        for st_uid, style_name, desc in fetched_styles:
            style_card = ctk.CTkFrame(
                master=styles, width=400, height=220, corner_radius=6, fg_color="white"
            )
            style_card.pack_propagate(0)
            name = ctk.CTkLabel(
                master=style_card, text=style_name, font=("Merriweather", 18, "bold")
            )
            desc = ctk.CTkLabel(
                master=style_card, text=desc, font=("Merriweather", 15, "bold")
            )
            image = fetch_style_card(st_uid)
            img_display = ctk.CTkLabel(
                master=style_card,
                text="",
                image=load_image_ctk(image, (200, 0)),
            )

            img_display.place(relx=0.25, rely=0.4, anchor="nw")


            name.pack(pady=4)
            desc.pack(pady=2)
            style_card.uid = st_uid

            def designs(uid):
                win.style_id = uid
                win.nav.navigate_to("designs")

            style_card.bind("<Button-1>", lambda _, x=st_uid: designs(x))

            style_card.grid(row=row, column=col)
            styles.columnconfigure(col, minsize=400)

            styles.rowconfigure(row + 1, minsize=35)
            styles.columnconfigure(col + 1, minsize=20)

            if col == 6:
                col = 2
                row += 2
            else:
                col += 2

        styles.place(x=0, y=210, anchor="nw")

    banner_frame = ctk.CTkFrame(master=page, width=1280, height=210)

    banner_img = ctk.CTkLabel(
        master=banner_frame,
        image="",
        text="",
        font=("Merriweather", 50, "bold"),
        text_color="white",
    )

    banner_img.place(relx=0, rely=0, anchor="nw")

    back = ctk.CTkButton(
        master=banner_frame,
        text="< Back",
        font=("Merriweather", 15),
        width=100,
        height=35,
        corner_radius=0,
        command=lambda: win.nav.navigate_to("roomselect"),
        bg_color="#EAC7C5",
        fg_color="#f95959",
        hover_color="#e15151",
        background_corner_colors=("#EAC7C5",) * 4,
    )
    back.place(relx=0.9, rely=0.5, anchor="e")

    strip = ctk.CTkLabel(
        master=banner_frame,
        text="",
        height=10,
        width=1280,
        image=load_image_ctk("./assets/golden_strip.png", (1280, 10)),
    )
    strip.place(x=0, y=200, anchor="nw")

    banner_frame.place(relx=0, rely=0, anchor="nw")

    return "styleselect", page, on_mount, lambda: None
