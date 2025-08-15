from flask import Flask, request, jsonify
from flask_cors import CORS
from generate_text import generate_text  # Import the function to generate text from your trained LLM

# Initialize Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) to allow frontend requests
CORS(app)

# Define route for generating AI response
@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        # Parse the JSON data from the request
        data = request.json
        user_input = data.get('message')

        # Validate the input
        if not user_input:
            return jsonify({"error": "Message is required"}), 400

        # Generate response using the trained LLM
        response = generate_text(user_input)

        # Return the generated response as JSON
        return jsonify({"reply": response})

    except Exception as e:
        # Handle errors and return a generic error message
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)