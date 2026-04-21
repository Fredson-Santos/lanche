import socket
import time
import os
import sys

def wait_for_db():
    database_url = os.environ.get("DATABASE_URL", "")
    if "postgresql" not in database_url:
        print("DATABASE_URL não é Postgres, pulando espera.")
        return

    # Extrair host e porta da URL: postgresql://user:pass@host:port/db
    try:
        host_port = database_url.split("@")[1].split("/")[0]
        if ":" in host_port:
            host, port = host_port.split(":")
            port = int(port)
        else:
            host = host_port
            port = 5432
    except Exception as e:
        print(f"Erro ao parsear DATABASE_URL: {e}")
        sys.exit(1)

    print(f"Aguardando o banco {host}:{port} estar pronto...")
    
    start_time = time.time()
    timeout = 30
    
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                print("Banco de dados pronto!")
                return
        except (socket.timeout, ConnectionRefusedError):
            time.sleep(1)
            
    print("Tempo limite atingido aguardando o banco de dados.")
    sys.exit(1)

if __name__ == "__main__":
    wait_for_db()
