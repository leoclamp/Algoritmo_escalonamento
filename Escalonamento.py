import requests
import time

# Função que baixa um arquivo em partes usando FCFS
def download_file_fcfs(url, num_chunks):
    print(f"\nBaixando {url} em {num_chunks} partes usando FCFS...")

    # Primeira requisição para obter o tamanho do arquivo
    response = requests.head(url)
    file_size = int(response.headers.get('Content-Length', 0))
    chunk_size = file_size // num_chunks  # Tamanho de cada parte

    # Armazenar o conteúdo completo
    full_content = bytearray()
    
    # Armazenar tempos de espera
    wait_times = []

    total_time = 0
    for i in range(num_chunks):
        start = i * chunk_size
        end = start + chunk_size - 1 if i < num_chunks - 1 else file_size - 1
        
        headers = {'Range': f'bytes={start}-{end}'}
        
        print(f"Baixando parte {i + 1} de {num_chunks}...")
        start_time = time.time()
        chunk_response = requests.get(url, headers=headers)

        if chunk_response.status_code in [200, 206]:  # 200 OK ou 206 Partial Content
            full_content.extend(chunk_response.content)
            time_taken = time.time() - start_time
            total_time += time_taken
            
            wait_time = total_time - time_taken  # Tempo total menos o tempo da parte atual
            wait_times.append(wait_time)
            print(f"Parte {i + 1} de {num_chunks} baixada com {len(chunk_response.content)} bytes em {time_taken:.2f} segundos.")
            print(f"Tempo de espera para a parte {i + 1}: {wait_time:.2f} segundos.")
        else:
            print(f"Erro ao baixar parte {i + 1}: {chunk_response.status_code}")
            break

    print(f"\nDownload FCFS completo: {len(full_content)} bytes baixados.")
    return wait_times

# Função que baixa um arquivo em partes usando SJF
def download_file_sjf(url, num_chunks):
    print(f"\nBaixando {url} em {num_chunks} partes usando SJF...")

    # Primeira requisição para obter o tamanho do arquivo
    response = requests.head(url)
    file_size = int(response.headers.get('Content-Length', 0))
    chunk_size = file_size // num_chunks  # Tamanho de cada parte

    # Armazenar o conteúdo completo
    full_content = bytearray()
    
    # Lista para armazenar informações sobre cada parte
    chunks_info = []

    # Calculando o tamanho de cada parte
    for i in range(num_chunks):
        start = i * chunk_size
        end = start + chunk_size - 1 if i < num_chunks - 1 else file_size - 1
        size = end - start + 1  # Tamanho do pacote
        chunks_info.append((i, start, end, size))

    # Ordenando pacotes pelo tamanho (SJF)
    chunks_info.sort(key=lambda x: x[3])  # Ordenar pelo tamanho do pacote

    # Armazenar tempos de espera
    wait_times = []

    total_time = 0
    for i, (index, start, end, size) in enumerate(chunks_info):
        headers = {'Range': f'bytes={start}-{end}'}
        
        print(f"Baixando parte {index + 1} de {num_chunks} (tamanho: {size} bytes)...")
        start_time = time.time()
        chunk_response = requests.get(url, headers=headers)

        if chunk_response.status_code in [200, 206]:
            full_content.extend(chunk_response.content)
            time_taken = time.time() - start_time
            total_time += time_taken
            
            wait_time = total_time - time_taken
            wait_times.append(wait_time)
            print(f"Parte {index + 1} de {num_chunks} baixada com {len(chunk_response.content)} bytes em {time_taken:.2f} segundos.")
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
    num_chunks = 4

    # Executar o download usando FCFS
    fcfs_wait_times = download_file_fcfs(url, num_chunks)
    fcfs_avg_wait_time = sum(fcfs_wait_times) / len(fcfs_wait_times) if fcfs_wait_times else 0
    print(f"\nTempo médio de espera (FCFS): {fcfs_avg_wait_time:.2f} segundos.")

    # Executar o download usando SJF
    sjf_wait_times = download_file_sjf(url, num_chunks)
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
