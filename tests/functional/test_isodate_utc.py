from unittest.mock import Mock

import asyncio
import datetime
import pytest

from freezegun import freeze_time
from tartiflette import Resolver, create_engine


@freeze_time("2019-09-04T13:49:12.585158", tz_offset=0)
@pytest.mark.asyncio
async def test_isodate_defaults():
    logger = Mock()
    logger.debug = Mock()

    @Resolver("Query.createdAt", schema_name="test_isodate_defaults_utc")
    async def created_at_resolver(*_args, **_kwargs):
        return {}

    @Resolver("ISODate.date", schema_name="test_isodate_defaults_utc")
    async def created_at_date_resolver(*_args, **_kwargs):
        await asyncio.sleep(0.100)
        return "OVERWRITTEN"

    engine = await create_engine(
        sdl="""
        type ISODate {
            date: String @isoDateNow
        }
        type Query {
            createdAt: ISODate
        }
        """,
        modules=[
            {
                "name": "tartiflette_plugin_isodatenow",
                "config": {}
            }
        ],
        schema_name="test_isodate_defaults_utc",
    )
    
    assert await engine.execute("query a { createdAt { date } } ") == {
        "data": {"createdAt": {"date": "2019-09-04T13:49:12.585158+00:00"}}
    }


@freeze_time("2019-09-04T13:49:12", tz_offset=0)
@pytest.mark.asyncio
async def test_isodate_no_microseconds():
    logger = Mock()
    logger.debug = Mock()

    @Resolver("Query.createdAt", schema_name="test_isodate_no_microseconds_utc")
    async def created_at_resolver(*_args, **_kwargs):
        return {}

    @Resolver("ISODate.date", schema_name="test_isodate_no_microseconds_utc")
    async def created_at_date_resolver(*_args, **_kwargs):
        await asyncio.sleep(0.100)
        return "OVERWRITTEN"

    engine = await create_engine(
        sdl="""
        type ISODate {
            date: String @isoDateNow(microseconds: false)
        }
        type Query {
            createdAt: ISODate
        }
        """,
        modules=[
            {
                "name": "tartiflette_plugin_isodatenow",
                "config": {},
            }
        ],
        schema_name="test_isodate_no_microseconds_utc",
    )

    assert await engine.execute("query a { createdAt { date } } ") == {
        "data": {"createdAt": {"date": "2019-09-04T13:49:12+00:00"}}
    }


@freeze_time("2019-09-04T13:49:12.585158")
@pytest.mark.asyncio
async def test_isodate_no_timezone():
    logger = Mock()
    logger.debug = Mock()

    @Resolver("Query.createdAt", schema_name="test_isodate_no_timzone_utc")
    async def created_at_resolver(*_args, **_kwargs):
        return {}

    @Resolver("ISODate.date", schema_name="test_isodate_no_timzone_utc")
    async def created_at_date_resolver(*_args, **_kwargs):
        await asyncio.sleep(0.100)
        return "OVERWRITTEN"

    engine = await create_engine(
        sdl="""
        type ISODate {
            date: String @isoDateNow(timezone: false)
        }
        type Query {
            createdAt: ISODate
        }
        """,
        modules=[
            {
                "name": "tartiflette_plugin_isodatenow",
                "config": {}
            }
        ],
        schema_name="test_isodate_no_timzone_utc",
    )
    
    assert await engine.execute("query a { createdAt { date } } ") == {
        "data": {"createdAt": {"date": "2019-09-04T13:49:12.585158"}}
    }


@freeze_time("2019-09-04T13:49:12", tz_offset=0)
@pytest.mark.asyncio
async def test_isodate_no_microseconds_timezone():
    logger = Mock()
    logger.debug = Mock()

    @Resolver("Query.createdAt", schema_name="test_isodate_no_microseconds_timezone_utc")
    async def created_at_resolver(*_args, **_kwargs):
        return {}

    @Resolver("ISODate.date", schema_name="test_isodate_no_microseconds_timezone_utc")
    async def created_at_date_resolver(*_args, **_kwargs):
        await asyncio.sleep(0.100)
        return "OVERWRITTEN"

    engine = await create_engine(
        sdl="""
        type ISODate {
            date: String @isoDateNow(microseconds: false, timezone: false)
        }
        type Query {
            createdAt: ISODate
        }
        """,
        modules=[
            {
                "name": "tartiflette_plugin_isodatenow",
                "config": {},
            }
        ],
        schema_name="test_isodate_no_microseconds_timezone_utc",
    )

    assert await engine.execute("query a { createdAt { date } } ") == {
        "data": {"createdAt": {"date": "2019-09-04T13:49:12"}}
    }
