from flask import Flask, render_template, request, redirect, session
import sqlite3
import yfinance as yf
import requests
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = "finance_secret_key"

# =============================
# DATABASE
# =============================     

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT)
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS portfolio(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    type TEXT,
    code TEXT,
    buy_price REAL,
    qty REAL)
    """)

    conn.commit()
    conn.close()

init_db()

# =============================
# HOME
# =============================

@app.route("/")
def home():
    return redirect("/login")

# =============================
# REGISTER
# =============================

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        conn=sqlite3.connect("database.db")
        cur=conn.cursor()

        cur.execute("INSERT INTO users(username,password) VALUES(?,?)",(username,password))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# =============================
# LOGIN
# =============================

@app.route("/login",methods=["GET","POST"])
def login():

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        conn=sqlite3.connect("database.db")
        cur=conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))

        user=cur.fetchone()

        conn.close()

        if user:
            session["user_id"]=user[0]
            return redirect("/dashboard")
        else:
            return "Invalid Login"

    return render_template("login.html")

# =============================
# DASHBOARD
# =============================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    conn=sqlite3.connect("database.db")
    cur=conn.cursor()

    cur.execute("SELECT * FROM portfolio WHERE user_id=?",(session["user_id"],))

    rows=cur.fetchall()

    conn.close()

    portfolio=[]

    total_invested=0
    total_current=0

    for row in rows:

        id=row[0]
        type_=row[2]
        code=row[3]
        buy=row[4]
        qty=row[5]

        live_price=0

        # STOCK
        if type_=="Stock":

            try:
                stock=yf.Ticker(code)
                data=stock.history(period="1d")

                if not data.empty:
                    live_price=data["Close"].iloc[-1]
            except:
                live_price=0

            invested=buy*qty
            current=live_price*qty

        # MUTUAL FUND
        else:

            try:
                url=f"https://api.mfapi.in/mf/{code}"
                data=requests.get(url).json()

                nav=float(data["data"][0]["nav"])

                live_price=nav

            except:
                live_price=0

            invested=buy
            current=nav*qty

        profit=current-invested

        total_invested+=invested
        total_current+=current

        portfolio.append({
            "id":id,
            "type":type_,
            "code":code,
            "buy":buy,
            "qty":qty,
            "live":round(live_price,2),
            "profit":round(profit,2)
        })

    total_profit=total_current-total_invested

    return render_template("dashboard.html",
                           portfolio=portfolio,
                           total_profit=round(total_profit,2))

# =============================
# ADD STOCK
# =============================

@app.route("/add_stock",methods=["POST"])
def add_stock():

    symbol=request.form["symbol"]
    buy=float(request.form["buy_price"])
    qty=float(request.form["qty"])

    conn=sqlite3.connect("database.db")
    cur=conn.cursor()

    cur.execute("INSERT INTO portfolio(user_id,type,code,buy_price,qty) VALUES(?,?,?,?,?)",
                (session["user_id"],"Stock",symbol,buy,qty))

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# =============================
# ADD MUTUAL FUND
# =============================

@app.route("/add_mf",methods=["POST"])
def add_mf():

    code=request.form["mf_code"]
    invest=float(request.form["invest"])
    units=float(request.form["units"])

    conn=sqlite3.connect("database.db")
    cur=conn.cursor()

    cur.execute("INSERT INTO portfolio(user_id,type,code,buy_price,qty) VALUES(?,?,?,?,?)",
                (session["user_id"],"MutualFund",code,invest,units))

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# =============================
# DELETE INVESTMENT
# =============================

@app.route("/delete/<int:id>")
def delete(id):

    conn=sqlite3.connect("database.db")
    cur=conn.cursor()

    cur.execute("DELETE FROM portfolio WHERE id=?",(id,))

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# =============================
# GOLD PRICE
# =============================

@app.route("/gold")
def gold():

    gold=yf.Ticker("GC=F")

    data=gold.history(period="1d")

    price=data["Close"].iloc[-1]

    return f"Live Gold Price: ${price}"

# =============================
# EXPORT PDF
# =============================

@app.route("/export_pdf")
def export_pdf():

    conn=sqlite3.connect("database.db")
    cur=conn.cursor()

    cur.execute("SELECT code,buy_price,qty FROM portfolio WHERE user_id=?",(session["user_id"],))

    data=cur.fetchall()

    conn.close()

    c=canvas.Canvas("portfolio_report.pdf")

    y=750

    for row in data:

        text=f"{row[0]} Buy:{row[1]} Qty:{row[2]}"
        c.drawString(100,y,text)

        y-=20

    c.save()

    return "PDF Generated in Project Folder"

# =============================
# LOGOUT
# =============================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

# =============================
# RUN
# =============================

if __name__=="__main__":
    app.run(debug=True)