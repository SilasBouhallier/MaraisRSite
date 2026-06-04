import sys
import os

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'), override=True)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.application import Application

if __name__ == "__main__":
    app = Application("utils/configuration.cfg")
    app.start() 