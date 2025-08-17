from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)


# /help API endpoint
@app.route('/help', methods=['POST'])
# Handle POST requests to /help
def help():
    print("Received help request")
    # Convert Gemini API response to JSON format
    return jsonify({
        "status": "success",
        "answer": {
            "explanation": "Placeholder for result from Gemini API",
            "fileName": "ex.py",
            "codeSnippet": "Ex: print('Hello, World!')"
        }
    })


# Run app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
