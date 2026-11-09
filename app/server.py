import socket
import time
import threading

clients = []
clients_lock = threading.Lock()

messages = []
messages_lock = threading.Lock()

message_ok = "Yhank you for your message"

hostname = socket.gethostname()
port = 12312


def loop():
    while True:
        time.sleep(5)
    
        with messages_lock:
            if not messages:
                continue
                
            package_messages = ('\n'.join(messages)).encode()
            messages.clear()
        
        with clients_lock:
            dead_clients = []
            for client in clients:
                try:
                    client.sendall(package_messages)
                except OSError:
                    dead_clients.append(client)
                    
            for client in dead_clients:
                try:
                    clients.remove(client)
                except OSError:
                    ...
                    
def handle_client(conn, addr):
    print(f"[+] Клиент подключён: {addr}")
    with clients_lock:
        clients.append(conn)

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode(errors="ignore")
            print(f"[{addr}] -> {message}")

            with messages_lock:
                messages.append(f"{addr}: {message}")

            # подтверждение отправителю
            try:
                conn.sendall(message_ok.encode())
            except OSError:
                break
    except OSError as e:
        print(f"[!] Ошибка с клиентом {addr}: {e}")
    finally:
        with clients_lock:
            if conn in clients:
                clients.remove(conn)
        try:
            conn.close()
        except OSError:
            pass
        print(f"[-] Клиент отключён: {addr}")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((hostname, port))
    server.listen(5)
    print(f"Сервер запущен на {hostname}:{port}")

    threading.Thread(target=loop, daemon=True).start()

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(
                target=handle_client, args=(conn, addr), daemon=True
            ).start()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
    finally:
        server.close()


if __name__ == "__main__":
    main()