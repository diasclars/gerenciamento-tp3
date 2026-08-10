from hash import (
    inicializa_arquivos, inserir_pokemon, buscar_pokemon, 
    remover_pokemon, popular_base_1000_pokemons, imprimir_tudo
)

def menu():
    inicializa_arquivos()
    while True:
        print("Menu - Escolha")
        print("1. Inserir UM Pokemon")
        print("2. Inserir Banco de Dados (1000 Pokemons)")
        print("3. Buscar Pokemon")
        print("4. Remover Pokemon")
        print("5. Visualizar Estrutura dos Arquivos")
        print("6. Reinicializar Banco de Dados")
        print("0. Sair")
        
        opcao = input("Escolha uma opcao: ")
        
        if opcao == "1":
            try:
                id_poke = int(input("Digite o ID (inteiro): "))
                nome = input("Digite o nome do Pokemon: ")
                poder = int(input("Digite o poder de combate: "))
                inserir_pokemon(id_poke, nome, poder)
            except ValueError:
                print("Digite valores validos.")
                
        elif opcao == "2":
            confirmacao = input("Isso apagará o banco atual e gerará 1000 Pokémons. Deseja prosseguir? (s/n): ")
            if confirmacao.lower() == 's':
                popular_base_1000_pokemons()
                
        elif opcao == "3":
            try:
                id_poke = int(input("Digite o ID que deseja buscar: "))
                poke, rrn = buscar_pokemon(id_poke)
                if poke:
                    print(f"\nSucesso! Pokemon encontrado no RRN {rrn}:")
                    print(poke)
                else:
                    print("\nPokemon nao encontrado.")
            except ValueError:
                print("ID invalido.")
                
        elif opcao == "4":
            try:
                id_poke = int(input("Digite o ID que deseja remover: "))
                remover_pokemon(id_poke)
            except ValueError:
                print("ID invalido.")
                
        elif opcao == "5":
            imprimir_tudo()
            
        elif opcao == "6":
            confirmacao = input("Deseja apagar todos os dados e começar com tabela vazia? (s/n): ")
            if confirmacao.lower() == 's':
                inicializa_arquivos(forcar=True)
                print("Arquivos resetados. Banco de dados vazio!")
                
        elif opcao == "0":
            print("Saindo do programa.")
            break
        else:
            print("Opcao invalida.")
        print("-" * 50)

if __name__ == "__main__":
    menu()