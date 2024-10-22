import customtkinter as ctk
from sql.api import fetch_room_by_id, fetch_style_by_id, fetch_designs
from widgets.image import load_image_ctk
import pickle 

current_image_index = 0
image_widgets = []
images = []
add_to_interest = None
liked = []

def DesignPage(win):
    global current_image_index, image_widgets


    page = ctk.CTkFrame(master=win, width=1280, height=720)
    page.grid_propagate(0)

    image_height = 500

    def onmount():
        global actions_frame, image_name, image_widgets, current_image_index, images, liked, add_to_interest
        
        try:
            with open("interested", "rb") as f:
                liked = pickle.load(f)

        except:
            with open("interested", "wb") as f:
                pickle.dump([], f)
        
        image_widgets = []
        images = []
        current_image_index = 0

        win.title("Urban Utopia - Designs")
        room_name = fetch_room_by_id(win.room_id)[1]
        style_name = fetch_style_by_id(win.style_id)[1]

        title.configure(text=f"{style_name} {room_name}")

        res = fetch_designs(win.room_id, win.style_id)

        name = None

        for result in res:
            images.append((result[0], result[1], result[2]))

        for i, t in enumerate(images):
            uid, name, image = t
            img, size = load_image_ctk(image, (0, image_height), ret_size=True)

            image_widget = ctk.CTkLabel(
                master=images_frame,
                text="",
                image=img,
            )

            image_widgets.append((uid, image_widget, size, name))

        actions_frame = ctk.CTkFrame(
            master=page,
            width=1000,
            height=int((720 - image_height) / 2),
            fg_color="#e5e5e5",
        )
        actions_frame.place(relx=0.5, rely=0.88, anchor="center")

        image_name = ctk.CTkLabel(
            master=actions_frame,
            text=name,
            bg_color="#e5e5e5",
            font=("Merriweather", 20),
        )

        image_name.grid(row=1, column=1, sticky="w", pady=10)


        def interested():
            global liked
            try:
                with open("interested", "rb") as f:
                    liked = pickle.load(f)

                with open("interested", "wb") as f:
                    print(liked, image_widgets[current_image_index][0])
                    if (x:=image_widgets[current_image_index][0]) in liked:
                        liked.pop(liked.index(x))
                        add_to_interest.configure(text="Add To Interested")
                    else:
                        liked.append(image_widgets[current_image_index][0])
                        add_to_interest.configure(text="Remove From Interested")
                    pickle.dump(liked, f)
                
            except:
                with open("interested", "wb") as f:
                    pickle.dump([image_widgets[current_image_index][0]], f)
        

        add_to_interest = ctk.CTkButton(
            master=actions_frame,
            text="Add To Interested",
            bg_color="#EAC7C5",
            fg_color="#101621",
            hover_color="#101621",
            background_corner_colors=("#EAC7C5",) * 4,
            width=250,
            font=("Merriweather", 12),
            command=lambda: interested()
        )

        add_to_interest.grid(row=1, column=2, sticky="e", pady=10, padx=80)

        move_images(0)

    title = ctk.CTkLabel(master=page, text="", font=("Merriweather", 25))
    title.grid(row=1, column=2, sticky="we")

    back = ctk.CTkButton(
        master=page,
        text="< Back",
        font=("Merriweather", 15),
        width=100,
        height=35,
        command=lambda: win.nav.navigate_to("styleselect"),
        bg_color="#EAC7C5",
        fg_color="#101621",
        hover_color="#101621",
        background_corner_colors=("#EAC7C5",) * 4,
    )

    back.grid(row=1, column=1)

    images_frame = ctk.CTkFrame(
        master=page, width=1280, height=image_height, fg_color="#E5E5E5"
    )
    images_frame.place(relx=0.5, rely=0.5, anchor="center")

    def move_images(shift):
        global current_image_index, actions_frame, add_to_interest

        current_image_index += shift

        if current_image_index < 0:
            current_image_index = len(image_widgets) - 1

        if current_image_index > len(image_widgets) - 1:
            current_image_index = 0

        for i, t in enumerate(image_widgets):
            uid, image, size, name = t

            image.place(
                rely=0,
                relx=0.52 + i - (size[0] / 2400) - current_image_index,
                anchor="nw",
            )

            if i == current_image_index:
                image_name.configure(text=name)
                image_name.grid(row=1, column=1, sticky="w")
                print(liked)
                if uid in liked:
                    add_to_interest.configure(text="Remove From Interested")

                else:
                    add_to_interest.configure(text="Add To Interested")

    prev = ctk.CTkButton(
        master=page,
        text="<",
        command=lambda: move_images(-1),
        width=50,
        height=50,
    )

    fwd = ctk.CTkButton(
        master=page,
        text=">",
        command=lambda: move_images(+1),
        width=50,
        height=50,
    )

    page.columnconfigure(1, minsize=50)
    page.columnconfigure(2, minsize=1000)
    page.columnconfigure(3, minsize=50)

    page.rowconfigure(1, minsize=int((720 - image_height) / 2))
    page.rowconfigure(2, minsize=image_height)
    page.rowconfigure(3, minsize=int((720 - image_height) / 2))

    prev.grid(
        row=2,
        column=1,
        padx=50,
    )
    fwd.grid(
        row=2,
        column=3,
        padx=50,
    )

    def ondestroy():
        global actions_frame
        actions_frame.place_forget()
        del actions_frame
        
        for _, child in images_frame.children.items():
            child.place_forget()

        

    return "designs", page, onmount, ondestroy

