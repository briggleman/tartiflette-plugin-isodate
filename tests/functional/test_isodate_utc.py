import asyncio
import pytest

from unittest.mock import Mock
from tartiflette import Resolver, create_engine
from freezegun import freeze_time


@freeze_time("2019-09-04T13:49:12.585158", tz_offset=0)
@pytest.mark.asyncio
async def test_isodate_defaults():
    logger = Mock()
    logger.debug = Mock()

    @Resolver("Query.createdAt", schema_name="test_isodate_defaults")
    async def created_at_resolver(*_args, **_kwargs):
        return {}

    @Resolver("ISODate.date", schema_name="test_isodate_defaults")
    async def created_at_date_resolver(*_args, **_kwargs):
        await asyncio.sleep(0.100)
        return "OVERWRITTEN"

    engine = await create_engine(
        sdl="""
        type ISODate {
            date: String @isoDate
        }
        type Query {
            createdAt: ISODate
        }
        """,
        modules=[
            {
                "name": "tartiflette_plugin_isodate",
                "config": {}
            }
        ],
        schema_name="test_isodate_defaults",
    )
    
    assert await engine.execute("query a { createdAt { date } } ") == {
        "data": {"createdAt": {"date": "2019-09-04T13:49:12.585158+00:00"}}
    }


@freeze_time("2019-09-04T13:49:12", tz_offset=0)
@pytest.mark.asyncio
async def test_isodate_no_microseconds():
    logger = Mock()
    logger.debug = Mock()

    @Resolver("Query.createdAt", schema_name="test_isodate_no_microseconds")
    async def created_at_resolver(*_args, **_kwargs):
        return {}

    @Resolver("ISODate.date", schema_name="test_isodate_no_microseconds")
    async def created_at_date_resolver(*_args, **_kwargs):
        await asyncio.sleep(0.100)
        return "OVERWRITTEN"

    engine = await create_engine(
        sdl="""
        type ISODate {
            date: String @isoDate(microseconds: false)
        }
        type Query {
            createdAt: ISODate
        }
        """,
        modules=[
            {
                "name": "tartiflette_plugin_isodate",
                "config": {},
            }
        ],
        schema_name="test_isodate_no_microseconds",
    )

    assert await engine.execute("query a { createdAt { date } } ") == {
        "data": {"createdAt": {"date": "2019-09-04T13:49:12+00:00"}}
    }


@freeze_time("2019-09-04T13:49:12.585158")
@pytest.mark.asyncio
async def test_isodate_no_timezone():
    logger = Mock()
    logger.debug = Mock()

    @Resolver("Query.createdAt", schema_name="test_isodate_no_timzone")
    async def created_at_resolver(*_args, **_kwargs):
        return {}

    @Resolver("ISODate.date", schema_name="test_isodate_no_timzone")
    async def created_at_date_resolver(*_args, **_kwargs):
        await asyncio.sleep(0.100)
        return "OVERWRITTEN"

    engine = await create_engine(
        sdl="""
        type ISODate {
            date: String @isoDate(timezone: false)
        }
        type Query {
            createdAt: ISODate
        }
        """,
        modules=[
            {
                "name": "tartiflette_plugin_isodate",
                "config": {}
            }
        ],
        schema_name="test_isodate_no_timzone",
    )
    
    assert await engine.execute("query a { createdAt { date } } ") == {
        "data": {"createdAt": {"date": "2019-09-04T13:49:12.585158"}}
    }


@freeze_time("2019-09-04T13:49:12", tz_offset=0)
@pytest.mark.asyncio
async def test_isodate_no_microseconds_timezone():
    logger = Mock()
    logger.debug = Mock()

    @Resolver("Query.createdAt", schema_name="test_isodate_no_microseconds_timezone")
    async def created_at_resolver(*_args, **_kwargs):
        return {}

    @Resolver("ISODate.date", schema_name="test_isodate_no_microseconds_timezone")
    async def created_at_date_resolver(*_args, **_kwargs):
        await asyncio.sleep(0.100)
        return "OVERWRITTEN"

    engine = await create_engine(
        sdl="""
        type ISODate {
            date: String @isoDate(microseconds: false, timezone: false)
        }
        type Query {
            createdAt: ISODate
        }
        """,
        modules=[
            {
                "name": "tartiflette_plugin_isodate",
                "config": {},
            }
        ],
        schema_name="test_isodate_no_microseconds_timezone",
    )

    assert await engine.execute("query a { createdAt { date } } ") == {
        "data": {"createdAt": {"date": "2019-09-04T13:49:12"}}
    }
