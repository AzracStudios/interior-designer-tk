import customtkinter as ctk
from widgets.table import Table
from widgets.image import load_image_ctk, Image
from sql.api import store_image
import uuid
import mysql.connector
from tkinter.filedialog import askopenfilename

from widgets.image_preview import ImagePreview

# Table Schema:
#   uid varchar(36) not null primary key,
#   style_name varchar(255) not null unique,
#   style_desc varchar(255) not null,
#   style_banner varchar(255) not null

def fetch_styles(cursor):
    cursor.execute("select * from styles")
    return cursor.fetchall()


def fetch_style_by_id(cursor, id):
    cursor.execute(f"select * from styles where uid='{id}'")
    return cursor.fetchone()


def handle_sql_create(
    window, db, cursor, uid, style_name, style_desc, refresh_callback
):
    if not (
        len(uid) > 0
        and len(style_name) > 0
    ):
        print("hi")
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
            f'insert into styles (uid, style_name, style_desc) values ("{uid}", "{style_name}",  "{style_desc}")'
        )

        db.commit()

        window.destroy()
        refresh_callback(fetch_styles(cursor))

    except mysql.connector.Error as err:
        return print(err)

    return True


def handle_sql_edit(
    window, db, cursor, uid, style_name, style_desc, refresh_callback
):
    if not (len(uid) or len(style_name) or len(style_desc)):
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
            f'update styles set style_name="{style_name}", style_desc="{style_desc}" where uid="{uid}"'
        )

        db.commit()

        window.destroy()
        refresh_callback(fetch_styles(cursor))

    except mysql.connector.Error as err:
        return print(err)

    return True



def handle_sql_delete(db, cursor, uid, refresh_callback):
    try:
        cursor.execute(f'delete from styles where uid="{uid}"')

        db.commit()
        refresh_callback(fetch_styles(cursor))

    except mysql.connector.Error as err:
        return print(err)

    return True

def edit_style(win, db, cursor, uid, refresh_callback):
    window = ctk.CTkToplevel()
    window.transient(win)
    window.title("Ubran Utopia Admin - Update Styles")
    window.geometry("500x500")

    uid, style_name, style_desc = fetch_style_by_id(cursor, uid)

    form_frame = ctk.CTkFrame(master=window, width=400, fg_color="transparent")

    ctk.CTkLabel(
        master=form_frame, text="Update Styles", font=("Roboto", 16, "bold")
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

    style_name_label = ctk.CTkLabel(
        master=form_frame, text="Style Name", font=("Roboto", 14)
    )
    style_name_entry = ctk.CTkEntry(
        master=form_frame, width=400, height=40, font=("Roboto", 16)
    )
    style_name_entry.insert(0, style_name)
    style_name_label.grid(row=4, column=1, sticky="w")
    style_name_entry.grid(row=5, column=1, sticky="we")

    ####

    style_desc_label = ctk.CTkLabel(
        master=form_frame, text="Style Description", font=("Roboto", 14)
    )
    style_desc_entry = ctk.CTkEntry(
        master=form_frame, width=400, height=40, font=("Roboto", 16)
    )
    style_desc_entry.insert(0, style_desc)
    style_desc_label.grid(row=7, column=1, sticky="w")
    style_desc_entry.grid(row=8, column=1, sticky="we")

    
    #############

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
            style_name_entry.get().strip(),
            style_desc_entry.get().strip(),
            refresh_callback,
        ),
    )

    submit.grid(row=13, column=1, sticky="we")

    for i in [3, 6, 9, 12]:
        form_frame.rowconfigure(i, minsize=20)

    form_frame.place(relx=0.5, rely=0.5, anchor="center")


def create_style(win, db, cursor, refresh_callback):
    window = ctk.CTkToplevel()
    window.transient(win)
    window.title("Ubran Utopia Admin - Create Style")
    window.geometry("500x500")

    uid = uuid.uuid4()  # generate universal unique identifier

    form_frame = ctk.CTkFrame(master=window, width=400, fg_color="transparent")

    ctk.CTkLabel(
        master=form_frame, text="Create Style", font=("Roboto", 16, "bold")
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

    style_name_label = ctk.CTkLabel(
        master=form_frame, text="Style Name", font=("Roboto", 14)
    )
    style_name_entry = ctk.CTkEntry(
        master=form_frame, width=400, height=40, font=("Roboto", 16)
    )
    style_name_label.grid(row=4, column=1, sticky="w")
    style_name_entry.grid(row=5, column=1, sticky="we")

    style_desc_label = ctk.CTkLabel(
        master=form_frame, text="Style Description", font=("Roboto", 14)
    )
    style_desc_entry = ctk.CTkEntry(
        master=form_frame, width=400, height=40, font=("Roboto", 16)
    )
    style_desc_label.grid(row=7, column=1, sticky="w")
    style_desc_entry.grid(row=8, column=1, sticky="we")

    #############

    submit = ctk.CTkButton(
        master=form_frame,
        text="Create Style",
        height=40,
        text_color="#ffffff",
        command=lambda: handle_sql_create(
            window,
            db,
            cursor,
            str(uid),
            style_name_entry.get().strip(),
            style_desc_entry.get().strip(),
            refresh_callback,
        ),
    )

    submit.grid(row=13, column=1, sticky="we")

    for i in [3, 6, 9, 12]:
        form_frame.rowconfigure(i, minsize=20)

    form_frame.place(relx=0.5, rely=0.5, anchor="center")

def StylesPage(win, db, cursor):
    page = ctk.CTkFrame(
        master=win, width=1280, height=720, bg_color="#ececec", fg_color="#ececec"
    )
    page.pack_propagate(0)

    ## Create Table Component
    action_row = ctk.CTkFrame(master=page, fg_color="#ececec", width=900, height=50)
    page.window = win

    table, refersh_callback = Table(
        page,
        "Styles",
        [
            ("ID", 300),
            ("Style Name", 200),
            ("Style Description", 400),
        ],
        fetch_styles(cursor),
        edit_style,
        handle_sql_delete,
        db,
        cursor,
        null_data_text="No Styles Found",
        row_height=50,
    )

    title = ctk.CTkLabel(master=action_row, text="Styles", font=("Roboto", 20))
    add_style = ctk.CTkButton(
        master=action_row,
        text="+  Add Style",
        command=lambda: create_style(win, db, cursor, refersh_callback),
    )

    def reload_func():
        return refersh_callback(fetch_styles(cursor))

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
    add_style.place(relx=1, rely=0, anchor="ne")

    # spacing
    ctk.CTkLabel(master=page, text="").pack(pady=10)
    action_row.pack(pady=10)

    table.pack(pady=10)

    return "styles", page
