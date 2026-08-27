"""
Kaggle Cyber Agent - Server Script
Executa o daemon do Ollama com modelo de Cibersegurança (DeepHat / WhiteRabbitNeo)
e abre um túnel seguro via Cloudflare Tunnels (Zero Port-Forwarding).
Execute este script em um Notebook Kaggle com GPU T4 x2 e Internet: ON.
"""

import os
import sys
import time
import subprocess
import threading
import queue
import re
import socket

WORKDIR = "/kaggle/working"


def run_cmd(cmd, desc, ignore_error=False):
    print(f"[*] {desc}...")
    try:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL)
        print("    [+] Sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"    [-] Falha ao executar: {cmd}")
        print(f"    [-] Detalhes do erro do sistema: {e}")
        if not ignore_error:
            sys.exit(1)


# 1. Variáveis de ambiente
os.environ["OLLAMA_MODELS"] = f"{WORKDIR}/ollama_models"
os.environ["OLLAMA_HOST"] = "127.0.0.1:11434"
os.environ["OLLAMA_DEBUG"] = "1"
os.environ["OLLAMA_ORIGINS"] = "*"
env = os.environ.copy()

os.makedirs(os.environ["OLLAMA_MODELS"], exist_ok=True)

# Limpeza de processos anteriores
print("[!] Limpando processos anteriores...")
try:
    subprocess.run("pkill -f 'bin/ollama serve'", shell=True, check=True, stdout=subprocess.DEVNULL)
    print("    [+] Ollama encerrado.")
except subprocess.CalledProcessError:
    print("    [+] Nenhum processo Ollama encontrado.")

try:
    subprocess.run("pkill -f './cloudflared tunnel'", shell=True, check=True, stdout=subprocess.DEVNULL)
    print("    [+] Cloudflared encerrado.")
except subprocess.CalledProcessError:
    print("    [+] Nenhum processo Cloudflared encontrado.")


# 2. Instalação das dependências (user-space)
run_cmd("apt-get update -qq && apt-get install -y -qq zstd", "Instalando Zstandard para extração")
run_cmd("curl -fL --retry 3 https://ollama.com/download/ollama-linux-amd64.tar.zst -o ollama-linux-amd64.tar.zst", "Baixando o binário do Ollama (zst)")

with open("ollama-linux-amd64.tar.zst", "rb") as f:
    magic = f.read(2)
if magic != b"\x28\xb5":
    print("    [-] Arquivo baixado inválido. Verifique se Internet está ON no Kaggle.")
    sys.exit(1)

run_cmd(f"zstd -d -c ollama-linux-amd64.tar.zst | tar -xf - -C {WORKDIR}/", "Extraindo o Ollama")
run_cmd("curl -fL --retry 3 https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o ./cloudflared", "Baixando binário do Cloudflared")
run_cmd("chmod +x ./cloudflared", "Tornando o Cloudflared executável")


# 3. Iniciar o daemon do Ollama em background
print("[*] Iniciando o servidor Ollama...")
try:
    ollama_proc = subprocess.Popen([f"{WORKDIR}/bin/ollama", "serve"], env=env, stdout=subprocess.DEVNULL)
except Exception as e:
    print(f"    [-] Erro crítico ao iniciar daemon Ollama: {e}")
    sys.exit(1)


def wait_port(host, port, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False


if wait_port("127.0.0.1", 11434, timeout=30):
    print("    [+] Servidor rodando na porta 11434.")
else:
    print("    [-] Timeout esperando o Ollama subir na porta 11434.")
    sys.exit(1)

# 4. Baixar modelo de Cyber / AI Agent
MODEL = "monotykamary/whiterabbitneo-v1.5a:7b"
run_cmd(f"{WORKDIR}/bin/ollama pull {MODEL}", f"Baixando a IA {MODEL}")

# 5. Inicializar o Túnel Cloudflare
print("[*] Estabelecendo túnel seguro Cloudflare...")


def read_stream(stream, q):
    for line in iter(stream.readline, ""):
        q.put(line)
    q.put(None)


try:
    tunnel_proc = subprocess.Popen(
        [
            "./cloudflared",
            "tunnel",
            "--url",
            "http://127.0.0.1:11434",
            "--http-host-header",
            "127.0.0.1:11434",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    q = queue.Queue()
    t = threading.Thread(target=read_stream, args=(tunnel_proc.stderr, q), daemon=True)
    t.start()

    public_url = None
    deadline = time.time() + 25
    while time.time() < deadline:
        try:
            line = q.get(timeout=0.5)
        except queue.Empty:
            continue
        if line is None:
            break
        match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
        if match:
            public_url = match.group(0)
            break

    if public_url:
        print("\n" + "=" * 70)
        print("🚀 IA OPERACIONAL E ONLINE!")
        print(f"👉 Copie esta URL para a BASE_URL do seu Cliente/Agente: {public_url}/v1")
        print("=" * 70)
    else:
        print("\n[-] Timeout: Não foi possível obter URL do túnel Cloudflare.")

except Exception as e:
    print(f"\n[-] Erro ao gerenciar o túnel: {e}")
    sys.exit(1)
