import pyapi

name = 'p3'
ids = ['date', 'time', 'frame']
numeric_fields = ['confidence', 'lol']
discrete_fields = {'color': ['red', 'green', 'blue', 'orange'],
                   'value': ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']}

client = pyapi.Client()

project = client.create_project(name, ids, numeric_fields, discrete_fields)

project.add_fdata('data/red0.jpg', 'data/red0.meta')
project.add_fdata('data/red1.png', 'data/red1.meta')
project.add_fdata('data/red2.jpeg', 'data/red2.meta')
project.add_fdata('data/blue0.png', 'data/blue0.meta')
project.add_fdata('data/green1.jpg', 'data/green1.meta')
project.add_fdata('data/orange2.png', 'data/orange2.meta')
project.add_fdata('data/orange3.png', 'data/orange3.meta')
