import customtkinter as ctk
from widgets.image import load_image_ctk
from widgets.image_preview import ImagePreview


def Table(
    parent,
    table_title,
    column_headers,
    data,
    edit_callback,
    delete_callback,
    db,
    cursor,
    null_data_text="No Data Provided",
    row_height=30,
    corner_radius=8,
    header_row_color="#243142",
    table_background="#ECECEC",
    header_row_text="#FFFFFF",
    row_colors=["#DFDFDF"],
    text_colors=["#111111"],
):
    table = ctk.CTkFrame(
        master=parent,
    )

    column_headers.extend([("[ACTION]", 50), ("[ACTION]", 50)])

    image_columns = []

    for i, header in enumerate(column_headers):
        column_header, width = header
        table.columnconfigure(i, minsize=width)

        if column_header[:7] == "[IMAGE]":
            column_header = column_header[7:]
            image_columns.append(i)

        element = ctk.CTkFrame(
            master=table,
            width=width,
            height=row_height,
            fg_color=header_row_color,
            corner_radius=corner_radius,
            background_corner_colors=(
                table_background if i == 0 else header_row_color,
                table_background if i == len(column_headers) - 1 else header_row_color,
                header_row_color,
                header_row_color,
            ),
        )

        element.pack_propagate(0)

        if not column_header == "[ACTION]":
            label = ctk.CTkLabel(
                master=element, text=column_header, text_color=header_row_text
            )
            label.place(relx=0.5, rely=0.5, anchor="center")

        element.grid(row=0, column=i)

    def refresh_callback(data):
        header_ptr = 0
        edit_img = load_image_ctk("./assets/edit_icon.png", (30, 30))
        del_img = load_image_ctk("./assets/delete_icon.png", (30, 30))

        for _, child in table.children.items():
            header_ptr += 1

            if header_ptr > len(column_headers) + 1:
                child.grid_forget()
                del child

        if len(data) == 0:
            no_data_row = ctk.CTkFrame(
                master=table,
                fg_color=row_colors[0],
                height=row_height,
                corner_radius=corner_radius,
                background_corner_colors=(
                    row_colors[0],
                    row_colors[0],
                    table_background,
                    table_background,
                ),
            )
            no_data_row.pack_propagate(0)

            label = ctk.CTkLabel(
                master=no_data_row, text=null_data_text, text_color=text_colors[0]
            )
            label.place(relx=0.5, rely=0.5, anchor="center")

            no_data_row.grid(
                row=1, column=0, columnspan=len(column_headers), sticky="ew"
            )

        row_color_index = 0
        if len(text_colors) > 1 and len(row_colors) != len(text_colors):
            raise ValueError("Length of text color must match row color!")

        for y, row in enumerate(data):
            id_obj = {}

            for x, column in enumerate(row):
                if x == 0:
                    id_obj["id"] = column

                row_frame = ctk.CTkFrame(
                    master=table,
                    height=row_height,
                    width=0,
                    fg_color=row_colors[row_color_index],
                    corner_radius=corner_radius,
                    background_corner_colors=(
                        row_colors[row_color_index],
                        row_colors[row_color_index],
                        row_colors[row_color_index],
                        table_background
                        if y == len(data) - 1 and x == 0
                        else row_colors[row_color_index],
                    ),
                )
                

                if x in image_columns:
                    row_data, _ = ImagePreview(
                        row_frame, width - 20, column, bg=row_colors[row_color_index]
                    )

                else:
                    row_data = ctk.CTkLabel(
                        master=row_frame,
                        text=column,
                        text_color=text_colors[row_color_index]
                        if len(text_colors) > 1
                        else text_colors[0],
                    )

                row_data.place(relx=0.5, rely=0.5, anchor="center")

                row_frame.grid(column=x, row=y + 1, sticky="ew")

                row_color_index += 1
                if row_color_index > len(row_colors) - 1:
                    row_color_index = 0

                if x == len(column_headers) - 3:
                    break

            nonlocal parent
            edit_btn = ctk.CTkButton(
                master=table,
                image=edit_img,
                width=50,
                height=50,
                text="",
                fg_color=row_colors[row_color_index],
                corner_radius=0,
                hover_color=row_colors[row_color_index],
                command=lambda x=id_obj["id"]: edit_callback(
                    parent, db, cursor, x, refresh_callback
                ),
            )
            delete_btn = ctk.CTkButton(
                master=table,
                image=del_img,
                width=50,
                height=50,
                text="",
                fg_color=row_colors[row_color_index],
                corner_radius=corner_radius,
                hover_color=row_colors[row_color_index],
                background_corner_colors=(
                    row_colors[row_color_index],
                    row_colors[row_color_index],
                    table_background
                    if y == len(data) - 1
                    else row_colors[row_color_index],
                    row_colors[row_color_index],
                ),
                command=lambda x=id_obj["id"]: delete_callback(
                    db, cursor, x, refresh_callback
                ),
            )

            edit_btn.grid(column=x + 1, row=y + 1)
            delete_btn.grid(column=x + 2, row=y + 1)

    refresh_callback(data)

    return table, refresh_callback
