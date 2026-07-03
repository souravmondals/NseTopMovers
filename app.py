import os
import sys
import time
import subprocess
from datetime import datetime
from helper import CommonHelper, StockDetails
from module import ManageExcel
from config import config
 
# xlwings talks directly to a live Excel instance (no file-lock issues)
import xlwings as xw

 
# ── Configuration ─────────────────────────────────────────────
OUTPUT_PATH = config["Excel-file-path"]  # <-- Change this path
REFRESH_INTERVAL = 240  # seconds (4 minutes)
# ──────────────────────────────────────────────────────────────
 

 
# ── Main loop ──────────────────────────────────────────────────
print("Fetching initial NSE data...")
All_Future_Stocks = CommonHelper.get_all_FutureList()
 
# First run: create file if missing, then open it
#if not os.path.exists(OUTPUT_PATH):
    #print("Creating Excel file...")
    #ManageExcel.build_fresh_workbook(OUTPUT_PATH, gainers, losers)
 
if not CommonHelper.is_file_open(OUTPUT_PATH):
    print("Opening Excel...")
    CommonHelper.open_excel(OUTPUT_PATH)
    time.sleep(3)  # give Excel a moment to open
 
# Update data (handles both fresh file and already-open file)
print(f"[{datetime.now().strftime('%H:%M:%S')}] Writing data to Excel...")
StockDetails.add_fno_stock_data(OUTPUT_PATH, All_Future_Stocks)
CommonHelper.fetch_data(OUTPUT_PATH, All_Future_Stocks)
print(f"Done. Next refresh in {REFRESH_INTERVAL // 60} min. Press Ctrl+C to stop.\n")
 
while True:
    time.sleep(REFRESH_INTERVAL)
    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Refreshing NSE data...")     
        CommonHelper.fetch_data(OUTPUT_PATH, All_Future_Stocks)
        StockDetails.add_fno_stock_data(OUTPUT_PATH, All_Future_Stocks)
        print(f"Updated. Next refresh in {REFRESH_INTERVAL // 60} min.\n")
    except KeyboardInterrupt:
        print("Stopped.")
        break
    except Exception as e:
        print(f"Error during refresh: {e}. Retrying next cycle...")