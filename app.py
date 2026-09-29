from db import setup_db
from ui import App

if __name__ == '__main__':
    setup_db()
    App().mainloop()
