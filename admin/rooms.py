import customtkinter as ctk
from widgets.table import Table
from widgets.image import load_image_ctk, Image
from sql.api import store_image
import uuid
import mysql.connector
from tkinter.filedialog import askopenfilename

from widgets.image_preview import ImagePreview
import io

# Table Schema:
#   uid varchar(36) not null primary key,
#   room_name varchar(255) not null unique


def fetch_rooms(cursor):
    cursor.execute("select * from rooms")
    return cursor.fetchall()


def fetch_room_by_id(cursor, id):
    cursor.execute(f"select * from rooms where uid='{id}'")
    return cursor.fetchone()


def handle_sql_create(
    window, db, cursor, uid, room_name, banner_loc, card_loc, refresh_callback
):
    if not (
        len(uid) > 0
        and len(room_name) > 0
        and len(banner_loc) > 0
        and len(card_loc) > 0
    ):
        err = ctk.CTkToplevel()
        err.transient(master=window)
        err.title("Urban Utopia Admin - Error")
        err.geometry("200x100")
        ctk.CTkLabel(
            master=err,
            text="Not all fields are filled!",
            font=("Roboto", 16),
            text_color="#f11",
        ).place(relx=0.5, rely=0.5, anchor="center")
        return False

    try:
        cursor.execute(
            f'insert into rooms (uid, room_name, room_banner, room_card) values ("{uid}", "{room_name}", "{store_image(banner_loc)}", "{store_image(card_loc)}")'
        )

        db.commit()

        window.destroy()
        refresh_callback(fetch_rooms(cursor))

    except mysql.connector.Error as err:
        return print(err)

    return True


def handle_sql_edit(
    window, db, cursor, uid, room_name, banner_loc, card_loc, refresh_callback
):
    if not (len(uid) or len(room_name)):
        err = ctk.CTkToplevel(window)
        err.title("Urban Utopia Admin - Error")
        err.geometry("200x100")
        ctk.CTkLabel(
            master=err,
            text="Not all fields are filled!",
            font=("Roboto", 16),
            text_color="#f11",
        ).place(relx=0.5, rely=0.5, anchor="center")

    try:
        cursor.execute(
            f'update rooms set room_name="{room_name}", room_banner="{store_image(banner_loc)}", room_card="{store_image(card_loc)}" where uid="{uid}"'
        )

        db.commit()

        window.destroy()
        refresh_callback(fetch_rooms(cursor))

    except mysql.connector.Error as err:
        return print(err)

    return True


def handle_sql_delete(db, cursor, uid, refresh_callback):
    try:
        cursor.execute(f'delete from rooms where uid="{uid}"')

        db.commit()
        refresh_callback(fetch_rooms(cursor))

    except mysql.connector.Error as err:
        return print(err)

    return True


