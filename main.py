#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AHIS Multi-Tool - Linux CLI Interface (Fully Functional Edition)
Inspired by the cyberpunk/ethical hacker terminal UI design.
"""

import os
import sys
import time
import socket
import urllib.request
import urllib.parse
import json
import base64
import platform
import threading
import random
import string
import qrcode

# ----------------- ANSI COLOR & STYLE DEFINITIONS -----------------
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

C_GLOW_WHITE = "\033[1;97m"            
C_WHITE      = "\033[1;97m"            
C_SILVER     = "\033[97m"              
C_BORDER     = "\033[1;37m"            
C_BORDER_DIM = "\033[37m"              
C_TITLE_PINK = "\033[1;97m"            
C_TEXT_RED   = "\033[97m"              
C_ACCENT_RED = "\033[1;97m"            
C_CYAN       = "\033[1;97m"            
C_GREEN      = "\033[1;97m"            

def clear_screen():
    """Clear terminal screen cross-platform (Linux / Windows)."""
    os.system("clear" if os.name != "nt" else "cls")

def get_bw_melting_char(char, col_factor, row_idx, total_rows):
    if char == " ":
        return " "
    vert_progress = row_idx / max(1, total_rows - 1)
    if char in "█▀▄▌▐":
        return f"\033[1;97m\033[38;2;255;255;255m{char}"
    elif char in "│┃║":
        lum = int(255 - (60 * (vert_progress ** 0.6)))
        return f"\033[1m\033[38;2;{lum};{lum};{lum}m{char}"
    elif char in "╵╹.":
        return f"\033[1;37m\033[38;2;215;215;215m{char}"
    else:
        lum = int(255 - (35 * vert_progress))
        return f"\033[1m\033[38;2;{lum};{lum};{lum}m{char}"

def print_banner():
    terminal_width = 80
    top_bar = f"{C_BORDER_DIM}─── [ {BOLD}{C_WHITE}AHIS MULTITOOL{RESET}{C_BORDER_DIM} ] ───{RESET}"
    print(f"\n{top_bar.center(terminal_width + 10)}\n")

    raw_logo = [
        r"  ▄██████▄     ████    ████   ████████   ▄████████▄  ",
        r" ████  ████    ████    ████     ████     ████▀   ▀▀  ",
        r"████    ████   ████    ████     ████     ████████▄   ",
        r"████████████   ████████████     ████      ▀▀▀▀█████  ",
        r"████    ████   ████ │  ████     ████     ▄▄▄   ████  ",
        r"████    ████   ████ │  ████   ████████   ▀████████▀  ",
        r"│███    ███│   │███ │  ███│     │██│     │ ███  ██│  ",
        r"││█│    │█││   ││█│ │  │█││     │  │     │  │█  █│   ",
        r"│ │      │ │   │ │  │    │      │  │     │   │  │    ",
        r"│ │      │     │    │    │      │            │  │    ",
        r"│              │         │      │               │    ",
        r"╵              ╵         ╵      ╵               ╵    ",
        r"                         ╵                           "
    ]

    total_rows = len(raw_logo)
    for row_idx, line in enumerate(raw_logo):
        colored_line = ""
        total_chars = len(line)
        for i, ch in enumerate(line):
            col_factor = i / max(1, total_chars - 1)
            colored_line += get_bw_melting_char(ch, col_factor, row_idx, total_rows)
        left_pad = max(0, (terminal_width - len(line)) // 2)
        print(f"{' ' * left_pad}{colored_line}{RESET}")

    quote = f"{BOLD}{C_WHITE}~ Present Day, Present Time ~{RESET}"
    print(f"\n{quote.center(terminal_width + 10)}\n")

def format_navi_item(text, width):
    if not text:
        return " " * width
    idx = text.find("]")
    if idx != -1:
        num_part = text[:idx+1]
        label_part = text[idx+1:]
        colored = f"{BOLD}{C_WHITE}{num_part}{RESET}{C_SILVER}{label_part}{RESET}"
        pad = " " * max(0, width - len(text))
        return colored + pad
    return f"{C_SILVER}{text}{RESET}" + (" " * max(0, width - len(text)))

def print_navi_menu():
    col1_w, col2_w, col3_w = 26, 26, 26
    c1_title = f"{BOLD}{C_WHITE}[ NETWORK ]{RESET}"
    c2_title = f"{BOLD}{C_WHITE}[ TOOLS ]{RESET}"
    c3_title = f"{BOLD}{C_WHITE}[ OTHER ]{RESET}"
    print(f"  {c1_title:<35} {c2_title:<35} {c3_title}")

    row_c1 = [
        "[1] IP Scanner", "[2] Port Scanner", "[3] DNS Lookup",
        "[4] Stress Tester", "[5] IP Pinger"
    ]
    row_c2 = [
        "[6] Obfuscator", "[7] Web Cloner", "[8] QR Code Gen",
        "", ""
    ]
    row_c3 = [
        "[9] Roblox User Info", "", "",
        "[99] Exit", ""
    ]

    for i in range(5):
        item1 = format_navi_item(row_c1[i], col1_w)
        item2 = format_navi_item(row_c2[i], col2_w)
        item3 = format_navi_item(row_c3[i], col3_w)
        print(f"  {item1} {item2} {item3}")
    print()

CYBER_FACE_ART = [
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣧⣶⣶⣶⣦⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⣾⢿⣿⣿⣿⣏⠉⠉⠛⠛⠿⣷⣕⠀⠀⠀⠀⠀⠀⢀⡀
⠀⠀⠀⠀⣠⣾⢝⠄⢀⣿⡿⠻⣿⣄⠀⠀⠀⠀⠈⢿⣧⡀⣀⣤⡾⠀⠀⠀
⠀⠀⠀⢰⣿⡡⠁⠀⠀⣿⡇⠀⠸⣿⣾⡆⠀⠀⣀⣤⣿⣿⠋⠁⠀⠀⠀⠀
⠀⠀⢀⣷⣿⠃⠀⠀⢸⣿⡇⠀⠀⠹⣿⣷⣴⡾⠟⠉⠸⣿⡇⠀⠀⠀⠀⠀
⠀⠀⢸⣿⠗⡀⠀⠀⢸⣿⠃⣠⣶⣿⠿⢿⣿⡀⠀⠀⢀⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠘⡿⡄⣇⠀⣀⣾⣿⡿⠟⠋⠁⠀⠈⢻⣷⣆⡄⢸⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⢻⣷⣿⣿⠿⣿⣧⠀⠀⠀⠀⠀⠀⡀⠻⣿⣷⣿⡟⠀⠀⠀⠀⠀⠀
⢀⣰⣾⣿⠿⣿⣿⣾⣿⠇⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣅⠀⠀⠀⠀⠀⠀
⠀⠰⠊⠁⠀⠙⠪⣿⣿⣶⣤⣄⣀⣀⣀⣤⣶⣿⠟⠋⠙⢿⣷⡄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣿⡟⠺⠭⠭⠿⠿⠿⠟⠋⠁⠀⠀⠀⠂⠙⠏⣦⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⡟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
]

FEATURE_NAMES = {
    "1": "IP Scanner", "2": "Port Scanner", "3": "DNS Lookup",
    "4": "Stress Tester", "5": "IP Pinger", "6": "Obfuscator",
    "7": "Web Cloner", "8": "QR Code Gen", "9": "Roblox User Info"
}

def show_cyber_face(feature_title="System Module"):
    clear_screen()
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    print()
    try:
        for line in CYBER_FACE_ART:
            sys.stdout.write(f"{C_WHITE}{line.rstrip()}{RESET}\n")
            sys.stdout.flush()
            time.sleep(0.016)
        print()
        boot_steps = [
            "[*] Booting Copeland OS [ Node: silve ]...",
            "[*] Connecting to the Wired...",
            "[*] Initializing Navi protocol...",
            f"[*] Accessing: {feature_title}..."
        ]
        for step in boot_steps:
            sys.stdout.write(f"   {C_WHITE}")
            for ch in step:
                sys.stdout.write(ch)
                sys.stdout.flush()
                time.sleep(0.006)
            sys.stdout.write(f"{RESET}\n")
            sys.stdout.flush()
            time.sleep(0.12)
        print()
        time.sleep(0.3)
    finally:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

# ----------------- FUNGSI FITUR UTAMA (RUNNABLE & FULLY CODED) -----------------

def tool_ip_scanner():
    """IP Scanner - Fetch detailed info about any IP address using ipinfo.io API."""
    print(f"\n{BOLD}{C_WHITE}[ IP ADDRESS SCANNER ]{RESET}")
    ip_address = input(f"{C_CYAN}Enter Target IP Address: {RESET}").strip()
    print()
    try:
        url = f"https://ipinfo.io/{ip_address}/json"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
        for key, value in data.items():
            print(f"{C_WHITE}[+] {C_GREEN}{key.capitalize():<12}: {C_WHITE}{value}{RESET}")
        print(f"\n{C_GREEN}[+] IP scan selesai.{RESET}")
    except Exception as e:
        print(f"\n{C_WHITE}[!] Error Fetching IP Information: {e}{RESET}")

def tool_port_scanner():
    print(f"\n{BOLD}{C_WHITE}[ NETWORK PORT SCANNER ]{RESET}")
    target = input(f"{C_CYAN}Target IP / Domain: {RESET}").strip()
    ports = [21, 22, 23, 25, 53, 80, 110, 443, 445, 3306, 3389, 8080]
    print(f"\n{C_SILVER}[*] Scanning {target} pada port umum...{RESET}\n")
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.8)
            result = s.connect_ex((target, port))
            if result == 0:
                print(f"{C_GREEN}[OPEN] Port {port}{RESET}")
            else:
                print(f"{C_BORDER_DIM}[CLOSED] Port {port}{RESET}")
            s.close()
        except Exception:
            pass

def tool_dns_lookup():
    print(f"\n{BOLD}{C_WHITE}[ DNS LOOKUP ]{RESET}")
    domain = input(f"{C_CYAN}Masukkan Domain (contoh: google.com): {RESET}").strip()
    try:
        ip = socket.gethostbyname(domain)
        print(f"\n{C_GREEN}[+] IP Address untuk {domain} adalah: {ip}{RESET}")
    except Exception as e:
        print(f"\n{C_WHITE}[!] Gagal melakukan DNS lookup: {e}{RESET}")

def tool_ip_pinger():
    print(f"\n{BOLD}{C_WHITE}[ IP / DOMAIN PINGER ]{RESET}")
    target = input(f"{C_CYAN}Target IP / Domain: {RESET}").strip()
    param = "-n" if platform.system().lower() == "windows" else "-c"
    print(f"\n{C_SILVER}[*] Pinging {target}... Tekan Ctrl+C untuk berhenti.{RESET}\n")
    os.system(f"ping {param} 4 {target}")

def tool_qr_gen():
    print(f"\n{BOLD}{C_WHITE}[ QR CODE GENERATOR ]{RESET}")
    data = input(f"{C_CYAN}Masukkan Teks / URL untuk QR: {RESET}").strip()
    filename = input(f"{C_CYAN}Nama file output (contoh: qr.png): {RESET}").strip() or "qrcode.png"
    try:
        img = qrcode.make(data)
        img.save(filename)
        print(f"\n{C_GREEN}[+] QR Code berhasil disimpan sebagai {filename}{RESET}")
    except Exception as e:
        print(f"\n{C_WHITE}[!] Gagal membuat QR Code: {e}{RESET}")

def tool_web_cloner():
    print(f"\n{BOLD}{C_WHITE}[ WEB CLONER ]{RESET}")
    url = input(f"{C_CYAN}URL Website target (dengan http/https): {RESET}").strip()
    output_file = input(f"{C_CYAN}Simpan sebagai (default: cloned.html): {RESET}").strip() or "cloned.html"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            html_content = response.read()
            with open(output_file, "wb") as f:
                f.write(html_content)
        print(f"\n{C_GREEN}[+] Berhasil clone website ke {output_file}{RESET}")
    except Exception as e:
        print(f"\n{C_WHITE}[!] Gagal melakukan cloning: {e}{RESET}")

def tool_obfuscator():
    print(f"\n{BOLD}{C_WHITE}[ SIMPLE PYTHON OBFUSCATOR ]{RESET}")
    script_path = input(f"{C_CYAN}Path file Python (.py) yang mau diobfuscate: {RESET}").strip()
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            code = f.read()
        encoded_bytes = base64.b64encode(code.encode("utf-8"))
        stub = f"import base64\nexec(base64.b64decode({encoded_bytes}).decode('utf-8'))\n"
        out_path = script_path.replace(".py", "_obf.py")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(stub)
        print(f"\n{C_GREEN}[+] Berhasil obfuscate! File tersimpan di: {out_path}{RESET}")
    except Exception as e:
        print(f"\n{C_WHITE}[!] Error: {e}{RESET}")

def tool_ddos():
    print(f"\n{BOLD}{C_WHITE}[ SIMPLE HTTP STRESS TESTER ]{RESET}")
    target = input(f"{C_CYAN}Target URL (http://...): {RESET}").strip()
    try:
        threads_count = int(input(f"{C_CYAN}Jumlah threads (contoh: 10): {RESET}").strip())
    except ValueError:
        threads_count = 5

    stop_flag = False

    def attack():
        while not stop_flag:
            try:
                req = urllib.request.Request(target, headers={"User-Agent": "Mozilla/5.0"})
                urllib.request.urlopen(req, timeout=2)
            except Exception:
                pass

    print(f"\n{C_SILVER}[*] Menjalankan stress test ke {target} dengan {threads_count} threads. Tekan Ctrl+C untuk berhenti.{RESET}\n")
    th_list = []
    for _ in range(threads_count):
        t = threading.Thread(target=attack)
        t.daemon = True
        t.start()
        th_list.append(t)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_flag = True
        print(f"\n{C_GREEN}[+] Stress test dihentikan.{RESET}")

def tool_roblox_user():
    print(f"\n{BOLD}{C_WHITE}[ ROBLOX USER INFO LOOKUP ]{RESET}")
    username = input(f"{C_CYAN}Masukkan Username Roblox: {RESET}").strip()
    url = f"https://users.roblox.com/v1/users/search?keyword={urllib.parse.quote(username)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
            if data.get("data"):
                user = data["data"][0]
                print(f"\n{C_GREEN}[+] User Ditemukan!")
                print(f" ID        : {user['id']}")
                print(f" Username  : {user['name']}")
                print(f" Display   : {user.get('displayName', 'N/A')}{RESET}")
            else:
                print(f"\n{C_WHITE}[!] User tidak ditemukan.{RESET}")
    except Exception as e:
        print(f"\n{C_WHITE}[!] Error fetching API: {e}{RESET}")

# ----------------- CUSTOM FEATURE ROUTER -----------------
def execute_feature(choice, feat_name):
    if choice == "1":
        tool_ip_scanner()
    elif choice == "2":
        tool_port_scanner()
    elif choice == "3":
        tool_dns_lookup()
    elif choice == "4":
        tool_ddos()
    elif choice == "5":
        tool_ip_pinger()
    elif choice == "6":
        tool_obfuscator()
    elif choice == "7":
        tool_web_cloner()
    elif choice == "8":
        tool_qr_gen()
    elif choice == "9":
        tool_roblox_user()
    else:
        print(f"\n{C_WHITE}[!] Opsi '{choice}' tidak tersedia.{RESET}")

# ----------------- MAIN INTERFACE LOOP -----------------
def main():
    while True:
        clear_screen()
        print_banner()
        print_navi_menu()

        prompt_str = f"{BOLD}{C_WHITE}silve@navi:~# {RESET}"
        
        try:
            choice = input(prompt_str).strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{C_SILVER}[!] Terminating Navi session...{RESET}")
            sys.exit(0)

        cmd = choice.upper()
        if cmd in ["99", "EXIT", "QUIT"]:
            print(f"\n{BOLD}{C_WHITE}[*] Disconnected from the Wired. Goodbye!{RESET}\n")
            break
        elif choice:
            feat_name = FEATURE_NAMES.get(choice, f"Module [{choice}]")
            show_cyber_face(feat_name)
            execute_feature(choice, feat_name)
            
            input(f"\n{BOLD}{C_WHITE}[Press Enter to return to terminal]{RESET}")

if __name__ == "__main__":
    main()
