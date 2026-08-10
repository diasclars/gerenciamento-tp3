import os
import struct
from entidades import Pokemon, CompartimentoHash

NOME_ARQUIVO_CONFIG = "config.dat"

# grava um pokémon em um rrn
def salva_pokemon_em(pokemon, rrn, f_out):
    f_out.seek(rrn * Pokemon.TAMANHO_REGISTRO)
    f_out.write(pokemon.to_bytes())

# le o pokemon na rrn e grava na memória ram
def le_pokemon_em(rrn, f_in):
    f_in.seek(rrn * Pokemon.TAMANHO_REGISTRO)
    dados = f_in.read(Pokemon.TAMANHO_REGISTRO)
    return Pokemon.from_bytes(dados)

# atualiza na tabela hash em disco usando o rrn correspondente
def salva_compartimento_em(compartimento, rrn, f_out):
    f_out.seek(rrn * CompartimentoHash.TAMANHO_REGISTRO)
    f_out.write(compartimento.to_bytes())

# lê o ponteiro na tabela hash em disco e o traz para a memória ram como um objeto de controle
def le_compartimento_em(rrn, f_in):
    f_in.seek(rrn * CompartimentoHash.TAMANHO_REGISTRO)
    dados = f_in.read(CompartimentoHash.TAMANHO_REGISTRO)
    return CompartimentoHash.from_bytes(dados)

# salva o rrn que está no topo da pilha de excluídos
def salvar_topo_pilha(topo):
    with open(NOME_ARQUIVO_CONFIG, "wb") as f:
        f.write(struct.pack("i", topo))

# lê o rrn que está no topo da pilha de excluídos. retorna -1 se não existir.
def ler_topo_pilha():
    if not os.path.exists(NOME_ARQUIVO_CONFIG):
        return -1
    with open(NOME_ARQUIVO_CONFIG, "rb") as f:
        dados = f.read(4)
        if len(dados) < 4:
            return -1
        topo, = struct.unpack("i", dados)
        return topo