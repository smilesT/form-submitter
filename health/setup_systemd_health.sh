#!/usr/bin/bash
# Enable User Services for Docker Compose

# Define the directory for user-level systemd services
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

# Ensure the directory exists
mkdir -p "$SYSTEMD_USER_DIR"

# Copy all service and timer files from the systemd-services directory to the systemd user config directory
cp systemd-health/* "$SYSTEMD_USER_DIR" || {
    echo "Failed to copy files to $SYSTEMD_USER_DIR"
    exit 1
}

# Enable and start the watchtower timer
systemctl --user enable formsubmitterhealth.timer || {
    echo "Failed to enable watchtower.timer"
    exit 1
}
systemctl --user start formsubmitterhealth.timer || {
    echo "Failed to start watchtower.timer"
    exit 1
}

echo "All services and timers have been enabled and started successfully."
