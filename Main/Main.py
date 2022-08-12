from tkinter import*
from ctypes import windll
from tkinterweb import HtmlFrame
import os
import sys
import requests
from bs4 import BeautifulSoup

GWL_EXSTYLE=-20
WS_EX_APPWINDOW=0x00040000
WS_EX_TOOLWINDOW=0x00000080

LastElement = ["https://google.com"]
r = False
config_lines = "en\n500\nwhite\nFalse\n127.0.0.1:5000\n127.0.0.1:5000\n127.0.0.1:5000\n"
SettingsIsActive = False
ToolsIsActive = False
SourceTools = None
num = 0

def set_appwindow():
    global hasstyle
    if not hasstyle:
        hwnd = windll.user32.GetParent(window.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        window.withdraw()
        window.after(100, lambda:window.wm_deiconify())
        hasstyle=True
    
def move(e):
    xwin = window.winfo_x()
    ywin = window.winfo_y()
    startx = e.x_root
    starty = e.y_root
    ywin = ywin - starty
    xwin = xwin - startx
    def move_(e):
        window.geometry(f"+{e.x_root + xwin}+{e.y_root + ywin}")
    startx = e.x_root
    starty = e.y_root
    frame.bind("<B1-Motion>",move_)
def minieme1_(event=None):
    global hasstyle
    window.update_idletasks()
    window.overrideredirect(False)
    window.state("iconic")
    hasstyle = False
def frame_map(event=None):
    window.overrideredirect(True)
    window.update_idletasks()
    set_appwindow()
    window.state("normal")
def minimefunction(event=None):
    global size
    if size:
        window.geometry(f"{screen_width}x{screen_height-40}+0+0")
        minimsi.config(text=" \u2752 ")
        size = False
    else:
        window.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
        minimsi.config(text=" \u25a0 ")
        size = True
            
def quitApp():
    path = os.path.dirname(os.path.abspath(__file__))

    with open(path + "\Configuration.txt", "r+", encoding="UTF-8") as config:
        con = config.readlines()
        proxy_choose = str(con[3].replace("\n", ""))
    if proxy_choose == "Now":
        with open(path + "\Configuration.txt", "r+", encoding="UTF-8") as config:
            con = config.readlines()
            strings = str(con[0]) + str(con[1]) + str(con[2]) + "False\n" + str(con[4]) + str(con[5]) + str(con[6])
            with open(path + "\Configuration.txt", "w", encoding="UTF-8") as c:
                c.write("")
            config.write(strings)
    window.destroy()
def close_blink(event=None):
    close_button.config(bg="red")
def close_blink1(event=None):
    close_button.config(bg="gray19")
def minimsi_blink(event=None):
    minimsi.config(bg="gray29")
def minimsi_blink1(event=None):
    minimsi.config(bg="gray19")
def minimsi1_blink(event=None):
    minimsi1.config(bg="gray29")
def minimsi1_blink1(event=None):
    minimsi1.config(bg="gray19")

def quitSettings(win: Frame, e1: Entry, e2: Entry, e3: Entry, chooseString: str):
    global editor, SettingsIsActive
    win.pack_forget()
    editor.pack(expand=True, fill=BOTH)
    SettingsIsActive = False
    proxy_https = e1.get()
    proxy_http =  e2.get()
    proxy_ftp = e3.get()
    path = os.path.dirname(os.path.abspath(__file__))
    proxy_lists = {"Deactivate" : "False", "Active only now" :  "Now", "Active always" : "True"}
    proxy_choose = proxy_lists[chooseString]
    with open(path + "\Configuration.txt", "r+", encoding="UTF-8") as config:
        con = config.readlines()
    strings = str(con[0]) + str(con[1]) + str(con[2]) + proxy_choose + "\n" + proxy_https + "\n" + proxy_http + "\n" + proxy_ftp + "\n"
    with open(path + "\Configuration.txt", "w", encoding="UTF-8") as config:
        config.write("")
    with open(path + "\Configuration.txt", "w", encoding="UTF-8") as config:
        config.write(strings)

def checkStar():
    proxies = None
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "\Configuration.txt", "r", encoding="UTF-8") as config:
        con = config.readlines()
        changed = str(con[3].replace("\n", ""))
    
    if (changed == "True") or (changed == "Now"):
        with open(path + "\Configuration.txt", "r", encoding="UTF-8") as config:
            con = config.readlines()
            proxy_https = int(con[4].replace("\n", ""))
            proxy_http = int(con[5].replace("\n", ""))
            proxy_ftp = int(con[6].replace("\n", ""))

            proxies = {
                "https": proxy_https,
                "http": proxy_http,
                "ftp": proxy_ftp
            }

    url = entryUrl.get()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36', 'Content-Type': 'text/html',}
    
    page = requests.get(url, headers=headers, proxies=proxies)
    page = BeautifulSoup(page.content, "html.parser")
    p = page.find("title").get_text()
            
    shortLabel = '<a href="' + url + '"><h1>' + p + '</h1></a>\n'
    with open(path + "\Favourites.txt", "r", encoding="UTF-8") as f:
        lines = f.readlines()
    if shortLabel in lines:
        return True
    else:
        return False