def edit_room(win, db, cursor, uid, refresh_callback):
    window = ctk.CTkToplevel()
    window.transient(win)
    window.title("Ubran Utopia Admin - Update Room")
    window.geometry("500x500")

    uid, room_name, room_banner, room_card = fetch_room_by_id(cursor, uid)

    form_frame = ctk.CTkFrame(master=window, width=400, fg_color="transparent")

    ctk.CTkLabel(
        master=form_frame, text="Update Room", font=("Roboto", 16, "bold")
    ).grid(row=0, column=1, sticky="we")

    id_label = ctk.CTkLabel(master=form_frame, text="ID", font=("Roboto", 14))
    id_entry = ctk.CTkEntry(
        master=form_frame,
        placeholder_text=str(uid),
        width=400,
        height=40,
        font=("Roboto", 16),
    )
    id_entry.configure(state="disabled")
    id_label.grid(row=1, column=1, sticky="w")
    id_entry.grid(row=2, column=1, sticky="we")

    room_name_label = ctk.CTkLabel(
        master=form_frame, text="Room Name", font=("Roboto", 14)
    )
    room_name_entry = ctk.CTkEntry(
        master=form_frame, width=400, height=40, font=("Roboto", 16)
    )
    room_name_entry.insert(0, room_name)
    room_name_label.grid(row=4, column=1, sticky="w")
    room_name_entry.grid(row=5, column=1, sticky="we")

    def get_image(store, callback):
        store.set(askopenfilename(filetypes=[("Image Files", ".png .jpg .jpeg")]))
        callback(store.get())

    room_banner_label = ctk.CTkLabel(master=form_frame, text="Banner")
    banner_select = ctk.CTkFrame(master=form_frame, fg_color="transparent")
    room_banner_preview, prev_banner_set = ImagePreview(banner_select, 50, room_banner)

    banner_loc_store = ctk.StringVar(value=room_banner, name="banner_loc_store")

    room_banner_button = ctk.CTkButton(
        master=banner_select,
        text="Select Image",
        width=100,
        height=40,
        font=("Roboto", 16),
        command=lambda: get_image(banner_loc_store, prev_banner_set),
    )
    room_banner_label.grid(row=7, column=1, sticky="w")

    room_banner_preview.grid(row=1, column=1, sticky="w")
    room_banner_button.grid(row=1, column=2, sticky="w")

    banner_select.grid(row=8, column=1, sticky="w")

    #############

    room_card_label = ctk.CTkLabel(master=form_frame, text="Card")
    card_select = ctk.CTkFrame(master=form_frame, fg_color="transparent")
    room_card_preview, prev_card_set = ImagePreview(card_select, 50, room_card)

    card_loc_store = ctk.StringVar(value=room_card, name="card_loc_store")

    room_card_button = ctk.CTkButton(
        master=card_select,
        text="Select Image",
        width=100,
        height=40,
        font=("Roboto", 16),
        command=lambda: get_image(card_loc_store, prev_card_set),
    )

    room_card_label.grid(row=10, column=1, sticky="w")

    room_card_preview.grid(row=1, column=1, sticky="w")
    room_card_button.grid(row=1, column=2, sticky="w")

    card_select.grid(row=11, column=1, sticky="w")

    ##########

    submit = ctk.CTkButton(
        master=form_frame,
        text="Update",
        height=40,
        text_color="#ffffff",
        command=lambda: handle_sql_edit(
            window,
            db,
            cursor,
            str(uid),
            room_name_entry.get().strip(),
            banner_loc_store.get().strip(),
            card_loc_store.get().strip(),
            refresh_callback,
        ),
    )

    submit.grid(row=13, column=1, sticky="we")

    for i in [3, 6, 9, 12]:
        form_frame.rowconfigure(i, minsize=20)

    form_frame.place(relx=0.5, rely=0.5, anchor="center")


