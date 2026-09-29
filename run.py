from db import setup_db
from ui import App

setup_db()
App().mainloop()
