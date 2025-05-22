import webbrowser
import threading
from app import app

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")

if __name__ == '__main__':
    threading.Timer(1.5, open_browser).start()
    app.run(debug=False)  #True si es modo de desarrollo, False si es de producción
