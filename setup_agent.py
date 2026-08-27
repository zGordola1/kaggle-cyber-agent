"""
Configurador do Agente Sandbox (Windows / Linux)
Configura o Open Interpreter e as variáveis de ambiente apontando para o túnel do Kaggle.

Uso:
    python setup_agent.py --cloudflare-url https://sua-url.trycloudflare.com
"""

import argparse
import ctypes
import os
import re
import subprocess
import sys
import urllib.request

SANDBOX_DIR = r"C:\Sandbox_IA" if os.name == "nt" else os.path.expanduser("~/sandbox_ia")


class C:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"


def enable_ansi():
    if os.name == "nt":
        try:
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            kernel32.SetConsoleMode(handle, 7)
        except Exception:
            pass


def cprint(msg, color=""):
    print(f"{color}{msg}{C.RESET}" if color else msg)


def run_step(description, action, failure_hint=""):
    cprint(f"\n[*] {description}...")
    try:
        action()
        cprint("    [+] OK.", C.GREEN)
    except Exception as e:
        cprint(f"    [-] Falha: {e}", C.RED)
        if failure_hint:
            cprint(f"    [-] {failure_hint}", C.RED)
        sys.exit(1)


def set_persistent_env_var(name, value):
    if os.name == "nt":
        import winreg

        with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)

        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x1A
        SMTO_ABORTIFHUNG = 0x0002
        result = ctypes.c_long()
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment",
            SMTO_ABORTIFHUNG, 5000, ctypes.byref(result)
        )
    os.environ[name] = value


def main():
    parser = argparse.ArgumentParser(description="Configura o Agente na sandbox apontando pro túnel do Kaggle.")
    parser.add_argument("-u", "--cloudflare-url", required=True, help="URL gerada no Kaggle (ex: https://xxxx.trycloudflare.com)")
    args = parser.parse_args()

    enable_ansi()

    cprint("=" * 60, C.CYAN)
    cprint(" INICIANDO SETUP DO AGENTE SANDBOX CYBER", C.CYAN)
    cprint("=" * 60, C.CYAN)

    if not re.match(r"^https?://\S+$", args.cloudflare_url):
        cprint(f"[-] URL inválida: '{args.cloudflare_url}'.", C.RED)
        sys.exit(1)

    def check_python():
        if sys.version_info < (3, 10):
            raise RuntimeError("Requer Python 3.10+")
        cprint(f"    Python encontrado: {sys.version.split()[0]}")

    run_step("Verificando versão do Python", check_python)

    def install_interpreter():
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, "-m", "pip", "install", "open-interpreter"], check=True)

    run_step("Instalando/Atualizando Open Interpreter", install_interpreter)

    base_url = args.cloudflare_url.rstrip("/")
    if not base_url.endswith("/v1"):
        base_url += "/v1"

    def configure_env():
        set_persistent_env_var("OPENAI_API_BASE", base_url)
        set_persistent_env_var("OPENAI_API_KEY", "sk-local")
        cprint(f"    [+] OPENAI_API_BASE definida como: {base_url}", C.GREEN)

    run_step("Configurando variáveis de ambiente", configure_env)

    # Diretório de contenção (sandbox)
    cprint(f"\n[*] Verificando diretório de contenção em {SANDBOX_DIR}...")
    os.makedirs(SANDBOX_DIR, exist_ok=True)
    cprint("    [+] Diretório pronto.", C.GREEN)

    cprint("\n" + "=" * 60, C.CYAN)
    cprint(" SETUP CONCLUÍDO COM SUCESSO! ", C.GREEN)
    cprint("=" * 60, C.CYAN)


if __name__ == "__main__":
    main()