def create_room(win, db, cursor, refresh_callback):
    window = ctk.CTkToplevel()
    window.transient(win)
    window.title("Ubran Utopia Admin - Create Room")
    window.geometry("500x500")

    uid = uuid.uuid4()  # generate universal unique identifier

    form_frame = ctk.CTkFrame(master=window, width=400, fg_color="transparent")

    ctk.CTkLabel(
        master=form_frame, text="Create Room", font=("Roboto", 16, "bold")
    ).grid(row=0, column=1, sticky="we")

    id_label = ctk.CTkLabel(master=form_frame, text="ID", font=("Roboto", 14))
    id_entry = ctk.CTkEntry(
        master=form_frame,
        placeholder_text=str(uid),
        width=400,
        height=40,
        font=("Roboto", 16),
    )
    id_entry.configure(state="disabled")
    id_label.grid(row=1, column=1, sticky="w")
    id_entry.grid(row=2, column=1, sticky="we")

    room_name_label = ctk.CTkLabel(
        master=form_frame, text="Room Name", font=("Roboto", 14)
    )
    room_name_entry = ctk.CTkEntry(
        master=form_frame, width=400, height=40, font=("Roboto", 16)
    )
    room_name_label.grid(row=4, column=1, sticky="w")
    room_name_entry.grid(row=5, column=1, sticky="we")

    def get_image(store, callback):
        store.set(askopenfilename(filetypes=[("Image Files", ".png .jpg .jpeg")]))
        callback(store.get())

    room_banner_label = ctk.CTkLabel(master=form_frame, text="Banner")
    banner_select = ctk.CTkFrame(master=form_frame, fg_color="transparent")
    room_banner_preview, prev_banner_set = ImagePreview(banner_select, 50, None)

    banner_loc_store = ctk.StringVar(value="", name="banner_loc_store")

    room_banner_button = ctk.CTkButton(
        master=banner_select,
        text="Select Image",
        width=100,
        height=40,
        font=("Roboto", 16),
        command=lambda: get_image(banner_loc_store, prev_banner_set),
    )
    room_banner_label.grid(row=7, column=1, sticky="w")

    room_banner_preview.grid(row=1, column=1, sticky="w")
    room_banner_button.grid(row=1, column=2, sticky="w")

    banner_select.grid(row=8, column=1, sticky="w")

    #############

    room_card_label = ctk.CTkLabel(master=form_frame, text="Card")
    card_select = ctk.CTkFrame(master=form_frame, fg_color="transparent")
    room_card_preview, prev_card_set = ImagePreview(card_select, 50, None)

    card_loc_store = ctk.StringVar(value="", name="card_loc_store")

    room_card_button = ctk.CTkButton(
        master=card_select,
        text="Select Image",
        width=100,
        height=40,
        font=("Roboto", 16),
        command=lambda: get_image(card_loc_store, prev_card_set),
    )

    room_card_label.grid(row=10, column=1, sticky="w")

    room_card_preview.grid(row=1, column=1, sticky="w")
    room_card_button.grid(row=1, column=2, sticky="w")

    card_select.grid(row=11, column=1, sticky="w")

    ##########

    submit = ctk.CTkButton(
        master=form_frame,
        text="Create Room",
        height=40,
        text_color="#ffffff",
        command=lambda: handle_sql_create(
            window,
            db,
            cursor,
            str(uid),
            room_name_entry.get().strip(),
            banner_loc_store.get().strip(),
            card_loc_store.get().strip(),
            refresh_callback,
        ),
    )

    submit.grid(row=13, column=1, sticky="we")

    for i in [3, 6, 9, 12]:
        form_frame.rowconfigure(i, minsize=20)

    form_frame.place(relx=0.5, rely=0.5, anchor="center")


def RoomsPage(win, db, cursor):
    page = ctk.CTkFrame(
        master=win, width=1280, height=720, bg_color="#ececec", fg_color="#ececec"
    )
    page.pack_propagate(0)

    ## Create Table Component
    action_row = ctk.CTkFrame(master=page, fg_color="#ececec", width=900, height=50)
    page.window = win

    table, refersh_callback = Table(
        page,
        "Rooms",
        [
            ("ID", 300),
            ("Room Name", 300),
            ("[IMAGE]Banner", 100),
            ("[IMAGE]Card", 100),
        ],
        fetch_rooms(cursor),
        edit_room,
        handle_sql_delete,
        db,
        cursor,
        null_data_text="No Rooms Found",
        row_height=50,
    )

    title = ctk.CTkLabel(master=action_row, text="Rooms", font=("Roboto", 20))
    add_room = ctk.CTkButton(
        master=action_row,
        text="+  Add Room",
        command=lambda: create_room(win, db, cursor, refersh_callback),
    )

    def reload_func():
        return refersh_callback(fetch_rooms(cursor))

    refresh = ctk.CTkButton(
        master=action_row,
        text="",
        width=25,
        height=25,
        fg_color="#ececec",
        hover_color="#ececec",
        image=load_image_ctk("./assets/reload_icon.png", (25, 25)),
        command=reload_func,
    )

    backbtn = ctk.CTkButton(
        master=action_row,
        text="",
        width=25,
        height=25,
        fg_color="#ececec",
        hover_color="#ececec",
        image=load_image_ctk("./assets/back_icon.png", (10, 19)),
        command=lambda: win.nav.navigate_to("tableselect"),
    )

    backbtn.place(relx=0, rely=0.03, anchor="nw")
    title.place(relx=0.05, rely=0, anchor="nw")
    refresh.place(relx=0.845, rely=0, anchor="ne")
    add_room.place(relx=1, rely=0, anchor="ne")

    # spacing
    ctk.CTkLabel(master=page, text="").pack(pady=10)
    action_row.pack(pady=10)

    table.pack(pady=10)

    return "rooms", page
