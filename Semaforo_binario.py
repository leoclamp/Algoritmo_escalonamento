import concurrent.futures
import requests
import time
from threading import Semaphore

# Função que baixa uma parte de um arquivo
def download_part(url, part_num, start, end, sem):
    with sem:  # Semáforo binário controla o acesso
        print(f"Baixando a parte {part_num + 1}")
        headers = {'Range': f'bytes={start}-{end}'}
        response = requests.get(url, headers=headers)
        print(f"Download da parte {part_num + 1}, finalizado com {len(response.content)} bytes.")
        return response.content

def download_with_binary_semaphore(url, num_parts):
    response = requests.head(url)
    file_size = int(response.headers.get('Content-Length', 0))
    part_size = file_size // num_parts
    futures = []
    sem = Semaphore(1)  # Semáforo binário

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_parts) as executor:
        for i in range(num_parts):
            start = i * part_size
            end = start + part_size - 1 if i < num_parts - 1 else file_size - 1
            futures.append(executor.submit(download_part, url, i, start, end, sem))

    for future in concurrent.futures.as_completed(futures):
        future.result()

# URL para download
url = "http://example.com/file"

# Número de partes
num_parts = 4

# Medir o tempo de execução
start_time = time.time()
download_with_binary_semaphore(url, num_parts)
end_time = time.time()
print(f"Tempo total com semáforo binário: {end_time - start_time:.2f} segundos")
