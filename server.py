"""Importer Module Section"""
import socket
import sqlite3
from tkinter import *
from tkinter import ttk
import time
import threading
from ServerDatabase import ServerDatabase as SDB
import customtkinter
from PIL import Image,ImageTk
import sys


IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (IP,PORT)
DISCONNECTED_MSG = "!DISCONNECT"
SIZE = 4096
FORMAT = 'utf-8'


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

class ServerFrontEnd(SDB):
	# Server Main Class (HANDDLE INYETFACE AND CONNECTIONS)
	OpenedTable = ""
	def ServerInterface(self):
		WIDTH = 1000 # window width
		HEIGHT=750 # window height
		self.root= customtkinter.CTk()
		self.root.title("CashCup")
		self.root.resizable(False,False) # Tesizeble is turn offed
		
		# Change Window Icon 
		ico = Image.open('Images/icon.png')
		photo = ImageTk.PhotoImage(ico)
		self.root.wm_iconphoto(False, photo)

		customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
		customtkinter.set_default_color_theme("blue")

        # get screen width and height
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()
        # calculate position x and y coordinates
		x = (screen_width/2) - (WIDTH/2)
		y = (screen_height/2) - (HEIGHT/2)
		self.root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y-50))

		titlebar = customtkinter.CTkFrame(master=self.root,fg_color="#003333",width=1000,height=60,corner_radius=0)
		titlebar.place(x=0,y=0)
		self.connectButton = customtkinter.CTkButton(master=self.root,text="SERVER IS OFFLINE",fg_color="red",text_color="white",corner_radius=20,bg_color="#003333",font=("Berlin Sans FB Demi",14))
		self.connectButton.place(x=800,y=15)

		logo = customtkinter.CTkImage(light_image=Image.open("Images/logo.png"),dark_image=Image.open("Images/logo.png"),size=(44, 44))
		customtkinter.CTkButton(master=titlebar,image=logo,text="",fg_color="transparent",width=44,height=44).place(x=25,y=5)
		customtkinter.CTkLabel(master=titlebar,text = "CashCup",font=("Cooper Black",35),text_color="white").place(x=85,y=5)

		self.getStockDataBtn = customtkinter.CTkButton(master=titlebar,text = "   Stock Details   ",height=40,width=20,fg_color="red",text_color="black",font=("Berlin Sans FB Demi",14),hover_color="yellow",state = 'normal',command=self.show_all_Stock_data_in_database)
		self.getStockDataBtn.place(x=470,y=10)
		self.getCustomerDataBtn = customtkinter.CTkButton(master=titlebar,text = "Customer Details",height=40,width=20,fg_color="red",text_color="black",font=("Berlin Sans FB Demi",14),hover_color="yellow",state = 'normal',command = self.tableChangeForCustomers)
		self.getCustomerDataBtn.place(x=600,y=10)


		self.tableBar = customtkinter.CTkFrame(master=self.root,fg_color="red",width=1020,height=400,corner_radius=0)
		self.tableBar.place(x=0,y=60)
		self.tableBar.grid_propagate(1)

		# TREEVIEW Styling =======================================================
		style = ttk.Style()
		style.theme_use("clam")
		style.configure("Treeview",background = "#004444",foreground="white",rowheight=35,fieldbackground = "#003333")

		style.map("Treeview",background = [('selected','green')])

		scrollbar = Scrollbar(self.tableBar,orient=VERTICAL)
		scrollbar.pack(fill=Y,side=RIGHT)
		# ========================================================================

		# MAIN TABLE COMFIGURATION ====================================================================================
		columns = {'StockId':200,'StockOwner':210,'BasePrice':200,'Profit':200,'AvailableHighPrice':200,'HighPriceOwner':220}
		self.serverTable=ttk.Treeview(self.tableBar,column=(tuple(column for column in columns.keys())),yscrollcommand=scrollbar.set,height=19)

		for columnNames in columns.keys():self.serverTable.heading(columnNames,text=columnNames)
		self.serverTable['show']='headings' # Configuring Column Headers
		
		for columnNames,columnSize in columns.items():self.serverTable.column(columnNames,width = columnSize)
		self.serverTable.pack(fill=BOTH,expand=1) # Configuring Column Sizes

		scrollbar.configure(command=self.serverTable.yview)

		commandBar = customtkinter.CTkFrame(master=self.root,width=1000,height=150,fg_color="red",corner_radius=0)
		commandBar.place(x=0,y=610)
		self.textbox = customtkinter.CTkTextbox(master=commandBar,width=1000,corner_radius=0,activate_scrollbars=True,height=150,text_color="#39FF14",fg_color="black")
		self.textbox.grid(row=0,column=0)


		self.powerOnBtn = customtkinter.CTkImage(light_image=Image.open("Images/switch-off.png"),dark_image=Image.open("Images/switch-off.png"),size=(50, 50))
		self.poweOffBtn = customtkinter.CTkImage(light_image=Image.open("Images/switch-on.png"),dark_image=Image.open("Images/switch-on.png"),size=(50, 50))
		self.serverPowerOffBtn = customtkinter.CTkButton(master=self.root,width=0,height=0,image=self.powerOnBtn,fg_color='#003333',text="",font=('Berlin Sans FB Demi',14),hover_color="#003333",state= "normal",command=self.startedThread)
		self.serverPowerOffBtn.place(x=320,y=1)

		# ===========================================================================================================
		SDB().excelImport() # Load Details from excel to Database
		self.root.mainloop()

	def startedThread(self):
		global threadEl
		threadEl = threading.Thread(target=self.connections)
		threadEl.daemon = True
		threadEl.start()

	def tableChangeForCustomers(self):
		self.CustomertableBar = customtkinter.CTkFrame(master=self.root,fg_color="red",width=1000,height=400,corner_radius=0)
		self.CustomertableBar.place(x=0,y=60)
		self.CustomertableBar.grid_propagate(1)

		style = ttk.Style()
		style.theme_use("clam")
		style.configure("Treeview",background = "#004444",foreground="white",rowheight=35,fieldbackground = "#004444")

		style.map("Treeview",background = [('selected','transparent')])

		scrollbar = Scrollbar(self.CustomertableBar,orient=VERTICAL)
		scrollbar.pack(fill=Y,side=RIGHT)

		# Customer Details Table Configuration========================================================================
		columns = {"ClientID":200,"ClientName":200,"NIC":200,"Username":200,"Password":250,"Status":180} # Column Headers and Column Sizes
		self.serverClientTable=ttk.Treeview(self.CustomertableBar,column=(tuple(column for column in columns.keys())),yscrollcommand=scrollbar.set,height=19)
		self.serverClientTable.configure(column=(tuple(column for column in columns.keys())))

		for columnNames in columns.keys() : self.serverClientTable.heading(columnNames,text = columnNames)
		self.serverClientTable['show']='headings'	# Configuring Column Headers

		for columnNames,columnSize in columns.items():self.serverClientTable.column(columnNames,width = columnSize)
		self.serverClientTable.pack(fill=BOTH,expand=1) # Configuring Column Sizes

		scrollbar.configure(command=self.serverClientTable.yview)
		self.show_all_Client_data_in_database()
		#==============================================================================================================



