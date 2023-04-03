import sqlite3
import datetime
from tkinter import messagebox


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
class ClientDatabase:
    """HANDLE BIDDING HISTORY DATABASE"""
    def __init__(self):
        """create Bidding History Database """
        conn = sqlite3.connect("Clientdatabase/main.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS BiddingHistory(
                  StockId TEXT NOT NULL,
                  BidPrice TEXT NOT NULL,
                  Date TEXT NOT Null,
                  Time TEXT NOT NULL
        )""")
        conn.commit()
        c.close()
    
    def storeBiddingHistory(self,StockId,BidPrice):
        current_time = datetime.datetime.now()
        Date = f"{current_time.year}/{current_time.month}/{current_time.day}"
        Time = f"{current_time.hour}:{current_time.minute}:{current_time.second}"

        conn = sqlite3.connect("Clientdatabase/main.db")
        c = conn.cursor()
        c.execute(f"""INSERT INTO BiddingHistory ('StockId','BidPrice','Date','Time') VALUES (
                        "{StockId}",
                        "{BidPrice}",
                        "{Date}",
                        "{Time}"
                    )""")
        conn.commit()
        c.close()

    def ClearHistory():
        try:
            conn = sqlite3.connect("Clientdatabase/main.db")
            c = conn.cursor()
            c.execute(f"""DELETE FROM BiddingHistory""")
            conn.commit()
            c.close()
            messagebox.showinfo("Bidding History","History Deleted Successfully")
        except:
            pass