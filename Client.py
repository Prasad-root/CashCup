"""Importer Module Section"""
from tkinter import *
from tkinter import messagebox
import customtkinter
import threading
from tkinter import ttk
import customtkinter
import sys
from PIL import Image,ImageTk
import tkinter as tk
import hashlib
import sqlite3
from ClientDatabase import ClientDatabase as Cd



class ClientSideSockets:
    #COLOR VARIABLES FOR INTERFACES
    #This Class Handle All of the connectivities between Client and the server

    ButtonColor = "#008080"
    stockDetailsboxColor = "#B2D8D8"
    stockDetailsboxTextColor = "black"


    OnlineUserName = "EMPTY" # THIS VARIABLE USE FOR IDENTIFY ONLINE CLIENT
    LoggingUsername = "EMPTY" 
    threadE2Status = False

    TrackingStock = "" # THIS IS THE INDEX OF TRACHING STOCK

    SERVER_IP = "0.0.0.0"
    def socket(self):
            try:
                import socket
                global client_socket
                global IP 
                global PORT
                global ADDR
                global DISCONNECTED_MSG
                global SIZE
                global FORMAT

                #IP = socket.gethostbyname(socket.gethostname())
                IP = self.SERVER_IP
                PORT = 9999
                ADDR = (IP,PORT)
                DISCONNECTED_MSG = "!DISCONNECT"
                SIZE = 4096
                FORMAT = 'utf-8'
                
                client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                client_socket.connect(ADDR)

                
            except:
                messagebox.showerror("Connection Establishment Error","Please Re-check Server IP address...")
                self.ipAddressWindow()
            else:
                global threadEl
                threadEl = threading.Thread(target=self.CustomerMain())
                threadEl.daemon = True # without the daemon parameter, the function in parallel will continue even your main program ends
                threadEl.start()
        
    def SendAndRecieve(self,message):
        connected = True
        while connected:
            msg = message
            client_socket.send(msg.encode(FORMAT))
            if msg == "Disconnected":
                connected = False
                print("[[[[[DISCONNECTED]]]]]")
            else:
                msg = client_socket.recv(SIZE).decode(FORMAT)
                self.checker(message=msg)
                connected = False

    """

 .----------------. .----------------. .----------------. .----------------.   .----------------. .----------------. .----------------. 
| .--------------. | .--------------. | .--------------. | .--------------. | | .--------------. | .--------------. | .--------------. |
| |     ______   | | |      __      | | |    _______   | | |  ____  ____  | | | |     ______   | | | _____  _____ | | |   ______     | |
| |   .' ___  |  | | |     /  \     | | |   /  ___  |  | | | |_   ||   _| | | | |   .' ___  |  | | ||_   _||_   _|| | |  |_   __ \   | |
| |  / .'   \_|  | | |    / /\ \    | | |  |  (__ \_|  | | |   | |__| |   | | | |  / .'   \_|  | | |  | |    | |  | | |    | |__) |  | |
| |  | |         | | |   / ____ \   | | |   '.___`-.   | | |   |  __  |   | | | |  | |         | | |  | '    ' |  | | |    |  ___/   | |
| |  \ `.___.'\  | | | _/ /    \ \_ | | |  |`\____) |  | | |  _| |  | |_  | | | |  \ `.___.'\  | | |   \ `--' /   | | |   _| |_      | |
| |   `._____.'  | | ||____|  |____|| | |  |_______.'  | | | |____||____| | | | |   `._____.'  | | |    `.__.'    | | |  |_____|     | |
| |              | | |              | | |              | | |              | | | |              | | |              | | |              | |
| '--------------' | '--------------' | '--------------' | '--------------' | | '--------------' | '--------------' | '--------------' |
 '----------------' '----------------' '----------------' '----------------'   '----------------' '----------------' '----------------' 

    """

