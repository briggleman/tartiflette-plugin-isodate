# tartiflette-plugin-isodate

ISO Date Format Directive for Tartiflette

## TOC
- Overview
- Use

## Overview

The `tartiflette-plugin-isodate` plugin adds an `@isoDate` directive to [tartiflette](https://github.com/tartiflette/tartiflette).

## Use

```graphql
type Example {
    createdAt: String @isoDate
}
```

Querying `createdAt` would return the following:

```json
{
    "data": {
        "example": {
            "createdAt": "2019-09-04T13:49:12.585158+00:00"
        }
    }
}
```

The `@isoDate` also takes the following optional arguments:

- microseconds: Boolean = true

```graphql
type Example {
    createdAt: String @isoDate(microseconds: false)
}
```

Querying `createdAt` would return the following:

```json
{
    "data": {
        "example": {
            "createdAt": "2019-09-04T13:49:12+00:00"
        }
    }
}
```


- timezone: Boolean = true

```graphql
type Example {
    createdAt: String @isoDate(timezone: false)
}
```

Querying `createdAt` would return the following:

```json
{
    "data": {
        "example": {
            "createdAt": "2019-09-04T13:49:12.585158"
        }
    }
}
```

- utc: Boolean = true

```graphql
type Example {
    createdAt: String @isoDate(utc: false)
}
```

Querying `createdAt` would return the following:

```json
{
    "data": {
        "example": {
            "createdAt": "2019-09-04T09:49:12.585158-04:00"
        }
    }
}
```


The arguments can be used in any combination and will return an [ISO8601 compliant date](https://en.wikipedia.org/wiki/ISO_8601).

For example settings `microseconds` to `false` and `timezone` to `true` would yield: 2019-09-04T13:49:12+00:00.

Possible combinations:

- microsecond = `true` and timezone = `true`: "2019-09-04T13:49:12.585158+00:00"
- microsecond = `true` and timezone = `false`: "2019-09-04T13:52:43.476260"
- microsecond = `false` and timezone = `true`: "2019-09-04T13:50:02+00:00"
- microsecond = `false` and timezone = `false`: "2019-09-04T13:53:31"

The time can also be set to the `local` time by setting `utc` to `false`.

Using the `@isoDate` directive will override any value sent.