import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from unittest.mock import MagicMock, patch
from src.api_base import BaseDownloaderAPI
from src.types import NSFWOption


class MockDownloaderAPI(BaseDownloaderAPI):
    def get_image_url(self, nsfw_mode=NSFWOption.BLOCK_NSFW):
        return None

    def get_artist(self, info=None):
        return None

    def get_link(self, info=None):
        return None

    def get_filename_suggestion(self, extension=None, info=None):
        return "test"


class TestBaseDownloaderAPI:
    def setup_method(self):
        self.api = MockDownloaderAPI()

    def test_parse_blacklist_empty(self):
        self.api.blacklist_tags = ""
        result = self.api._parse_blacklist()
        assert result == []

    def test_parse_blacklist_single_tag(self):
        self.api.blacklist_tags = "tag1"
        result = self.api._parse_blacklist()
        assert result == ["tag1"]

    def test_parse_blacklist_multiple_tags(self):
        self.api.blacklist_tags = "tag1 tag2 tag3"
        result = self.api._parse_blacklist()
        assert result == ["tag1", "tag2", "tag3"]

    def test_parse_blacklist_with_spaces(self):
        self.api.blacklist_tags = "  tag1   tag2  "
        result = self.api._parse_blacklist()
        assert result == ["tag1", "tag2"]

    def test_parse_blacklist_lowercase(self):
        self.api.blacklist_tags = "TAG1 TaG2"
        result = self.api._parse_blacklist()
        assert result == ["tag1", "tag2"]

    def test_check_blacklist_match_no_blacklist(self):
        self.api.blacklist_tags = ""
        result = self.api._check_blacklist_match(["tag1", "tag2"])
        assert result == []

    def test_check_blacklist_match_no_match(self):
        self.api.blacklist_tags = "tag1 tag2"
        result = self.api._check_blacklist_match(["tag3", "tag4"])
        assert result == []

    def test_check_blacklist_match_single(self):
        self.api.blacklist_tags = "tag1"
        result = self.api._check_blacklist_match(["tag1", "tag2"])
        assert result == ["tag1"]

    def test_check_blacklist_match_multiple(self):
        self.api.blacklist_tags = "tag1 tag2"
        result = self.api._check_blacklist_match(["TAG1", "tag2", "tag3"])
        assert set(result) == {"tag1", "tag2"}

    def test_check_blacklist_match_case_insensitive(self):
        self.api.blacklist_tags = "tag1"
        result = self.api._check_blacklist_match(["TAG1"])
        assert result == ["tag1"]

    def test_get_filename_id_default(self):
        with patch("time.time", return_value=1234567890):
            result = self.api.get_filename_id()
            assert result == "1234567890"

    def test_get_filename_id_from_info_not_implemented(self):
        info = {"id": "abc123"}
        with patch("time.time", return_value=1234567890):
            result = self.api.get_filename_id(info)
            assert result == "1234567890"

    def test_get_filename_id_from_info_missing(self):
        info = {}
        with patch("time.time", return_value=1234567890):
            result = self.api.get_filename_id(info)
            assert result == "1234567890"

    def test_get_blacklist_tags(self):
        self.api.blacklist_tags = "test_tag"
        result = self.api.get_blacklist_tags()
        assert result == "test_tag"
