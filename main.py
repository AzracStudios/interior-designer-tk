import os

import customtkinter as ctk

from utils import correct_path
from tknav import Navigator

from pages.welcome import WelcomePage
from pages.about import AboutPage
from pages.terms import TermsAndConditionsPage
from pages.signin import SignInPage
from pages.signup import SignUpPage
from pages.roomselect import RoomSelectPage
from pages.pwdreset import PasswordResetPage
from pages.styleselect import StyleSelectPage
from pages.designs import DesignPage

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
        page_info = page(win)
        if len(page_info) == 2:
            nav.add_page(page_name=page_info[0], page_widget=page_info[1])
        else:
            nav.add_page(
                page_name=page_info[0],
                page_widget=page_info[1],
                on_mount=page_info[2],
                on_destroy=page_info[3],
            )

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
        StyleSelectPage,
        DesignPage
    ]
    nav = config_navigator(window, PAGES)

    nav.navigate_to("welcome")

    window.mainloop()


if __name__ == "__main__":
    main()