def getStar():
    global starButton
    proxies = None
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "\Configuration.txt", "r", encoding="UTF-8") as config:
        con = config.readlines()
        changed = str(con[3].replace("\n", ""))
    
    if (changed == "True") or (changed == "Now"):
        with open(path + "\Configuration.txt", "r", encoding="UTF-8") as config:
            con = config.readlines()
            proxy_https = int(con[4].replace("\n", ""))
            proxy_http = int(con[5].replace("\n", ""))
            proxy_ftp = int(con[6].replace("\n", ""))

            proxies = {
                "https": proxy_https,
                "http": proxy_http,
                "ftp": proxy_ftp
            }
    url = entryUrl.get()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36', 'Content-Type': 'text/html',}
    
    page = requests.get(url, headers=headers, proxies=proxies)
    page = BeautifulSoup(page.content, "html.parser")
    p = page.find("title").get_text()

    if not checkStar():

        with open(path + "\Favourites.txt", "a", encoding="UTF-8") as f:
            StarTitle = ""
            p = page.find("title").get_text()
            
            StarTitle = StarTitle + '<a href="' + url + '"><h1>' + p + '</h1></a>\n'
            f.write(StarTitle)
            starButton.config(text="\u2605")
    else:
        starButton.config(text="\u2606")
        with open(path + "\Favourites.txt", "w+", encoding="UTF-8") as f:
            h = f.readlines()
            f.write("")
        if len(h) != 0:
            with open(path + "\Favourites.txt", "a", encoding="UTF-8") as f:
                StarTitle = '<a href="' + url + '"><h1>' + p + '</h1></a>\n'
                h.remove(StarTitle)
                f.write(h)


def getFavourites():
    global editor
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "\Favourites.txt", "r", encoding="UTF-8") as f:
        h = f.readlines()
        h.reverse()
        line = ""

        for i in range(len(h)):
            line = line + h[i]
        
        HistoryPage = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title></head><body style="margin-left: 5%;"><h1>Your Favourites:</h1>' + line + '</body></html>'
        editor.load_html(html_source=HistoryPage)


def getHistory():
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "\History.txt", "r", encoding="UTF-8") as f:
        h = f.readlines()
        h.reverse()
        line = ""

        for i in range(len(h)):
            line = line + h[i]
        
        HistoryPage = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title></head><body style="margin-left: 5%;"><h1>Your Browse History:</h1>' + line + '</body></html>'
        editor.load_html(html_source=HistoryPage)

def quitTools(ToolsFrame):
    global window, editor, ToolsIsActive
    ToolsFrame.pack_forget()
    editor.pack(expand=True, fill=BOTH)
    ToolsIsActive = False

def getTools(w):
    global window, editor, SourceTools, ToolsIsActive
    if checkConfigure() and (ToolsIsActive == False):
        ToolsFrame = Frame(window)
        TopFrame = Frame(ToolsFrame, bg="gray29")
        Label(TopFrame, text="HTML Source:", bg="gray29", fg="white", font="Consolas 15", relief=GROOVE, borderwidth=0).pack(side=LEFT, padx=5, pady=5)
        editor.pack_forget()
        w.destroy()
        ToolsIsActive = True
        ToolsFrame.pack(side=TOP, ipadx=100, ipady=100, padx=5, pady=5, fill=X)
        TopFrame.pack(side=TOP, fill=X)
        Scroll = Scrollbar(ToolsFrame, orient="vertical")
        Scroll.pack(side=RIGHT, fill=Y, padx=0, pady=5)
        SourceTools = Text(ToolsFrame, yscrollcommand=Scroll.set, font="Consolas 9", relief=GROOVE, borderwidth=0)
        Scroll.config(command=SourceTools.yview)
        SourceTools.pack(side=TOP, ipady=59, fill=BOTH)

        cButton = Button(TopFrame, text=" X ", font="Consolas 15", bg="gray19", fg="white", relief=GROOVE, borderwidth=0, command=lambda: quitTools(ToolsFrame))

        cButton.bind("<Enter>", (lambda event: cButton.config(bg="red")))
        cButton.bind("<Leave>", (lambda event: cButton.config(bg="gray19")))

        cButton.pack(side=RIGHT)

