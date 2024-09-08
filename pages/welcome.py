import customtkinter as ctk
from widgets.image import ImageWidget
import os
from sql.api import login_user, get_user
from tkinter.messagebox import askyesno


def WelcomePage(win):
    page = ctk.CTkFrame(master=win, width=1280, height=720)

    user_details = None

    def onmount():
        win.title("Urban Utopia - Welcome")
        page.after(0, on_mount)

    canvas = ctk.CTkCanvas(
        master=page, width=1280, height=720, borderwidth=0, highlightthickness=0
    )
    canvas.place(x=0, y=0)


    signupact = signinact = None
    def on_mount():
        nonlocal user_details,  signupact, signinact
        user_details = None

        def setup_actionbuttons():
            nonlocal signupact, signinact
            signupact = ctk.CTkButton(
                    master=canvas,
                    text="Sign Up",
                    font=("Merriweather", 18),
                    corner_radius=0,
                    height=40,
                    command=lambda: win.nav.navigate_to("signup"),
                )
            signupact.place(relx=0.98, rely=0.03, anchor="ne")

            signinact = ctk.CTkButton(
                    master=canvas,
                    text="Sign In",
                    font=("Merriweather", 18),
                    corner_radius=0,
                    height=40,
                    command=lambda: win.nav.navigate_to("signin"),
                )
            signinact.place(relx=0.85, rely=0.03, anchor="ne")

        if os.path.isfile("login"):
            with open("login", "r") as f:
                content = f.readlines()
                
                if len(content) and login_user(content[1].strip(), content[2], hashed=True) == 1:
                    user_details = content[0].strip()
        ## actions
        if user_details is None:
            setup_actionbuttons()
        
        else:
            def signout():
                if askyesno("Urban Utopia - Logout", message="Do you want to logout?"):
                    with open("login", "w") as f:
                        f.write("")
                
                    signedtext.destroy()
                    setup_actionbuttons()

            if signupact and signinact:
                signupact.destroy()
                signinact.destroy()

            signedtext =  ctk.CTkButton(
                master=canvas,
                text=f"Welcome, {user_details}",
                font=("Merriweather", 18),
                corner_radius=0,
                height=40,
                command=signout,
            )

            liked =  ctk.CTkButton(
                master=canvas,
                text=f"Interested Designs",
                font=("Merriweather", 18),
                corner_radius=0,
                height=40,
                width=200,
                command=lambda: win.nav.navigate_to("interested"),
            )
            
            signedtext.place(relx=0.95, rely=0.03, anchor="ne")
            liked.place(relx=0.8, rely=0.03, anchor="ne")
    

    

    ## background image
    ImageWidget(canvas, "./assets/welcome_bg.png", (1280, 720), x=0, y=0, anchor="nw")

    ## logo
    ImageWidget(canvas, "./assets/logo.png", (200, 200), relx=0.5, rely=0.25)

    ## logo text
    ImageWidget(canvas, "./assets/name.png", (250, 100), relx=0.5, rely=0.5)

    ## quote
    ImageWidget(canvas, "./assets/quote.png", (400, 40), relx=0.5, rely=0.63)

    ## explore btn
    explore = ctk.CTkButton(
        master=canvas,
        text="Explore!",
        corner_radius=0,
        height=50,
        font=("Merriweather", 18),
        command=lambda: win.nav.navigate_to("roomselect"),
    )
    explore.place(relx=0.5, rely=0.8, anchor="center")

    ## quick links

    ## ABOUT ##
    about = ctk.CTkButton(
        master=canvas,
        text="About Us",
        font=("Merriweather", 15),
        corner_radius=0,
        width=100,
        height=35,
        command=lambda: win.nav.navigate_to("about"),
    )
    about.place(relx=0.02, rely=0.98, anchor="sw")

    ## CONTACT ##
    contact = ctk.CTkButton(
        master=canvas,
        text="Contact Us",
        font=("Merriweather", 15),
        corner_radius=0,
        width=100,
        height=35,
    )
    contact.place(relx=0.11, rely=0.98, anchor="sw")

    ## TERMS AND CONDITIONS ##
    tnc = ctk.CTkButton(
        master=canvas,
        text="Terms & Conditions",
        font=("Merriweather", 15),
        corner_radius=0,
        width=180,
        height=35,
        command=lambda: win.nav.navigate_to("termsandconditions"),
    )
    tnc.place(relx=0.2, rely=0.98, anchor="sw")

    return "welcome", page, onmount, lambda: None
