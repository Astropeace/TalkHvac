import sqlite3
import typer
from typing import List, Dict
from pathlib import Path

DB_PATH = "hvac_parts.db"

class SQLiteManager:
    def __init__(self, db_path: str = DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS parts (
                oem_number TEXT PRIMARY KEY,
                manufacturer TEXT,
                description TEXT,
                alternate_numbers TEXT,
                price REAL,
                source_url TEXT
            )
        """)
        self.conn.commit()

    def insert_parts(self, parts: List[Dict]):
        for part in parts:
            self.cursor.execute("""
                INSERT OR REPLACE INTO parts 
                (oem_number, manufacturer, description, alternate_numbers, price, source_url)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                part["oem_number"],
                part["manufacturer"],
                part["description"],
                ",".join(part["alternate_numbers"]),
                part["price"],
                part["source_url"]
            ))
        self.conn.commit()

    def search_part(self, oem_number: str) -> Dict:
        self.cursor.execute("""
            SELECT * FROM parts WHERE oem_number = ?
        """, (oem_number,))
        result = self.cursor.fetchone()
        if result:
            return {
                "oem_number": result[0],
                "manufacturer": result[1],
                "description": result[2],
                "alternate_numbers": result[3].split(",") if result[3] else [],
                "price": result[4],
                "source_url": result[5]
            }
        return None

    def search_by_keyword(self, keyword: str) -> List[Dict]:
        self.cursor.execute("""
            SELECT * FROM parts 
            WHERE description LIKE ? 
            OR manufacturer LIKE ?
        """, (f"%{keyword}%", f"%{keyword}%"))
        return [self._row_to_dict(row) for row in self.cursor.fetchall()]

    def _row_to_dict(self, row):
        return {
            "oem_number": row[0],
            "manufacturer": row[1],
            "description": row[2],
            "alternate_numbers": row[3].split(",") if row[3] else [],
            "price": row[4],
            "source_url": row[5]
        }

app = typer.Typer()
db_manager = SQLiteManager()

@app.command()
def find_part(oem_number: str):
    """Lookup HVAC parts by OEM number"""
    part = db_manager.search_part(oem_number)
    if part:
        typer.echo("\nPart Found:")
        typer.echo(f"OEM Number: {part['oem_number']}")
        typer.echo(f"Manufacturer: {part['manufacturer']}")
        typer.echo(f"Description: {part['description']}")
        typer.echo(f"Alternates: {', '.join(part['alternate_numbers']) or 'None'}")
        typer.echo(f"Price: ${part['price']:.2f}")
        typer.echo(f"Source: {part['source_url']}")
    else:
        typer.echo(f"No part found with OEM number: {oem_number}")

if __name__ == "__main__":
    # Initialize with sample data for testing
    db_manager.insert_parts([{
        "oem_number": "Trane-1234",
        "manufacturer": "Trane",
        "description": "Compressor Contactor 30 Amp",
        "alternate_numbers": ["Generic-5678", "Carrier-9012"],
        "price": 89.99,
        "source_url": "https://example.partssupplier.com/trane-1234"
    }])
    app()
