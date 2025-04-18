from flask import Flask, request, jsonify
from part_lookup import SQLiteManager, DB_PATH
from api_client import query_model

app = Flask(__name__)
db_manager = SQLiteManager(DB_PATH)

@app.route("/diagnose", methods=["POST"])
def diagnose():
    data = request.json
    issue = data.get("issue")
    model_url = data.get("model_url", "http://localhost:1234/v1")
    api_key = data.get("api_key")
    if not issue:
        return jsonify({"error": "Missing issue"}), 400
    response = query_model(
        f"HVAC Technician: Diagnose this issue and provide detailed troubleshooting steps.\n\nIssue: {issue}",
        model_url,
        api_key
    )
    return jsonify({"diagnosis": response})

@app.route("/find_part/<oem_number>", methods=["GET"])
def find_part(oem_number):
    part = db_manager.search_part(oem_number)
    if part:
        return jsonify(part)
    else:
        return jsonify({"error": "Part not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)