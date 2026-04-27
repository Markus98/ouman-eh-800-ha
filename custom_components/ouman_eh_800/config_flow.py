"""Config flow for the Ouman EH-800 integration."""

from __future__ import annotations

import logging
import uuid
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlowWithReload,
)
from homeassistant.const import CONF_PASSWORD, CONF_URL, CONF_USERNAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from ouman_eh_800_api import (
    OumanClientAuthenticationError,
    OumanClientCommunicationError,
    OumanEh800Client,
)

from .const import CONF_SCAN_INTERVAL_SECONDS, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL): str,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Optional(
            CONF_SCAN_INTERVAL_SECONDS, default=DEFAULT_SCAN_INTERVAL
        ): vol.All(vol.Coerce(int), vol.Range(min=5, max=300)),
    }
)


def _normalize_url(url: str) -> str:
    """Normalize URL by stripping whitespace, trailing slashes, and /eh800.html."""
    return url.strip().removesuffix("/").removesuffix("/eh800.html").removesuffix("/")


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> None:
    """Validate the user input allows us to connect and login.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    client = OumanEh800Client(
        session=async_get_clientsession(hass),
        username=data[CONF_USERNAME],
        password=data[CONF_PASSWORD],
        address=data[CONF_URL],
    )

    await client.login()


class OumanEh800ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ouman EH-800."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlowWithReload:
        """Get the options flow for this handler."""
        return OumanEh800OptionsFlow()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            user_input[CONF_URL] = _normalize_url(user_input[CONF_URL])
            try:
                await validate_input(self.hass, user_input)
            except OumanClientCommunicationError:
                errors["base"] = "cannot_connect"
            except OumanClientAuthenticationError:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                self._async_abort_entries_match({CONF_URL: user_input[CONF_URL]})
                _ = await self.async_set_unique_id(uuid.uuid4().hex)
                return self.async_create_entry(title="Ouman EH-800", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class OumanEh800OptionsFlow(OptionsFlowWithReload):
    """Handle options flow for Ouman EH-800."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                OPTIONS_SCHEMA, self.config_entry.options
            ),
        )