class ClientInterface(ClientSideSockets):
    # All Of the Interfaces Inludes here
    def CustomerMain(self):
        global LoadDetailsStockID
        global LoadDetailsStockOwner
        global LoadDetailsBasePrice
        global LoadDetailsProfit
        global LoadDetailsAvailableHighPrice
        global LoadDetailsStockIDHighPriceOwner
        global stockStatus
        global stockPrice
        global BetPrice
        global displayID

        WIDTH = 900 # window width
        HEIGHT = 600 # window height
        
        self.main_root= customtkinter.CTk()
        self.main_root.title("CashCup")
        self.main_root.resizable(False,False) # Tesizeble is turn offed
        self.main_root.configure(fg_color = "#004444")

        # Change Window Icon 
        ico = Image.open('Images/icon.png')
        photo = ImageTk.PhotoImage(ico)
        self.main_root.wm_iconphoto(False, photo)

        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")

        # get screen width and height
        screen_width = self.main_root.winfo_screenwidth()
        screen_height = self.main_root.winfo_screenheight()
        # calculate position x and y coordinates
        x = (screen_width/2) - (WIDTH/2)
        y = (screen_height/2) - (HEIGHT/2)
        self.main_root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y-50))

        # Top Frame ======================================================================================================
        TopFrame = customtkinter.CTkFrame(master = self.main_root,width=900,height=52,fg_color="#003333",corner_radius=0)
        TopFrame.place(x=0,y=0)

        serverConnectButtonImage = customtkinter.CTkImage(light_image=Image.open("Images/connect.png"),dark_image=Image.open("Images/connect.png"),size=(18, 18))
        serverDisconnectButtonImage = customtkinter.CTkImage(light_image=Image.open("Images/disconnect.png"),dark_image=Image.open("Images/disconnect.png"),size=(18, 18))
        
        self.ServerConnectButton = customtkinter.CTkButton(master=TopFrame,width=170,height=35,image=serverConnectButtonImage,text="Connect",fg_color=self.ButtonColor,hover_color="#73B604",font=('Berlin Sans FB Demi',14),command=self.logging)
        self.ServerConnectButton.place(x=545,y=8)
        self.ServerDisconnectButton = customtkinter.CTkButton(master=TopFrame,width=170,height=35,image=serverDisconnectButtonImage,text="Disconnect",fg_color=self.ButtonColor,font=('Berlin Sans FB Demi',14),hover_color="#A30800",state= DISABLED,command=self.disconnect)
        self.ServerDisconnectButton.place(x=722,y=8)

        
        stockStatus = StringVar()
        self.timerWindow = customtkinter.CTkEntry(master=TopFrame,width=235,font=("arcade",26,"bold"),textvariable=stockStatus,state="readonly",fg_color="black",border_color="#39FF14",text_color="#39FF14",justify = "center",height = 35)
        self.timerWindow.place(x=290,y=9)
        # Left Frame ======================================================================================================

        LeftFrame = customtkinter.CTkFrame(master = self.main_root,width=270,height=600,fg_color="#003333",corner_radius=0)
        LeftFrame.place(x=0,y=0)
        logo = customtkinter.CTkImage(light_image=Image.open("Images/logo.png"),dark_image=Image.open("Images/logo.png"),size=(44, 44))
        customtkinter.CTkButton(master=LeftFrame,image=logo,text="",fg_color="transparent",width=44,height=44).place(x=25,y=10)
        customtkinter.CTkLabel(master=LeftFrame,text = "CashCup",font=("Cooper Black",35),text_color="white").place(x=85,y=15)
        
        # Stock List Frame ================================================================================================
        stockFrame = customtkinter.CTkFrame(master=self.main_root,width=228,height=424,corner_radius=10,fg_color="white")
        sctollbar = Scrollbar(stockFrame,orient=VERTICAL)

        self.stockListBox = tk.Listbox(stockFrame,width=23,height=22,yscrollcommand=sctollbar.set,bg=self.stockDetailsboxColor,selectmode=SINGLE,font=("Arial",15))
        sctollbar.config(command=self.stockListBox.yview)
        sctollbar.pack(side=RIGHT,fill=Y)

        self.stockListBox.pack()
        stockFrame.place(x=21,y=105)

        getStockButtonImage = customtkinter.CTkImage(light_image=Image.open("Images/getstock.png"),dark_image=Image.open("Images/getstock.png"),size=(20, 20))
        self.getStockDetailsbtn = customtkinter.CTkButton(master=LeftFrame,width=179,height=34,corner_radius=39,text="Stock Details",font=("Berlin Sans FB Demi",14),fg_color=self.ButtonColor,hover_color="#003333",text_color="white",border_color="#66B2B2",image=getStockButtonImage,state=DISABLED,command=self.LoadDetailsStock)
        self.getStockDetailsbtn.place(x=44,y=545)
        # Middle Area =====================================================================================================
        
        stockPrice = IntVar()
        BetPrice = tk.StringVar()

        customtkinter.CTkEntry(self.main_root,width=500,height=77,placeholder_text=0000,font=("Digital-7 Mono",60),text_color="white",fg_color="#037C6E",state="readonly",textvariable=stockPrice,justify="right",border_color="#66B2B2").place(x=335,y=77)
        BetPrice=customtkinter.CTkEntry(self.main_root,width=265,height=42,text_color="black",fg_color="#B2D8D8",textvariable=BetPrice,corner_radius=40)
        BetPrice.place(x=349,y=180)
        self.addBettToStockbtn = customtkinter.CTkButton(self.main_root,width=176,height=42,corner_radius=20,fg_color=self.ButtonColor,text_color="white",hover_color="#003333",text="Add Bett to Stock",state=DISABLED,font=("Berlin Sans FB Demi",16),command=self.Bedding)
        self.addBettToStockbtn.place(x=628,y=180)
       

        # StockLoad Frame ==================================================================================================
        LoadStockDetailsFrame = customtkinter.CTkFrame(master=self.main_root,height=200,width=450,fg_color="#003333")
        LoadStockDetailsFrame.place(x=380,y=250)
        customtkinter.CTkLabel(master=LoadStockDetailsFrame,text="Stock Details",font=("Berlin Sans FB Demi",18)).grid(row=0,column=0,columnspan=2,padx=150,pady=20)

        # Labels Of Stock Details Section
        entryText = {"StockID":5,'StockOwner':5,"BasePrice":5,'Profit':5,'AvailableHighPrice':5,'HighPriceOwner':(5,20)};rows = [row for row in range(1,7)]
        for text,padY,row in zip(entryText.keys(),entryText.values(),rows):customtkinter.CTkLabel(master=LoadStockDetailsFrame,text=text,font=("Berlin Sans FB Demi",13)).grid(row=row,column=0,pady=padY)

        LoadDetailsStockID = StringVar()
        LoadDetailsStockOwner = StringVar()
        LoadDetailsBasePrice = StringVar()
        LoadDetailsProfit = StringVar()
        LoadDetailsAvailableHighPrice = StringVar()
        LoadDetailsStockIDHighPriceOwner = StringVar()


        customtkinter.CTkEntry(master=LoadStockDetailsFrame,width=150,font=("Berlin Sans FB Demi",13),textvariable=LoadDetailsStockID,state="readonly",fg_color=self.stockDetailsboxColor,border_color=self.stockDetailsboxColor,text_color=self.stockDetailsboxTextColor).grid(row=1,column=1,pady=5)
        customtkinter.CTkEntry(master=LoadStockDetailsFrame,width=150,font=("Berlin Sans FB Demi",13),textvariable=LoadDetailsStockOwner,state="readonly",fg_color=self.stockDetailsboxColor,border_color=self.stockDetailsboxColor,text_color=self.stockDetailsboxTextColor).grid(row=2,column=1,pady=5)
        customtkinter.CTkEntry(master=LoadStockDetailsFrame,width=150,font=("Berlin Sans FB Demi",13),textvariable=LoadDetailsBasePrice,state="readonly",fg_color=self.stockDetailsboxColor,border_color=self.stockDetailsboxColor,text_color=self.stockDetailsboxTextColor).grid(row=3,column=1,pady=5)
        customtkinter.CTkEntry(master=LoadStockDetailsFrame,width=150,font=("Berlin Sans FB Demi",13),textvariable=LoadDetailsProfit,state="readonly",fg_color=self.stockDetailsboxColor,border_color=self.stockDetailsboxColor,text_color=self.stockDetailsboxTextColor).grid(row=4,column=1,pady=5)
        customtkinter.CTkEntry(master=LoadStockDetailsFrame,width=150,font=("Berlin Sans FB Demi",13),textvariable=LoadDetailsAvailableHighPrice,state="readonly",fg_color=self.stockDetailsboxColor,border_color=self.stockDetailsboxColor,text_color=self.stockDetailsboxTextColor).grid(row=5,column=1,pady=5)
        customtkinter.CTkEntry(master=LoadStockDetailsFrame,width=150,font=("Berlin Sans FB Demi",13),textvariable=LoadDetailsStockIDHighPriceOwner,state="readonly",fg_color=self.stockDetailsboxColor,border_color=self.stockDetailsboxColor,text_color=self.stockDetailsboxTextColor).grid(row=6,column=1,pady=(5,20))
        

        # Botton Area ======================================================================================================
        
        displayID = StringVar()
        displayIdEntry = customtkinter.CTkEntry(master=self.main_root,state='readonly',textvariable=displayID,bg_color="transparent",fg_color="black",text_color="#39FF14",font = ("arcade",20,"bold"),justify = "center",border_color="#39FF14")
        displayIdEntry.place(x=70,y=70)

        #self.biddingHistoryButton = 
        biddingHistoryButtonImage = customtkinter.CTkImage(light_image=Image.open("Images/biddingHistory.png"),dark_image=Image.open("Images/biddingHistory.png"),size=(18, 18))
        self.biddingHistoryButton = customtkinter.CTkButton(master=self.main_root,width=150,height=28,image=biddingHistoryButtonImage,text="Bidding History",fg_color=self.ButtonColor,font=('Berlin Sans FB Demi',14),hover_color="#A30800",state= DISABLED,command=self.biddingHistory)
        self.biddingHistoryButton.place(x=742,y=565)

        self.main_root.mainloop() 


    def ipAddressWindow(self):
        WIDTH = 250 # window width
        HEIGHT = 150 # window height
        self.serverIp_root = customtkinter.CTk()
        self.serverIp_root.title("CashCup")
        self.serverIp_root.resizable(False,False) # Tesizeble is turn offed
        self.serverIp_root.configure(fg_color = "black")

        ico = Image.open('Images/icon.png')
        photo = ImageTk.PhotoImage(ico)
        self.serverIp_root.wm_iconphoto(False, photo)

        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")

        # get screen width and height
        screen_width = self.serverIp_root.winfo_screenwidth()
        screen_height = self.serverIp_root.winfo_screenheight()
        # calculate position x and y coordinates
        x = (screen_width/2)
        y = (screen_height/2) - (HEIGHT/2)

        global inputServerIp
        inputServerIp = StringVar()
        self.serverIp_root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))
        customtkinter.CTkLabel(self.serverIp_root, text="ENTER SERVER IP", width=30 ,height=25,corner_radius=8,font=("arcade",26,"bold"),justify = "center",text_color="#39FF14").grid(row = 0,column = 0,pady = 10,padx=10)
        customtkinter.CTkEntry(self.serverIp_root,width=210,height=30,border_width=1,fg_color="black",text_color="#39FF14",font=("arcade",26,"bold"),textvariable = inputServerIp,justify = "center").grid(row=1,column=0,padx = (0,10),pady=0)
        customtkinter.CTkButton(self.serverIp_root,text='CONNECTION ESTABLISH',width=25,fg_color="#39ff14",font=("arcade",15,"bold"),border_color = "#39ff14",border_width = 1,text_color = "black",command = self.connectionEstablish).grid(row=2,column=0,pady=(10,20),columnspan=2)

        self.serverIp_root.mainloop()

    def logging(self):
        global username
        global password

        WIDTH = 400 # window width
        HEIGHT = 250 # window height
        self.logging_root = customtkinter.CTkToplevel(self.main_root)
        self.logging_root.title("CashCup")
        self.logging_root.resizable(False,False) # Tesizeble is turn offed
        self.logging_root.configure(fg_color = "#004444")


        # Change Window Icon 
        ico = Image.open('Images/icon.png')
        photo = ImageTk.PhotoImage(ico)
        self.logging_root.wm_iconphoto(False, photo)

        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")

        # get screen width and height
        screen_width = self.logging_root.winfo_screenwidth()
        screen_height = self.logging_root.winfo_screenheight()
        # calculate position x and y coordinates
        x = (screen_width/2) - (WIDTH/2)
        y = (screen_height/2) - (HEIGHT/2)
        self.logging_root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y-50))
    

        # Variabels for USERNAME and PASSWORD =================
        username = StringVar()
        password = StringVar()
        # =====================================================

        customtkinter.CTkLabel(self.logging_root, text="Log Here...", width=30 ,height=25,corner_radius=8,font=('arial',18)).grid(row = 0,column = 0, columnspan = 2,pady = 10,padx=150)
        customtkinter.CTkLabel(self.logging_root, text="Username : ", width=10 ,height=25,corner_radius=8,font=('arial',18),text_color="white").grid(row = 1,column = 0,pady = 10,padx=(10,0))
        customtkinter.CTkLabel(self.logging_root, text="Password : ", width=10 ,height=25,corner_radius=8,font=('arial',18)).grid(row = 2,column = 0,pady = 10,padx=(10,0))
        customtkinter.CTkEntry(self.logging_root,width=200,height=30,border_width=1,corner_radius=10,placeholder_text="Username",textvariable=username,fg_color=self.stockDetailsboxColor,text_color=self.stockDetailsboxTextColor).grid(row=1,column=1,padx = (0,10),pady=0)
        customtkinter.CTkEntry(self.logging_root,width=200,height=30,border_width=1,corner_radius=10,placeholder_text="Password",show="*",textvariable=password,fg_color=self.stockDetailsboxColor,text_color=self.stockDetailsboxTextColor).grid(row=2,column=1,padx = (0,10),pady=0)
        customtkinter.CTkButton(self.logging_root,text='Login',width=350,fg_color=self.ButtonColor,hover_color="#003333",font=("Berlin Sans FB Demi",16),command=self.sendingData_logging).grid(row=3,column=0,pady=(20,5),columnspan=2)
        customtkinter.CTkButton(self.logging_root,text='Register',width=350,fg_color=self.ButtonColor,hover_color="#003333",font=("Berlin Sans FB Demi",16),command=self.Register).grid(row=4,column=0,pady=(0,20),columnspan=2)

        self.logging_root.mainloop()
        

    def Register(self):
        global clientId
        global nic
        global clientName
        global reg_username
        global reg_password
        global ConformPassword

        WIDTH = 600 # window width
        HEIGHT = 500 # window height
        self.register_root = customtkinter.CTkToplevel(self.main_root)
        self.register_root.title("CashCup")
        self.register_root.resizable(False,False) # Tesizeble is turn offed
        self.register_root.configure(fg_color="#004444")

        # Change Window Icon 
        ico = Image.open('Images/icon.png')
        photo = ImageTk.PhotoImage(ico)
        self.register_root.wm_iconphoto(False, photo)

        self.logging_root.destroy()
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")

        # get screen width and height
        screen_width = self.register_root.winfo_screenwidth()
        screen_height = self.register_root.winfo_screenheight()
        # calculate position x and y coordinates
        x = (screen_width/2) - (WIDTH/2)
        y = (screen_height/2) - (HEIGHT/2)
        self.register_root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y-50))
    
        # Variabels for ClientId | NIC | ClientName | Username | Password | ConformPassword =================

        clientId = StringVar()
        nic = StringVar()
        clientName = StringVar()
        reg_username = StringVar()
        reg_password = StringVar()
        ConformPassword = StringVar()
        # =====================================================
        customtkinter.CTkLabel(self.register_root, text="Register Here...", width=30 ,height=25,corner_radius=8,font=('arial',22)).grid(row = 0,column = 0, columnspan = 3,pady = 10,padx=60)

        registerWindowComponent = {'ClientID : ':1,'NIC : ':2,'Client Name : ':3,'Username':4,'Password':5,'Conform Password':6}# Regisitration window Label Components
        for text,row in registerWindowComponent.items():customtkinter.CTkLabel(self.register_root, text=text, width=10 ,height=25,corner_radius=8,font=('arial',16),text_color="white").grid(row = row,column = 0,pady = 10,padx=(10,0))

        customtkinter.CTkEntry(self.register_root,width=340,height=30,border_width=1,corner_radius=10,placeholder_text="Client ID",textvariable=clientId,fg_color=self.stockDetailsboxColor,text_color=self.stockDetailsboxTextColor).grid(row=1,column=1,columnspan=2,padx = 30,pady=20)
        customtkinter.CTkEntry(self.register_root,width=340,height=30,border_width=1,corner_radius=10,placeholder_text="NIC Number",textvariable=nic,fg_color=self.stockDetailsboxColor,text_color=self.stockDetailsboxTextColor).grid(row=2,column=1,columnspan = 2,padx = 30,pady=0)
        customtkinter.CTkEntry(self.register_root,width=340,height=30,border_width=1,corner_radius=10,placeholder_text="ClientName",textvariable=clientName,fg_color=self.stockDetailsboxColor,text_color=self.stockDetailsboxTextColor).grid(row=3,column=1,columnspan=2,padx = 30,pady=20)
        customtkinter.CTkEntry(self.register_root,width=340,height=30,border_width=1,corner_radius=10,placeholder_text="Username",textvariable=reg_username,fg_color=self.stockDetailsboxColor,text_color=self.stockDetailsboxTextColor).grid(row=4,column=1,columnspan = 2,padx = 30,pady=0)
        customtkinter.CTkEntry(self.register_root,width=340,height=30,border_width=1,corner_radius=10,placeholder_text="Password",show = "*",textvariable=reg_password,fg_color=self.stockDetailsboxColor,text_color=self.stockDetailsboxTextColor).grid(row=5,column=1,columnspan=2,padx = 30,pady=20)
        customtkinter.CTkEntry(self.register_root,width=340,height=30,border_width=1,corner_radius=10,placeholder_text="Conform Password",show="*",textvariable=ConformPassword,fg_color=self.stockDetailsboxColor,text_color=self.stockDetailsboxTextColor).grid(row=6,column=1,columnspan = 2,padx = 30,pady=0)
        customtkinter.CTkButton(self.register_root,text='Register',width=500,fg_color=self.ButtonColor,hover_color="#003333",font=("Berlin Sans FB Demi",16), command=self.sendingData_Register).grid(row=7,column=0,pady=20,columnspan = 2,padx=50)
        self.logging_root.destroy()
        self.register_root.mainloop()


    def BiddingHistoryWindow(self):
        WIDTH = 600 # window width
        HEIGHT = 350 # window height
        self.history_root = customtkinter.CTkToplevel(self.main_root)
        self.history_root.title("CashCup Bidding History")
        self.history_root.resizable(False,False) # Tesizeble is turn offed
        self.history_root.configure(fg_color="#004444")
        # Change Window Icon 
        ico = Image.open('Images/icon.png')
        photo = ImageTk.PhotoImage(ico)
        self.history_root.wm_iconphoto(False, photo)

        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")

        # get screen width and height
        screen_width = self.history_root.winfo_screenwidth()
        screen_height = self.history_root.winfo_screenheight()
        # calculate position x and y coordinates
        x = (screen_width/2) - (WIDTH/2)
        y = (screen_height/2) - (HEIGHT/2)
        self.history_root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y-50))
    
        tableBar = customtkinter.CTkFrame(master=self.history_root,fg_color="red",width=1000,height=400,corner_radius=0)
        tableBar.place(x=0,y=0)
        tableBar.grid_propagate(1)

		# TREEVIEW Styling =======================================================
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",background = "#004444",foreground="white",rowheight=35,fieldbackground = "#003333")

        style.map("Treeview",background = [('selected','green')])

        scrollbar = Scrollbar(tableBar,orient=VERTICAL)
        scrollbar.pack(fill=Y,side=RIGHT)
		# ========================================================================


        columns = {'StockId':150,'BidPrice':180,'Date':190,'Time':200}
        self.biddingHistoryTable=ttk.Treeview(tableBar,column=tuple(columns.keys()),yscrollcommand=scrollbar.set,height=10)

        for column in columns.keys():self.biddingHistoryTable.heading(column,text=column)
        self.biddingHistoryTable['show']='headings'

        for column,columnSize in columns.items():self.biddingHistoryTable.column(column,width=columnSize)
        self.biddingHistoryTable.pack(fill=BOTH,expand=1)

        scrollbar.configure(command=self.biddingHistoryTable.yview)

        self.biddingHistoryButton = customtkinter.CTkButton(master=self.history_root,width=150,height=28,text="Clear History",fg_color=self.ButtonColor,font=('Berlin Sans FB Demi',14),hover_color="#A30800",state= "normal",command=self.clearnBidHistory)
        self.biddingHistoryButton.place(x=430,y=315)

        self.loadBiddingHistory()
        self.history_root.mainloop()


    def clearnBidHistory(self):
        #CLEARN BID HISTORY FROM DATABASE AND INTERFACE
        Cd.ClearHistory()
        self.history_root.destroy()

