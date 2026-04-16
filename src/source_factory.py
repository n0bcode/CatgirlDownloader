from .catgirl import CatgirlDownloaderAPI
from .waifu import WaifuDownloaderAPI
from .danbooru import DanbooruDownloaderAPI


class SourceFactory:
    SOURCES = {
        "catgirl": CatgirlDownloaderAPI,
        "waifu": WaifuDownloaderAPI,
        "danbooru": DanbooruDownloaderAPI,
    }

    @classmethod
    def create(cls, source_id: str, settings=None):
        source_class = cls.SOURCES.get(source_id)
        if source_class:
            return source_class(settings=settings)
        return None

    @classmethod
    def get_source_ids(cls):
        return list(cls.SOURCES.keys())

    @classmethod
    def check_conflict(cls, source_id: str, settings):
        if source_id == "danbooru":
            api = cls.create(source_id, settings)
            if api:
                search_tags = settings.get_preference("danbooru_tags") or ""
                return api.check_search_blacklist_conflict(search_tags)
        return []
