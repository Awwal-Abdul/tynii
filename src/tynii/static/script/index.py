import sqlite3
import uuid
from datetime import datetime

from js import Uint8Array, alert, document, window
from pyscript import when

BACKEND_URL = "http://localhost:5000"
DB_NAME = "url_shortener.sqlite3"


conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        short_code TEXT UNIQUE NOT NULL,
        original_url TEXT NOT NULL,
        click_count INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS click_analytics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        link_id INTEGER NOT NULL,
        clicked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        user_agent TEXT,
        referer TEXT,
        FOREIGN KEY (link_id) REFERENCES links(id) ON DELETE CASCADE
    );
""")

conn.commit()


def persist_db():
    """Reads the SQLite file from Pyodide virtual disk and saves it to IndexedDB."""
    with open(DB_NAME, "rb") as f:
        db_bytes = f.read()
    uint8_arr = Uint8Array.new(db_bytes)
    # Call JS helper asynchronously
    window.saveToIndexedDB(uint8_arr.buffer)


def encode_base62(num: int) -> str:
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if num == 0:
        return chars[0]
    encoded = []
    while num > 0:
        num, remainder = divmod(num, 62)
        encoded.append(chars[remainder])
    return "".join(reversed(encoded))


def generate_short_code() -> str:
    u = uuid.uuid4().int
    return encode_base62(u)[:7]


def load_links():
    tbody = document.getElementById("linksTableBody")
    tbody.innerHTML = ""

    cursor.execute(
        "SELECT id, short_code, original_url, click_count FROM links ORDER BY id DESC;"
    )
    links = cursor.fetchall()

    for link in links:
        link_id = link[0]
        short_code = link[1]
        original_url = link[2]
        click_count = link[3]

        tr = document.createElement("tr")
        tr.innerHTML = f"""
            <td><b><a href="{BACKEND_URL}/{short_code}" target="_blank">{short_code}</a></b></td>
            <td><a href="{original_url}" target="_blank">{original_url}</a></td>
            <td>{click_count}</td>
            <td><button id="click-{link_id}" style="padding: 4px 8px; font-size: 0.8rem;">Simulate Visit</button></td>
        """
        tbody.appendChild(tr)


@when("click", "#createBtn")
def handler():
    longUrl = str(document.getElementById("longUrl").value).strip()

    print(longUrl)

    if not longUrl:
        alert("PLease enter a url")
        return

    short_code = generate_short_code()

    try:
        # Use SQLAlchemy session to insert the new link
        cursor.execute(
            "INSERT INTO links (short_code, original_url) VALUES (?, ?);",
            (short_code, longUrl),
        )
        conn.commit()

        document.getElementById("longUrl").value = ""
        persist_db()
        load_links()
    except Exception as e:
        window.alert(f"Error creating link: {str(e)}")


load_links()
