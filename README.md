## Algoritmos e Estruturas de Dados II - Trabalho Prático (Parte III)

Este repositório contém a implementação do Trabalho Prático - Parte III da disciplina de Algoritmos e Estruturas de Dados II. O projeto consiste no gerenciamento de arquivos binários utilizando uma Tabela Hash com Encadeamento Exterior e um mecanismo para reutilização de espaços vazios em registros de tamanho fixo.

## Funcionalidades

- **Tabela Hash com Encadeamento Exterior:** Mapeamento de registros da entidade Pokemon via função hash modular (h(x) = x mod M, com M = 7). As colisões são tratadas por meio de listas encadeadas diretamente no arquivo de dados através do ponteiro prox.

- **Operações Básicas:**
  - **Busca:** Localização de registros em tempo eficiente navegando pela lista de colisões.
  - **Inserção:** Inserção de novos registros com verificação de duplicidade e atualização da lista encadeada da hash.
  - **Remoção:** Desvinculação do registro da lista de colisões e marcação de status como LIBERADO.

- **Gerenciamento de Espaço Livre:** Implementação de uma pilha de registros excluídos. Quando um registro é removido, seu RRN (Relative Record Number) é empilhado no topo da pilha de excluídos. Inserções subsequentes reaproveitam prioritariamente esses espaços vagos antes de expandir o arquivo.
- **Persistência de Metadados:** Armazenamento contínuo dos ponteiros da tabela hash (tabHash.dat), dos registros (pokemons.dat) e do topo da pilha de descartes (config.dat).
- **Interface via Terminal:** Menu interativo para inserção individual, criação automatizada de bases de teste com 1000 registros, buscas, remoções e visualização estruturada dos arquivos.

## Estrutura do Código
- entidades.py: Definição das estruturas Pokemon e CompartimentoHash formatadas via struct para serialização binária.
- gerenciador_arquivos.py: Funções auxiliares de I/O em baixo nível (leitura/escrita por RRN com f.seek e manipulação do arquivo de metadados).
- hash.py: Módulo principal com a implementação da tabela hash, tratamento de colisões, operações CRUD e gerenciador de espaço via pilha de excluídos.
- main.py: Interface de linha de comando com o menu interativo para simulação e gerenciamento do banco de dados.
