# Download de Arquivos em Partes com Algoritmos de Escalonamento, Controle de Acesso e Semáforos

## Descrição
O arquivo `Escalonamento.py` realiza downloads em partes de tamanhos variáveis, utilizando dois algoritmos diferentes de gerenciamento de filas: FCFS (First-Come, First-Served) e SJF (Shortest Job First). O `Monitor.py` é utilizado para controlar o acesso ao recurso compartilhado durante o download. O `Semaforo_binario` utiliza um semáforo binário para controlar o acesso ao recurso durante o download de um arquivo. O `Semaforo_contagem` implementa um downloader de arquivos que utiliza um semáforo de contagem para gerenciar o acesso concorrente. O semáforo permite que um número limitado de threads (neste caso, duas) acesse o recurso simultaneamente.

O arquivo `Escalonamento.py` realiza downloads de arquivos em partes de tamanhos variáveis, empregando dois algoritmos distintos de gerenciamento de filas: FCFS (First-Come, First-Served) e SJF (Shortest Job First). O arquivo `Monitor.py` é utilizado para controlar o acesso ao recurso compartilhado durante o processo de download. O módulo `Semaforo_binario.py` implementa um semáforo binário que regula o acesso ao recurso durante o download. Por sua vez, o `Semaforo_contagem.py` implementa um semáforo de contagem para gerenciar o acesso concorrente, permitindo que um número limitado de threads (neste caso, duas) acesse o recurso simultaneamente.

## Funcionalidades

- Arquivo `Escalonamento.py`:
    - `generate_variable_partes`: Gera tamanhos de partes variáveis para o download.
    - `download_part`: Realiza o download de uma única parte do arquivo.
    - `download_file_fcfs`: Faz o download usando o algoritmo FCFS.
    - `download_file_sjf`: Faz o download usando o algoritmo SJF.
    - `main()`: Função principal que controla o fluxo do programa, gerando as partes e chamando as funções de download.

- Arquivo `Monitor.py`:
    - `Classe Monitor`: Implementa um monitor para controlar o acesso ao recurso compartilhado durante o download.
    - `download_with_monitor`: Utilizam um monitor para controlar o acesso ao recurso durante os downloads.

- Arquivo `Semaforo_binario.py`:
    - `download_with_binary_semaphore`: Utilizam um semáforos para controlar o acesso ao recurso durante os downloads.

- Arquivo `Semaforo_contagem.py`:
    - `download_with_counting_semaphore`: Usa um semáforo de contagem para permitir um número limitado de acessos simultâneos.

## Requisitos

- Python 3.x
- Bibliotecas:
  - `requests`
  - `concurrent.futures` (incluída na biblioteca padrão do Python)
  
Para instalar a biblioteca `requests`, você pode usar o seguinte comando:

```
pip install requests
```

