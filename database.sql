
CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    price INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger_name TEXT NOT NULL,
    flight_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total_price INTEGER NOT NULL,
    FOREIGN KEY (flight_id) REFERENCES flights(id)
);

INSERT OR IGNORE INTO flights
    (id, origin, destination, price)
VALUES
    (1, 'Jakarta', 'Bali', 850000),
    (2, 'Jakarta', 'Surabaya', 600000),
    (3, 'Jakarta', 'Yogyakarta', 500000),
    (4, 'Bali', 'Jakarta', 850000);
