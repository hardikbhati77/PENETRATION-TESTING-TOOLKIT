import socket
import requests
import time

# -------------------- PORT SCANNER --------------------
def scan_ports(target, start_port=1, end_port=1024):
    print(f"\n[+] Scanning {target} from port {start_port} to {end_port}...")
    open_ports = []

    try:
        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(0.5)
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"🟢 Port {port} is open")
                open_ports.append(port)
            sock.close()
    except KeyboardInterrupt:
        print("⛔ Scan interrupted by user.")
    except socket.gaierror:
        print("❌ Hostname could not be resolved.")
    except socket.error:
        print("❌ Connection error.")
    
    if not open_ports:
        print("❌ No open ports found.")
    return open_ports


# -------------------- BRUTE FORCE TOOL --------------------
def brute_force_login(url, username, password_file):
    print(f"\n[+] Starting brute-force attack on {url}")
    try:
        with open(password_file, 'r') as file:
            for password in file:
                password = password.strip()
                data = {"username": username, "password": password}
                response = requests.post(url, data=data)
                if "Login Failed" not in response.text:
                    print(f"✅ Success: Username: {username}, Password: {password}")
                    return
                else:
                    print(f"❌ Tried: {password}")
                time.sleep(0.5)  # To avoid getting blocked
        print("❌ Password not found in wordlist.")
    except FileNotFoundError:
        print("❌ Password file not found.")
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")


# -------------------- MAIN MENU --------------------
def main():
    while True:
        print("\n===============================")
        print("🔧 Penetration Testing Toolkit")
        print("===============================")
        print("1. Port Scanner")
        print("2. Brute-Force Login")
        print("0. Exit")
        print("===============================")

        choice = input("Choose an option: ")

        if choice == "1":
            target = input("Enter IP address or domain: ")
            try:
                start = int(input("Start port (default 1): ") or "1")
                end = int(input("End port (default 1024): ") or "1024")
                scan_ports(target, start, end)
            except ValueError:
                print("❌ Please enter valid port numbers.")
        elif choice == "2":
            url = input("Enter login URL (e.g. http://site.com/login): ")
            username = input("Enter username: ")
            password_file = input("Enter path to password list file (e.g. passwords.txt): ")
            brute_force_login(url, username, password_file)
        elif choice == "0":
            print("👋 Exiting toolkit. Goodbye!")
            break
        else:
            print("❌ Invalid option. Please choose 1, 2, or 0.")

# Entry point
if __name__ == "__main__":
    main()