def opened(url):
    entryUrl.delete(0, END)
    entryUrl.insert(0, url)
    enter()

def getApps(w):
    w.geometry('%dx%d+%d+%d' % (300, 500, 1000, 100))
    Button(w, width=20, text="Github", font="Consolas 15", bg="gray19", fg="white", relief=GROOVE, borderwidth=0, command=lambda: opened("https://github.com")).pack(side=TOP, padx=5, pady=5)
    Button(w, width=20, text="Google", font="Consolas 15", bg="gray19", fg="white", relief=GROOVE, borderwidth=0, command=lambda: opened("https://google.com")).pack(side=TOP, padx=5, pady=5)
    Button(w, width=20, text="Gmail", font="Consolas 15", bg="gray19", fg="white", relief=GROOVE, borderwidth=0, command=lambda: opened("https://gmail.com")).pack(side=TOP, padx=5, pady=5)
    Button(w, width=20, text="Stackoverflow", font="Consolas 15", bg="gray19", fg="white", relief=GROOVE, borderwidth=0, command=lambda: opened("https://stackoverflow.com")).pack(side=TOP, padx=5, pady=5)
    Button(w, width=20, text="YouTube", font="Consolas 15", bg="gray19", fg="white", relief=GROOVE, borderwidth=0, command=lambda: opened("https://youtube.com")).pack(side=TOP, padx=5, pady=5)
    
def openSettings(w: Tk):
    global SettingsIsActive, window, editor
    if checkConfigure() and (SettingsIsActive == False):
        editor.pack_forget()
        w.destroy()
        SettingsIsActive = True
        win = Frame(window, bg="gray29")
        framer = Frame(win, bg="gray29")
        framed = Frame(win, bg="gray29")
        framel = Frame(framed, bg="gray29")
        framee = Frame(framed, bg="gray29")

        framer.pack(side=TOP, fill=BOTH)
        framed.pack(side=TOP, fill=BOTH, padx=250, pady=0)
        framel.pack(side=LEFT, padx=10, pady=10)
        framee.pack(side=RIGHT, padx=10, pady=10)

        path = os.path.dirname(os.path.abspath(__file__))

        with open(path + "\Configuration.txt", "r", encoding="UTF-8") as config:
            con = config.readlines()
            proxy_https = str(con[4].replace("\n", ""))
            proxy_http = str(con[5].replace("\n", ""))
            proxy_ftp = str(con[6].replace("\n", ""))
            proxy_choose = str(con[3].replace("\n", ""))
        
        proxy_lists = {"False" : "Deactivate", "Now" : "Active only now", "True" : "Active always"}

        l1 = Label(framel, text="https:", font="Consolas 15", bg="gray29", fg="white")
        l2 = Label(framel, text="http:", font="Consolas 15", bg="gray29", fg="white")
        l3 = Label(framel, text="ftp:", font="Consolas 15", bg="gray29", fg="white")
        l4 = Label(framel, text="When worked", font="Consolas 15", bg="gray29", fg="white")

        entry1 = Entry(framee, font="Consolas 15", bg="gray29", fg="white")
        entry2 = Entry(framee, font="Consolas 15", bg="gray29", fg="white")
        entry3 = Entry(framee, font="Consolas 15", bg="gray29", fg="white")

        chooseString = StringVar()
        chooseString.set(proxy_lists[proxy_choose])
        ch = list(proxy_lists.values())
        chooseMenu = OptionMenu(framee, chooseString, *ch)
        chooseMenu.config(bg="gray29", activebackground="gray29", text="Deactivate", fg="white", font="Consolas 15", relief=GROOVE, borderwidth=0)

        closeButton = Button(framer, text=" X ", font="Consolas 15", bg="gray19", fg="white", relief=GROOVE, borderwidth=0, command=lambda: quitSettings(win, entry1, entry2, entry3, chooseString.get()))
        closeButton.pack(side=RIGHT)

        closeButton.bind("<Enter>", (lambda event: closeButton.config(bg="red")))
        closeButton.bind("<Leave>", (lambda event: closeButton.config(bg="gray19")))

        l1.pack(ipady=5)
        l2.pack(ipady=5)
        l3.pack(ipady=5)
        l4.pack(ipady=5)

        entry1.pack(ipady=5)
        entry2.pack(ipady=5)
        entry3.pack(ipady=5)

        chooseMenu.pack(ipady=5, fill=BOTH)

        entry1.insert(0, proxy_https)
        entry2.insert(0, proxy_http)
        entry3.insert(0, proxy_ftp)

        win.pack(side=TOP, ipadx=100, ipady=100, padx=5, pady=5,fill=X)

