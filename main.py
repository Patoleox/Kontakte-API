from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

def init_db():
    conn = sqlite3.connect("kontakte.sqlite")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Kontakte 
        (name TEXT, email TEXT)""")
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect("kontakte.sqlite")
    conn.row_factory = sqlite3.Row
    return conn

class Kontakt(BaseModel):
    name: str
    email: str

app = FastAPI()
init_db()

@app.get("/")
def startseite():
    return {"nachricht": "Hallo! Meine erste API"}

@app.get("/kontakte")
def kontakte():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT name, email FROM Kontakte")
    rows = cur.fetchall()
    conn.close()
    return [{"name": row["name"], "email": row["email"]} for row in rows]

@app.get("/kontakte/{name}")
def kontakte_suchen(name: str):
    return {"name": name}

@app.post("/kontakte")
def kontakt_hinzufuegen(kontakt: Kontakt):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO Kontakte (name, email) VALUES (?, ?)", (kontakt.name, kontakt.email))
    conn.commit()
    conn.close()
    return {"nachricht": f"{kontakt.name} wurde hinzugefügt!"}

@app.delete("/kontakte/{name}")
def kontakt_loeschen(name: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM Kontakte WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    return {"nachricht": f"{name} wurde gelöscht."}

@app.put("/kontakte/{name}")
def kontakt_updaten(name: str, kontakt: Kontakt):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE Kontakte SET email = ? WHERE name = ?", (kontakt.email, name))
    conn.commit()
    conn.close()
    return {"nachricht": f"{name} wurde aktualisiert! "}


