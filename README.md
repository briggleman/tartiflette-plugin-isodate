# tartiflette-plugin-isodate

<a href="https://buddy.works"><img src="https://assets.buddy.works/automated-dark.svg" alt="Buddy.Works logo."></img></a>

[![buddy pipeline](https://app.buddy.works/benriggleman/tartiflette-plugin-isodate/pipelines/pipeline/208276/badge.svg?token=ff05a3fb6bb08b48350b4170e0c447aa3ccc198abbddd48c222205c3c61a7cff "buddy pipeline")](https://app.buddy.works/benriggleman/tartiflette-plugin-isodate/pipelines/pipeline/208276)

ISO Date Format Directive for Tartiflette

## TOC
- [Overview](#overview)
- [Installation](#install)
- [Usage](#usage)
    - [Options](#usage-options)
        - [microseconds](#usage-options-microseconds)
        - [timezone](#usage-options-timezone)
        - [utc](#usage-options-utc)


## [Overview](#overview)

The `tartiflette-plugin-isodate` plugin adds an `@isoDate` directive to [tartiflette](https://github.com/tartiflette/tartiflette).

## [Installation](#install)

To install with [poetry](https://poetry.eustace.io):

```sh
$ poetry add tartiflette-plugin-isodate
```

To install with pip:

```sh
$ pip install tartiflette-plugin-isodate
```

## [Usage](#usage)

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


### [Options](#usage-options)

The `@isoDate` also takes the following optional arguments:

#### [@isoDate(microseconds: false)](#usage-options-microseconds)

Returns date and time _without_ microseconds.

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

#### [@isoDate(timezone: false)](#usage-options-timezone)

Returns date and time _without_ timezone.

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

#### [@isoDate(utc: false)](#usage-options-utc)

Returns date and time in the _local_ timezone.

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

- `@isoDate` >> "2019-09-04T13:49:12.585158+00:00"
- `@isoDate(timezone: false)` >> "2019-09-04T13:52:43.476260"
- `@isoDate(microseconds: false)` >> "2019-09-04T13:50:02+00:00"
- `@isoDate(microseconds: false, timezone: false)` >> "2019-09-04T13:53:31"

The time can also be set to the `local` time by setting `utc` to `false`.  

`@isoDate(utc: false)` >> "2019-09-04T09:50:02+00:00"

Using the `@isoDate` directive will override any value sent.