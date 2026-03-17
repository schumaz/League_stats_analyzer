import os
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open_new("http://localhost:8501")

if __name__ == '__main__':
    print("Starting League Stats Analyzer...")
    Timer(2, open_browser).start()
    
    os.system("streamlit run dashboard.py")