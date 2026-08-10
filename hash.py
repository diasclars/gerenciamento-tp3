import os
import random
from entidades import Pokemon, CompartimentoHash, LIBERADO, OCUPADO
from gerenciador_arquivos import (
    le_compartimento_em, salva_compartimento_em,
    le_pokemon_em, salva_pokemon_em,
    salvar_topo_pilha, ler_topo_pilha, NOME_ARQUIVO_CONFIG
)

NOME_ARQUIVO_HASH = "tabHash.dat"
NOME_ARQUIVO_DADOS = "pokemons.dat"
M = 7  # tamanho da tabela hash

# função hash: h(x) = x mod M
def hash_func(id_pokemon):
    return id_pokemon % M

# inicializa arquivos zerados
def inicializa_arquivos(forcar=False):
    if forcar or not os.path.exists(NOME_ARQUIVO_HASH):
        tab_hash = [CompartimentoHash(-1) for _ in range(M)]
        with open(NOME_ARQUIVO_HASH, "wb") as f:
            for c in tab_hash:
                f.write(c.to_bytes())
    if forcar or not os.path.exists(NOME_ARQUIVO_DADOS):
        open(NOME_ARQUIVO_DADOS, "wb").close()
    if forcar or not os.path.exists(NOME_ARQUIVO_CONFIG):
        salvar_topo_pilha(-1)  # inicializa a pilha de excluídos vazia (-1)

# busca da tabela hash com encadeamento exterior
def buscar_pokemon(id_pokemon):
    if not os.path.exists(NOME_ARQUIVO_HASH) or not os.path.exists(NOME_ARQUIVO_DADOS):
        return None, -1

    # recebe o resto de h(x) - qual compartimento está
    pos_hash = hash_func(id_pokemon)

    # abre os arquivos e descobre por qual linha (RRN) do arquivo de dados a busca deve começar
    with open(NOME_ARQUIVO_HASH, "rb") as f_hash, open(NOME_ARQUIVO_DADOS, "rb") as f_dados:
        # pega a posição calculada h(X) e lê o compartimento correspondente no arquivo
        comp = le_compartimento_em(pos_hash, f_hash)
        rrn_atual = comp.prox

        while rrn_atual != -1:
            poke = le_pokemon_em(rrn_atual, f_dados)
            if poke is None:
                break
            # se achou o id e o registro está de fato OCUPADO
            if poke.id == id_pokemon and poke.ocupado == OCUPADO:
                return poke, rrn_atual
            rrn_atual = poke.prox

    return None, -1

def obter_posicao_insercao():
    # usa a pilha de registros excluídos. retorna(rrn_destino, reutilizou_espaco).
    topo = ler_topo_pilha()
    
    if topo != -1:
        rrn_destino = topo
        
        # lê o registro excluído para descobrir para onde aponta o próximo da pilha
        with open(NOME_ARQUIVO_DADOS, "rb") as f:
            registro_vazio = le_pokemon_em(rrn_destino, f)
            
        # o novo topo da pilha
        novo_topo = registro_vazio.prox
        salvar_topo_pilha(novo_topo)
        
        return rrn_destino, True
    else:
        # se a pilha está vazia insere no fim do arquivo
        if not os.path.exists(NOME_ARQUIVO_DADOS):
            return 0, False
        tamanho_arquivo = os.path.getsize(NOME_ARQUIVO_DADOS)
        rrn_destino = tamanho_arquivo // Pokemon.TAMANHO_REGISTRO
        return rrn_destino, False

def inserir_pokemon(id_pokemon, nome, poder, silencioso=False):
    inicializa_arquivos()

    poke_existente, _ = buscar_pokemon(id_pokemon)
    if poke_existente:
        if not silencioso:
            print(f"Erro: Pokemon com ID {id_pokemon} já existe.")
        return False

    pos_hash = hash_func(id_pokemon)

    with open(NOME_ARQUIVO_HASH, "r+b") as f_hash, open(NOME_ARQUIVO_DADOS, "r+b") as f_dados:
        # recupera espaço em O(1) usando o topo da pilha de removidos
        rrn_destino, reutilizou = obter_posicao_insercao()

        comp = le_compartimento_em(pos_hash, f_hash)
        rrn_antigo_topo_hash = comp.prox

        # salva o novo pokémon. seu ponteiro vai apontar para o antigo topo da lista de colisões
        novo_poke = Pokemon(id=id_pokemon, nome=nome, poder=poder, prox=rrn_antigo_topo_hash, ocupado=OCUPADO)
        salva_pokemon_em(novo_poke, rrn_destino, f_dados)

        # atualiza a tabela hash
        comp.prox = rrn_destino
        salva_compartimento_em(comp, pos_hash, f_hash)

    if not silencioso:
        status_reuso = "reutilizando espaço vago" if reutilizou else " "
        print(f"Pokemon '{nome}' inserido com sucesso no RRN {rrn_destino} {status_reuso}")
    return True

