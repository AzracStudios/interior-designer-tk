import uuid

import mysql.connector
import customtkinter as ctk
from tkinter.filedialog import askopenfilename


from sql.api import store_image

from widgets.table import Table
from widgets.image import load_image_ctk
from widgets.image_preview import ImagePreview
from widgets.dropselect import DropSelect

# Table Schema:
# uid varchar(36) not null,
# design_name varchar(255) not null unique,
# design_img varchar(255) not null unique,
# roomId varchar(36) not null,
# styleId varchar(36) not null,


def fetch_designs(cursor):
    cursor.execute("select * from designs")
    return cursor.fetchall()


def fetch_design_by_id(cursor, id):
    cursor.execute(f"select * from designs where uid='{id}'")
    return cursor.fetchone()


def handle_sql_create(
    window,
    db,
    cursor,
    uid,
    design_name,
    design_img,
    room_id,
    style_id,
    refresh_callback,
):
    if not (
        len(uid) or len(design_name) or len(design_img) or len(room_id) or len(style_id)
    ):
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
            f"insert into designs (uid, design_name, design_img, roomID, styleID) values ('{uid}', '{design_name}', '{store_image(design_img)}', '{room_id}', '{style_id}')"
        )

        db.commit()

        window.destroy()
        refresh_callback(fetch_designs(cursor))

    except mysql.connector.Error as err:
        return print(err)

    return True


def handle_sql_edit(
    window,
    db,
    cursor,
    uid,
    design_name,
    design_img,
    room_id,
    style_id,
    refresh_callback,
):
    if not (
        len(uid) or len(design_name) or len(design_img) or len(room_id) or len(style_id)
    ):
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
            f"update designs set design_name='{design_name}', design_img='{store_image(design_img)}', roomID='{room_id}', styleID='{style_id}' where uid='{uid}'"
        )

        db.commit()

        window.destroy()
        refresh_callback(fetch_designs(cursor))

    except mysql.connector.Error as err:
        return print(err)

    return True


def handle_sql_delete(db, cursor, uid, refresh_callback):
    try:
        cursor.execute(f'delete from designs where uid="{uid}"')

        db.commit()
        refresh_callback(fetch_designs(cursor))

    except mysql.connector.Error as err:
        return print(err)

    return True


