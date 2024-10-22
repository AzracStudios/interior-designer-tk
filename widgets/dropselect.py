import customtkinter as ctk


def DropSelect(parent, cursor, label, table, id_field, display_field, dropvar):
    cursor.execute(f"select {id_field}, {display_field} from {table}")
    data = cursor.fetchall()
    data_map = {}

    for uid, disp in data:
        data_map[disp] = uid

    drop_frame = ctk.CTkFrame(master=parent, width=400, fg_color="#f2f2f2")

    drop_label = ctk.CTkLabel(master=drop_frame, text=label)
    drop_label.grid(row=1, column=1, sticky="w")

    dropdown = ctk.CTkComboBox(
        master=drop_frame, values=data_map.keys(), variable=dropvar,
        width=400, height=40
    )

    dropdown.grid(row=2, column=1, sticky="w")

    return drop_frame, data_map
