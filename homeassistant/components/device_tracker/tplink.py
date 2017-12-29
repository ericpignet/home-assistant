"""
Support for TP-Link routers.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/device_tracker.tplink/
"""
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.device_tracker import (
    DOMAIN, PLATFORM_SCHEMA, DeviceScanner)
from homeassistant.const import (
    CONF_HOST, CONF_PASSWORD, CONF_USERNAME)

REQUIREMENTS = ['pytplinkrouter==0.1.0']

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})


def get_scanner(hass, config):
    """Validate the configuration and returns a TPLink scanner."""
    info = config[DOMAIN]
    host = info.get(CONF_HOST)
    username = info.get(CONF_USERNAME)
    password = info.get(CONF_PASSWORD)

    scanner = TPLinkDeviceScanner(host, username, password)

    return scanner if scanner.success_init else None


class TPLinkDeviceScanner(DeviceScanner):
    """Queries a TPLink wireless router."""

    def __init__(self, host, username, password):
        """Initialize the scanner."""
        import pytplinkrouter

        _LOGGER.info("Asking API to try logging in each type of router")
        self.success_init = False
        factory = pytplinkrouter.TPLinkRouterFactory(host, username, password)
        self._api = factory.get_router()

        if self._api is None:
            _LOGGER.error("Failed to Login")
            return

        results = self._api.scan_devices()

        if results is None:
            _LOGGER.error("Failed to find attached devices")
            return

        self.success_init = True

    def scan_devices(self):
        """Scan for new devices and return a list with found device IDs."""
        return self._api.scan_devices()

    def get_device_name(self, mac):
        """Return the name of the given device or None if we don't know."""
        return self._api.get_device_name(mac)
