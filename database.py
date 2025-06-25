import sqlite3
import os

def save_chemical(name, cas, cid, image_url):
    # Make sure the data folder exists
    os.makedirs("chemical_research_agent/data", exist_ok=True)

    # Connect to SQLite database
    conn = sqlite3.connect("chemical_research_agent/data/chemicals.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS chemicals (name TEXT, cas TEXT, cid INTEGER, image_url TEXT)")
    c.execute("INSERT INTO chemicals VALUES (?, ?, ?, ?)", (name, cas, cid, image_url))
    conn.commit()
    conn.close()
