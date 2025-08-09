#!/usr/bin/env python3
"""
MCP Docker Client Simulator

A standalone utility to simulate an MCP client speaking JSON-RPC 2.0 to the
Your-Turn MCP server inside Docker (stdin/stdout protocol).

Features:
- Sends properly formatted JSON-RPC requests via stdin
- Reads and parses JSON-RPC responses from stdout (one JSON per line)
- Works with your-turn 'your_turn' tool for interactive response via Telegram
- Clear logging of request/response cycle
- Two modes: 'reply' (you respond in Telegram), 'timeout' (wait 300s)

Usage examples:

  # Quick capability check
  python3 mcp_docker_client.py tools-list \
    --token "$TELEGRAM_BOT_TOKEN" --chat "$TELEGRAM_CHAT_ID"

  # Run full your_turn and wait for your reply in Telegram (press a button or type)
  python3 mcp_docker_client.py your-turn \
    --reason "End-to-end test" \
    --token "$TELEGRAM_BOT_TOKEN" --chat "$TELEGRAM_CHAT_ID" \
    --mode reply --max-wait 600

  # Run full your_turn and intentionally time out (300s)
  python3 mcp_docker_client.py your-turn \
    --reason "Timeout test" \
    --token "$TELEGRAM_BOT_TOKEN" --chat "$TELEGRAM_CHAT_ID" \
    --mode timeout --max-wait 620

Notes:
- The container must be run with -i for MCP stdin/stdout
- This tool runs the container for you using docker run
- All server logs go to stderr; JSON-RPC responses go to stdout
"""

import argparse
import json
import os
import sys
import time
import shlex
import subprocess
from typing import List, Optional, Tuple

DOCKER_IMAGE = os.getenv("YOUR_TURN_IMAGE", "your-turn-server")


def _run_docker_with_input(lines: List[str], token: Optional[str], chat: Optional[str], network_host: bool = True,
                           max_wait: int = 600) -> Tuple[int, str, str]:
    """Run docker container, feed JSON lines via stdin, capture stdout/stderr.

    Returns (exit_code, stdout_text, stderr_text)
    """
    env_args = []
    if token:
        env_args += ["-e", f"TELEGRAM_BOT_TOKEN={token}"]
    if chat:
        env_args += ["-e", f"TELEGRAM_CHAT_ID={chat}"]

    net_args = ["--network", "host"] if network_host else []

    cmd = [
        "docker", "run", "--rm", "-i",
        *net_args,
        *env_args,
        DOCKER_IMAGE,
    ]

    # Launch process
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,  # line buffered
    )

    try:
        # Write all request lines
        for line in lines:
            proc.stdin.write(line.rstrip("\n") + "\n")
            proc.stdin.flush()
        # Close stdin so server can exit after processing
        proc.stdin.close()
        # Avoid communicate() trying to flush a closed stdin
        proc.stdin = None

        # Non-blocking read loop with timeout
        start = time.time()
        stdout_chunks: List[str] = []
        stderr_chunks: List[str] = []
        while True:
            # Read one line from stdout if available
            if proc.stdout:
                out_line = proc.stdout.readline()
                if out_line:
                    stdout_chunks.append(out_line)
            if proc.stderr:
                err_line = proc.stderr.readline()
                if err_line:
                    stderr_chunks.append(err_line)

            if proc.poll() is not None:
                break

            if time.time() - start > max_wait:
                # Timed out waiting; kill the process and break
                proc.kill()
                break

            # small sleep to avoid busy loop
            time.sleep(0.05)

        # Collect remaining output
        try:
            so, se = proc.communicate(timeout=1)
            if so:
                stdout_chunks.append(so)
            if se:
                stderr_chunks.append(se)
        except subprocess.TimeoutExpired:
            pass

        exit_code = proc.returncode if proc.returncode is not None else -1
        return exit_code, "".join(stdout_chunks), "".join(stderr_chunks)
    finally:
        try:
            if proc.poll() is None:
                proc.kill()
        except Exception:
            pass


def _parse_json_lines(stdout_text: str) -> List[dict]:
    """Parse each non-empty line of stdout as JSON, return list of parsed dicts.
    Ignores lines that fail to parse.
    """
    results = []
    for line in stdout_text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            results.append(json.loads(line))
        except json.JSONDecodeError:
            # Leave a hint for debugging, but don't crash
            print(f"[CLIENT] ⚠️ Non-JSON line on stdout (ignored): {line[:120]}", file=sys.stderr)
    return results


