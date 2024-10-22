import customtkinter as ctk
from widgets.image import ImageWidget, load_image_ctk
from sql.api import fetch_design_by_id, fetch_room_by_id, fetch_style_by_id
import pickle

def InterestedPage(win):
    page = ctk.CTkFrame(master=win, width=1280, height=720)
    interested = pickle.load(open("interested", "rb"))

    def onmount():
        nonlocal interested
        win.title("Urban Utopia - Interested Designs")
        interested = pickle.load(open("interested", "rb"))

    page_title = ctk.CTkLabel(master=page, text="Interested Designs", font=("Merriweather", 32))
    frame = ctk.CTkFrame(master=page, fg_color="#e5e5e5")

    w = ctk.CTkScrollbar(master=frame)
    
    for design_id in interested:
        uid, design_name, design_img, roomId, styleId = fetch_design_by_id(design_id)
        _, room_name, _, _ = fetch_room_by_id(roomId)
        _, style_name, _ = fetch_style_by_id(styleId)

        interested_frame = ctk.CTkFrame(master=frame, width=700, fg_color="#d9d9d9")
        interested_frame.grid_propagate(False)
        img, size = load_image_ctk(design_img, (0, 200), ret_size=True)
        img = ctk.CTkLabel(
            master=interested_frame,
            text="",
            image=img,
        )
        img.grid(row=1, column=1, sticky="w")

        data_frame = ctk.CTkFrame(master=interested_frame, fg_color="#d9d9d9")

        def remove():
            data = []
            with open("interested", "rb") as f:
                data = pickle.load(f)
            
            with open("interested", "wb") as f:
                data.pop(data.index(uid))
                pickle.dump(data, f)

            interested_frame.destroy()

        remove_from_interested = ctk.CTkButton(master=data_frame, text="Remove From Interested", command=remove)
        
        design_name = ctk.CTkLabel(master=data_frame, text=design_name,  font=("Merriweather", 28))
        design_room_style = ctk.CTkLabel(master=data_frame, text=f"{style_name} {room_name}", font=("Merriweather", 20))

        design_name.grid(row=1, column=1, sticky="w")
        design_room_style.grid(row=2,column=1, sticky="w")
        remove_from_interested.grid(row=3, column=1, sticky="w")
        data_frame.grid(row=1, column=2, sticky="w", padx=10)
        
        interested_frame.pack(anchor="w", pady=10, padx=10)


    back = ctk.CTkButton(
        master=page,
        text="< Back",
        font=("Merriweather", 15),
        width=100,
        height=35,
        command=lambda: win.nav.navigate_to("welcome"),
        bg_color="#EAC7C5",
        fg_color="#f95959",
        hover_color="#e15151",
        background_corner_colors=("#EAC7C5",)*4
    )
    back.place(relx=0.91, rely=0.02, anchor="nw")
    
    frame.pack_propagate(True)
    page.pack_propagate(False)

    page_title.pack(pady=20)
    frame.pack()

    return "interested", page, onmount, lambda: None
