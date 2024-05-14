import customtkinter as ctk
from widgets.image import ImageWidget
from sql.api import change_password


def PasswordResetPage(win):
    page = ctk.CTkFrame(
        master=win,
        width=1280,
        height=720,
    )
    win.title("Urban Utopia - Reset Password")

    canvas = ctk.CTkCanvas(
        master=page, width=1280, height=720, borderwidth=0, highlightthickness=0
    )
    canvas.place(x=0, y=0)

    ImageWidget(
        canvas,
        "./assets/signin_banner.png",
        (536, 651),
        anchor="w",
        rely=0.5,
        relx=0.02,
    )

    form_frame = ctk.CTkFrame(master=page, width=740, height=720)

    ## title
    form_title = ctk.CTkLabel(
        master=form_frame, text="Reset Password", font=("Merriweather", 25)
    )
    form_title.pack(pady=10)

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
    ctk.CTkLabel(master=form_frame, text="").pack(pady=5)

    ## password
    form_pwd_label = ctk.CTkLabel(
        master=form_frame, text="🔒 New Password", font=("Merriweather", 18)
    )
    form_pwd_label.pack(pady=5, anchor="w")

    form_pwd_entry = ctk.CTkEntry(
        master=form_frame, font=("Merriweather", 15), width=500, height=40
    )
    form_pwd_entry.pack(pady=5, anchor="w")

    ## space
    ctk.CTkLabel(master=form_frame, text="").pack(pady=5)

    ## password
    form_cfmpwd_label = ctk.CTkLabel(
        master=form_frame, text="🔒 Confirm Password", font=("Merriweather", 18)
    )
    form_cfmpwd_label.pack(pady=5, anchor="w")

    form_cfmpwd_entry = ctk.CTkEntry(
        master=form_frame, font=("Merriweather", 15), width=500, height=40
    )
    form_cfmpwd_entry.pack(pady=5, anchor="w")

    ## space
    ctk.CTkLabel(master=form_frame, text="").pack(pady=5)

    def handle_pwd_change():
        error_text.configure(text="")
        help_text.configure(text="")
        if form_cfmpwd_entry.get() != form_pwd_entry.get():
            error_text.configure(text="Passwords do not match!")
            return

        change_pwd = change_password(form_email_entry.get(), form_pwd_entry.get())

        if change_pwd == -1:
            error_text.configure(text="User Does Not Exist!")
            help_text.configure(text="Don't have an account? Click here to sign up...")
            help_text.bind(
                "<Button-1>", command=lambda e: win.nav.navigate_to("signup")
            )
            return

        success = ctk.CTkToplevel()

        def cont():
            success.destroy()
            win.nav.navigate_to("welcome")

        txt = ctk.CTkLabel(
            master=success,
            text="Password Changed Successfully!",
            font=("Merriweather", 16),
        )
        btn = ctk.CTkButton(
            master=success, text="Continue", command=cont, font=("Merriweather", 15)
        )

        txt.pack(pady=5)
        btn.pack(pady=10)

    ## submit
    form_submit = ctk.CTkButton(
        master=form_frame,
        text="Change Password",
        height=50,
        width=150,
        font=("Merriweather", 18),
        command=handle_pwd_change,
    )

    error_text = ctk.CTkLabel(
        master=form_frame, text="", font=("Merriweather", 16), text_color="red"
    )

    help_text = ctk.CTkLabel(
        master=form_frame, text="", font=("Merriweather", 16), text_color="blue"
    )

    error_text.pack(pady=2)
    help_text.pack(pady=3)

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
    return "pwdreset", page
