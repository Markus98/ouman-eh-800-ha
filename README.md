> [!IMPORTANT]
> This custom integration has been superseded by the [official Ouman EH-800 Home Assistant integration](https://www.home-assistant.io/integrations/ouman_eh_800/). Please migrate to the official integration to receive future updates and support.

> [!WARNING]
> Migrating from this custom integration to the official integration will not migrate existing entities. New entities will be created instead.

# Ouman EH-800 Home Assistant Integration

Home Assistant integration for the [Ouman EH-800 heating controller](https://ouman.fi/en/product/ouman-eh-800-and-eh-800b/).

The Ouman EH-800 is a heating controller used for controlling water-based central heating systems. It supports up to two heating circuits (L1 and L2) with control curves based on outside temperature. This integration allows you to monitor and control your EH-800 device directly from Home Assistant over your local network.

## Features

This integration provides the following entities:

### Sensors
- Outside temperature
- Supply water temperatures and setpoints
- Room temperatures and setpoints (if room sensor is installed)
- Valve positions
- Circuit status information

### Numbers (Controls)
- Heating curve temperatures (-20°C, 0°C, +20°C points)
- Temperature drop settings
- Room temperature fine tuning
- Water out min/max temperatures
- Manual valve position control

### Selects (Controls)
- Home/Away mode
- L1/L2 operation modes (Automatic, Temperature drop, Big temperature drop, Normal temperature, Shutdown, Manual valve control)

## Supported Devices

- **Ouman EH-800**

> [!WARNING]
> **Ouman EH-800B is not supported** as it does not have network connectivity.

## Data Updates

This integration polls your Ouman EH-800 device over the local network at a configurable interval (default: 60 seconds). You can adjust the polling frequency in the integration options from 5 to 300 seconds.

## Known Limitations

- **Single device per entry**: Each integration entry connects to one EH-800 device; add multiple entries for multiple devices
- **Unverified features**: L2 (second heating circuit) and room sensor functionality have not been verified due to lack of test hardware
- **Local network only**: The device must be reachable on your local network

> [!CAUTION]
> **Security Warning**: The EH-800 uses an unencrypted HTTP connection and does not adhere to modern cybersecurity standards. While it is technically possible to expose the device to the internet via port forwarding, this is **highly insecure** and strongly discouraged. Keep the device on your local network only and access it remotely through secure methods like a VPN.

## Prerequisites

- Ouman EH-800 heating controller
- The device must be configured with a reachable IP address, subnet mask, and username/password (see the device manual for setup instructions)
- The device's web interface (`http://<ip_address>:<port>`) must be reachable from Home Assistant

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click the three dots menu in the top right corner
3. Select "Custom repositories"
4. Add `https://github.com/Markus98/ouman-eh-800-ha` as a custom repository with category "Integration"
5. Click "Add"
6. Search for "Ouman EH-800" in HACS and install it
7. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [GitHub releases page](https://github.com/Markus98/ouman-eh-800-ha/releases)
2. Extract the `custom_components/ouman_eh_800` folder to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings** > **Devices & Services**
2. Click **Add Integration**
3. Search for "Ouman EH-800"
4. Enter the following information:
   - **URL**: The URL of your Ouman EH-800 web interface (e.g., `http://192.168.1.100`)
   - **Username**: Your device username
   - **Password**: Your device password
5. Click **Submit**

### Options

After installation, you can configure the following options:

- **Polling interval**: How often to poll the device for updates (default: 60 seconds, range: 5-300 seconds)

## Removal

This integration follows standard integration removal. To remove the integration:

1. Go to **Settings** > **Devices & Services**
2. Find the "Ouman EH-800" integration
3. Click the three dots menu
4. Select **Delete**

This will remove the integration and all associated entities from Home Assistant. No changes are made to your Ouman EH-800 device.