def cmd_tools_list(args: argparse.Namespace) -> int:
    lines = [
        json.dumps({"jsonrpc": "2.0", "id": 0, "method": "initialize"}),
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}),
    ]
    code, so, se = _run_docker_with_input(lines, args.token, args.chat, network_host=args.network_host, max_wait=args.max_wait)

    print("[CLIENT] --- STDERR (server logs) ---", file=sys.stderr)
    print(se, file=sys.stderr)
    print("[CLIENT] --- STDOUT (JSON-RPC) ---")
    print(so)

    parsed = _parse_json_lines(so)
    ok = any(obj.get("result", {}).get("tools") is not None for obj in parsed)
    return 0 if ok else 2


def cmd_your_turn(args: argparse.Namespace) -> int:
    # Build the your_turn call
    initialize = {"jsonrpc": "2.0", "id": 0, "method": "initialize"}
    call = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "your_turn",
            "arguments": {"reason": args.reason or "End-to-end test"}
        }
    }

    lines = [json.dumps(initialize), json.dumps(call)]

    print("[CLIENT] 🚀 Launching your-turn-server in Docker...", file=sys.stderr)
    print(f"[CLIENT]     Image: {DOCKER_IMAGE}", file=sys.stderr)
    print(f"[CLIENT]     Mode: {args.mode} | Max wait: {args.max_wait}s", file=sys.stderr)
    print("[CLIENT] 📤 Sending requests: initialize + tools/call(your_turn)", file=sys.stderr)
    print(f"[CLIENT] 📝 Reason: {call['params']['arguments']['reason']}", file=sys.stderr)

    if args.mode == "reply":
        print("[CLIENT] 📱 Please respond in Telegram (tap a quick button or type a message).", file=sys.stderr)
        print("[CLIENT]    The server will return immediately after your reply is received.", file=sys.stderr)
    else:
        print("[CLIENT] ⏳ Timeout test: do NOT reply; waiting up to 300s for timeout.", file=sys.stderr)

    code, so, se = _run_docker_with_input(lines, args.token, args.chat, network_host=args.network_host, max_wait=args.max_wait)

    print("[CLIENT] --- STDERR (server logs) ---", file=sys.stderr)
    print(se, file=sys.stderr)
    print("[CLIENT] --- STDOUT (JSON-RPC) ---")
    print(so)

    parsed = _parse_json_lines(so)
    # Find the response with id==2
    reply = next((obj for obj in parsed if obj.get("id") == 2), None)
    if not reply:
        print("[CLIENT] ❌ No reply with id=2 found on stdout.", file=sys.stderr)
        return 3

    if "result" in reply and reply["result"].get("content"):
        text = reply["result"]["content"][0].get("text", "")
        print("[CLIENT] ✅ Received JSON-RPC result for your_turn.", file=sys.stderr)
        print(f"[CLIENT] 🧾 First 200 chars: {text[:200].replace('\n',' ')}", file=sys.stderr)
        return 0
    elif "error" in reply:
        print(f"[CLIENT] ⚠️ Error response: {reply['error']}", file=sys.stderr)
        return 4
    else:
        print("[CLIENT] ❌ Unexpected response shape.", file=sys.stderr)
        return 5


def main() -> int:
    p = argparse.ArgumentParser(description="Standalone MCP client simulator for your-turn-server (Docker)")

    sub = p.add_subparsers(dest="command", required=True)

    # tools-list command
    p_list = sub.add_parser("tools-list", help="Send initialize and tools/list, print outputs")
    p_list.add_argument("--token", help="Telegram bot token", default=os.getenv("TELEGRAM_BOT_TOKEN"))
    p_list.add_argument("--chat", help="Telegram chat id", default=os.getenv("TELEGRAM_CHAT_ID"))
    p_list.add_argument("--no-network-host", action="store_true", help="Do not pass --network host to Docker")
    p_list.add_argument("--max-wait", type=int, default=30, help="Max seconds to wait for container to finish")
    p_list.set_defaults(func=cmd_tools_list)

    # your-turn command
    p_run = sub.add_parser("your-turn", help="Send your_turn tool call. Use --mode reply or timeout.")
    p_run.add_argument("--reason", default="End-to-end test", help="Reason passed to the your_turn tool")
    p_run.add_argument("--mode", choices=["reply", "timeout"], default="reply", help="Select test scenario")
    p_run.add_argument("--token", help="Telegram bot token", default=os.getenv("TELEGRAM_BOT_TOKEN"))
    p_run.add_argument("--chat", help="Telegram chat id", default=os.getenv("TELEGRAM_CHAT_ID"))
    p_run.add_argument("--max-wait", type=int, default=600, help="Max seconds to wait for container to finish")
    p_run.add_argument("--no-network-host", action="store_true", help="Do not pass --network host to Docker")
    p_run.set_defaults(func=cmd_your_turn)

    args = p.parse_args()
    args.network_host = not args.no_network_host

    # Minimal validation
    if args.command in ("your-turn",) and (not args.token or not args.chat):
        print("[CLIENT] ❌ TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are required for your-turn tests.", file=sys.stderr)
        return 10

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

