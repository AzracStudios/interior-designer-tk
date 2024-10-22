import customtkinter as ctk
from widgets.image import ImageWidget

EMAIL = "support@urbanutopia.com"


def TermsAndConditionsPage(win):
    page = ctk.CTkFrame(
        master=win, width=1280, height=720, bg_color="#f2e7e1", fg_color="#f2e7e1"
    )

    container = ctk.CTkFrame(
        master=page, width=1280, height=720, bg_color="#f2e7e1", fg_color="#f2e7e1"
    )

    def onmount():
        win.title("Urban Utopia - Terms And Conditions")
    
        

    ########

    title_font = ctk.CTkFont(family="Merriweather", size=40, weight="bold")
    title = ctk.CTkLabel(
        master=container, text="Terms & Conditions", fg_color="#f2e7e1", font=title_font
    )
    title.pack(pady=15)

    ########

    sub = ctk.CTkLabel(
        master=container,
        text="""
Welcome to the Urban Utopia app. These terms and conditions govern your use of our app; by using our app, you accept these terms and 
conditions in full. If you disagree with these terms and conditions or any part of these terms and conditions, you must not use our app. """[
            1:
        ],
        fg_color="#f2e7e1",
        font=("Merriweather", 16),
    )

    sub.pack()

    ########

    license_to_use_application = """
Unless otherwise stated, Urban Utopia and/or its licensors own the intellectual property rights in the app and material 
on the app. Subject to the license below, all these intellectual property rights are reserved

You must not:
• Republish material from this app (including republication on another app)
• Sell, rent, or sub-license material from the app
• Show any material from the app in public
• Reproduce, duplicate, copy, or otherwise exploit material on our app for a commercial purpose
• Edit or otherwise modify any material on the app
• Redistribute material from this app except for content specifically and expressly made available for redistribution
"""[
        1:
    ]

    acceptable_use = """
• You must not use our app in any way that causes, or may cause, damage to the app or impairment of the availability or 
accessibility of the app; or in any way that is unlawful, illegal, fraudulent, or harmful, or in connection with any 
unlawful, illegal, fraudulent, or harmful purpose or activity. 

• You must not use our app to copy, store, host, transmit, send, use, publish, or distribute any material that consists 
of (or is linked to) any spyware, computer virus, Trojan horse, worm, keystroke logger, rootkit, or other malicious computer software. 

• You must not conduct any systematic or automated data collection activities (including without limitation scraping, 
data mining, data extraction, and data harvesting) on or about our app without our express written consent.
"""[
        1:
    ]

    limitations_of_liability = """
Urban Utopia will not be liable to you (whether under the law of contact, the law of torts or otherwise) in relation to the contents of, 
or use of, or otherwise in connection with, this app:

• To the extent that the app is provided free-of-charge, for any direct loss
• For any indirect, special, or consequential loss
• For any business losses, loss of revenue, income, profits, or anticipated savings, loss of contracts or business relationships, loss of 
reputation or goodwill, or loss or corruption of information or data
• These limitations of liability apply even if Urban Utopia has been expressly advised of the potential loss.
"""[
        1:
    ]

    variation = """
Urban Utopia may revise these terms and conditions from time-to-time. Revised terms and conditions will apply to the use of this app 
from the date of the publication of the revised terms and conditions on this app. Please check this page regularly to ensure you are 
familiar with the current version.
"""[
        1:
    ]

    entire_agreement = """
These terms and conditions constitute the entire agreement between you and Urban Utopia in relation to your use of this app and 
supersede all previous agreements in respect of your use of this app.
"""[
        1:
    ]

    copyright_agreement = f"""
• Unless otherwise stated, all intellectual property rights in the original content and materials created by Urban Utopia and 
appearing on this app, including but not limited to text, graphics, logos, audio clips, video clips, digital downloads, data 
compilations, and software, are owned by Urban Utopia and are protected by copyright laws.

• However, it should be noted that all images used on this app are sourced from third-party providers for which Urban Utopia 
does not claim copyrights. The use of these images is purely for illustrative purposes and does not imply ownership or 
endorsement by Urban Utopia.

• You may access, view, and print the original content and materials created by Urban Utopia on this app for your personal 
and non-commercial use only. Any other use, reproduction, modification, distribution, or republication of such content and 
materials without prior written permission from Urban Utopia is strictly prohibited.

• For permission requests or inquiries regarding the use of content and materials created by Urban Utopia, please contact 
us at {EMAIL}.

• For inquiries regarding the use of images sourced from third-party providers, please refer to the respective copyright 
holders and their terms of use.
"""

    sections = [
        ("License To Use Application", license_to_use_application),
        ("Acceptable Use", acceptable_use),
        ("Limitations Of Liability", limitations_of_liability),
        ("Variation", variation),
        ("Entire Agreement", entire_agreement),
        ("Copyright Agreement", copyright_agreement),
    ]

    section_index = 0

    sec_title_font = ctk.CTkFont(family="Merriweather", size=20, weight="bold")

    section_frame = ctk.CTkFrame(
        master=container, width=1280, height=450, fg_color="#f2e7e1", bg_color="#f2e7e1"
    )

    section_title = ctk.CTkLabel(
        master=section_frame,
        fg_color="#f2e7e1",
        bg_color="#f2e7e1",
        text="",
        font=sec_title_font,
    )
    section_title.pack(pady=15)

    section_content = ctk.CTkLabel(
        master=section_frame,
        fg_color="#f2e7e1",
        bg_color="#f2e7e1",
        text="",
        font=("Merriweather", 16),
        justify="left",
    )
    section_content.pack(pady=10)

    section_frame.pack_propagate(0)

    section_frame.pack(pady=10)

    section_select = ctk.CTkFrame(
        master=container, fg_color="#f2e7e1", bg_color="#f2e7e1"
    )

    def update_select(index):
        nonlocal section_index, section_title, section_content
        for _, child in section_select.children.items():
            try:
                child.index
            except:
                continue
            if child.index == section_index:
                child.configure(fg_color="gray75")
            if child.index == index:
                child.configure(fg_color="black")

        section_index = index
        section_title.configure(text=sections[section_index][0])
        section_content.configure(text=sections[section_index][1])

    prev = ctk.CTkButton(
        master=section_select,
        text="<",
        width=20,
        height=20,
        fg_color="gray75",
        text_color="black",
        hover_color="gray90",
        command=lambda: update_select(section_index - 1 if section_index > 0 else 0),
    )

    prev.grid(row=1, column=1)

    for i in range(len(sections)):
        select = ctk.CTkButton(
            master=section_select,
            text="",
            corner_radius=100,
            width=10,
            height=10,
            fg_color="gray75" if i != section_index else "black",
            command=lambda x=i: update_select(x),
        )
        select.index = i
        select.grid(row=1, column=i + 2, padx=10)

    nxt = ctk.CTkButton(
        master=section_select,
        text=">",
        width=20,
        height=20,
        fg_color="gray75",
        text_color="black",
        hover_color="gray90",
        command=lambda: update_select(
            section_index + 1
            if section_index < len(sections) - 1
            else len(sections) - 1
        ),
    )

    nxt.grid(row=1, column=len(sections) + 2)

    update_select(0)
    section_select.pack()

    ########

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
        background_corner_colors=("#EAC7C5",) * 4,
    )
    back.place(relx=0.5, rely=0.98, anchor="s")

    ########

    container.place(relx=0.5, rely=0.5, anchor="center")
    page.pack_propagate(0)

    ########

    return "termsandconditions", page, onmount, lambda: None
