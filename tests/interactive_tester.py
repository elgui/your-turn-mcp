import asyncio
import json
import os
import sys
from typing import Optional

# This tester runs the container and drives MCP over stdin/stdout to validate behaviors

REQ_INIT = {"jsonrpc": "2.0", "id": 0, "method": "initialize"}

CALL_TEMPLATE = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
        "name": "your_turn",
        "arguments": {
            "reason": "TEST: please reply 'X'"
        }
    }
}

async def run_once(reason: str, token: str, chat: str, timeout: int = 35) -> dict:
    import subprocess
    call = json.loads(json.dumps(CALL_TEMPLATE))
    call["params"]["arguments"]["reason"] = reason
    lines = [json.dumps(REQ_INIT), json.dumps(call)]
    env = os.environ.copy()
    env["TELEGRAM_BOT_TOKEN"] = token
    env["TELEGRAM_CHAT_ID"] = chat

    proc = await asyncio.create_subprocess_exec(
        "docker", "run", "--rm", "-i", "--network", "host",
        "your-turn-server",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env
    )
    await proc.stdin.write("\n".join(lines).encode()+b"\n")
    await proc.stdin.drain()
    proc.stdin.close()
    out, err = await proc.communicate()
    return {"code": proc.returncode, "stdout": out.decode(), "stderr": err.decode()}

async def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        print("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in env", file=sys.stderr)
        sys.exit(2)

    # 1) Custom typed reply path
    print("[TEST] Custom typed reply (type 'alpha' in Telegram)")
    res = await run_once("TEST custom reply: type 'alpha'", token, chat)
    print("STDOUT:\n", res["stdout"][:500])
    assert 'User Response' in res["stdout"], "No user response captured"
    assert 'alpha' in res["stdout"] or 'ALPHA' in res["stdout"], res["stdout"]

    # 2) Prewritten button path (ensure only button text used)
    print("[TEST] Prewritten reply (click a prewritten button)")
    res2 = await run_once("TEST prewritten: click a button", token, chat)
    print("STDOUT:\n", res2["stdout"][:500])
    assert 'User Response' in res2["stdout"], "No user response captured for prewritten"

if __name__ == "__main__":
    asyncio.run(main())

