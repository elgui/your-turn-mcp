import json
import sys

# Test basic stdin/stdout communication
print("Testing stdin/stdout communication", file=sys.stderr)

# Read a line from stdin
try:
    line = input()
    print(f"Received: {line}", file=sys.stderr)
    
    # Try to parse as JSON
    try:
        request = json.loads(line)
        print(f"Parsed JSON: {request}", file=sys.stderr)
        
        # Send a response
        response = {
            "jsonrpc": "2.0",
            "id": request.get("id", 1),
            "result": {"message": "Test response"}
        }
        
        print(json.dumps(response), flush=True)
        print("Response sent", file=sys.stderr)
        
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        
except EOFError:
    print("No input received", file=sys.stderr)
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
