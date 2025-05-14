from flask import Flask, request, jsonify
from flask_cors import CORS
import ast

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask backend running!"})

@app.route("/parse", methods=["POST"])
def parse_code():
    data = request.json
    code = data.get("code", "")
    language = data.get("language", "python")

    if not code:
        return jsonify({"error": "No code provided"}), 400

    parsed_steps = []

    try:
        if language.lower() == "python":
            parsed = ast.parse(code)

            for node in ast.walk(parsed):
                if isinstance(node, ast.Assign):
                    parsed_steps.append("Initialize variable")
                elif isinstance(node, ast.For):
                    parsed_steps.append("Start a for loop")
                elif isinstance(node, ast.While):
                    parsed_steps.append("Start a while loop")
                elif isinstance(node, ast.If):
                    parsed_steps.append("If condition check")
                elif isinstance(node, ast.FunctionDef):
                    parsed_steps.append(f"Define function: {node.name}")
                elif isinstance(node, ast.Call):
                    parsed_steps.append("Function call")

            if not parsed_steps:
                parsed_steps.append("No major steps detected.")
        else:
            # For C++/Java/JS -> if not Python, just return a default
            parsed_steps.append("Code parsing not supported for this language without AI.")
            parsed_steps.append("Showing default flow.")

        return jsonify({"steps": parsed_steps})
    except Exception as e:
        print("Error parsing code:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