# remove o pokémon da lista de colisões da tabela hash e insere na pilha de excluídos
def remover_pokemon(id_pokemon):
    if not os.path.exists(NOME_ARQUIVO_HASH) or not os.path.exists(NOME_ARQUIVO_DADOS):
        print("Erro: Arquivos não inicializados.")
        return False

    pos_hash = hash_func(id_pokemon)

    with open(NOME_ARQUIVO_HASH, "r+b") as f_hash, open(NOME_ARQUIVO_DADOS, "r+b") as f_dados:
        comp = le_compartimento_em(pos_hash, f_hash)
        rrn_atual = comp.prox
        rrn_anterior = -1

        while rrn_atual != -1:
            poke_atual = le_pokemon_em(rrn_atual, f_dados)
            if poke_atual is None:
                break

            if poke_atual.id == id_pokemon and poke_atual.ocupado == OCUPADO:
                proximo_colisao = poke_atual.prox 
                
                if rrn_anterior == -1:
                    comp.prox = proximo_colisao
                    salva_compartimento_em(comp, pos_hash, f_hash)
                else:
                    poke_anterior = le_pokemon_em(rrn_anterior, f_dados)
                    poke_anterior.prox = proximo_colisao
                    salva_pokemon_em(poke_anterior, rrn_anterior, f_dados)

                topo_atual_pilha = ler_topo_pilha()
                
                poke_atual.ocupado = LIBERADO
                poke_atual.prox = topo_atual_pilha  
                
                salva_pokemon_em(poke_atual, rrn_atual, f_dados)
                salvar_topo_pilha(rrn_atual)  

                print(f"Pokemon ID {id_pokemon} removido. RRN {rrn_atual} adicionado à pilha de excluídos!")
                return True

            rrn_anterior = rrn_atual
            rrn_atual = poke_atual.prox

    print(f"Erro: Pokemon com ID {id_pokemon} não encontrado.")
    return False

def popular_base_1000_pokemons():
    inicializa_arquivos(forcar=True)  # começa tabela vazia
    print("Gerando base de 1000 Pokémon...")
    
    nomes_base = ["Pikachu", "Charizard", "Bulbasaur", "Squirtle", "Mewtwo", "Eevee", "Snorlax", "Gengar", "Lucario", "Dragonite"]
    
    sucessos = 0

    for id_gerado in range(1, 1001):
        nome_gerado = random.choice(nomes_base)
        poder_gerado = random.randint(50, 1000)
        if inserir_pokemon(id_gerado, nome=nome_gerado, poder=poder_gerado, silencioso=True):
            sucessos += 1
                
    print(f"\nBase de dados criada com sucesso!")

# imprime o estado atual dos metadados e da tabela hash base
def imprimir_tudo():
    inicializa_arquivos()
    print(f"Topo da pilha de excluídos (RRN): {ler_topo_pilha()}")
    
    print("\n" + "TABELA HASH")
    with open(NOME_ARQUIVO_HASH, "rb") as f:
        for rrn in range(M):
            c = le_compartimento_em(rrn, f)
            print(f"Compartimento [{rrn}]: {c}")

    print("\n" + "ARQUIVO DE DADOS")
    if os.path.exists(NOME_ARQUIVO_DADOS):
        tamanho_arquivo = os.path.getsize(NOME_ARQUIVO_DADOS)
        total_registros = tamanho_arquivo // Pokemon.TAMANHO_REGISTRO
        with open(NOME_ARQUIVO_DADOS, "rb") as f:
            if total_registros <= 20:
                for rrn in range(total_registros):
                    poke = le_pokemon_em(rrn, f)
                    print(f"RRN [{rrn}]: {poke}")
            else:
                print(f"Exibindo os 10 primeiros de {total_registros} registros:")
                for rrn in range(10):
                    poke = le_pokemon_em(rrn, f)
                    print(f"RRN [{rrn}]: {poke}")
                
                print("Exibindo os 10 últimos registros:")
                for rrn in range(total_registros - 10, total_registros):
                    poke = le_pokemon_em(rrn, f)
                    print(f"RRN [{rrn}]: {poke}")
    