class ServerBackEnd(ServerFrontEnd):

	def handle_thread(self,connecntion,address):
		"""Threading For Each Client"""
		self.textbox.insert(END,f"[NEW Connection Established {address} Connected.]"+'\n')
		connected = True
		while connected:
			try:
				message = connecntion.recv(SIZE).decode(FORMAT)
				commandSMessage = self.commandSelector(message)
				connecntion.send(commandSMessage.encode(FORMAT))
			except:
				time.sleep(2)

	def connections(self):
		"""Handle All Connectivity Between Client and server"""
		# SERVER START
		self.serverOn()
		server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			server_socket.bind(ADDR)
			server_socket.listen()
			self.textbox.insert(END,f"Server Is listning for connections IP : {IP}:{PORT}"+'\n')
		except socket.error as err_msg:
			self.textbox.insert(END,f"Connecntion Error | {err_msg}")
		while True:
			connecntion,address = server_socket.accept()
			thread = threading.Thread(target = self.handle_thread,args = (connecntion,address))
			thread.start()


	def commandSelector(self,message):
		"""Request Selector"""
		message = message.split(",")
		if str(message[0])=="logging":
			# Logging(Username = "xxxxxx",Password = "xxxxxxxxxxxxxxx")
			sendcommand = SDB().Logging(Username=str(message[1]),Password=str(message[2]))
			if sendcommand == "LoginSucess" and self.OpenedTable == "ClientDetailsTable" :self.loader(self.serverClientTable,"customerDetails")
			return sendcommand

		elif str(message[0])=="Register":
			#Register(ClientId = "1234",NicNo = "200104801533",clientName = "Prasad",Username = "PrrasadClient1",Password = "23615")
			sendcommand = SDB().Register(ClientId = str(message[1]),NicNo = str(message[2]),clientName = str(message[3]),Username = str(message[4]),Password = str(message[5]))
			if sendcommand == "RegistrationSucessfully" and self.OpenedTable == "ClientDetailsTable" :self.loader(self.serverClientTable,"customerDetails")
			return sendcommand
			
		elif str(message[0])=="GetFullStockDetails":
			# In this section use for get available stock from server to client interface
			# This Section is runing automatically
			sendcommand = SDB().AvailableStocks("Stockes")
			return sendcommand

		elif str(message[0]) == "LoadDetailsStock":
			sendcommand = SDB().LoadDetailsStock(str(message[1]))
			return sendcommand

		elif str(message[0])=="Bedding":
			sendcommand = SDB().Betting(StockId=str(message[2]),AvailableHighPrice=str(message[3]),HighPriceOwner=str(message[1]),BasePrice = str(message[4]))
			self.refresher(sendcommand)
			return sendcommand
	
		elif str(message[0]) == DISCONNECTED_MSG:
			SDB().removeOnlineCustomer(message[1])
			if self.OpenedTable == "ClientDetailsTable": self.loader(self.serverClientTable,"customerDetails")
			# messagebox.showwarning("Message","Disconnect message receive")
			return "Disconnected"


	def show_all_Stock_data_in_database(self):
		#Load Available All Stock Details To Server Side Interface
		try:
			self.OpenedTable = "StockTable"
			self.CustomertableBar.destroy()
			self.getStockDataBtn.configure(state = DISABLED)
			self.getCustomerDataBtn.configure(state = "normal")
		except:
			pass
		finally:
			self.loader(self.serverTable,"Stockes")


	def show_all_Client_data_in_database(self):
		#Load Available All Customer Data To Server Side Interface
		try:
			self.OpenedTable = "ClientDetailsTable"
			self.getStockDataBtn.configure(state = "normal")
			self.getCustomerDataBtn.configure(state = DISABLED)
		except:
			pass
		finally:
			self.loader(self.serverClientTable,"customerDetails")



	def serverOn(self):
		# SERVER ONLINE CHANGERS
		self.serverPowerOffBtn.configure(image=self.poweOffBtn,command = self.serverOff)
		self.connectButton.configure(state = 'normal',text = 'SERVER IS ONLINE',fg_color = "#39FF14",text_color = "black")
		self.textbox.insert(END,"[STARTING] Server is Started..."+'\n')

	def serverOff(self):
		#SERVER OFFLINE CHANGERS
		SDB.activeDatabaseClean(self)# CLEARNING ACTIVE DATABASE
		self.serverPowerOffBtn.configure(image=self.powerOnBtn,state = DISABLED)
		self.connectButton.configure(state = 'normal',text = 'SERVER IS OFFLINE',fg_color = "red",text_color = "white")
		self.textbox.insert(END,f"[<<<<<<<<<<<< SERVER IS OFFLINE >>>>>>>>>>>>>>>.]")
		self.root.after(4000,sys.exit)
		
	
	def refresher(self,message):
		#After Proccess Runinig Refresh Server side Interface
		message = message.split(",")
		if message[0]=="Bedding_Sucess" and self.OpenedTable == "StockTable" :
			self.loader(self.serverTable,"Stockes")


	def loader(self,loader_root,table):
		#This is the main method for Data loading to interfaces
		loader_root.tag_configure("ONLINE",background = "#008000")
		loader_root.tag_configure("OFFLINE",background = "#B71401")
		loader_root.tag_configure("NORMAL", background = "#004444")
		for item in loader_root.get_children():
			loader_root.delete(item)
		conn=sqlite3.connect('ServerDatabase/main.db')
		c=conn.cursor()
		c.execute(f"SELECT *FROM {table}")
		items=c.fetchall()
		for data in items:
			rowcolor = "OFFLINE "if data[5] == "OFFLINE" else "ONLINE" if data[5]=="ONLINE" else "NORMAL"
			loader_root.insert('',END ,values=data,tags = (rowcolor))
		conn.commit()
		c.close()

if __name__ == '__main__':
	server = ServerBackEnd()
	server.ServerInterface()