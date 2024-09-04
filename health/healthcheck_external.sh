#!/bin/bash

HEALTH_URL="https://flux.milesguard.com/health"
EMAIL="miles@milesguard.com"
DEBUG=1

# Function to send an alert email
# This function is responsible for sending an email when a health check fails.
# Params:
#   $1 - The status message that contains the details of the failure.
send_alert_email() {
    local status_message=$1
    echo "Sending alert: $status_message"
    /usr/sbin/sendmail --from=default -t $EMAIL <<EOF
Subject: Health Check Alert $1
EOF
}

# Function to check the health status of the service
# It fetches the status from the HEALTH_URL and validates the health.
# If the status is not 'healthy', it sends an alert email.
check_health() {
    local response
    response=$(curl -s "$HEALTH_URL")

    local timestamp
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")

    local status
    status=$(echo "$response" | jq -r '.status')

    if [[ "$status" == "healthy" ]]; then
        echo "[$timestamp] Health check passed. URL: $HEALTH_URL"
        if [[ $DEBUG -eq 1 ]]; then
            send_alert_email "[$timestamp] DEBUG: Health check passed. Status: $status. URL: $HEALTH_URL"
        fi
    else
        echo "[$timestamp] Health check FAILED. Status: $status. URL: $HEALTH_URL"
        send_alert_email "[$timestamp] Health check failed. Status: $status. URL: $HEALTH_URL"
    fi
}

check_health
