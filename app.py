
import sqlite3
from pathlib import Path
from flask import Flask, render_template, request

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB = "/tmp/tiket.db"
SQL_FILE = BASE_DIR / "database.sql"


def connect_db():
    return sqlite3.connect(DB)


def initialize_db():
    with connect_db() as db:
        db.executescript(
            SQL_FILE.read_text(encoding="utf-8")
        )


initialize_db()


@app.route("/", methods=["GET", "POST"])
def home():
    pesan = None

    with connect_db() as db:
        flights = db.execute(
            "SELECT id, origin, destination, price FROM flights"
        ).fetchall()

    if request.method == "POST":
        nama = request.form.get("nama", "").strip()

        try:
            flight_id = int(request.form.get("flight_id", ""))
            jumlah = int(request.form.get("jumlah", ""))
        except ValueError:
            flight_id = 0
            jumlah = 0

        flight = next(
            (f for f in flights if f[0] == flight_id),
            None
        )

        if not nama or len(nama) > 100:
            pesan = "Masukkan nama yang valid."
        elif flight is None or not 1 <= jumlah <= 6:
            pesan = "Pilih penerbangan dan jumlah tiket yang valid."
        else:
            total = flight[3] * jumlah

            with connect_db() as db:
                db.execute(
                    """INSERT INTO bookings
                    (passenger_name, flight_id, quantity, total_price)
                    VALUES (?, ?, ?, ?)""",
                    (nama, flight_id, jumlah, total)
                )

            pesan = f"Simulasi berhasil! Total: Rp{total:,}"

    return render_template(
        "index.html",
        flights=flights,
        pesan=pesan
    )


if __name__ == "__main__":
    app.run(debug=True)
