import subprocess
import sys
import os

processes = []

# ANSI-код очистки экрана и перевода курсора в начало
CLEAR = "\033[2J\033[H"

def clear_screen():
    # В Windows 10+ ANSI работает; если нет — раскомментируйте os.system("cls")
    sys.stdout.write(CLEAR)
    sys.stdout.flush()

def start_process(script_name):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if not os.path.exists(script_path):
        return f"[!] Файл {script_name} не найден"
    proc = subprocess.Popen(
        [sys.executable, script_path],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    processes.append((proc, script_name))
    return f"[+] Запущен {script_name} (PID {proc.pid})"

def stop_all():
    count = 0
    for proc, name in processes:
        if proc.poll() is None:
            proc.terminate()
            count += 1
    processes.clear()
    return f"Отправлен сигнал завершения {count} процессам"

def render(last_message=""):
    """Полностью перерисовывает экран менеджера."""
    clear_screen()
    print("=== Центр управления клиент-серверным приложением ===")
    print("Команды: server | client | list | stop | exit")
    print("=" * 54)

    # Статус процессов
    if processes:
        print("Запущенные процессы:")
        for proc, name in processes:
            status = "работает" if proc.poll() is None else "завершён"
            print(f"  {name:<12} PID {proc.pid:<6} -> {status}")
    else:
        print("Запущенных процессов нет.")
    print("-" * 54)

    if last_message:
        print(last_message)
        print("-" * 54)

def main():
    last_message = ""
    while True:
        render(last_message)
        try:
            cmd = input("manager> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            break

        if cmd == "server":
            last_message = start_process("server.py")
        elif cmd == "client":
            last_message = start_process("client.py")
        elif cmd == "list":
            last_message = ""  # список и так в шапке
        elif cmd == "stop":
            last_message = stop_all()
        elif cmd == "exit":
            print("Выход из центра управления.")
            break
        elif cmd == "":
            last_message = ""
        else:
            last_message = f"[!] Неизвестная команда: {cmd}"

if __name__ == "__main__":
    main()