import socket
import threading

HOST = socket.gethostname()
PORT = 12312


def recv_loop(sock):
    """Постоянно читает сообщения от сервера."""
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                print("\n[!] Сервер закрыл соединение")
                break
            print(f"\n===================\n{data.decode(errors='ignore')}")
            print("Введите сообщение: ", end="", flush=True)
    except OSError:
        pass


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"Подключено к {HOST}:{PORT}")

    threading.Thread(target=recv_loop, args=(client,), daemon=True).start()

    try:
        while True:
            message = input("Введите сообщение: ")
            if not message:
                continue
            if message.lower() in ("exit", "quit"):
                break
            client.sendall(message.encode())
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        client.close()
        print("Клиент завершён")


if __name__ == "__main__":
    main()