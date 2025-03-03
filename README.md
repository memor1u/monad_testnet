# Monad Testnet Guide 🚀

Welcome to the **Monad Testnet**! This guide will help you set up a node, configure your wallet, and interact with the network.

## 🌐 What is Monad?
Monad is a high-performance blockchain designed for efficiency, scalability, and developer-friendly execution. The testnet allows developers to experiment with transactions, smart contracts, and network operations before mainnet deployment.

## 📌 Prerequisites
Before getting started, ensure you have:
- A Linux/macOS system (Ubuntu 20.04 recommended)
- At least **4 CPU cores, 8GB RAM, and 100GB SSD**
- Installed dependencies: `git`, `curl`, `jq`, `docker`, `docker-compose`

## 🛠️ Node Setup
Follow these steps to run a Monad testnet node:

### 1️⃣ Install Dependencies
```bash
sudo apt update && sudo apt install -y git curl jq docker.io docker-compose
```

### 2️⃣ Clone Monad Repository
```bash
git clone https://github.com/monad-labs/monad.git
cd monad
```

### 3️⃣ Run the Node
```bash
docker-compose up -d
```
Check logs to verify:
```bash
docker logs -f monad-node
```

## 🔑 Wallet Setup
You can use MetaMask or a CLI wallet to interact with Monad Testnet.

### 🦊 Connect MetaMask
1. Open MetaMask and go to **Settings > Networks > Add Network**
2. Enter:
   - **Network Name:** Monad Testnet
   - **RPC URL:** `https://testnet-rpc.monad.io`
   - **Chain ID:** `999`
   - **Currency Symbol:** `MONA`
   - **Explorer URL:** `https://testnet-explorer.monad.io`
3. Save and switch to Monad Testnet.

### 🔄 Get Test Tokens
Use the Monad Faucet to receive test MONA:
```bash
curl -X POST https://testnet-faucet.monad.io/request -d '{"address": "YOUR_WALLET_ADDRESS"}'
```

## 📜 Interact with Monad Testnet
### Send a Transaction
```bash
monad-cli tx send --to <recipient_address> --amount 10MONA --gas auto --fees 0.01MONA
```

### Check Account Balance
```bash
monad-cli query balance <your_address>
```

## 🚀 Additional Resources
- [Monad Docs](https://docs.monad.io)
- [Testnet Explorer](https://testnet-explorer.monad.io)
- [Discord Community](https://discord.gg/monad)

Happy testing on Monad Testnet! 🎉

