"""Texture manager for caching and managing image resources."""

from app.core.canvas import Canvas
from app.core.texture import Texture


class TextureManager:
    """Registry and cache for game textures."""

    def __init__(self, canvas: Canvas) -> None:
        self._canvas = canvas
        self._cache: dict[str, Texture] = {}

    def get(self, path: str) -> Texture:
        """Return cached texture, loading via canvas if not yet present."""
        if path not in self._cache:
            self._cache[path] = self._canvas.load_texture(path)
        return self._cache[path]

    def preload(self, *paths: str) -> None:
        """Explicitly load textures into cache."""
        for path in paths:
            self.get(path)

    def clear(self) -> None:
        """Evict all textures from cache."""
        self._cache.clear()

    def __contains__(self, path: str) -> bool:
        """Check if texture is already loaded into cache."""
        return path in self._cache

    def __len__(self) -> int:
        """Return number of currently cached textures."""
        return len(self._cache)
