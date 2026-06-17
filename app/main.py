import Model.databaseModel as db

def run_tests():
    print("🔧 Iniciando testes com a nova estrutura de 4 pontos...\n")
    
    # 1. Configura o banco zerado
    print("-> Configurando o banco de dados (search_history.db)...")
    db.setup_db()
    
    # 2. Inserindo dados simulando o cálculo de Bounding Box dos guris
    print("-> Salvando pesquisas de teste com quinas TL e BR...")
    # Teste 1: Uma área hipotética
    db.save_search(
        slug="08/11/2002 12h 00m 00s", 
        lat_tl=-28.9333, lon_tl=-49.4833, 
        lat_br=-28.9400, lon_br=-49.4700
    )
    # Teste 2: Outra área no mesmo dia
    db.save_search(
        slug="08/11/2002 23h 59m 59s", 
        lat_tl=-28.9500, lon_tl=-49.5000, 
        lat_br=-28.9600, lon_br=-49.4900
    )
    
    # 3. Testando a busca por termo
    termo_pesquisa = "08/11/2002"
    print(f"-> Buscando pelo termo: '{termo_pesquisa}'...\n")
    
    resultados = db.find_search_by_term(termo_pesquisa)
    
    # 4. Exibindo os resultados
    print("✅ Resultados encontrados no banco:")
    if resultados:
        for res in resultados:
            print(f"  - {res}")
    else:
        print("  Nenhum resultado encontrado.")
        
    print("\n🚀 Primeira missão concluída com sucesso!")

if __name__ == "__main__":
    run_tests()