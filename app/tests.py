import Model.databaseModel as db
import sqlite3

def run_tests():
    print("🔧 Iniciando testes de Relacionamento (1:1)...\n")
    
    # 1. Configura o banco zerado
    print("-> Configurando o banco de dados (search_history.db)...")
    db.setup_db()
    
    # 2. Criando a pesquisa e capturando o ID
    print("-> Salvando pesquisa e capturando o ID gerado...")
    meu_id_gerado = db.save_search(
        slug="17/06/2026 22h 44m", 
        lat_tl=-28.9333, lon_tl=-49.4833, 
        lat_br=-28.9400, lon_br=-49.4700
    )
    print(f"✅ Pesquisa salva com sucesso! ID gerado na main: {meu_id_gerado}")
    
    # 3. Inserindo os resultados populacionais vinculados a esse ID
    print(f"-> Salvando os resultados da IA vinculados ao ID {meu_id_gerado}...")
    db.save_result(
        search_id=meu_id_gerado,
        population=15420,
        population_density=125.5
    )
    print("✅ Resultados salvos na nova tabela com sucesso!")
    
    # 4. Prova real (buscando direto no banco com JOIN para confirmar)
    print("\n-> 🕵️‍♂️ PROVA REAL: Cruzando as tabelas no banco de dados...")
    conn = sqlite3.connect(db.DB_NAME)
    cursor = conn.cursor()
    
    # Fazendo um JOIN simples para ver as duas tabelas juntas
    cursor.execute('''
        SELECT h.slug, r.population, r.population_density
        FROM search_history h
        JOIN search_results r ON h.id = r.id
        WHERE h.id = ?
    ''', (meu_id_gerado,))
    
    resultado_join = cursor.fetchone()
    conn.close()
    
    if resultado_join:
        print("🎉 Sucesso Absoluto! Dados amarrados encontrados:")
        print(f"   Slug da Pesquisa: {resultado_join[0]}")
        print(f"   População Estimada: {resultado_join[1]} habitantes")
        print(f"   Densidade: {resultado_join[2]} hab/km²")
    else:
        print("❌ Ops, algo deu errado. Dados não encontrados.")
        
    print("\n🚀 Todos os testes passaram!")

if __name__ == "__main__":
    run_tests()