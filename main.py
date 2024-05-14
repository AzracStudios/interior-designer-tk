import os

import customtkinter as ctk

from utils import correct_path
from tknav import Navigator

from pages.welcome import WelcomePage
from pages.about import AboutPage
from pages.terms import TermsAndConditionsPage
from pages.signin import SignInPage
from pages.signup import SignUpPage
from pages.room_select import RoomSelectPage
from pages.pwdreset import PasswordResetPage

def make_window():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme(correct_path("./theme/uu.json"))

    window = ctk.CTk()
    window.title("Urban Utopia")
    window.geometry("1280x720")

    window.resizable(False, False)
    return window


def config_navigator(win, pages):
    nav = Navigator()
    for page in pages:
        nav.add_page(*page(win))

    win.nav = nav
    return nav


def main():
    window = make_window()

    PAGES = [
        WelcomePage,
        AboutPage,
        TermsAndConditionsPage,
        SignInPage,
        SignUpPage,
        PasswordResetPage,
        RoomSelectPage,
    ]
    nav = config_navigator(window, PAGES)

    nav.navigate_to("welcome")

    window.mainloop()


if __name__ == "__main__":
    main()
