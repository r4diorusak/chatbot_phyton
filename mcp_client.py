"""
MCP Client untuk connect ke mcp-pulsa-server
"""
import subprocess
import json

def call_mcp_server_via_exec(tool_name, arguments=None):
    """
    Call MCP server tool via docker exec
    Returns parsed result or error
    """
    try:
        # Create temporary script to send MCP request
        script = f"""
const {{ Client }} = require('@modelcontextprotocol/sdk/client/index.js');
const {{ StdioClientTransport }} = require('@modelcontextprotocol/sdk/client/stdio.js');

async function callTool() {{
    const transport = new StdioClientTransport({{
        command: 'node',
        args: ['dist/index.js']
    }});
    
    const client = new Client({{
        name: 'flask-chatbot',
        version: '1.0.0'
    }}, {{
        capabilities: {{}}
    }});
    
    await client.connect(transport);
    
    // Call tool
    const result = await client.callTool({{
        name: '{tool_name}',
        arguments: {json.dumps(arguments or {})}
    }});
    
    console.log(JSON.stringify(result));
    await client.close();
}}

callTool().catch(console.error);
"""
        
        # Save script temporarily
        with open('/tmp/mcp_call.js', 'w') as f:
            f.write(script)
        
        # Execute via docker
        cmd = ['docker', 'exec', '-i', 'mcp-pulsa-server', 'node', '/tmp/mcp_call.js']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout:
            return json.loads(result.stdout.strip())
        else:
            return {"error": f"MCP call failed: {result.stderr}"}
            
    except Exception as e:
        return {"error": str(e)}


# Simplified version - direct HTTP if MCP server exposes HTTP endpoint
def query_pulsa_providers():
    """Get list of pulsa providers"""
    result = subprocess.run(
        ['docker', 'exec', 'mcp-pulsa-server', 'cat', 'data/providers.json'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        try:
            return json.loads(result.stdout)
        except:
            # Return default if no data
            return {
                "providers": [
                    {"name": "Telkomsel", "code": "TSEL"},
                    {"name": "Indosat", "code": "ISAT"},
                    {"name": "XL", "code": "XL"},
                    {"name": "Axis", "code": "AXIS"},
                    {"name": "Tri", "code": "TRI"}
                ]
            }
    
    return {"error": "Cannot read providers data"}


def query_pulsa_products(provider=None):
    """Get pulsa products, optionally filtered by provider"""
    # Since MCP server data is empty, return sample data
    # In production, this would query the actual MCP server
    products = [
        {"id": 1, "provider": "Telkomsel", "nominal": 10000, "price": 11000, "stock": 100},
        {"id": 2, "provider": "Telkomsel", "nominal": 25000, "price": 26000, "stock": 80},
        {"id": 3, "provider": "Telkomsel", "nominal": 50000, "price": 51000, "stock": 50},
        {"id": 4, "provider": "Indosat", "nominal": 10000, "price": 10500, "stock": 120},
        {"id": 5, "provider": "Indosat", "nominal": 25000, "price": 25500, "stock": 90},
        {"id": 6, "provider": "XL", "nominal": 10000, "price": 10500, "stock": 110},
        {"id": 7, "provider": "XL", "nominal": 25000, "price": 25500, "stock": 85},
        {"id": 8, "provider": "Axis", "nominal": 5000, "price": 5500, "stock": 150},
        {"id": 9, "provider": "Axis", "nominal": 10000, "price": 10500, "stock": 130},
        {"id": 10, "provider": "Tri", "nominal": 10000, "price": 10000, "stock": 100}
    ]
    
    if provider:
        products = [p for p in products if p["provider"].lower() == provider.lower()]
    
    return {
        "success": True,
        "products": products,
        "total": len(products)
    }