def binded():
    window.unbind("<Button>")

def showMenu():
    w = Tk()
    w.overrideredirect(True)
    w.bind("<Destroy>", lambda event: binded())
    window.bind("<Button>", lambda event: w.destroy())
    
    w.geometry('%dx%d+%d+%d' % (300, 250, 1000, 100))
    Button(w, width=20, text="</> Apps", font="Consolas 15", bg="gray19", fg="white", relief=GROOVE, borderwidth=0, command=lambda: getApps(w)).pack(side=TOP, padx=5, pady=5)
    Button(w, width=20,text="\u2699 Settings", font="Consolas 15", bg="gray19", fg="white", relief=GROOVE, borderwidth=0, command=lambda: openSettings(w)).pack(side=TOP, padx=5, pady=5)
    Button(w, width=20, text="\u2692 Tools", font="Consolas 15", bg="gray19", fg="white", relief=GROOVE, borderwidth=0, command=lambda: getTools(w)).pack(side=TOP, padx=5, pady=5)
    Button(w, width=20, text="\u26c1 History", font="Consolas 15", bg="gray19", fg="white", relief=GROOVE, borderwidth=0, command=lambda: getHistory()).pack(side=TOP, padx=5, pady=5)
    Button(w, width=20, text="\u2764 Favourites", font="Consolas 15", bg="gray19", fg="white", relief=GROOVE, borderwidth=0, command= lambda: getFavourites()).pack(side=TOP, padx=5, pady=5)
    w.mainloop()

def createConfigure(c: bool, w: Tk):
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + "\Configuration.txt", "w+", encoding="UTF-8") as configuration:
        configuration.write(config_lines)
    if c:
        w.destroy()

def checkConfigure():
    path = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(path + "\Configuration.txt"):
        return True
    else:
        w = Tk()
        l = Label(w, text="Configuration file is not exists!\nYou may create new configuration file in Settings", font=("Sans-serif", 12))
        l.pack(padx=10, pady=10)
        create_btn = Button(w, text="Create new file", font=("Sans-serif", 12), command=lambda: createConfigure(True, w=w))
        close_btn = Button(w, text="Close", font=("Sans-serif", 12), command=lambda: w.destroy())
        create_btn.pack(side="left", padx=50, pady=5)
        close_btn.pack(side="right", padx=50, pady=5)

def enter():
    global r, LastElement, num, SourceTools, starButton
    url = entryUrl.get()
    proxies = None
    path = os.path.dirname(os.path.abspath(__file__))

    if checkConfigure():

        with open(path + "\Configuration.txt", "r", encoding="UTF-8") as config:
            con = config.readlines()
            changed = str(con[3].replace("\n", ""))
    
        if (changed == "True") or (changed == "Now"):
            with open(path + "\Configuration.txt", "r", encoding="UTF-8") as config:
                con = config.readlines()
                proxy_https = int(con[4].replace("\n", ""))
                proxy_http = int(con[5].replace("\n", ""))
                proxy_ftp = int(con[6].replace("\n", ""))

                proxies = {
                    "https": proxy_https,
                    "http": proxy_http,
                    "ftp": proxy_ftp
                }

        if not r:
            if num < len(LastElement):
                num = num + 1
                LastElement.append(url)
                r = False
        
        if r:
            for i in range(0, len(LastElement)):
                print(num)
                if i > num:
                    del LastElement[i]
            LastElement.append(url)
            if num < len(LastElement):
                num = num + 1
            r = False

        #headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)', 'Content-Type': 'text/html',}

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36', 'Content-Type': 'text/html',}

        page = requests.get(url, headers=headers, proxies=proxies)
        page = BeautifulSoup(page.content, "html.parser")

        path = os.path.dirname(os.path.abspath(__file__))

        if ToolsIsActive:
            SourceTools.insert(INSERT, str(page))

        editor.load_html(html_source=str(page))

        if checkStar():
            starButton.config(text="\u2605")
        else:
            starButton.config(text="\u2606")

        # Check overflow of history #

        with open(path + "\Configuration.txt", "r", encoding="UTF-8") as config:
            con = config.readlines()
            count = int(con[1].replace("\n", ""))

        with open(path + "\History.txt", "r+", encoding="UTF-8") as history:
            lines = history.readlines()
    
        if len(lines) >= count:
            del lines[0]
            
            with open(path + "\History.txt", "w", encoding="UTF-8") as history:
                history.write("")
                for i in range(len(lines)):
                    history.write(lines[i])
    
        # __________________________ #

        with open(path + "\History.txt", "a", encoding="UTF-8") as a:
            l = ""
            p = page.find("title").get_text()
            
            l = l + '<a href="' + url + '"><h1>' + p + '</h1></a>\n'
            a.write(l)

        with open(path + "\Pages\Page.html", "w+", encoding="UTF-8") as f:
            f.write(str(page))

