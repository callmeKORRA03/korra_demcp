# eth_balance_server.py
import asyncio
import os
import logging
import httpx
from web3 import AsyncWeb3
from web3.providers import AsyncHTTPProvider
from solana.rpc.async_api import AsyncClient as SolClient
from solders.pubkey import Pubkey
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("EthBalanceMCP")

# Initialize MCP Server
mcp = FastMCP("eth_balance", protocol_version="2024-11-05")

# Load environment variables
load_dotenv()


async def initialize_blockchain_clients():
    """Initialize and verify all blockchain connections"""
    clients = {}
    try:
        # Ethereum-based chains
        chains = {
            'ethereum': os.getenv("ETH_RPC"),
            'polygon': os.getenv("POL_RPC"),
            'arbitrum': os.getenv("ARB_RPC")
        }

        for chain_name, rpc_url in chains.items():
            if not rpc_url:
                raise ValueError(f"Missing RPC URL for {chain_name}")

            provider = AsyncHTTPProvider(rpc_url)
            w3 = AsyncWeb3(provider)
            version = await w3.provider.make_request("web3_clientVersion", [])
            clients[chain_name] = w3
            logger.info(
                f"✅ Connected to {chain_name.upper()} node (Client: {version['result']})")

        # Solana
        sol_client = SolClient(
            "https://api.mainnet-beta.solana.com", timeout=30)
        logger.info("✅ Connected to SOLANA node")

        return clients
    except Exception as e:
        logger.critical(f"🔴 Blockchain connection failed: {str(e)}")
        raise


async def initialize_server():
    """Server startup sequence"""
    try:
        mcp.state.clients = await initialize_blockchain_clients()
        logger.info("🌐 All blockchain connections verified")
    except Exception as e:
        logger.error(f"💥 Critical initialization failure: {str(e)}")
        os._exit(1)


@mcp.tool()
async def get_wallet_balance(address: str, chain: str) -> dict:
    """Get cryptocurrency balance across supported chains"""
    try:
        chain = chain.lower()
        clients = mcp.state.clients

        if chain in ["eth", "ethereum"]:
            balance_wei = await clients['ethereum'].eth.get_balance(address)
            return {"chain": "Ethereum", "balance": float(AsyncWeb3.from_wei(balance_wei, "ether"))}

        elif chain in ["polygon", "matic"]:
            balance_wei = await clients['polygon'].eth.get_balance(address)
            return {"chain": "Polygon", "balance": float(AsyncWeb3.from_wei(balance_wei, "ether"))}

        elif chain == "arbitrum":
            balance_wei = await clients['arbitrum'].eth.get_balance(address)
            return {"chain": "Arbitrum", "balance": float(AsyncWeb3.from_wei(balance_wei, "ether"))}

        elif chain == "solana":
            pubkey = Pubkey.from_string(address)
            resp = await clients['solana'].get_balance(pubkey)
            return {"chain": "Solana", "balance": resp.value / 1e9}

        return {"error": "Unsupported chain"}

    except ValueError as e:
        logger.error(f"Invalid address: {str(e)}")
        return {"error": "Invalid wallet address"}
    except Exception as e:
        logger.error(f"Balance check failed: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
async def analyze_wallet_risk(address: str, chain: str) -> dict:
    """AI-powered wallet risk assessment using on-chain data"""
    try:
        # Get balance first
        balance_data = await get_wallet_balance(address, chain)
        if "error" in balance_data:
            return balance_data

        # Generate AI analysis
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://api-inference.huggingface.co/models/ProsusAI/finbert",
                headers={"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"},
                json={
                    "inputs": f"Analyze risk profile for {address} with {balance_data['balance']} {chain} balance"
                }
            )
            response.raise_for_status()
            results = response.json()

        return {
            "address": address,
            "chain": chain,
            "balance": balance_data["balance"],
            "risk_analysis": max(results, key=lambda x: x["score"])
        }

    except Exception as e:
        logger.error(f"Risk analysis failed: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    logger.info("🚀 Starting MCP Server: Crypto Balance Analyzer")
    try:
        # Run async initialization before starting server
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(initialize_blockchain_clients())
        mcp.run(transport="stdio")
        logger.info("🤖 Ready to receive Claude requests")
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.critical(f"💥 Fatal error: {str(e)}")
