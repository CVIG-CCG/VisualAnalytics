from mydatabase import transform
from app import app
from layout import sidepanel, navbar
import dash_html_components as html

df = transform.get_data()

app.layout = html.Div([
    navbar.Navbar(), sidepanel.layout
])

if __name__ == '__main__':
    app.run_server()
