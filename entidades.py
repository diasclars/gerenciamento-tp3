import struct

LIBERADO = 0
OCUPADO = 1
TAM_NOME = 24  

class Pokemon:
    # formato struct: i (id), 24s (nome), i (poder), i (prox), i (ocupado)
    FORMATO = f"i{TAM_NOME}siii"
    TAMANHO_REGISTRO = struct.calcsize(FORMATO)

    # recebe os dados do pokémon e guarda de forma organizada
    def __init__(self, id, nome, poder, prox=-1, ocupado=OCUPADO):
        self.id = id
        self.nome = nome
        self.poder = poder
        # hash = aponta para o próximo da colisão. pilha de excluídos = aponta para o próximo RRN vago
        self.prox = prox 
        self.ocupado = ocupado 

    # tranforma em bytes
    def to_bytes(self):
        nome_bytes = self.nome.encode('utf-8')[:TAM_NOME].ljust(TAM_NOME, b'\x00')
        return struct.pack(self.FORMATO, self.id, nome_bytes, self.poder, self.prox, self.ocupado)
    
    # processo inverso
    @classmethod
    def from_bytes(cls, dados_bytes):
        if not dados_bytes or len(dados_bytes) < cls.TAMANHO_REGISTRO:
            return None
        id, nome_bytes, poder, prox, ocupado = struct.unpack(cls.FORMATO, dados_bytes)
        nome = nome_bytes.decode('utf-8').strip('\x00')
        return cls(id, nome, poder, prox, ocupado)
    
    # como o pokemon vai ser exibido no terminal
    def __repr__(self):
        status = "OCUPADO" if self.ocupado == OCUPADO else "LIBERADO"
        return f"Pokemon(ID: {self.id}, Nome: {self.nome}, Poder: {self.poder}, Prox RRN: {self.prox}, Status: {status})"


class CompartimentoHash:
    FORMATO = "i"
    TAMANHO_REGISTRO = struct.calcsize(FORMATO)

    # o ponteiro prox começa com -1
    def __init__(self, prox=-1):
        self.prox = prox  

    # pega o número inteiro self.prox armazenado na memória RAM e o empacota em 4 bytes
    def to_bytes(self):
        return struct.pack(self.FORMATO, self.prox)
    
    # caminho inverso. lê 4 bytes brutos do arquivo tabHash.dat, desempacota-os e descobre
    # qual é o número inteiro gravado ali (rrn)
    @classmethod
    def from_bytes(cls, dados_bytes):
        if not dados_bytes or len(dados_bytes) < cls.TAMANHO_REGISTRO:
            return None
        prox, = struct.unpack(cls.FORMATO, dados_bytes)
        return cls(prox)
    
    # exibição na tela
    def __repr__(self):
        return f"Prox RRN: {self.prox}"