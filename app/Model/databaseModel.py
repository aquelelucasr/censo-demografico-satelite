import sqlite3

DB_NAME = "search_history.db"

def setup_db():
    """Cria a tabela de histórico se ela ainda não existir."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT NOT NULL,
            lat_tl REAL NOT NULL,
            lon_tl REAL NOT NULL,
            lat_br REAL NOT NULL,
            lon_br REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

### create
def save_search(slug: str, lat_tl: float, lon_tl: float, lat_br: float, lon_br: float) -> None:
    """Recebe o slug e os 4 pontos da bounding box e faz a inserção no banco."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(
        """INSERT INTO search_history (slug, lat_tl, lon_tl, lat_br, lon_br) 
           VALUES (?, ?, ?, ?, ?)""",
        (slug, lat_tl, lon_tl, lat_br, lon_br)
    )
    
    conn.commit()
    conn.close()

### read
def find_search_by_term(term: str) -> list:
    """Busca no banco todas as slugs que contêm o termo digitado."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT slug FROM search_history WHERE slug LIKE ?",
        (f"%{term}%",)
    )
    
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return results