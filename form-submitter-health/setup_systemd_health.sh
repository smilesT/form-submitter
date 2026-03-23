#!/usr/bin/bash
# Enable System Services for formsubmitterhealth

# Define the directory for system-level systemd services
SYSTEMD_SYSTEM_DIR="/etc/systemd/system"

# Ensure the systemd service directory exists
if [ ! -d "$SYSTEMD_SYSTEM_DIR" ]; then
    echo "Systemd directory $SYSTEMD_SYSTEM_DIR does not exist. Exiting."
    exit 1
fi

# Copy all service and timer files to the systemd system config directory
cp ./systemd-services/* "$SYSTEMD_SYSTEM_DIR" || {
    echo "Failed to copy files to $SYSTEMD_SYSTEM_DIR"
    exit 1
}

# Reload systemd to pick up new services and timers
systemctl daemon-reload || {
    echo "Failed to reload systemd daemon"
    exit 1
}

# Enable and start the formsubmitterhealth timer
systemctl enable formsubmitterhealth.timer || {
    echo "Failed to enable formsubmitterhealth.timer"
    exit 1
}
systemctl start formsubmitterhealth.timer || {
    echo "Failed to start formsubmitterhealth.timer"
    exit 1
}

echo "All services and timers have been enabled and started successfully."
