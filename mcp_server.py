import sys
import json
from client import DominatorTree

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "compute_dominators",
                        "description": "Calculate dominators and immediate dominators for directed control-flow graph",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "num_nodes": {"type": "integer"},
                                "edges": {
                                    "type": "array",
                                    "items": {"type": "array", "items": {"type": "integer"}}
                                },
                                "root": {"type": "integer", "default": 0}
                            },
                            "required": ["num_nodes", "edges"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "compute_dominators":
            dt = DominatorTree(args["num_nodes"])
            for u, v in args["edges"]:
                dt.add_edge(u, v)
            dom, idom = dt.compute_dominators(root=args.get("root", 0))
            dom_serializable = {str(k): list(v) for k, v in dom.items()}
            idom_serializable = {str(k): v for k, v in idom.items()}
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"dominators": dom_serializable, "immediate_dominators": idom_serializable})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
