# app.py
import os
import sys
import json
import time
import argparse
from datetime import datetime
from web3 import Web3

DEFAULT_RPC = os.environ.get("RPC_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_KEY")

def get_latest_blocks(w3: Web3, count: int) -> list:
    """
    Fetches the latest N blocks and returns key info for each.
    """
    latest = w3.eth.block_number
    blocks = []
    for i in range(latest, latest - count, -1):
        block = w3.eth.get_block(i)
        blocks.append({
            "number": block.number,
            "timestamp": block.timestamp,
            "tx_count": len(block.transactions),
            "gas_used": block.gasUsed,
            "miner": block.miner,
            "hash": block.hash.hex(),
        })
    return blocks

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="zk-latestblocks-soundness — retrieves recent blocks and checks temporal soundness and miner diversity."
    )
    p.add_argument("--rpc", default=DEFAULT_RPC, help="EVM-compatible RPC URL (default from RPC_URL)")
    p.add_argument("--count", type=int, default=10, help="Number of recent blocks to analyze (default: 10)")
    p.add_argument("--json", action="store_true", help="Output results in JSON format")
    p.add_argument("--timeout", type=int, default=30, help="RPC timeout in seconds (default: 30)")
    return p.parse_args()

def analyze_soundness(blocks: list) -> dict:
    if not blocks:
        return {"ok": False, "message": "No blocks fetched"}
    timestamps = [b["timestamp"] for b in blocks]
    deltas = [timestamps[i] - timestamps[i + 1] for i in range(len(timestamps) - 1)]
    avg_time = sum(deltas) / len(deltas)
    miners = {b["miner"] for b in blocks}
    diversity = len(miners)
    ok = avg_time < 20 and diversity > 1
    return {
        "average_block_time": round(avg_time, 2),
        "miner_diversity": diversity,
        "block_count": len(blocks),
        "soundness_ok": ok,
        "message": (
            "✅ Sound network: stable block times and miner diversity."
            if ok else "⚠️ Potential anomaly: unstable block interval or low miner diversity."
        )
    }

def main() -> None:
    args = parse_args()
    w3 = Web3(Web3.HTTPProvider(args.rpc, request_kwargs={"timeout": args.timeout}))
    if not w3.is_connected():
        print("❌ RPC connection failed. Check your RPC_URL or --rpc parameter.")
        sys.exit(1)

    print("🔧 zk-latestblocks-soundness")
    print(f"🔗 RPC: {args.rpc}")
    print(f"🧱 Fetching {args.count} latest blocks...")

    start = time.time()
    try:
        blocks = get_latest_blocks(w3, args.count)
    except Exception as e:
        print(f"❌ Error fetching blocks: {e}")
        sys.exit(2)

    results = analyze_soundness(blocks)
    timestamp = datetime.utcnow().isoformat() + "Z"

    print(f"🕒 Timestamp: {timestamp}")
    print(f"📊 Average Block Time: {results['average_block_time']}s")
    print(f"👷 Miner Diversity: {results['miner_diversity']}")
    print(f"📦 Blocks Analyzed: {results['block_count']}")
    print(results["message"])

    elapsed = round(time.time() - start, 2)
    print(f"⏱️ Completed in {elapsed:.2f}s")

    if args.json:
        output = {
            "rpc": args.rpc,
            "timestamp_utc": timestamp,
            "results": results,
            "elapsed_seconds": elapsed,
            "blocks": blocks
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))

    sys.exit(0 if results["soundness_ok"] else 2)

if __name__ == "__main__":
    main()
