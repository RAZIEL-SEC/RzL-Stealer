# 🚀 CrypToolBuild

O **CrypTool Build** é uma interface de linha de comando (CLI) avançada projetada para automatizar o processo de compilação, ofuscação e empacotamento de scripts Python. Ele foi desenvolvido para transformar scripts complexos em executáveis robustos, permitindo o controle total sobre o comportamento do runtime.

## ✨ Funcionalidades Principais

- **Interface CLI Interativa:** Menu intuitivo para facilitar o fluxo de trabalho sem necessidade de editar código.
- **Modos de Execução Customizáveis:**
  - 🛠️ **Modo DEBUG (Console):** Mantém a janela do terminal aberta. Ideal para desenvolvedores testarem o comportamento do payload e visualizarem logs de erro em tempo real.
  - 🕵️ **Modo STEALTH (Background):** Remove a necessidade de console. O executável roda silenciosamente em segundo plano, ideal para payloads de produção.
- **Gerenciamento de Dependências:** Automatiza o empacotamento de bibliotecas pesadas e complexas (como **`cryptography`** e **`opencv`**) através de flags de injeção automática.
- **Limpeza Automática de Workspace:** Gerencia pastas de build (**`build/`**, **`dist/`**) para garantir compilações limpas e evitar conflitos de cache.

## 📋 Requisitos

Para utilizar o Engine, você deve configurar um ambiente de desenvolvimento controlado:

- **Python:** **`3.10`** ou superior.
- **Ambiente:** Recomenda-se o uso de um Ambiente Virtual (**`venv`**) para isolar as dependências.
- **Sistema Operacional:** Windows (Otimizado para ambientes Windows).

## 🛠️ Instalação e Uso

### 1. Clonar e Preparar o Ambiente

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto

# Crie e ative sua venv
python -m venv venv
.\venv\Scripts\activate

# Instale as dependências necessárias
pip install -r requirements.txt
```

### 2. Executando o Engine

Com a venv ativa e o seu código alvo na pasta, basta rodar:

```bash
python Professional_Builder_Pro.py
```

### 3. Fluxo de Trabalho Recomendado

1. **Configurar Arquivo:** Defina o script **`.py`** que será o alvo da compilação.
2. **Escolher Modo:**
   - Use **`Modo DEBUG`** para garantir que o seu código está funcionando.
   - Use **`Modo STEALTH`** para gerar a versão final para distribuição.
3. **Compilar:** Inicie o processo de build e aguarde a conclusão.
4. **Resultado:** O executável final será gerado na pasta **`dist/`**.

## 📦 Dependências do Sistema

O Engine gerencia automaticamente o empacotamento de:

- **`cryptography`** (Criptografia de alto nível)
- **`cv2`** (OpenCV - Processamento de imagem)
- **`win32crypt`** (Integração com APIs Windows)
- **`requests`**, **`psutil`**, **`browser_cookie3`** (Dependências de rede e sistema)
