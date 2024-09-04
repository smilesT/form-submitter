#!/bin/bash

# URL to check the health status
HEALTH_URL="https://flux.milesguard.com/health"

# Function to send email (you can define this later)
send_alert_email() {
    local status_message=$1
    # Replace the below line with your actual mail function
    echo "Sending alert: $status_message"
    # Example of a mail function you can add later:
    # echo "$status_message" | mail -s "Health Check Alert" recipient@example.com
}

# Check the health status
check_health() {
    response=$(curl -s $HEALTH_URL)

    # Extract the status field from the JSON response
    status=$(echo $response | grep -o '"status":"[^"]*' | grep -o '[^"]*$')

    if [[ "$status" == "healthy" ]]; then
        echo "System is healthy."
    else
        echo "System is NOT healthy! Status: $status"
        # Send an alert if not healthy
        send_alert_email "System health check failed. Status: $status"
    fi
}

# Run the health check
check_health