class ClientBackEnd(ClientInterface):
    # All of the Back-End Proccess Here
    def sendingData_logging(self):
        ''' username
            password'''
        message = password.get().encode()
        hashedPasswordLogIn = hashlib.md5(message).hexdigest()
        Message = f'logging,{username.get()},{hashedPasswordLogIn}'
        self.LoggingUsername = username.get()
        self.SendAndRecieve(Message)

    def sendingData_Register(self): 
        # CONVERTING HASH TO USER PASSWORD [MD5 HASH ALGORITHEM]
        message = reg_password.get().encode()
        hashedPasswordRegister = hashlib.md5(message).hexdigest()

        Message = f'Register,{clientId.get()},{nic.get()},{clientName.get()},{reg_username.get()},{hashedPasswordRegister}'
        if reg_password.get() == ConformPassword.get():
            self.SendAndRecieve(Message)
        else:
            messagebox.showerror("Password Error","Password And ConformPassword in not equal.")
            reg_password.set("");ConformPassword.set("")
            clientId.set(clientId.get());nic.set(nic.get());clientName.set(clientName.get());reg_username.set(reg_username.get())


    def connectionEstablish(self):
        #Started Window
        self.SERVER_IP = inputServerIp.get()
        self.serverIp_root.destroy()
        self.socket()


    def LoadDetailsStock(self):
        # UPDATING THREAD
        global threadE2
        threadE2 = threading.Thread(target=self.stockAutoUpdater(),args =(lambda : self.threadE2Status, ))
        threadE2.daemon= True
        threadE2.start()   

        stockId = self.stockListBox.get(ANCHOR)
        Message = f'LoadDetailsStock,{stockId}'
        self.TrackingStock = stockId
        self.SendAndRecieve(Message)


    def loadBiddingHistory(self):
        #Load Bidding History
        for item in self.biddingHistoryTable.get_children():
            self.biddingHistoryTable.delete(item)
                        
        conn = sqlite3.connect('Clientdatabase/main.db')
        c=conn.cursor()
        c.execute("SELECT *FROM BiddingHistory")
        items=c.fetchall()
        for data in items:
            self.biddingHistoryTable.insert('',END ,values=data)
        conn.commit()
        c.close()
    
    # ==========================================  
    def disconnect(self):
        Message = f'{DISCONNECTED_MSG},{self.OnlineUserName}'
        self.SendAndRecieve(Message)
    # ==========================================
    
    def biddingHistory(self):
        self.BiddingHistoryWindow()

    def Bedding(self):
        sendBetPrice = BetPrice.get()
        sendusername = username.get()

        if sendBetPrice.isnumeric() and float(sendBetPrice)>float(stockPrice.get()):
            sendLoadDetailsStockID = LoadDetailsStockID.get()
            Message = f'Bedding,{sendusername},{sendLoadDetailsStockID},{sendBetPrice},{str(LoadDetailsBasePrice.get())}'
            self.SendAndRecieve(Message)
            BetPrice.delete(0, END)
        else:
            messagebox.showerror("Betting Error","Plese Add Valied Bet !")
            BetPrice.delete(0, END)
    
    
    def stockAutoUpdater(self):
        try:
            Message = f'LoadDetailsStock,{self.TrackingStock}'
            if  self.TrackingStock != "":
                self.SendAndRecieve(Message)
        except:
            pass
        else:
            threading.Timer(2, self.stockAutoUpdater).start()
    
            
    def checker(self,message):
        self.message = message.split(",")

        if self.message[0] == "LoginSucess":
            #addBettToStockbtn
            messagebox.showinfo('Login','Login Sucess, Welcome!')
            self.ServerConnectButton.configure(text = "Connected")
            self.OnlineUserName = self.LoggingUsername
            displayID.set(username.get())
            self.ServerConnectButton.configure(state= DISABLED,text_color="black")
            self.getStockDetailsbtn.configure(state="normal")
            self.addBettToStockbtn.configure(state="normal")
            self.ServerDisconnectButton.configure(state = "normal")
            self.SendAndRecieve("GetFullStockDetails")
            self.ServerConnectButton.configure(fg_color="#39FF14",text="Connected",text_color="black")
            self.biddingHistoryButton.configure(state = "normal")
            self.logging_root.destroy()
        
        elif self.message[0] == "LoginFail":
            self.logging_root.destroy()
            messagebox.showerror("LogIn","Already Logged or Username and Password Incorrect")

        elif self.message[0] == "RegistrationSucessfully":
            messagebox.showinfo('Register','Registration Sucess')
            self.register_root.destroy()

        elif self.message[0] == "RegistationError":
            messagebox.showerror("Register","Registration Error.Check Your Details Again")

        elif self.message[0] == "AvailableStocks":
            stock = [item for item in self.message[1:]]
            for item in stock:
                self.stockListBox.insert(END,item)

        elif self.message[0] == "LoadToStockDetails":
            stockPrice.set(int(float(self.message[5])))
            try:
                entrys = [LoadDetailsStockID,LoadDetailsStockOwner,LoadDetailsBasePrice,LoadDetailsProfit,LoadDetailsAvailableHighPrice,LoadDetailsStockIDHighPriceOwner]
                messagePossitions = [n for n in range(1,7)]
                for entrybox,possition in zip(entrys,messagePossitions):
                    entrybox.set(self.message[possition])
            except:
                pass

            if self.message[9] == "NoBetStock":self.timerWindow.configure(text_color = "#39FF14",border_color = "#39FF14");stockStatus.set("NOT ACTIVATED")
            elif self.message[9] == "StockExpier":stockStatus.set("TIMEOUT");self.timerWindow.configure(text_color = "red",border_color = "red")
            elif self.message[9] == "StockNearToExpier":stockStatus.set("EXPIER SOON");self.timerWindow.configure(text_color = "yellow",border_color = "yellow")  
            elif self.message[9] == "CanBedStock":stockStatus.set("ACTIVATED");self.timerWindow.configure(text_color = "#39FF14",border_color = "#39FF14")

        elif self.message[0] == "Bedding_Sucess":
            # Bedding_Sucess,1500,prasad123
            try:
                Cd.storeBiddingHistory(self,LoadDetailsStockID.get(),str(BetPrice.get()))
                LoadDetailsAvailableHighPrice.set(self.message[1])
                LoadDetailsStockIDHighPriceOwner.set(self.message[2])
                stockPrice.set(int(self.message[1]))
                messagebox.showinfo("Betting","Your Bet is Accepted.")
                BetPrice.delete(0, END)

            except:
                Cd.storeBiddingHistory(self,LoadDetailsStockID.get(),str(BetPrice.get()))
                messagebox.showinfo("Betting","Your Bet is Accepted.")
                LoadDetailsAvailableHighPrice.set(self.message[5])
                LoadDetailsStockIDHighPriceOwner.set(self.message[6])
                stockPrice.set(int(self.message[5]))
                BetPrice.delete(0, END)

        elif self.message[0] == "NotRegisted":
            messagebox.showerror("Logging Error","Not Registerd or Username Password incorrect")
            self.logging_root.destroy()
            
        elif self.message[0] == "Disconnected":
            messagebox.showwarning("Exit","You Are Offline...")
            sys.exit()

        elif self.message[0] == "StockExpier":
            BetPrice.delete(0,END)
            messagebox.showerror("Stock Error","Stock is Expired ....")
        else:
            pass
if __name__ == '__main__':
    inter = ClientBackEnd()
    inter.ipAddressWindow()
    
