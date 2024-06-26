import customtkinter as ctk
from widgets.image import ImageWidget
from sql.api import register_user, get_name
from sql.api import encrypt


def SignUpPage(win):
    page = ctk.CTkFrame(master=win, width=1280, height=720)
    canvas = ctk.CTkCanvas(
        master=page, width=1280, height=720, borderwidth=0, highlightthickness=0
    )
    canvas.place(x=0, y=0)

    def onmount():
        win.title("Urban Utopia - Sign Up")

    def ondestroy():
        form_name_entry.delete(0, len(form_name_entry.get()))
        form_email_entry.delete(0, len(form_email_entry.get()))
        form_pwd_entry.delete(0, len(form_pwd_entry.get()))
        form_cfm_pwd_entry.delete(0, len(form_cfm_pwd_entry.get()))

    ImageWidget(
        canvas,
        "./assets/signup_banner.png",
        (536, 651),
        anchor="w",
        rely=0.5,
        relx=0.02,
    )

    form_frame = ctk.CTkFrame(master=page, width=740, height=720)

    ## title
    form_title = ctk.CTkLabel(
        master=form_frame, text="Sign Up", font=("Merriweather", 25)
    )
    form_title.pack(pady=10)

    ## name
    form_name_label = ctk.CTkLabel(
        master=form_frame, text="Full Name", font=("Merriweather", 18)
    )
    form_name_label.pack(pady=5, anchor="w")

    form_name_entry = ctk.CTkEntry(
        master=form_frame, font=("Merriweather", 15), width=500, height=40
    )
    form_name_entry.pack(pady=5, anchor="w")

    ## space
    ctk.CTkLabel(master=form_frame, text="").pack(pady=2)

    ## email
    form_email_label = ctk.CTkLabel(
        master=form_frame, text="📪 Email Address", font=("Merriweather", 18)
    )
    form_email_label.pack(pady=5, anchor="w")

    form_email_entry = ctk.CTkEntry(
        master=form_frame, font=("Merriweather", 15), width=500, height=40
    )
    form_email_entry.pack(pady=5, anchor="w")

    ## space
    ctk.CTkLabel(master=form_frame, text="").pack(pady=2)

    ## password
    form_pwd_label = ctk.CTkLabel(
        master=form_frame, text="🔒 Password", font=("Merriweather", 18)
    )
    form_pwd_label.pack(pady=5, anchor="w")

    form_pwd_entry = ctk.CTkEntry(
        master=form_frame, font=("Merriweather", 15), width=500, height=40
    )
    form_pwd_entry.pack(pady=5, anchor="w")

    ## space
    ctk.CTkLabel(master=form_frame, text="").pack(pady=2)

    ## confirm password
    form_cfm_pwd_label = ctk.CTkLabel(
        master=form_frame, text="🔒 Confirm Password", font=("Merriweather", 18)
    )
    form_cfm_pwd_label.pack(pady=5, anchor="w")

    form_cfm_pwd_entry = ctk.CTkEntry(
        master=form_frame, font=("Merriweather", 15), width=500, height=40
    )
    form_cfm_pwd_entry.pack(pady=5, anchor="w")

    ## space
    ctk.CTkLabel(master=form_frame, text="").pack(pady=2)

    ## submit
    def handle_signup():
        if not (form_pwd_entry.get(), form_email_entry.get(), form_pwd_entry.get()):
            return

        register_user(
            form_name_entry.get(), form_email_entry.get(), form_pwd_entry.get()
        )

        with open("login", "w") as f:
            f.write(
                f"{get_name(form_email_entry.get())}\n{form_email_entry.get()}\n{encrypt(form_pwd_entry.get())}"
            )

        form_email_entry.delete(0, len(form_email_entry.get()))
        form_pwd_entry.delete(0, len(form_pwd_entry.get()))
        win.nav.navigate_to("welcome")

    form_submit = ctk.CTkButton(
        master=form_frame,
        text="Sign Up",
        height=50,
        width=150,
        font=("Merriweather", 18),
        command=handle_signup,
    )
    form_submit.pack(pady=5)

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
        background_corner_colors=("#EAC7C5",) * 4,
    )
    back.place(relx=0.9, rely=0.047, anchor="nw")

    form_frame.place(relx=0.5, rely=0.5, anchor="w")

    page.pack_propagate(0)
    return "signup", page, onmount, ondestroy
