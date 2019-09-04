import logging
import time
import datetime

from tartiflette import Directive, Resolver, Scalar

_SDL = """
directive @isoDate(microseconds: Boolean! = true, timezone: Boolean! = true, utc: Boolean! = true) on FIELD_DEFINITION | FIELD
"""


class ISODate:
    def __init__(self, config):
        self._logger = config.get("logger", logging.getLogger(__name__))

    async def on_field_execution(
        self, directive_args, next_resolver, parent_result, args, ctx, info
    ):
        results = await next_resolver(parent_result, args, ctx, info)
        _time = await self._get_time(directive_args["utc"])
        _timezone = await self._get_timezone(directive_args["utc"])

        if directive_args["microseconds"] and directive_args["timezone"]:
            # microsecond = True and timezone = True: '2019-09-04T13:49:12.585158+00:00'
            results = _time.replace(tzinfo=_timezone).isoformat()
        elif directive_args["microseconds"] and not directive_args["timezone"]:
            # microsecond = True and timezone = False: '2019-09-04T13:52:43.476260'
            results = _time.isoformat()
        elif not directive_args["microseconds"] and directive_args["timezone"]:
            # microsecond = False and timezone = True: '2019-09-04T13:50:02+00:00'
            results = _time.replace(tzinfo=_timezone).isoformat()
        else:
            # microsecond = False and timezone = False: '2019-09-04T13:53:31'
            results = _time.replace(microsecond=0).isoformat()

        return results

    async def _get_time(self, _utc):
        if _utc:
            return datetime.datetime.utcnow()
        return datetime.datetime.now()

    async def _get_timezone(self, _utc):
        if _utc:
            return datetime.timezone.utc
        return datetime.timezone(offset=datetime.timedelta(seconds=-time.altzone))


async def bake(schema_name, config):
    Directive(name="isoDate", schema_name=schema_name)(ISODate(config))
    return _SDL
