from flask import Flask, request, jsonify
import ast
from executor import execute_script

app = Flask(__name__)

@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()
    
    # Basic validation
    if not data or "script" not in data:
        return jsonify({"error": "Missing 'script' in request body"}), 400

    script = data["script"]
    if not isinstance(script, str) or not script.strip():
        return jsonify({"error": "'script' must be a non-empty string"}), 400
    try:
        tree = ast.parse(script)
    except SyntaxError as e:
        return jsonify({"error": f"Syntax error in script: {e}"}), 400

    has_main = any(
        isinstance(node, ast.FunctionDef) and node.name == "main"
        for node in tree.body
    )
    if not has_main:
        return jsonify({"error": "Script must define a function named main()"}), 400
    try:
        result = execute_script(script)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
