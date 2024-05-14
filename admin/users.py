import customtkinter as ctk
from widgets.table import Table
from widgets.image import load_image_ctk
import uuid
import mysql.connector
from utils import encrypt

# Table Schema:
#   uid varchar(36) not null primary key,
#   name varchar(255) not null,
#   email varchar(255) not null unique,
#   password varchar(255) not null,


def fetch_users(cursor):
    cursor.execute("select * from users")
    return cursor.fetchall()


def fetch_user_by_id(cursor, id):
    cursor.execute(f"select * from users where uid='{id}'")
    return cursor.fetchone()


def handle_sql_create(window, db, cursor, uid, name, email, password, refresh_callback):
    if not (len(uid) or len(name) or len(email) or len(password)):
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
            f'insert into users (uid, name, email, password) values ("{uid}", "{name}", "{email}", "{encrypt(password)}")'
        )

        db.commit()

        window.destroy()
        refresh_callback(fetch_users(cursor))

    except mysql.connector.Error as err:
        return print(err)

    return True


def handle_sql_edit(window, db, cursor, uid, name, email, password, refresh_callback):
    if not (len(uid) or len(name) or len(email) or len(password)):
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
            f'update users set name="{name}", email="{email}", password="{password}" where uid="{uid}"'
        )

        db.commit()

        window.destroy()
        refresh_callback(fetch_users(cursor))

    except mysql.connector.Error as err:
        return print(err)

    return True


def handle_sql_delete(db, cursor, uid, refresh_callback):
    try:
        cursor.execute(f'delete from users where uid="{uid}"')

        db.commit()
        refresh_callback(fetch_users(cursor))

    except mysql.connector.Error as err:
        return print(err)

    return True


def edit_user(_, db, cursor, _id, refresh_callback):
    window = ctk.CTkToplevel()
    window.title("Ubran Utopia Admin - Edit User")
    window.geometry("500x500")

    uid, name, email, password = fetch_user_by_id(cursor, _id)

    form_frame = ctk.CTkFrame(master=window, width=400, fg_color="transparent")

    ctk.CTkLabel(master=form_frame, text="Edit User", font=("Roboto", 16, "bold")).grid(
        row=0, column=1, sticky="we"
    )

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

    name_label = ctk.CTkLabel(master=form_frame, text="Name", font=("Roboto", 14))
    name_entry = ctk.CTkEntry(
        master=form_frame, width=400, height=40, font=("Roboto", 16)
    )
    name_entry.insert(0, name)
    name_label.grid(row=4, column=1, sticky="w")
    name_entry.grid(row=5, column=1, sticky="we")

    email_label = ctk.CTkLabel(master=form_frame, text="Email", font=("Roboto", 14))
    email_entry = ctk.CTkEntry(
        master=form_frame, width=400, height=40, font=("Roboto", 16)
    )
    email_entry.insert(0, email)
    email_label.grid(row=7, column=1, sticky="w")
    email_entry.grid(row=8, column=1, sticky="we")

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
            name_entry.get().strip(),
            email_entry.get().strip(),
            password,
            refresh_callback,
        ),
    )

    submit.grid(row=13, column=1, sticky="we")

    for i in [3, 6, 9, 12]:
        form_frame.rowconfigure(i, minsize=20)

    form_frame.place(relx=0.5, rely=0.5, anchor="center")


def create_user(db, cursor, refresh_callback):
    window = ctk.CTkToplevel()
    window.title("Ubran Utopia Admin - Create User")
    window.geometry("500x500")

    uid = uuid.uuid4()  # generate universal unique identifier

    form_frame = ctk.CTkFrame(master=window, width=400, fg_color="transparent")

    ctk.CTkLabel(
        master=form_frame, text="Create User", font=("Roboto", 16, "bold")
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

    name_label = ctk.CTkLabel(master=form_frame, text="Name", font=("Roboto", 14))
    name_entry = ctk.CTkEntry(
        master=form_frame, width=400, height=40, font=("Roboto", 16)
    )
    name_label.grid(row=4, column=1, sticky="w")
    name_entry.grid(row=5, column=1, sticky="we")

    email_label = ctk.CTkLabel(master=form_frame, text="Email", font=("Roboto", 14))
    email_entry = ctk.CTkEntry(
        master=form_frame, width=400, height=40, font=("Roboto", 16)
    )
    email_label.grid(row=7, column=1, sticky="w")
    email_entry.grid(row=8, column=1, sticky="we")

    password_label = ctk.CTkLabel(
        master=form_frame, text="Password", font=("Roboto", 14)
    )
    password_entry = ctk.CTkEntry(
        master=form_frame, width=400, height=40, font=("Roboto", 16)
    )
    password_label.grid(row=10, column=1, sticky="w")
    password_entry.grid(row=11, column=1, sticky="we")

    submit = ctk.CTkButton(
        master=form_frame,
        text="Create User",
        height=40,
        text_color="#ffffff",
        command=lambda: handle_sql_create(
            window,
            db,
            cursor,
            str(uid),
            name_entry.get().strip(),
            email_entry.get().strip(),
            password_entry.get().strip(),
            refresh_callback,
        ),
    )

    submit.grid(row=13, column=1, sticky="we")

    for i in [3, 6, 9, 12]:
        form_frame.rowconfigure(i, minsize=20)

    form_frame.place(relx=0.5, rely=0.5, anchor="center")


def UsersPage(win, db, cursor):
    page = ctk.CTkFrame(
        master=win, width=1280, height=720, bg_color="#ececec", fg_color="#ececec"
    )
    page.pack_propagate(0)

    ## Create Table Component
    action_row = ctk.CTkFrame(master=page, fg_color="#ececec", width=900, height=50)

    table, refersh_callback = Table(
        page,
        "Users",
        [
            ("ID", 300),
            ("Name", 300),
            ("Email", 300),
        ],
        fetch_users(cursor),
        edit_user,
        handle_sql_delete,
        db,
        cursor,
        null_data_text="No Users Found",
        row_height=50,
    )

    title = ctk.CTkLabel(master=action_row, text="Users", font=("Roboto", 20))
    add_user = ctk.CTkButton(
        master=action_row,
        text="+  Add User",
        command=lambda: create_user(db, cursor, refersh_callback),
    )

    def reload_func():
        return refersh_callback(fetch_users(cursor))

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
    add_user.place(relx=1, rely=0, anchor="ne")

    # spacing
    ctk.CTkLabel(master=page, text="").pack(pady=10)
    action_row.pack(pady=10)

    table.pack(pady=10)

    return "users", page