def back():
    global entryUrl, r, num
    r = True
    if num > 0:
        num = num - 1
        print("page" + str(num) + str(LastElement))
    entryUrl.delete(0, END)
    entryUrl.insert(0, LastElement[num])
    enter()

def next():
    global entryUrl, r, num
    r = True
    if num < len(LastElement):
        entryUrl.delete(0, END)
        entryUrl.insert(1, LastElement[num])
        enter()
        num = num + 1
        print("page" + str(num) + str(LastElement))

window = Tk()
size = True
app_width = 1000
app_height = 590
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width/2) - (app_width/2)
y = (screen_height/2) - (app_height/2)
window.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
window.overrideredirect(True)


frame = Frame(window,bg="gray29")
urlFrame = Frame(window, bg="gray29")
Button(urlFrame, text="<-", font="Consolas 15", bg="gray19", fg="white", relief=GROOVE, borderwidth=0, command=lambda: back()).pack(side=LEFT, padx=5, pady=5)
Button(urlFrame, text="->", font="Consolas 15", bg="gray19", fg="white", relief=GROOVE, borderwidth=0, command=lambda: next()).pack(side=LEFT, padx=5, pady=5)
entryUrl = Entry(urlFrame, font="Consolas 15", bg="white", relief=GROOVE, borderwidth=0)
entryUrl.pack(side=LEFT,ipadx=150, padx=5, pady=5)
enterButton = Button(urlFrame, text="Enter", font="Consolas 15", bg="gray19", fg="white", relief=GROOVE, borderwidth=0, command=lambda: enter())
enterButton.pack(side=LEFT, padx=5, pady=5)
entryUrl.bind("<Return>", (lambda event: enter()))
starButton = Button(urlFrame, text="\u2606", font="Consolas 15", bg="gray29", fg="white", relief=GROOVE, borderwidth=0, command=lambda: getStar())
starButton.pack(side=LEFT, padx=5, pady=5)

menuButton = Button(urlFrame, text="\u2630", font="Consolas 15", bg="gray19", fg="white", relief=GROOVE, borderwidth=0, command=lambda: showMenu())
menuButton.pack(side=RIGHT, padx=5, pady=5)

Label(frame,text="Simplex",font="Consolas 15",bg="gray29",fg="white").pack(side=LEFT,padx=10)
close_button = Button(frame,text=" X ",font="Consolas 15",bg="gray19",fg="white",relief=GROOVE,borderwidth=0,command=quitApp)
close_button.pack(side=RIGHT)
minimsi = Button(frame,text=" \u25a0 ",font="Consolas 15",bg="gray19",fg="white",relief=GROOVE,borderwidth=0,command=minimefunction)
minimsi.pack(side=RIGHT)
minimsi1 = Button(frame,text=" - ",font="Consolas 15",bg="gray19",fg="white",relief=GROOVE,borderwidth=0,command=minieme1_)
minimsi1.pack(side=RIGHT)
frame.pack(fill=X)
urlFrame.pack(fill=X)

editor = HtmlFrame(window, messages_enabled=False, vertical_scrollbar="auto")
editor.pack(expand=True,fill=BOTH)
window.config(bg="gray19")

frame.bind("<Button-1>",move)
frame.bind("<B1-Motion>",move)
# minimsi1.bind("<Button-1>",minieme1_)
frame.bind("<Map>",frame_map)
close_button.bind("<Enter>",close_blink)
close_button.bind("<Leave>",close_blink1)
minimsi.bind("<Enter>",minimsi_blink)
minimsi.bind("<Leave>",minimsi_blink1)
minimsi1.bind("<Enter>",minimsi1_blink)
minimsi1.bind("<Leave>",minimsi1_blink1)

hasstyle = False
window.update_idletasks()
window.withdraw()
set_appwindow()


window.mainloop()