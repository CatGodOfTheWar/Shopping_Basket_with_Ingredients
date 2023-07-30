import json
from bs4 import BeautifulSoup
import requests
from os.path import exists
from tkinter import *

url = ""
recipe = {}


def update_list():
    old_list_keys = []
    new_list_keys = []
    new_list = json.loads(get_recipe())
    with open("List.json", "r") as input_file:
       old_list = json.load(input_file)
    for new in list(new_list.keys()):
        for old in old_list.keys():
            if new == old:
                if isinstance(old_list[old][0], str):
                    new_list.pop(new)
                else:
                    old_list[old][0] += new_list[new][0]
                    new_list.pop(new)
    if len(new_list) > 0:
        old_list.update(new_list)
    obj = json.dumps(old_list, indent=4)
    create_file(obj)
    show_list(obj)


def get_recipe():
    unit = []
    amount = []
    global recipe
    count = 0
    page = requests.get(url).text
    file = BeautifulSoup(page, "html.parser")
    list_ = file.find(class_="wprm-recipe-ingredients")
    for ing in list_.find_all(class_="wprm-recipe-ingredient-unit"):
        unit.append(ing.text)
    for ing in list_.find_all(class_="wprm-recipe-ingredient-amount"):
        try:
            amount.append(float(ing.text))
        except:
            amount.append(ing.text)
    while len(amount) > len(unit):
        unit.append('None')
    element = list(zip(amount, unit))
    for ing in list_.find_all(class_="wprm-recipe-ingredient-name"):
        try:
            recipe[ing.text] = element[count]
            count += 1
        except:
            recipe[ing.text] = ('None', 'None')
    json_obj = json.dumps(recipe, indent=4)
    return json_obj


def check_file():
    file_exits = exists('/home/catwarrior/Documents/Proiecte_Facultate_Python/Proiecte_de_tip_C/'
                        'Shopping_Basket_with_Ingredients/List.json')
    return file_exits


def create_file(items_to_buy):
    with open("List.json", "w+") as output:
        output.write(items_to_buy)


def submit():
    global url
    url = entry_url.get()
    entry_url.delete(0, END)
    main()


def show_list(list_ing):
    row, column = 0, 0
    list_ = json.loads(list_ing)
    for ing in list_:
        ing_label = Label(frame_list, text=f"{ing}: ", font=("Times New Roman", 16), height=2, bg="#ADB2D3")
        ing_label.grid(row=row, column=column)
        column += 1
        if column == 1:
            row += 1
            column = 0
    row, column = 0, 1
    for ing in list_:
        ing_label = Label(frame_list, text=f"{list_[ing][0]} ", font=("Times New Roman", 16), bg="#ADB2D3")
        ing_label.grid(row=row, column=column)
        column += 1
        if column == 2:
            row += 1
            column = 1
    row, column = 0, 2
    for ing in list_:
        ing_label = Label(frame_list, text=f"{list_[ing][1]} ", font=("Times New Roman", 16), bg="#ADB2D3")
        ing_label.grid(row=row, column=column)
        column += 1
        if column == 3:
            row += 1
            column = 2

def main():
    json_obj = get_recipe()
    if check_file():
        try:
            update_list()
        except:
            create_file(json_obj)
            show_list(json_obj)
    else:
        create_file(json_obj)
        show_list(json_obj)


if __name__ == '__main__':
    window = Tk()
    window.geometry("600x900")
    window.config(bg="#896279")
    window.title("Recipe list")
    window.resizable(False, False)

    frame_btn = Frame(window, bg="#ADB2D3", pady=10, padx=10)
    frame_btn.place(x=110, y=80)

    url_label = Label(frame_btn, text="URL: ", font=("Times New Roman", 25), borderwidth=0,
                      bg="#ADB2D3", fg="#594F3B")
    url_label.grid(row=0, column=0)
    entry_url = Entry(frame_btn, width=10, font=("Times New Roman", 25), borderwidth=0,
                      bg="#9C7CA5", fg="#594F3B")
    entry_url.grid(row=0, column=1)

    submit_btn = Button(window, text="Apply", font=("Times New Roman", 25), borderwidth=0,
                        bg="#ADB2D3", fg="#594F3B", activebackground="#ADB2D3", activeforeground="#594F3B",
                        command=submit)
    submit_btn.place(x=250, y=180)

    label_ing = Label(window, text="List of ingredients:", font=("Times New Roman", 20), borderwidth=0,
                      bg="#896279", fg="#ADB2D3")
    label_ing.place(x=80, y=270)

    frame_list = Frame(window, bg="#ADB2D3")
    frame_list.place(x=80, y=330)




    window.mainloop()
