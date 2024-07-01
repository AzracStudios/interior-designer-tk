from PIL import Image, ImageTk
import customtkinter as ctk
from utils import correct_path
import uuid


def load_blob(path, size):
    if len(path) == 0:
        return
    img_blob = Image.open(correct_path(path))
    if size == (0, 0):
        size = (img_blob.width, img_blob.height)
    elif size[0] == 0 and size[1] != 0:
        size = (int(img_blob.width * size[1] / img_blob.height), size[1])
    elif size[1] == 0 and size[0] != 0:
        size = (size[0], int(size[0] * img_blob.height / img_blob.width))

    img_blob = img_blob.resize(size)

    return img_blob, size


def load_image(path, size):
    blob, size = load_blob(path, size)
    itkimg = ImageTk.PhotoImage(blob)
    return itkimg


def load_image_ctk(path, size, ret_size=False):
    blob, size = load_blob(path, size)
    ctkimg = ctk.CTkImage(light_image=blob, size=size)
    if ret_size:
        return ctkimg, size
    return ctkimg


def ImageWidget(canvas, path, size, x=0, y=0, relx=0, rely=0, anchor="center"):
    ## store image object in canvas.buf{}[uuid] to avoid it being garbage collected
    try:
        getattr(canvas, "buf")
    except:
        canvas.buf = {}

    canvas.buf[uuid.uuid4()] = image = load_image(path, size)

    if relx == 0 and rely == 0:
        return canvas.create_image(x, y, anchor=anchor, image=image)

    else:
        return canvas.create_image(relx * 1280, rely * 720, anchor=anchor, image=image)


def ImageButton(
    parent, path, size, text="", compound="left", padx=0, pady=0, callback=lambda: None
):
    button_widget = ctk.CTkButton(
        master=parent,
        width=size[0] + padx,
        height=size[1] + pady,
        image=load_image(path, size),
        text=text,
        compound=compound,
        command=lambda: callback(),
    )
    return button_widget
