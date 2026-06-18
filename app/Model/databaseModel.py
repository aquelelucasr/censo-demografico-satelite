import sqlite3

DB_NAME = "search_history.db"

def setup_db():
    """Cria as tabelas de histórico e resultados se elas ainda não existirem."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # tabela de historico de pesquisas
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
    
    # tabela com os dados de cada pesquisa, 1:1 com search_history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_results (
            id INTEGER PRIMARY KEY,
            population INTEGER NOT NULL,
            population_density REAL NOT NULL,
            FOREIGN KEY (id) REFERENCES search_history (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close() 

### create da search_history
def save_search(slug: str, lat_tl: float, lon_tl: float, lat_br: float, lon_br: float) -> int:
    """Recebe o slug e os 4 pontos, faz a inserção e RETORNA o ID gerado."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(
        """INSERT INTO search_history (slug, lat_tl, lon_tl, lat_br, lon_br) 
           VALUES (?, ?, ?, ?, ?)""",
        (slug, lat_tl, lon_tl, lat_br, lon_br)
    )
    
    # Captura o ID que o SQLite acabou de criar automaticamente
    inserted_id = cursor.lastrowid 
    
    conn.commit()
    conn.close()
    
    return inserted_id

### create da search_results
def save_result(search_id: int, population: int, population_density: float) -> None:
    """Salva os resultados vinculados ao ID da pesquisa original."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Ativa as chaves estrangeiras para garantir a integridade da relação 1:1
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    cursor.execute(
        """INSERT INTO search_results (id, population, population_density) 
           VALUES (?, ?, ?)""",
        (search_id, population, population_density)
    )
    
    conn.commit()
    conn.close()

### reads da search_history
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

def get_all_history() -> list:
    """Busca todo o histórico de pesquisas salvo no banco de dados."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Selecionamos as colunas essenciais para mostrar na tela
    cursor.execute(
        "SELECT slug, lat_tl, lon_tl, lat_br, lon_br FROM search_history"
    )
    
    # fetchall() vai retornar uma lista de tuplas: [('slug1', -28.9, ...), ('slug2', ...)]
    results = cursor.fetchall()
    conn.close()
    
    return results