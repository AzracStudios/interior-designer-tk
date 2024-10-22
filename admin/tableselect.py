import customtkinter as ctk
from widgets.image import load_image_ctk


def TableSelectPage(win, db, sql):
    page = ctk.CTkFrame(
        master=win, width=1280, height=720, bg_color="#ececec", fg_color="#ececec"
    )
    page.pack_propagate(0)

    def onmount():
        win.title("Urban Utopia Admin - Select")

    frame = ctk.CTkFrame(master=page, bg_color="#ececec", fg_color="#ececec")

    def TableButton(table):
        table_btn = ctk.CTkButton(
            master=frame,
            text=f"\n{table}",
            image=load_image_ctk(f"./assets/{table.lower()}_icon.png", (100, 100)),
            compound="top",
            corner_radius=10,
            width=250,
            height=250,
            bg_color="white",
            fg_color="white",
            hover_color="#f3f3f3",
            text_color="black",
            font=("Roboto", 16),
            background_corner_colors=("#ececec",) * 4,
            command=lambda: win.nav.navigate_to(table.lower()),
        )
        return table_btn

    TableButton("Users").grid(row=1, column=1, padx=10, pady=10)
    TableButton("Feedbacks").grid(row=1, column=2, padx=10, pady=10)
    TableButton("Inquiries").grid(row=1, column=3, padx=10, pady=10)
    TableButton("Rooms").grid(row=2, column=1, padx=10, pady=10)
    TableButton("Styles").grid(row=2, column=2, padx=10, pady=10)
    TableButton("Designs").grid(row=2, column=3, padx=10, pady=10)

    logo_frame = ctk.CTkFrame(master=page, bg_color="#ececec", fg_color="#ececec")
    ctk.CTkLabel(
        master=logo_frame, text="", image=load_image_ctk("./assets/logo.png", (50, 50))
    ).grid(row=1, column=1)
    ctk.CTkLabel(
        master=logo_frame, text="", image=load_image_ctk("./assets/name.png", (120, 50))
    ).grid(row=1, column=2, padx=15)

    logo_frame.place(relx=0.5, rely=0.07, anchor="center")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    return "tableselect", page, onmount, lambda: None
