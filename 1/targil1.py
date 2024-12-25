# -*- coding: utf-8 -*-
"""targil1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1l35SqgkAw7fagEOI0RWfDXLgm4ar-48e
"""

print("hello")

import json

# Initialize an empty dictionary to store information
info = {}

# Open the file and load data into the variable
with open('/content/sample_data/students.txt', 'r') as file:
    # Parse the JSON data from the file
    students = json.load(file)

    # Store each student's data in the dictionary using their first name as the key
    for student in students:
        info[student["firstName"].lower()] = {
            "lastName": student["lastName"],
            "email": student["email"],
            "courses": student["subjects"],
            "website": student["website"]
        }

# Example usage
print(info.get("dan").get("courses"))

import ipywidgets as widgets
from IPython.display import display
import json
button = widgets.Button(description="Load info!")
output = widgets.Output()

info = {}

# print(students)

def on_button_clicked(b):
    i = 0
    # Output widget to display results
    output.clear_output()
    with output:
        with open('/content/sample_data/students.txt', 'r') as file:
          # Parse the JSON data from the file
          students = json.load(file)

          # Store each student's data in the dictionary using their first name as the key
          for student in students:
              info[student["firstName"].lower()] = {
                  "lastName": student["lastName"],
                  "email": student["email"],
                  "courses": student["subjects"],
                  "website": student["website"]
              }
        print(info)

print(info)
button.on_click(on_button_clicked)
display(button, output)

import ipywidgets as widgets
from typing import Text
info = {'rob': {'lastName': 'Doe', 'email': 'mail@braude.com', 'courses': ['English', 'Math'], 'website': 'google.ru'}, 'dan': {'lastName': 'Cohen', 'email': 'mail2@braude.com', 'courses': ['English', 'Data Mining', 'Algorithms'], 'website': 'maplestory.com'}, 'ron': {'lastName': 'Carmelianski', 'email': 'mail3@gmail.com', 'courses': ['Computers', 'Programming', 'Singing'], 'website': 'cartoons.com'}}
print(list(info.keys()))
names = list(info.keys())
# names = ''
w = widgets.Dropdown(
    options=names,
    value=names[0] if names else "",
    description='Student:',
)
txt1=widgets.Text()
txt1.value=names[0] if names else ""
# display(txt1)

# first name
txt_first_name = widgets.Text()
txt_first_name.value = txt1.value
display(txt_first_name)

# Last name
txt_last_name = widgets.Text()
txt_last_name.value = info.get(txt1.value).get('lastName')
display(txt_last_name)

# Email
txt_email = widgets.Text()
txt_email.value = info.get(txt1.value).get('email')
display(txt_email)

# Courses (join the list into a single string for display)
txt_courses = widgets.Text()
txt_courses.value = ", ".join(info.get(txt1.value).get('courses'))
display(txt_courses)

# Website
txt_website = widgets.Text()
txt_website.value = info.get(txt1.value).get('website')
display(txt_website)


# program
txt_program = widgets.Text()
txt_program.value = ""
display(txt_program)

def on_change(change):
    if change['type'] == 'change' and change['name'] == 'value':
        print("changed to %s" % change['new'])
    txt1.value=w.value
    txt_first_name.value = w.value
    txt_last_name.value = info.get(txt1.value).get('lastName')
    txt_email.value = info.get(txt1.value).get('email')
    txt_courses.value = ", ".join(info.get(txt1.value).get('courses'))
    txt_website.value = info.get(txt1.value).get('website')
    txt_program.value = info.get(txt1.value).get('program') if 'program' in info.get(txt1.value) else ""

button = widgets.Button(description="Change program!")
output = widgets.Output()



# print(students)

def on_button_clicked(b):
    i = 0
    # Output widget to display results
    output.clear_output()
    with output:
        # pass
        if len(info.get(txt1.value).keys()) == 4:
          info.get(txt1.value)['program'] = txt_program.value
          print(info.get(txt1.value))
          pass







button.on_click(on_button_clicked)
display(button, output)
w.observe(on_change)

display(w)