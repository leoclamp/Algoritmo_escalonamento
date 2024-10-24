import requests
import time
import random

# Função que divide o arquivo em partes de tamanhos variáveis
def generate_variable_partes(file_size, num_partes):
    # Gerar divisões proporcionais aleatórias
    proportions = [random.randint(1, 10) for _ in range(num_partes)]
    total_proportion = sum(proportions)
    
    # Calcular tamanhos com base nas proporções
    partes_sizes = [(file_size * prop) // total_proportion for prop in proportions]
    
    # Ajustar a última parte para garantir que o total seja igual ao file_size
    partes_sizes[-1] = file_size - sum(partes_sizes[:-1])
    
    return partes_sizes

# Função que baixa um arquivo em partes usando FCFS com tamanhos variáveis
def download_file_fcfs(url, num_partes):
    print(f"\nBaixando {url} em {num_partes} partes com tamanhos variáveis usando FCFS...")

    # Primeira requisição para obter o tamanho do arquivo
    response = requests.head(url)
    file_size = int(response.headers.get('Content-Length', 0))

    # Gerar partes de tamanhos variáveis
    partes_sizes = generate_variable_partes(file_size, num_partes)

    # Armazenar o conteúdo completo
    full_content = bytearray()
    
    # Armazenar tempos de espera
    wait_times = []

    total_time = 0
    start = 0
    for i in range(num_partes):
        chunk_size = partes_sizes[i]
        end = start + chunk_size - 1
        
        headers = {'Range': f'bytes={start}-{end}'}
        
        print(f"Baixando parte {i + 1} de {num_partes} (tamanho: {chunk_size} bytes)...")
        start_time = time.time()
        chunk_response = requests.get(url, headers=headers)

        if chunk_response.status_code in [200, 206]:  # 200 OK ou 206 Partial Content
            full_content.extend(chunk_response.content)
            time_taken = time.time() - start_time
            total_time += time_taken
            
            wait_time = total_time - time_taken  # Tempo total menos o tempo da parte atual
            wait_times.append(wait_time)
            print(f"Parte {i + 1} de {num_partes} baixada com {len(chunk_response.content)} bytes em {time_taken:.2f} segundos.")
            print(f"Tempo de espera para a parte {i + 1}: {wait_time:.2f} segundos.")
        else:
            print(f"Erro ao baixar parte {i + 1}: {chunk_response.status_code}")
            break

        start = end + 1  # Atualizar o início da próxima parte

    print(f"\nDownload FCFS completo: {len(full_content)} bytes baixados.")
    return wait_times

# Função que baixa um arquivo em partes usando SJF com tamanhos variáveis
def download_file_sjf(url, num_partes):
    print(f"\nBaixando {url} em {num_partes} partes com tamanhos variáveis usando SJF...")

    # Primeira requisição para obter o tamanho do arquivo
    response = requests.head(url)
    file_size = int(response.headers.get('Content-Length', 0))

    # Gerar partes de tamanhos variáveis
    partes_sizes = generate_variable_partes(file_size, num_partes)

    # Armazenar o conteúdo completo
    full_content = bytearray()
    
    # Lista para armazenar informações sobre cada parte
    partes_info = []

    start = 0
    for i in range(num_partes):
        chunk_size = partes_sizes[i]
        end = start + chunk_size - 1
        partes_info.append((i, start, end, chunk_size))
        start = end + 1

    # Ordenando as partes pelo tamanho para simular SJF
    partes_info.sort(key=lambda x: x[3])  # Ordenar pelo tamanho do chunk

    # Armazenar tempos de espera
    wait_times = []

    total_time = 0
    for i, (index, start, end, chunk_size) in enumerate(partes_info):
        headers = {'Range': f'bytes={start}-{end}'}
        
        print(f"Baixando parte {index + 1} de {num_partes} (tamanho: {chunk_size} bytes)...")
        start_time = time.time()
        chunk_response = requests.get(url, headers=headers)

        if chunk_response.status_code in [200, 206]:
            full_content.extend(chunk_response.content)
            time_taken = time.time() - start_time
            total_time += time_taken
            
            wait_time = total_time - time_taken
            wait_times.append(wait_time)
            print(f"Parte {index + 1} de {num_partes} baixada com {len(chunk_response.content)} bytes em {time_taken:.2f} segundos.")
            print(f"Tempo de espera para a parte {index + 1}: {wait_time:.2f} segundos.")
        else:
            print(f"Erro ao baixar parte {index + 1}: {chunk_response.status_code}")
            break

    print(f"\nDownload SJF completo: {len(full_content)} bytes baixados.")
    return wait_times

# Função principal
def main():
    # URL para download
    url = "http://example.com"

    # Número de partes para dividir o download
    num_partes = 4

    # Executar o download usando FCFS
    fcfs_wait_times = download_file_fcfs(url, num_partes)
    fcfs_avg_wait_time = sum(fcfs_wait_times) / len(fcfs_wait_times) if fcfs_wait_times else 0
    print(f"\nTempo médio de espera (FCFS): {fcfs_avg_wait_time:.2f} segundos.")

    # Executar o download usando SJF
    sjf_wait_times = download_file_sjf(url, num_partes)
    sjf_avg_wait_time = sum(sjf_wait_times) / len(sjf_wait_times) if sjf_wait_times else 0
    print(f"\nTempo médio de espera (SJF): {sjf_avg_wait_time:.2f} segundos.")

    # Comparar os tempos médios de espera
    print("\nComparação dos tempos médios de espera:")
    print(f"FCFS: {fcfs_avg_wait_time:.2f} segundos")
    print(f"SJF: {sjf_avg_wait_time:.2f} segundos")
    if fcfs_avg_wait_time < sjf_avg_wait_time:
        print("\nFCFS teve um tempo médio de espera menor.\n")
    elif sjf_avg_wait_time < fcfs_avg_wait_time:
        print("\nSJF teve um tempo médio de espera menor.\n")
    else:
        print("\nOs tempos médios de espera foram iguais.\n")

# Executar a função principal
if __name__ == "__main__":
    main()
