"""
This is a simple Flask web service that provides two endpoints:

1. `/submit`: Accepts POST requests with JSON payloads to process data and send it as an email.
2. `/health`: A GET endpoint for health checks, useful for Docker or uptime monitoring.

## Features:
- Sends email notifications using an SMTP server.
- Logs all requests and errors for easy debugging.
- Environment variables are used to configure the SMTP server and recipient email.

### Environment Variables:
- `SMTP_SERVER`: SMTP server address (default: smtp.example.com).
- `SMTP_PORT`: Port for the SMTP server (default: 587).
- `SMTP_USERNAME`: Username for SMTP authentication (default: mail@example.com).
- `SMTP_PASSWORD`: Password for SMTP authentication (default: password).
- `SMTP_TIMEOUT`: Timeout for SMTP connections in seconds (default: 10).
- `TO_EMAIL`: The recipient email address (default: mail@example.com).

### Example cURL Request to `/submit`:

```bash
curl -X POST http://localhost:5000/submit \
-H "Content-Type: application/json" \
-d '{"email": "test@test.com", "name": "John Doe", "text": "This is a test message."}'
```

### Endpoints:
1. `/submit` (POST):
   - Accepts JSON data with `email`, `name`, and `text` fields.
   - Sends the data as an email to the configured recipient.

2. `/health` (GET):
   - Returns a basic health check response.
"""

from flask import Flask, request, jsonify, Response
import logging
from typing import Tuple, Union
import smtplib
import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger()

# Type alias for the return type of the Flask view functions
FlaskResponse = Union[Response, Tuple[Response, int]]

SMTP_SERVER: str = str(os.getenv("SMTP_SERVER", "smtp.example.com"))
SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME: str = str(os.getenv("SMTP_USERNAME", "mail@example.com"))
SMTP_PASSWORD: str = str(os.getenv("SMTP_PASSWORD", "password"))
SMTP_TIMEOUT: int = int(os.getenv("SMTP_TIMEOUT", 10))
TO_EMAIL: str = str(os.getenv("TO_EMAIL", "mail@example.com"))


def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Send an email using the configured SMTP server.

    Args:
        to_email (str): Recipient email address.
        subject (str): Subject of the email.
        body (str): Body of the email (can be plain text or JSON).

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        from_email = SMTP_USERNAME

        if isinstance(body, dict):
            # logger.info(f"Body is a dict, converting to string: {body}")
            body = json.dumps(body)  # Convert dict to string if necessary

        # Create the email
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        # Attach the email body
        msg.attach(MIMEText(body, "plain"))

        # Set up the SMTP server connection using a context manager
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=SMTP_TIMEOUT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(from_email, to_email, msg.as_string())

        logger.info(f"Email sent successfully to {to_email}")
        return True
    except smtplib.SMTPException as smtp_error:
        logger.error(f"SMTP error occurred: {smtp_error}")
        return False
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False


@app.route("/submit", methods=["POST"])
def submit() -> Tuple[Response, int]:
    """
    Handle POST requests to submit data.

    Expects:
        - JSON payload in the request body with key-value pairs to be processed.

    Returns:
        Tuple[Response, int]:
        - 200 if data is successfully processed and email sent.
        - 400 if the request doesn't contain JSON data or if data is missing.
        - 500 if an internal error occurs.
    """
    try:
        # Check if the request contains JSON
        if not request.is_json:
            logger.warning("Request content type is not JSON.")
            return (
                jsonify({"error": "Invalid content type. Expected application/json"}),
                400,
            )

        data = request.get_json()

        if not data:
            logger.warning("No data provided in the request.")
            return jsonify({"error": "No data provided"}), 400

        # Log the received data
        logger.info(f"Received data: {json.dumps(data, indent=2)}")

        # Send the email
        if not send_email(TO_EMAIL, "Form Submission - milesguard.com", data):
            return jsonify({"error": "Failed to send email"}), 500

        return jsonify({"message": "Data received successfully", "data": data}), 200

    except json.JSONDecodeError:
        logger.error("Invalid JSON provided in the request.")
        return jsonify({"error": "Invalid JSON provided"}), 400
    except Exception as e:
        logger.error(f"Error while processing request: {e}")
        return jsonify({"error": "An internal error occurred"}), 500


@app.route("/health", methods=["GET"])
def health_check() -> FlaskResponse:
    """Endpoint for Docker Healthcheck"""
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