def edit_user(win, db, cursor, _id, refresh_callback):
    window = ctk.CTkToplevel()
    window.title("Ubran Utopia Admin - Edit Design")
    window.geometry("500x550")
    window.transient(win)

    uid, dname, dimage, roomid, styleid = fetch_design_by_id(
        cursor, _id
    )  # generate universal unique identifier

    form_frame = ctk.CTkFrame(master=window, width=400, fg_color="transparent")

    ctk.CTkLabel(
        master=form_frame, text="Edit Design", font=("Roboto", 16, "bold")
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

    design_name_label = ctk.CTkLabel(
        master=form_frame, text="Design Name", font=("Roboto", 14)
    )
    design_name_entry = ctk.CTkEntry(
        master=form_frame, width=400, height=40, font=("Roboto", 16)
    )
    design_name_entry.insert(0, dname)
    design_name_label.grid(row=4, column=1, sticky="w")
    design_name_entry.grid(row=5, column=1, sticky="we")

    def get_image(store, callback):
        store.set(askopenfilename(filetypes=[("Image Files", ".png .jpg .jpeg")]))
        callback(store.get())

    design_image_label = ctk.CTkLabel(master=form_frame, text="Banner")
    design_image_select = ctk.CTkFrame(master=form_frame, fg_color="transparent")
    design_image_preview, design_preview_set = ImagePreview(
        design_image_select, 50, dimage
    )

    designe_image_store = ctk.StringVar(value=dimage, name="design_image_store")

    design_image_button = ctk.CTkButton(
        master=design_image_select,
        text="Select Image",
        width=100,
        height=40,
        font=("Roboto", 16),
        command=lambda: get_image(designe_image_store, design_preview_set),
    )

    design_image_preview.grid(row=1, column=1, sticky="w")
    design_image_button.grid(row=1, column=2, sticky="w")

    design_image_label.grid(row=7, column=1, sticky="w")
    design_image_select.grid(row=8, column=1, sticky="w")

    room_var = ctk.StringVar(master=form_frame)
    room_select, room_name_id_map = DropSelect(
        form_frame,
        cursor,
        "Room",
        "rooms",
        "uid",
        "room_name",
        room_var,
    )

    room_var.set(
        list(room_name_id_map.keys())[list(room_name_id_map.values()).index(roomid)]
    )

    room_select.grid(row=10, column=1, sticky="w", rowspan=2)

    style_var = ctk.StringVar(master=form_frame)
    style_select, style_name_id_map = DropSelect(
        form_frame,
        cursor,
        "Style",
        "styles",
        "uid",
        "style_name",
        style_var,
    )

    style_select.grid(row=13, column=1, sticky="w", rowspan=2)

    style_var.set(
        list(style_name_id_map.keys())[list(style_name_id_map.values()).index(styleid)]
    )

    submit = ctk.CTkButton(
        master=form_frame,
        text="Edit Design",
        height=40,
        text_color="#ffffff",
        command=lambda: handle_sql_edit(
            window,
            db,
            cursor,
            str(uid),
            design_name_entry.get().strip(),
            designe_image_store.get(),
            room_name_id_map[room_var.get()],
            style_name_id_map[style_var.get()],
            refresh_callback,
        ),
    )

    submit.grid(row=16, column=1, sticky="we")

    for i in [3, 6, 9, 12, 15]:
        form_frame.rowconfigure(i, minsize=20)

    form_frame.place(relx=0.5, rely=0.5, anchor="center")


def create_design(win, db, cursor, refresh_callback):
    window = ctk.CTkToplevel()
    window.title("Ubran Utopia Admin - Create Design")
    window.geometry("500x550")
    window.transient(win)

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

    design_name_label = ctk.CTkLabel(
        master=form_frame, text="Design Name", font=("Roboto", 14)
    )
    design_name_entry = ctk.CTkEntry(
        master=form_frame, width=400, height=40, font=("Roboto", 16)
    )
    design_name_label.grid(row=4, column=1, sticky="w")
    design_name_entry.grid(row=5, column=1, sticky="we")

    def get_image(store, callback):
        store.set(askopenfilename(filetypes=[("Image Files", ".png .jpg .jpeg")]))
        callback(store.get())

    design_image_label = ctk.CTkLabel(master=form_frame, text="Banner")
    design_image_select = ctk.CTkFrame(master=form_frame, fg_color="transparent")
    design_image_preview, design_preview_set = ImagePreview(
        design_image_select, 50, None
    )

    designe_image_store = ctk.StringVar(value="", name="design_image_store")

    design_image_button = ctk.CTkButton(
        master=design_image_select,
        text="Select Image",
        width=100,
        height=40,
        font=("Roboto", 16),
        command=lambda: get_image(designe_image_store, design_preview_set),
    )

    design_image_preview.grid(row=1, column=1, sticky="w")
    design_image_button.grid(row=1, column=2, sticky="w")

    design_image_label.grid(row=7, column=1, sticky="w")
    design_image_select.grid(row=8, column=1, sticky="w")

    room_var = ctk.StringVar(master=form_frame)
    room_select, room_name_id_map = DropSelect(
        form_frame, cursor, "Room", "rooms", "uid", "room_name", room_var
    )

    room_select.grid(row=10, column=1, sticky="w", rowspan=2)

    style_var = ctk.StringVar(master=form_frame)
    style_select, style_name_id_map = DropSelect(
        form_frame, cursor, "Style", "styles", "uid", "style_name", style_var
    )

    style_select.grid(row=13, column=1, sticky="w", rowspan=2)

    submit = ctk.CTkButton(
        master=form_frame,
        text="Create Design",
        height=40,
        text_color="#ffffff",
        command=lambda: handle_sql_create(
            window,
            db,
            cursor,
            str(uid),
            design_name_entry.get().strip(),
            designe_image_store.get(),
            room_name_id_map[room_var.get()],
            style_name_id_map[style_var.get()],
            refresh_callback,
        ),
    )

    submit.grid(row=16, column=1, sticky="we")

    for i in [3, 6, 9, 12, 15]:
        form_frame.rowconfigure(i, minsize=20)

    form_frame.place(relx=0.5, rely=0.5, anchor="center")


def DesignsPage(win, db, cursor):
    page = ctk.CTkFrame(
        master=win, width=1280, height=720, bg_color="#ececec", fg_color="#ececec"
    )
    page.pack_propagate(0)

    ## Create Table Component
    action_row = ctk.CTkFrame(master=page, fg_color="#ececec", width=900, height=50)

    table, refersh_callback = Table(
        page,
        "designs",
        [
            ("ID", 300),
            ("Name", 300),
            ("[IMAGE]Image", 100),
            ("[GETNAME:room_name,rooms]Room", 100),
            ("[GETNAME:style_name,styles]Styles", 100),
        ],
        fetch_designs(cursor),
        edit_user,
        handle_sql_delete,
        db,
        cursor,
        null_data_text="No Designs Found",
        row_height=50,
    )

    title = ctk.CTkLabel(master=action_row, text="Designs", font=("Roboto", 20))
    add_user = ctk.CTkButton(
        master=action_row,
        text="+  Add Design",
        command=lambda: create_design(win, db, cursor, refersh_callback),
    )

    def reload_func():
        return refersh_callback(fetch_designs(cursor))

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

    return "designs", page
