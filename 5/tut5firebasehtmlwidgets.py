# -*- coding: utf-8 -*-
"""tut5FirebaseHTMLwidgets.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FtRbg00b1W4O421QlcTzrbeB3v-GVaks
"""

!pip install firebase



from firebase import firebase
FBconn = firebase.FirebaseApplication('https://test1-8bc2b-default-rtdb.europe-west1.firebasedatabase.app',None)
while True:
  temperature = int (input ("what is the temperature?"))
  data_to_upload = {
      'Temp' : temperature
  }
  result = FBconn.post('/myTest1/',data_to_upload)
  print(result)

import json
from firebase import firebase
FBconn = firebase.FirebaseApplication('https://test1-8bc2b-default-rtdb.europe-west1.firebasedatabase.app',None)
res=FBconn.get('/questions/',None)

for key in res:
    print(key+":\t", res[key])

from firebase import firebase
import time

# Initialize Firebase connection
FBconn = firebase.FirebaseApplication('https://test1-8bc2b-default-rtdb.europe-west1.firebasedatabase.app', None)

def get_all_records():
    """Retrieve all temperature records"""
    return FBconn.get('/Temperatures/', None)

def update_temperature(record_id, new_temp):
    """Update an existing temperature record"""
    return FBconn.put('/Temperatures/' + record_id, 'Temp', new_temp)

def delete_record(record_id):
    """Delete a temperature record"""
    return FBconn.delete('/Temperatures/', record_id)

def display_records():
    """Display all temperature records"""
    records = get_all_records()
    if records:
        print("\nCurrent Records:")
        for record_id, data in records.items():
            print(f"ID: {record_id} - Temperature: {data['Temp']}°C")
    else:
        print("\nNo records found")

while True:
    print("\nTemperature Tracker Menu:")
    print("1. Add new temperature")
    print("2. Update existing temperature")
    print("3. Delete temperature record")
    print("4. View all records")
    print("5. Exit")

    choice = input("\nEnter your choice (1-5): ")

    if choice == '1':
        # Add new temperature
        try:
            temperature = int(input("What is the temperature? "))
            data_to_upload = {
                'Temp': temperature,
                'timestamp': time.time()  # Adding timestamp for better tracking
            }
            result = FBconn.post('/Temperatures/', data_to_upload)
            print(f"Temperature added successfully! Record ID: {result['name']}")
        except ValueError:
            print("Please enter a valid number for temperature")

    elif choice == '2':
        # Update existing temperature
        display_records()
        record_id = input("\nEnter the record ID to update: ")
        try:
            new_temp = int(input("Enter the new temperature: "))
            result = update_temperature(record_id, new_temp)
            if result:
                print("Temperature updated successfully!")
            else:
                print("Failed to update temperature. Check if the ID exists.")
        except ValueError:
            print("Please enter a valid number for temperature")

    elif choice == '3':
        # Delete temperature record
        display_records()
        record_id = input("\nEnter the record ID to delete: ")
        result = delete_record(record_id)
        if result is None:
            print("Record deleted successfully!")
        else:
            print("Failed to delete record. Check if the ID exists.")

    elif choice == '4':
        # View all records
        display_records()

    elif choice == '5':
        print("Exiting program...")
        break

    else:
        print("Invalid choice. Please try again.")



from IPython.display import HTML
from google.colab.output import _publish as publish
publish.css("b {color: blue}")
HTML("Now <b>bold</b> and <b>blue</b> too.")

import IPython

html_code = \
'''
<p>Now this is <i>really</i> awesome!</p>
<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Python.svg/768px-Python.svg.png'></img>
'''


display(IPython.display.HTML(html_code))

import IPython
js_code = '''
document.querySelector("#output-area").appendChild(document.createTextNode("hello world!"));
'''
display(IPython.display.Javascript(js_code))

import IPython
from google.colab import output

display(IPython.display.HTML('''
    The items:
    <br><ol id="items"></ol>
    <button id='button'>Click to add</button>
    <script>
      document.querySelector('#button').onclick = () => {
        google.colab.kernel.invokeFunction('notebook.AddListItem', [], {});
      };
    </script>
    '''))

def add_list_item():
  # Use redirect_to_element to direct the elements which are being written.
  with output.redirect_to_element('#items'):
    # Use display to add items which will be persisted on notebook reload.
    display(IPython.display.HTML('<li> Another item</li>'))

output.register_callback('notebook.AddListItem', add_list_item)

import IPython
import uuid
from google.colab import output

class InvokeButton(object):
  def __init__(self, title, callback):
    self._title = title
    self._callback = callback

  def _repr_html_(self):
    callback_id = 'button-' + str(uuid.uuid4())
    output.register_callback(callback_id, self._callback)

    template = """<button id="{callback_id}">{title}</button>
        <script>
          document.querySelector("#{callback_id}").onclick = (e) => {{
            google.colab.kernel.invokeFunction('{callback_id}', [], {{}})
            e.preventDefault();
          }};
        </script>"""
    html = template.format(title=self._title, callback_id=callback_id)
    return html

def do_something():
  print('here')

InvokeButton('click me', do_something)

import altair as alt
import ipywidgets as widgets
from vega_datasets import data

source = data.stocks()

stock_picker = widgets.SelectMultiple(
    options=source.symbol.unique(),
    value=list(source.symbol.unique()),
    description='Symbols')

# The value of symbols will come from the stock_picker.
@widgets.interact(symbols=stock_picker)
def render(symbols):
  selected = source[source.symbol.isin(list(symbols))]

  return alt.Chart(selected).mark_line().encode(
      x='date',
      y='price',
      color='symbol',
      strokeDash='symbol',
  )

from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode

def take_photo(filename='photo.jpg', quality=0.8):
  js = Javascript('''
    async function takePhoto(quality) {
      const div = document.createElement('div');
      const capture = document.createElement('button');
      capture.textContent = 'Capture';
      div.appendChild(capture);

      const video = document.createElement('video');
      video.style.display = 'block';
      const stream = await navigator.mediaDevices.getUserMedia({video: true});

      document.body.appendChild(div);
      div.appendChild(video);
      video.srcObject = stream;
      await video.play();

      // Resize the output to fit the video element.
      google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

      // Wait for Capture to be clicked.
      await new Promise((resolve) => capture.onclick = resolve);

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      stream.getVideoTracks()[0].stop();
      div.remove();
      return canvas.toDataURL('image/jpeg', quality);
    }
    ''')
  display(js)
  data = eval_js('takePhoto({})'.format(quality))
  binary = b64decode(data.split(',')[1])
  with open(filename, 'wb') as f:
    f.write(binary)
  return filename

from IPython.display import Image
try:
  filename = take_photo()
  print('Saved to {}'.format(filename))

  # Show the image which was just taken.
  display(Image(filename))
except Exception as err:
  # Errors will be thrown if the user does not have a webcam or if they do not
  # grant the page permission to access it.
  print(str(err))

import ipywidgets as widgets

slider = widgets.IntSlider(20, min=0, max=100)
slider