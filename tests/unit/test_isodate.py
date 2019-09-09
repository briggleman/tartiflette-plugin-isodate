import pytest


@pytest.mark.asyncio
async def test_isodate_bake():
    from tartiflette_plugin_isodatenow import bake, _SDL

    assert await bake("a", {}) == _SDL
