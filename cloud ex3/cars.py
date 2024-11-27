from ipywidgets import Dropdown, VBox, Output
from IPython.display import display

import requests
import pandas as pd


# Initialize the output widget
output_area = Output()


url = 'https://data.gov.il/api/3/action/datastore_search?resource_id=053cea08-09bc-40ec-8f7a-156f0677aff3'


pd.set_option("display.max_columns", None)

response = requests.get(url)
data = response.json()
df = pd.DataFrame(data)

data_df = pd.DataFrame(data['result']['records'])


data_df.head()


makes = data_df['tozeret_nm'].unique()







# Initialize the output widget
output_area = Output()


make_dropdown = Dropdown(
    options=list(makes),
    description="Make:",
    value=list(makes)[0] if len(makes) > 0 else None,
)




def modelsList(selected_make):
    modelMark_dropdown = Dropdown(
    options=list(data_df['tozeret_nm'] == selected_make),
    description="Model:",
    value=list("select" if len(makes) > 0 else None,
               ))
    display(VBox([modelMark_dropdown, output_area]))


    


def on_make_change(change):
    output_area.clear_output()
    with output_area:
        selected_make = change['new']
        filtered_df = data_df[data_df['tozeret_nm'] == selected_make]
        modelsList(selected_make)
        display(filtered_df)
        display(VBox([make_dropdown, output_area]))



# Observe dropdown changes
make_dropdown.observe(on_make_change, names='value')

# Display the dropdown and output area
display(VBox([make_dropdown, output_area]))

