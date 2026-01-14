"""Common fixtures for the Ouman EH-800 tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest

pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> None:
    """Enable custom integrations for all tests."""
    return


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
        "custom_components.ouman_eh_800.async_setup_entry", return_value=True
    ) as mock_setup_entry:
        yield mock_setup_entry
