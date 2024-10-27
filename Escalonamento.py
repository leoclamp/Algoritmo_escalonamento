import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor

# Função que divide o arquivo em partes de tamanhos variáveis
def generate_variable_partes(file_size, num_partes):
    proportions = [random.randint(1, 10) for _ in range(num_partes)]
    total_proportion = sum(proportions)
    partes_sizes = [(file_size * prop) // total_proportion for prop in proportions]
    partes_sizes[-1] = file_size - sum(partes_sizes[:-1])
    return partes_sizes

# Função para download de uma única parte do arquivo
def download_part(url, start, end, part_num):
    headers = {'Range': f'bytes={start}-{end}'}
    start_time = time.time()
    response = requests.get(url, headers=headers)
    time_taken = time.time() - start_time
    
    if response.status_code in [200, 206]:  # 200 OK ou 206 Partial Content
        print(f"Parte {part_num} baixada com {len(response.content)} bytes em {time_taken:.2f} segundos.")
        return response.content, time_taken
    else:
        print(f"Erro ao baixar parte {part_num}: {response.status_code}")
        return None, time_taken

# Função que baixa um arquivo em partes de tamanhos variáveis usando FCFS
def download_file_fcfs(url, partes_info):
    print(f"\nBaixando {url} em partes com tamanhos variáveis usando FCFS...")

    full_content = bytearray()
    wait_times = []
    total_time = 0

    with ThreadPoolExecutor(max_workers=1) as executor:
        for i, (start, end) in enumerate(partes_info):
            wait_time = round(total_time, 2)
            wait_times.append(wait_time)
            
            future = executor.submit(download_part, url, start, end, i + 1)
            content, time_taken = future.result()
            
            if content:
                full_content.extend(content)
                total_time += time_taken

            print(f"Tempo de espera para a parte {i + 1}: {wait_time:.2f} segundos.")

    print(f"\nDownload FCFS completo: {len(full_content)} bytes baixados.")
    return wait_times

# Função que baixa um arquivo em partes usando SJF com tamanhos variáveis
def download_file_sjf(url, partes_info):
    print(f"\nBaixando {url} em partes com tamanhos variáveis usando SJF...")

    # Ordenar as partes pelo tamanho antes do download
    partes_info_sorted = sorted(partes_info, key=lambda x: x[1] - x[0])  # Ordenar pelo tamanho (end - start)

    full_content = bytearray()
    wait_times = []
    total_time = 0

    with ThreadPoolExecutor(max_workers=1) as executor:
        for i, (start, end) in enumerate(partes_info_sorted):
            wait_time = round(total_time, 2)
            wait_times.append(wait_time)
            
            future = executor.submit(download_part, url, start, end, i + 1)
            content, time_taken = future.result()
            
            if content:
                full_content.extend(content)
                total_time += time_taken

            print(f"Tempo de espera para a parte {i + 1}: {wait_time:.2f} segundos.")

    print(f"\nDownload SJF completo: {len(full_content)} bytes baixados.")
    return wait_times

# Função principal
def main():
    url = "http://example.com"
    num_partes = 4

    # Primeira requisição para obter o tamanho do arquivo
    response = requests.head(url)
    file_size = int(response.headers.get('Content-Length', 0))

    # Geração das partes uma vez, para que possam ser usadas por ambas as funções
    partes_sizes = generate_variable_partes(file_size, num_partes)
    partes_info = []
    start = 0
    for parte_size in partes_sizes:
        end = start + parte_size - 1
        partes_info.append((start, end))
        start = end + 1

    # Executar o download usando FCFS
    fcfs_wait_times = download_file_fcfs(url, partes_info)
    fcfs_avg_wait_time = sum(fcfs_wait_times) / len(fcfs_wait_times) if fcfs_wait_times else 0
    print(f"\nTempo médio de espera (FCFS): {fcfs_avg_wait_time:.2f} segundos.")

    # Executar o download usando SJF
    sjf_wait_times = download_file_sjf(url, partes_info)
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

if __name__ == "__main__":
    main()
