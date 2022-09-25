from app import app
from layout import layout
from callbacks import *

app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True)

#TO DO
#Take out x and y dropdowns
# Add in dynamic graph to graph stock info
# Refresh should refresh stock prices
