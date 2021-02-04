import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter.font import Font

# 紀錄選單左邊的值和輸出到label上
def callback1(selection):
    global left 
    left = float(buyIn.get(selection)) if buyIn.get(selection) != "-" else 0.0
    result1.config(text=f"目前匯率：{left} : 1.0")

# 紀錄選單右邊的值和輸出到label上
def callback2(selection):
    global right 
    right = float(buyIn.get(selection)) if buyIn.get(selection) != "-" else 0.0
    result2.config(text=f"目前匯率：{right} : 1.0") 

# 輸出轉換結果到label上
def getResult():
    print(left, right)
    r = round(right / left, 3) if left != 0.0 and right != 0.0 else 0.0
    result_label.config(text=f"{r} : 1.0")

# 抓取網站資料
request = requests.get("https://rate.bot.com.tw/xrt?Lang=zh-TW")

soup = BeautifulSoup(request.text, "html.parser")

names = soup.find_all("div", class_="visible-phone print_hide")

currency = []
buyIn = {}

# 利用attrs(attributes)取得指定資料
values1 = soup.find_all("td", class_="rate-content-cash", 
                    attrs={"data-table":"本行現金買入"})
values2 = soup.find_all("td", class_="rate-content-cash", 
                    attrs={"data-table":"本行現金賣出"})

for name in names:
    currency.append(str(name.text).strip())

for i in range(0, len(currency)):
    buyIn.update({currency[i]:str(values1[i].text)})

# 建立視窗
window = tk.Tk()
window.title = "Currency converter"
window.geometry("800x600")
title = tk.Label(window, text="幣值轉換器", font=("微軟正黑體", 25))
sub = tk.Label(window, text="(以臺灣銀行資料為準且以新臺幣換算匯率)", font=("微軟正黑體", 25))
title.pack()
sub.pack()

# 建立選單群組
menu = tk.Frame(window)
menu.pack()
var = tk.StringVar(menu)
var.set("請選擇幣別")
left_menu = tk.OptionMenu(menu, var, *currency, command=callback1)
left_menu.pack(side=tk.LEFT)

arrow = tk.Label(menu, text="換成", font=("微軟正黑體", 25))
arrow.pack(padx=40, side=tk.LEFT)

var2 =tk.StringVar(menu)
var2.set("請選擇幣別")
right_menu = tk.OptionMenu(menu, var2, *currency, command=callback2)
right_menu.pack(side=tk.LEFT)

# 建立匯率群組
rate = tk.Frame(window)
rate.pack()
left = 0.0
right = 0.0
result1 = tk.Label(rate, text=f"目前匯率：{buyIn.get(currency[0])} : 1.0")
result1.pack(padx=50, side=tk.LEFT)
convert = tk.Button(rate, text="轉換", font=("微軟正黑體", 15), command=getResult)
convert.pack(side=tk.LEFT)
result2 = tk.Label(rate, text=f"目前匯率：{buyIn.get(currency[0])} : 1.0")
result2.pack(padx=50, side=tk.LEFT)

# 轉換結果
result_label = tk.Label(window, font=("微軟正黑體", 15))
result_label.pack()

# 視窗迴圈
window.mainloop()