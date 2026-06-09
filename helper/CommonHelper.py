import os
import sys
import subprocess
import xlwings as xw
from nsetools import Nse
from module import ManageExcel
import pandas as pd

nse = Nse()
gainers = nse.get_top_gainers()
losers  = nse.get_top_losers()

def open_excel(path):
    if sys.platform == "win32":
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.run(["open", path])
    else:
        subprocess.run(["xdg-open", path])
 
 
def is_file_open(path):
    """Check if Excel already has this file open (Windows only via xlwings)."""
    try:
        for app in xw.apps:
            for book in app.books:
                if os.path.abspath(book.fullname) == os.path.abspath(path):
                    return True
    except Exception:
        pass
    return False

def fetch_data(path,All_Future_Stocks):
    ManageExcel.update_live(path, gainers, losers, All_Future_Stocks)

def get_all_FutureList()->list:
    #url = "https://nsearchives.nseindia.com/content/fo/fo_mktlots.csv"
    url = "fo_mktlots.csv"
    df = pd.read_csv(url)

    #print(df.columns.tolist())
    #print(df.head())
    # Get all stock names
    fno_stocks = df['SYMBOL    '].dropna().unique().tolist()
   
    return fno_stocks