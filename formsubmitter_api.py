from flask import Flask, request, jsonify, Response
import logging
from typing import Tuple, Union

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger()

# Type alias for the return type of the Flask view functions
FlaskResponse = Union[Response, Tuple[Response, int]]


@app.route("/submit", methods=["POST"])
def submit() -> FlaskResponse:
    """
    Example endpoint for submitting data via POST.
    Expects JSON payload.
    """
    try:
        # Parse the incoming JSON data
        data = request.get_json()

        if not data:
            logger.warning("No data provided in the request.")
            return jsonify({"error": "No data provided"}), 400

        # Log the received data
        logger.info(f"Received data: {data}")

        # Do something with the data (e.g., save to a database, process it, etc.)
        # In this example, we will just respond with the received data
        return jsonify({"message": "Data received successfully", "data": data}), 200

    except Exception as e:
        logger.error(f"Error while processing request: {e}")
        return jsonify({"error": "An internal error occurred"}), 500


@app.route("/health", methods=["GET"])
def health_check() -> FlaskResponse:
    """Endpoint for Docker Healthcheck"""
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
