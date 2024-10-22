import customtkinter as ctk
from widgets.image import load_image_ctk, load_blob
from PIL import Image, ImageDraw


def open_preview_popup(path):
    img = load_image_ctk(path, (0, 0))
    win = ctk.CTkToplevel()
    win.title("Urban Utopia Admin - Image Preview")
    win.geometry(f"{img.cget('size')[0]}x{img.cget('size')[1]}")
    ctk.CTkLabel(master=win, text="", image=img).place(relx=0, rely=0, anchor="nw")


def create_rounded_resized_image(path, size):
    img, size = load_blob(path, size)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), size], 150, fill=255)
    img.putalpha(mask)

    return ctk.CTkImage(light_image=img, size=size)


def ImagePreview(parent, width, path, bg="#F2F2F2"):
    btn = ctk.CTkButton(
        master=parent,
        width=width,
        height=width,
        fg_color=bg,
        hover_color=bg,
        bg_color=bg,
        text="",
        image=create_rounded_resized_image(path, (width, width)) if path else "",
        command=lambda: open_preview_popup(path),
    )

    def set_path(path):
        img = create_rounded_resized_image(path, (width, width))

        btn.configure(command=lambda: open_preview_popup(path), image=img)
        btn.image = img

    return btn, set_path
