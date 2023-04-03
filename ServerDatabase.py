"""Importer Module Section"""
import sqlite3
import pandas as pd
from datetime import datetime


#============================================================================================


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
  
#============================================================================================


''' Create Main Client Database'''
class ServerDatabase:
    OnlineUser = [] # This Sturcture stored Online users now
    # Create Database and Tables
    # Registration Process
    # Logging Process
    # Bedding Process
    # Stock Adding
    def __init__(self):

        """This Section Create main database file and 
            Create Main Client Table(Register) and Main Stock Table()"""

        """ Register Table { CleitnId,NicNo,ClientName,Username,Password }
            Stockes  Table { StockId,StockOwner,BasePrice,AvailableHighPrice,HighPriceOwner}
            **** Note : In Beginneing we Should Import stocks from excel file to StockTable
        """
        conn = sqlite3.connect('ServerDatabase/main.db')
        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS customerDetails(
                    ClientId TEXT NOT NULL PRIMARY KEY,
                    NicNo TEXT NOT NULL,
                    clientName TEXT NOT NULL,
                    Username TEXT NOT NULL,
                    Password TEXT NOT NULL,
                    Status TEXT DEFAULT "OFFLINE" NOT NULL
                )""") # CREATED CustomerDetails Table

        #print("CREATED CustomerDetails Table") #Garbage =======================================

        #c.execute("DROP TABLE Stockes")
        c.execute("""CREATE TABLE IF NOT EXISTS Stockes(
                    StockId TEXT NOT NULL PRIMARY KEY,
                    StockOwner TEXT NOT NULL,
                    BasePrice REAL NOT NULL,
                    Profit TEXT NOT NULL,
                    AvailableHighPrice REAL NOT NULL,
                    HighPriceOwner TEXT NOT NULL,
                    TimeDuration TEXT NOT NULL,
                    EndTime TEXT NOT NULL
                )""") # CREATED Stockes Table
        
        conn.commit()
        c.close()

        

    def excelImport(self):
        """ Stock Details load from excel to Database """
        cxn = sqlite3.connect('ServerDatabase/main.db')
        wb = pd.read_excel('StockExcel/stocks.xlsx',sheet_name = 'Sheet1')
        wb.to_sql(name='Stockes',con=cxn,if_exists='replace',index=False)
        cxn.commit()
        cxn.close()



    def Register(self,**kwargs):
        """ Registration Process """
        # Register(ClientId = "xxxx",NicNo = "xxxxxxx",clientName = "xxxx xxxx",Username = "xxxxxxxx",Password = "*******")
        ClientId=kwargs['ClientId']
        NicNo=kwargs['NicNo']
        ClientName=kwargs['clientName']
        Username=kwargs['Username']
        Password=kwargs['Password']

        try:
            conn = sqlite3.connect('ServerDatabase/main.db')
            c = conn.cursor()
            c.execute(f"""INSERT INTO customerDetails ('ClientId','NicNo','clientName','Username','Password') VALUES (
                        "{ClientId}",
                        "{NicNo}",
                        "{ClientName}",
                        "{Username}",
                        "{Password}"
                    )""")
            conn.commit()
            c.close()
        except:
            message = f"RegistationError"
        else:
            message = f"RegistrationSucessfully"

        return message
    


    def AddStock(self,**kwargs):
        # AddStock(StockId = "xxxx", StockOwner = "xxxxxxx", BasePrice = "xxxx xxxx", Profit = "xxxxxxxx", AvailableHighPrice = 0000.00, HighPriceOwner = "xxxxxxx")
        """ New Stock Add To Database """
        StockId=kwargs['StockId']
        StockOwner=kwargs['StockOwner']
        BasePrice=kwargs['BasePrice']
        Profit = kwargs['Profit']
        AvailableHighPrice=kwargs['AvailableHighPrice']
        HighPriceOwner=kwargs['HighPriceOwner']

        try:
            conn = sqlite3.connect('ServerDatabase/main.db')
            c = conn.cursor()
            c.execute(f"""INSERT INTO Stockes ('StockId','StockOwner','BasePrice','Profit','AvailableHighPrice','HighPriceOwner') VALUES (
                        "{StockId}",
                        "{StockOwner}",
                        "{BasePrice}",
                        "{Profit}",
                        "{AvailableHighPrice}",
                        "{HighPriceOwner}"
                    )""")
            conn.commit()
            c.close()
        except Exception as e:
            message = f"Stock Adding Error : {e}"
        else:
            message = f"Stock Added Sucessfully"

        return message # **************************************** This is Important ****************************************


    def Betting(self,**kwargs):
        StockId = kwargs["StockId"]
        AvailableHighPrice = float(kwargs["AvailableHighPrice"])
        HighPriceOwner = kwargs["HighPriceOwner"]
        BasePrice = kwargs["BasePrice"]

        try:
            conn = sqlite3.connect('ServerDatabase/main.db')
            c = conn.cursor()
            # ========================================
            c.execute("SELECT EndTime FROM Stockes WHERE StockId = ?",(StockId,))

            data = c.fetchall()[0][0]
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            Ctime = current_time.split(":")
            if str(data) != "NOT Updated":
            #    Time converting to seconds ========
                totalSecondsCtime = int(Ctime[0])*3600+int(Ctime[1])*60+int(Ctime[2])
                timeSectors = data.split(":")
                totelSecondsOfEndTime = int(timeSectors[0])*3600+int(timeSectors[1])*60+int(timeSectors[2])

                gapOfTime = totelSecondsOfEndTime-totalSecondsCtime # Calculate Gap of ENDTIME and NOW TIME
                if totelSecondsOfEndTime<=totalSecondsCtime:
                    return "StockExpier"
                elif gapOfTime<=30:
                    c.execute("SELECT EndTime From Stockes WHERE StockId = ?",(StockId,))
                    time = c.fetchall()[0][0].split(":")
                    time[1] = str(int(time[1])+1)
                    updatedTime = ":".join(time)
                    c.execute("UPDATE Stockes SET EndTime = ? WHERE StockId = ? ",(updatedTime,StockId,))
            else:
                c.execute("SELECT TimeDuration FROM Stockes WHERE StockId = ?",(StockId,))
                DurationTime = c.fetchall()
                # get time in minute
                Duration = str(DurationTime[0][0]).split(":")
                DurationH,DurationM,DurationS = int(Duration[0])*3600,int(Duration[1])*60,int(Duration[2])
                TotalSeconds = DurationH+DurationM+DurationS
                # End time Calculation Part
                #Hour Update
                Ctime[0] = str(int(Ctime[0])+(TotalSeconds//3600))
                #Min Update
                Ctime[1] = str((int(Ctime[1]))+(TotalSeconds%3600)//60)
                #Sec Update
                Ctime[2] = str(int(Ctime[2])+((TotalSeconds%3600)%60))
                # Time Arrangement ===========
                if int(Ctime[2])>59:
                    Ctime[2] = str(int(Ctime[2])%60)
                    Ctime[1] = str(int(Ctime[1])+1)
                if int(Ctime[1])>59:
                    Ctime[1] = str(int(Ctime[1])%60)
                    Ctime[0] = str(int(Ctime[0])+1)
                UpdatedEndTime = ":".join(Ctime) # Updated Time (End Time)

                c.execute("UPDATE Stockes SET EndTime = ? WHERE StockId = ? ",(UpdatedEndTime,StockId,)) 
            #=========================================
            c.execute("UPDATE Stockes SET AvailableHighPrice= ? , HighPriceOwner = ? ,Profit = ?  WHERE StockId = ?",(AvailableHighPrice,HighPriceOwner,(str(int(AvailableHighPrice)-int(BasePrice))),StockId,))
            conn.commit()
            c.close()
        except:
            return "Beddding_Unsucess"
        else:
            # IF TRY PART IS "OK" SEND UPDATED STOCK DETAILS TO CLIENTS
            conn = sqlite3.connect('ServerDatabase/main.db')
            c = conn.cursor()
            c.execute("SELECT AvailableHighPrice,HighPriceOwner FROM Stockes WHERE StockId=?", (StockId,))
            stock = c.fetchall()
            L = ["Bedding_Sucess"]
            for n in stock[0]:
                L.append(str(n))
            return (",".join(L))   # UPDATED STOCK DETAILS
    
    def Logging(self,**kwargs):
        # Online User Accounds ===========
        # Logging(Username = "xxxxxx",Password = "xxxxxxxxxxxxxxx")
        try:
            Username = kwargs['Username']
            Password = kwargs['Password']
            conn = sqlite3.connect('ServerDatabase/main.db')
            c = conn.cursor()
            c.execute("SELECT Password FROM customerDetails WHERE Username = ? ",(Username,))
            database_password = c.fetchall()[0][0]       
            if Password == database_password and (Username not in self.OnlineUser):
                self.OnlineUser.append(Username)
                c.execute("UPDATE customerDetails SET Status = 'ONLINE' WHERE Username = ?",(Username,))
                conn.commit()
                c.close()
                return "LoginSucess"
            else:
                return "LoginFail"
        except:
            return "LoginFail"


    #  This method use for send Available stocks from server to client interface =================================
    def AvailableStocks(self,table): 
        conn = sqlite3.connect('ServerDatabase/main.db')
        c = conn.cursor()
        c.execute(f"""SELECT StockId FROM "{table}" """)
        stock = c.fetchall()
        L  = ["AvailableStocks"]
        for n in stock:
            L.append(n[0])
        return (",".join(L))


    def LoadDetailsStock(self,stockId):
        try:
            conn = sqlite3.connect('ServerDatabase/main.db')
            c = conn.cursor()
            c.execute("SELECT * FROM Stockes WHERE StockId=?", (stockId,))
            stock = c.fetchall()
            L  = ["LoadToStockDetails"]
            for n in stock[0]:
                L.append(str(n))
            L.append(self.stockStatusSelector(stockId))
            return (",".join(L))
        except:
            return " "


    def removeOnlineCustomer(self,username):
        try:
            self.OnlineUser.remove(username)
            conn = sqlite3.connect('ServerDatabase/main.db')
            c = conn.cursor()
            c.execute("UPDATE customerDetails SET Status = 'OFFLINE' WHERE Username = ? ",(username,))
            conn.commit()
            c.close()
        except Exception as e:
            pass

    def activeDatabaseClean(self):
        # Clean active user records
        try:
            self.OnlineUser.clear()
            conn = sqlite3.connect('ServerDatabase/main.db')
            c = conn.cursor()
            c.execute("UPDATE customerDetails SET Status = 'OFFLINE'")
            conn.commit()
            c.close()
        except Exception as e:
            pass

    def stockStatusSelector(self,StockId):
        # 
        conn = sqlite3.connect('ServerDatabase/main.db')
        c = conn.cursor()
            # ========================================
        c.execute("SELECT EndTime FROM Stockes WHERE StockId = ?",(StockId,))

        data = c.fetchall()[0][0]
        if str(data) != "NOT Updated":
            #    Time converting to seconds ========
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            Ctime = current_time.split(":")
            totalSecondsCtime = int(Ctime[0])*3600+int(Ctime[1])*60+int(Ctime[2])
                
            timeSectors = data.split(":")
            totelSecondsOfEndTime = int(timeSectors[0])*3600+int(timeSectors[1])*60+int(timeSectors[2])

            gapOfTime = totelSecondsOfEndTime-totalSecondsCtime
            if totelSecondsOfEndTime<=totalSecondsCtime:
                return "StockExpier"
            elif gapOfTime<=30:
                return "StockNearToExpier"
            else:
                return "CanBedStock"
        else:
            return "NoBetStock";



