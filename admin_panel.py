import customtkinter as ctk

from utils import correct_path
from tknav import Navigator

from admin.tableselect import TableSelectPage
from admin.users import UsersPage
from admin.rooms import RoomsPage
from admin.styles import StylesPage
from admin.designs import DesignsPage

from sql.api import *


def make_window():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme(correct_path("./theme/uu.json"))

    window = ctk.CTk()
    window.title("Urban Utopia Admin")
    window.geometry("1280x720")
    window.resizable(False, False)
    return window


def config_navigator(win, pages):
    nav = Navigator()
    for page in pages:
        nav.add_page(*page(win, connection, cursor))

    win.nav = nav
    return nav


def main():
    window = make_window()

    PAGES = [TableSelectPage, UsersPage, RoomsPage, StylesPage, DesignsPage]
    nav = config_navigator(window, PAGES)

    nav.navigate_to("tableselect")

    window.mainloop()


if __name__ == "__main__":
    main()
