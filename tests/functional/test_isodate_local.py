from unittest.mock import Mock, patch

import asyncio
import datetime
import pytest

from freezegun import freeze_time
from tartiflette import Resolver, create_engine


@pytest.fixture
def mock_time_altzone(autouse=True):
    with patch("tartiflette_plugin_isodatenow.time") as mocked:
        mocked.altzone = 14400
        yield mocked


@freeze_time("2019-09-04T13:49:12.585158", tz_offset=-datetime.timedelta(hours=4))
@pytest.mark.asyncio
async def test_isodate_defaults(mock_time_altzone):
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
            date: String @isoDateNow(utc: false)
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
        schema_name="test_isodate_defaults",
    )
    
    assert await engine.execute("query a { createdAt { date } } ") == {
        "data": {"createdAt": {"date": "2019-09-04T09:49:12.585158-04:00"}}
    }


@freeze_time("2019-09-04T13:49:12", tz_offset=-datetime.timedelta(hours=4))
@pytest.mark.asyncio
async def test_isodate_no_microseconds(mock_time_altzone):
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
            date: String @isoDateNow(microseconds: false, utc: false)
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
        schema_name="test_isodate_no_microseconds",
    )

    assert await engine.execute("query a { createdAt { date } } ") == {
        "data": {"createdAt": {"date": "2019-09-04T09:49:12-04:00"}}
    }


@freeze_time("2019-09-04T13:49:12.585158", tz_offset=-datetime.timedelta(hours=4))
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
            date: String @isoDateNow(timezone: false, utc: false)
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
        schema_name="test_isodate_no_timzone",
    )
    
    assert await engine.execute("query a { createdAt { date } } ") == {
        "data": {"createdAt": {"date": "2019-09-04T09:49:12.585158"}}
    }


@freeze_time("2019-09-04T13:49:12", tz_offset=-datetime.timedelta(hours=4))
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
            date: String @isoDateNow(microseconds: false, timezone: false, utc: false)
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
        schema_name="test_isodate_no_microseconds_timezone",
    )

    assert await engine.execute("query a { createdAt { date } } ") == {
        "data": {"createdAt": {"date": "2019-09-04T09:49:12"}}
    }
