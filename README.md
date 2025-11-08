# zk-latestblocks-soundness

## Overview
**zk-latestblocks-soundness** is a lightweight tool that checks **block timing soundness** and **miner diversity** across the most recent blocks in an EVM chain.  
This tool helps developers, researchers, and rollup operators (Aztec, Zama, etc.) ensure network stability and detect anomalies in block production.

## Features
- ⏱️ Compute average block time over N latest blocks  
- 👷 Assess miner diversity for decentralization  
- 📦 Report transaction count and gas usage per block  
- 🧩 Detect anomalies (high latency or single-miner dominance)  
- 🌍 Works with any EVM RPC endpoint  
- 💾 JSON output for CI/CD pipelines  

## Installation
1. Requires Python 3.9+  
2. Install dependencies:
   pip install web3
3. Optionally set your RPC endpoint:
   export RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY

## Usage
Analyze last 10 blocks:
   python app.py --count 10

Check 50 blocks for consistency:
   python app.py --count 50

Use custom RPC:
   python app.py --rpc https://arb1.arbitrum.io/rpc --count 20

Output results as JSON:
   python app.py --count 10 --json

Increase timeout for slow RPCs:
   python app.py --count 10 --timeout 60

## Example Output
🧱 Fetching 10 latest blocks...  
🕒 Timestamp: 2025-11-08T17:42:10Z  
📊 Average Block Time: 12.4s  
👷 Miner Diversity: 8  
📦 Blocks Analyzed: 10  
✅ Sound network: stable block times and miner diversity.  
⏱️ Completed in 0.64s  

### Example JSON Output
{
  "rpc": "https://mainnet.infura.io/v3/YOUR_KEY",
  "timestamp_utc": "2025-11-08T17:42:10Z",
  "results": {
    "average_block_time": 12.4,
    "miner_diversity": 8,
    "block_count": 10,
    "soundness_ok": true,
    "message": "✅ Sound network: stable block times and miner diversity."
  },
  "elapsed_seconds": 0.64
}

## Notes
- **Soundness Criterion:** A sound network has consistent block intervals (< 20s average) and more than one unique miner.  
- **Anomalies:** Large timing gaps or single-miner dominance may indicate network issues, censorship, or validator centralization.  
- **ZK Relevance:** Reliable block timing improves determinism and scheduling in zk-proof systems.  
- **Use Cases:** network health monitoring, testnet verification, miner activity tracking.  
- **Exit Codes:**  
  `0` → Sound network  
  `2` → Detected anomaly or RPC error.  
