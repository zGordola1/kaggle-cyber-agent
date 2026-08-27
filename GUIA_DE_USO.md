# 🚀 Guia de Uso: Setup Completo do Agente IA (Open Interpreter + Kaggle)

Este guia prático vai te ensinar do zero a como rodar o seu próprio agente de Inteligência Artificial usando o poder de processamento do Kaggle (de graça!) e conectar com o seu computador local ou VPS (Sandbox) para que a IA realize tarefas automatizadas para você.

---

## 🧠 Parte 1: Preparando o "Cérebro" da IA (No Kaggle)

O Kaggle vai nos ceder gratuitamente placas de vídeo (GPUs) super potentes para rodar o modelo do nosso agente de forma rápida.

1. **Crie sua conta no Kaggle**
   - Acesse [kaggle.com](https://www.kaggle.com/) e crie uma conta.
   - **Importante:** Vá nas configurações da sua conta e **vincule um número de telefone**. O Kaggle exige essa verificação por SMS para liberar o uso das GPUs e da internet na máquina virtual.

2. **Crie um Novo Notebook**
   - Na página inicial do Kaggle, clique em **"Create"** (lado esquerdo) e depois escolha **"New Notebook"**.

3. **Configure a Máquina Virtual**
   - No canto direito da tela, procure o painel **"Notebook options"** ou **"Settings"**.
   - **Accelerator:** Mude a opção para **GPU T4 x2** (Isso é crucial para a IA responder rápido).
   - **Internet:** Mude a chave para **On** (Necessário para podermos baixar o Ollama e ativar o túnel da Cloudflare).

4. **Rode o Script do Servidor**
   - Apague qualquer código de exemplo que já venha na primeira célula do notebook.
   - Abra o arquivo `kaggle_server.py` que veio junto com este repositório, copie **todo o código** dele e cole na célula vazia do Kaggle.
   - Dê "Play" (Run) na célula.
   - Aguarde o download do Ollama e do modelo `whiterabbitneo-v1.5a:7b` (ou `DeepHat-V1-7B` se configurou a versão maior). No final, o terminal do Kaggle vai imprimir uma mensagem dizendo `🚀 IA OPERACIONAL E ONLINE!` e vai te dar um link parecido com `https://palavra-aleatoria.trycloudflare.com`.
   - **Copie esse link!** Você vai precisar dele na próxima etapa.

---

## 💻 Parte 2: Configurando o "Corpo" da IA (No seu Windows/VPS)

Agora vamos configurar a sua máquina Windows (ou sua VPS) para ouvir e obedecer os comandos da IA.

1. **Requisitos Mínimos**
   - Windows 10, Windows 11 ou Windows Server 2022 / Linux.
   - **Python 3.10, 3.11 ou 3.12** instalados. 
   - *Atenção na hora de instalar o Python:* Marque a caixa **"Add python.exe to PATH"** logo na primeira tela do instalador!

2. **Rodando o Instalador Automático**
   - Abra o seu **PowerShell** ou **Terminal**.
   - Navegue até a pasta do repositório:
     ```bash
     git clone https://github.com/zGordola1/kaggle-cyber-agent.git
     cd kaggle-cyber-agent
     ```
   - Execute o script `setup_agent.py` passando o link do Cloudflare que você copiou do Kaggle:
     ```powershell
     python setup_agent.py --cloudflare-url https://seu-link-aqui.trycloudflare.com
     ```
   - O script é 100% automático! Ele vai:
     - Baixar e instalar/atualizar o ambiente do Open Interpreter.
     - Configurar as variáveis de ambiente necessárias.
     - Criar uma pasta segura para o agente trabalhar (`C:\Sandbox_IA` ou `~/sandbox_ia`).

---

## 🎮 Parte 3: Como Usar o Seu Novo Agente IA

Após a instalação, um atalho chamado `Iniciar_Agente.bat` será criado automaticamente dentro da pasta `C:\Sandbox_IA`. 
Vá até essa pasta e dê um duplo clique no `.bat` para abrir o terminal interativo do seu agente!

### 🛡️ A Pasta de Testes (Sandbox)
O diretório `C:\Sandbox_IA` é o seu ambiente seguro. Se você quer que a IA analise uma planilha, altere um código fonte, estude um script ou crie relatórios, mova esses arquivos para dentro desta pasta. É uma boa prática manter as atividades da IA "contidas" no lugar onde ela foi programada para agir.

### 🛠️ O que você pode pedir para a IA fazer?
Você pode conversar em português natural! Como o Open Interpreter escreve e executa códigos reais no seu computador, o limite é a sua criatividade. Sempre que a IA bolar uma solução técnica para o seu pedido, ela vai mostrar o código e pedir a sua permissão (você digita `1` ou `y` para autorizar).

**Exemplos de ideias e comandos práticos:**

- 📊 **Análise de Dados:** 
  *"Leia a planilha `vendas.xlsx` que está nesta pasta, some o faturamento total de todos os meses, gere um gráfico de barras e salve o resultado como imagem."*

- 💻 **Programação e Debug:** 
  *"Abra o script `app.js`. Tem um bug na função de login. Identifique o erro e reescreva o arquivo consertado."*

- ⚙️ **Automação do Sistema (VPS/Windows):** 
  *"Descubra qual é o meu endereço IP público local e salve dentro de um arquivo chamado `meu_ip.txt`."*
  *"Crie um script em Python que faça backup de todos os PDFs desta pasta em um arquivo ZIP."*

- 🔍 **Pesquisa e Scraping:** 
  *"Faça um web scraping no Google pesquisando pelas cotações do Dólar na última semana e me dê a média."*

- 🔬 **Análise de Malware / Scripts Suspeitos em Sandbox:**
  *"Analise o script `payload_suspeito.ps1` nesta pasta, extraia todas as URLs, IPs e chamadas de API ofuscadas e faça um relatório de risco."*

> [!WARNING]
> **Aviso Importante sobre o Túnel:**
> O Kaggle reinicia as sessões e desliga as GPUs quando você fica inativo. Toda vez que você precisar ligar o seu Kaggle novamente, um **novo link** do Cloudflare será gerado. Quando isso acontecer, basta abrir o PowerShell no seu Windows e rodar o `setup_agent.py` passando a nova URL. Ele atualiza tudo em dois segundos!
