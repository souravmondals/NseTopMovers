import os
import sys
import xlwings as xw
from openpyxl import Workbook
from helper import Fyers



def add_fno_stock_data(path, All_Future_Stocks):

    try:
        wb = xw.Book(path)
    except Exception:
        xw.App(visible=True).books.open(path)
        wb = xw.Book(path)

    sht = wb.sheets["FNO"]
    i=0
    for stock in All_Future_Stocks:
        stockDpth = Fyers.get_Stock_Depth(stock)
        if stockDpth:
            row = 3 + i  # row 1 = title, row 2 = headers, data starts row 3
            try:
                stockDpth = Fyers.get_Stock_Depth(stock)
                sht.range(f"A{row}").value = stock
                sht.range(f"B{row}").value = stockDpth.get("o")
                sht.range(f"C{row}").value = stockDpth.get("h")
                sht.range(f"D{row}").value = stockDpth.get("l")
                sht.range(f"E{row}").value = stockDpth.get("c")
                sht.range(f"F{row}").value = stockDpth.get("chp")
                sht.range(f"G{row}").value = stockDpth.get("totalbuyqty")
                sht.range(f"H{row}").value = stockDpth.get("totalsellqty")             
            except Exception as e:
                print(f"Error fetching data for {stock}: {e}")

            i+= 1

