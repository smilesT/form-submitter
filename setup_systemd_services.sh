#!/usr/bin/bash
# Enable User Services for Docker Compose

# Define the directory for user-level systemd services
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

# Ensure the directory exists
mkdir -p "$SYSTEMD_USER_DIR"

# Copy all service and timer files from the systemd-services directory to the systemd user config directory
cp systemd-services/* "$SYSTEMD_USER_DIR" || {
    echo "Failed to copy files to $SYSTEMD_USER_DIR"
    exit 1
}

# List of services to enable and start
services=("formsubmitter")

# Loop through each service and enable/start it
for service in "${services[@]}"; do
    systemctl --user enable "${service}.service"
    systemctl --user restart "${service}.service"
    systemctl --user status "${service}.service"
done

echo "All services and timers have been enabled and started successfully."
