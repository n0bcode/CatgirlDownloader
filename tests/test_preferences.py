import sys
import os
import json
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from unittest.mock import patch, MagicMock


class TestUserPreferences:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "config.json")

        self.defaults = {
            "nsfw_mode": "Block NSFW",
            "auto_reload_enabled": False,
            "auto_reload_interval": 5,
            "danbooru_tags": "",
            "blacklist_tags": "",
        }

        with patch(
            "gi.repository.GLib.get_user_config_dir", return_value=self.temp_dir
        ):
            with patch("os.makedirs"):
                with patch("builtins.open", create=True) as mock_open:
                    mock_file = MagicMock()
                    mock_open.return_value.__enter__.return_value = mock_file
                    mock_file.read.return_value = json.dumps(self.defaults)
                    mock_file.write = MagicMock()

                    from src.preferences import UserPreferences

                    self.PreferencesClass = UserPreferences

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_default_preferences(self):
        with patch(
            "gi.repository.GLib.get_user_config_dir", return_value=self.temp_dir
        ):
            with patch("os.makedirs"):
                with patch("builtins.open", create=True) as mock_open:
                    mock_file = MagicMock()
                    mock_open.return_value.__enter__.return_value = mock_file
                    mock_file.read.return_value = "{}"
                    mock_file.write = MagicMock()

                    prefs = self.PreferencesClass()
                    assert prefs.preferences.get("nsfw_mode") == "Block NSFW"
                    assert prefs.preferences.get("blacklist_tags") == ""

    def test_get_preference(self):
        with patch(
            "gi.repository.GLib.get_user_config_dir", return_value=self.temp_dir
        ):
            with patch("os.makedirs"):
                with patch("builtins.open", create=True) as mock_open:
                    mock_file = MagicMock()
                    mock_open.return_value.__enter__.return_value = mock_file
                    mock_file.read.return_value = json.dumps(self.defaults)
                    mock_file.write = MagicMock()

                    prefs = self.PreferencesClass()
                    prefs.file = self.temp_file
                    prefs.preferences = dict(self.defaults)

                    result = prefs.get_preference("nsfw_mode")
                    assert result == "Block NSFW"

    def test_set_preference(self):
        with patch(
            "gi.repository.GLib.get_user_config_dir", return_value=self.temp_dir
        ):
            with patch("os.makedirs"):
                with patch("builtins.open", create=True) as mock_open:
                    mock_file = MagicMock()
                    mock_open.return_value.__enter__.return_value = mock_file
                    mock_file.read.return_value = json.dumps(self.defaults)
                    mock_file.write = MagicMock()

                    prefs = self.PreferencesClass()
                    prefs.file = self.temp_file
                    prefs.preferences = dict(self.defaults)

                    prefs.set_preference("nsfw_mode", "Only NSFW")
                    assert prefs.preferences["nsfw_mode"] == "Only NSFW"
