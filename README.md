# 🚀 Real-Time Crypto Wallet Balance & AI Risk Analyzer MCP Server

A high-performance, Claude-integrated MCP Server for checking real-time wallet balances on Ethereum, Polygon, Arbitrum, and (optionally) Solana, with AI-powered risk analysis using the Hugging Face FinBERT model.

Supports Claude's @eth_balance.get_wallet_balance and @eth_balance.analyze_wallet_risk tools out of the box.

📦 Features
🔗 Multi-chain support (Ethereum, Polygon, Arbitrum, Solana)

⚖️ Native token balances (ETH/MATIC/etc.) in real-time

🤖 AI-powered wallet risk analysis (via HuggingFace FinBERT)

🧠 Built-in MCP protocol for Claude AI Desktop

🧪 Async + HTTPX + Web3 + Solana support

---

## 📦 Features

- 🚀 FastAPI backend
- 🌍 Supports Ethereum, Polygon, and Arbitrum
- 💰 Converts balances to USD using CoinGecko API
- 🔐 Secure via `.env` for Alchemy API keys
- 🧪 Interactive Swagger docs for easy testing

---

## Prerequisites

- Python 3.9+
- Claude Desktop
- Alchemy API keys for Ethereum, Polygon, - Arbitrum
- HuggingFace API key for FinBERT model access

---

## 🛠️ Getting Started

Follow the steps below to set up and run the project on **Windows or macOS** (Intel & Apple Silicon/M1).

---

## 📁 Clone the Repository

```bash
git clone https://github.com/callmeKORRA03/korra_demcp
cd korra_demcp
```

🐍 Set Up Python Environment
Recommended Python Version: 3.9+

✅ Windows

```bash
uv venv

.venv\Scripts\activate

# Install dependencies
uv add mcp[cli]
```

✅ macOS (Intel & Apple Silicon)

```bash
uv venv

source .venv/bin/activate

# Install dependencies
uv add "mcp[cli]"
```

💡 Apple M1/M2 users: If you're using Homebrew-installed Python, use brew install python@3.9 and replace python3 accordingly.

📥 Install Dependencies
Make sure your virtual environment is activated, then run:

```bash
pip install -r requirements.txt

OR

uv pip install -r requirements.txt
```

🔐 Setup .env File
Create a .env file in the root directory and add your Alchemy RPC URLs for each network:

```bash
ETH_RPC=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY
POL_RPC=https://polygon-mainnet.g.alchemy.com/v2/YOUR_KEY
ARB_RPC=https://arb-mainnet.g.alchemy.com/v2/YOUR_KEY
HF_TOKEN=hf_YOUR_GENERATED_TOKEN
```

Get Alchemy Keys

```
Go to https://www.alchemy.com/
Create a free account
Create a new App for each chain (Ethereum, Polygon, Arbitrum)
Copy your RPC URLs from the dashboard
```

Get HuggingFace Token
Visit https://huggingface.co/settings/tokens

🧠 MCP Claude Integration Setup

1. Enable Developer Mode in Claude Desktop
   Go to Claude Desktop > Settings > Developer Mode

2. Find Claude Config Path
   Try the /balance endpoint by entering:

   - 🪟 Windows:

   ```
   code $env:AppData\Claude\claude_desktop_config.json
   ```

   - 🍎 macOS / 🐧 Linux:

   ```
   code ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

3. Add MCP Server Config
   Paste this inside the "mcpServers" object in your claude_desktop_config.json:

- Example for Windows:

```
{
  "mcpServers": {
    "eth_balance": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/ABSOLUTE/PATH/TO/eth_balance_mcp",
        "run",
        "eth_balance_server.py"
      ],
      "description": "Real-time crypto balances & AI risk analysis"
    }
  }
}
```

- Example for macOS/Linux:

```
{
  "mcpServers": {
    "eth_balance": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/eth_balance_mcp",
        "run",
        "eth_balance_server.py"
      ],
      "description": "Real-time crypto balances & AI risk analysis"
    }
  }
}
```

---

## ✅ Adjust the path to where you cloned the repo on your machine.

# ▶️ Run the MCP Server

```
uv --directory /PATH/TO/eth_balance_mcp run eth_balance_server.py
# or
python eth_balance_server.py
```

Claude will now auto-detect the eth_balance MCP server and expose:

🔹 @eth_balance.get_wallet_balance(address, chain)
Get native token balance of a wallet across:

ethereum

polygon

arbitrum

(optional) solana

# How To Prompt Claude

```
check safety for eth address 0x742d35C....

get balance for sol address 5J6L4Z7Vz9cR8KfT...
```

### chain: ethereum, polygon, arbitrum or solana (default is ethereum)

---

> Made for **Explore AI x Web3 with DeMCP — The MCP Side Track**  
> by **KORRA03**
