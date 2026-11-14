# datetime

Dates, times, durations, UTC offsets, and IANA time zones for
[stone](https://tarolling.github.io/stone), with ISO 8601 and strftime-style formatting and
parsing. Written in pure stone, it runs the same in the interpreter and in compiled programs.

```stone
use datetime.Date
use datetime.Duration
use datetime.Period
use datetime.TimeZone
use datetime.ZonedDateTime

print(Date.of(2026, 1, 31).unwrap() + Period.of_months(1))   // 2026-02-28

chicago = TimeZone.get("America/Chicago").unwrap()
meeting = ZonedDateTime.of(2026, 11, 6, 19, 13, 31, chicago).unwrap()
print(meeting)                                // 2026-11-06T19:13:31-06:00[America/Chicago]
print(meeting.to_instant())                   // 2026-11-07T01:13:31Z
print((meeting + Duration.of_minutes(90)).format("%-I:%M %p %Z"))   // 8:43 PM CST
print(meeting.in_zone(TimeZone.get("Asia/Kolkata").unwrap()))      // 2026-11-07T06:43:31+05:30[Asia/Kolkata]
```

## Install

```sh
stone add github:tarolling/datetime
```

This needs stone 0.4.6 or later. Then `use datetime` and write `datetime.Date`, or import each
type by name with `use datetime.Date`.

## Types

Each kind of value has its own type, as in java.time and Rust's chrono, so a value's type says
what it means:

| Type | Example | Meaning |
| --- | --- | --- |
| `Date` | `2026-11-06` | a calendar date |
| `Time` | `19:13:31.5` | a time of day |
| `DateTime` | `2026-11-06T19:13:31` | a date and time with no offset, as a wall clock shows |
| `Offset` | `+05:30`, `Z` | a fixed offset from UTC, from -18:00 to +18:00 |
| `OffsetDateTime` | `2026-11-06T19:13:31-06:00` | a date and time at an offset: one instant |
| `Instant` | `2026-11-07T01:13:31Z` | a point in time, counted from 1970-01-01T00:00:00Z |
| `TimeZone` | `America/Chicago` | a time zone's rules: its offset at every instant |
| `ZonedDateTime` | `2026-11-06T19:13:31-06:00[America/Chicago]` | a date and time in a time zone: one instant |
| `Duration` | `PT1H30M` | an exact length of time, to the nanosecond |
| `Period` | `P1Y2M3D` | a length in years, months, and days, whose exact length depends on the date |
| `Weekday` | `Weekday.Friday` | Monday to Sunday |
| `LocalTime` | `LocalTime.Gap(before=-06:00, after=-05:00)` | what a wall clock time means in a zone |
| `Disambiguation` | `Disambiguation.Compatible` | how to pick an instant for a time the clocks skip or repeat |

Dates use the proleptic Gregorian calendar with a year 0 (1 BC is year 0 and 2 BC is year -1),
for years -999999 to 999999. Times have nanosecond precision.

Every type but `Period`, `TimeZone`, and the enums can be compared with `<`, `==`, and so on,
and sorted. `print` and `str` write every type in ISO 8601, as in the table.

## Operators

Arithmetic uses `+`, `-`, `*`, `/`, and unary `-` (each also as a method, as `d.add(e)`):

| Expression | Result |
| --- | --- |
| `Duration + Duration`, `Duration - Duration`, `-Duration` | `Duration`, exact |
| `Duration * int`, `Duration / int` | `Duration`; `/` truncates toward zero to the nanosecond |
| `Period + Period`, `Period - Period`, `-Period`, `Period * int` | `Period`, part by part |
| `Date + Period`, `Date - Period` | `Date`: the years and months, then the days |
| `Time + Duration`, `Time - Duration` | `Time`, going around midnight |
| `DateTime`, `OffsetDateTime` `+ Duration` or `+ Period` (and `-`) | the same type, with the offset kept |
| `Instant + Duration`, `Instant - Duration` | `Instant` |
| `ZonedDateTime + Duration` (and `-`) | exact time: 24 hours across a change of the clocks is another wall clock time |
| `ZonedDateTime + Period` (and `-`) | wall clock time: a day later is the same time of day |

stone gives an operator's result the left operand's type, so the time between two values is a
method: `a.duration_until(b)`, `i.duration_since(earlier)`, and `d.days_until(other)`. `+=` and
`-=` work too, as in `total += Duration.of_minutes(5)`.

## Errors

- Building a value from parts or text returns a `result`: `Date.of(2026, 2, 30)` is
  `err("day 30 is out of range for 2026-02 (1 to 28)")`, and `Date.parse_iso("x")` is an `err`
  saying why the text is not a date.
- Arithmetic that would leave years -999999 to 999999, and `format` with a pattern it cannot
  write, stop the program with a message, as an index out of range does. Patterns are almost
  always fixed text in the program, so a mistake in one is a bug to fix rather than a case to
  handle.

## API

Arguments are ints unless noted. `→ result` marks functions that return `result[T, str]`.

### Date

| | |
| --- | --- |
| `Date.of(year, month, day)` → result | a date from its parts |
| `Date.from_ordinal(year, day_of_year)` → result | `Date.from_ordinal(2026, 310)` is 2026-11-06 |
| `Date.from_iso_week(iso_year, week, weekday: Weekday)` → result | a date from its ISO week |
| `Date.from_epoch_days(n)` | the date `n` days after 1970-01-01 |
| `Date.today_utc()`, `Date.today(zone: TimeZone)` | today in UTC, or in a zone |
| `.year`, `.month`, `.day` | the parts |
| `.weekday()`, `.day_of_year()`, `.iso_week()` | `Weekday.Friday`, `310`, `(2026, 45)` |
| `.is_leap_year()`, `.days_in_month()`, `.days_in_year()` | facts about the date's year and month |
| `.first_of_month()`, `.last_of_month()` | the month's first and last day |
| `.add_days(n)`, `.add_weeks(n)` | `n` may be negative |
| `.add_months(n)`, `.add_years(n)` | keeps the day, or uses the month's last day if the month is shorter |
| `d + p`, `d - p` | adds the years and months of a `Period` first, then the days |
| `.days_until(other: Date)` | days from this date to `other`, negative if `other` is earlier |
| `.to_epoch_days()` | days from 1970-01-01 |
| `.at(t: Time)` | a `DateTime` |
| `.format(pattern)`, `Date.parse(text, pattern)` → result, `Date.parse_iso(text)` → result | see [Formatting](#formatting-and-parsing) |

Free functions: `datetime.is_leap_year(year)`, `datetime.days_in_month(year, month)`,
`datetime.days_in_year(year)`, `datetime.weekday_number(w)` (1 for Monday to 7 for Sunday),
`datetime.weekday_from_number(n)` → result, `datetime.weekday_name(w)` ("Friday").

### Time

| | |
| --- | --- |
| `Time.of(hour, minute, second)` → result, `Time.of_nanos(hour, minute, second, nanosecond)` → result | a time from its parts |
| `Time.midnight()`, `Time.noon()` | |
| `Time.from_seconds_of_day(n)` → result, `Time.from_nanos_of_day(n)` → result | the time `n` after midnight |
| `.hour`, `.minute`, `.second`, `.nanosecond` | the parts |
| `.seconds_of_day()`, `.nanos_of_day()` | the time since midnight |
| `t + d`, `t - d` | a `Duration` later or earlier, going around midnight as a clock does |
| `.duration_until(other: Time)` | on the same day, negative if `other` is earlier |
| `.format`, `Time.parse`, `Time.parse_iso` | |

### DateTime

| | |
| --- | --- |
| `DateTime.of(year, month, day, hour, minute, second)` → result | |
| `DateTime.new(date: Date, time: Time)`, `date.at(time)` | |
| `DateTime.now_utc()`, `DateTime.now(zone: TimeZone)` | now, in UTC or on a zone's clocks |
| `.date`, `.time` | the parts |
| `dt + d`, `dt + p`, `dt - d`, `dt - p`, `.add_days(n)` | with a `Duration` or a `Period` |
| `.duration_until(other: DateTime)` | |
| `.at_offset(o: Offset)` | an `OffsetDateTime` |
| `.assume_utc()` | the `Instant` this names in UTC |
| `.in_zone(z: TimeZone)` | a `ZonedDateTime`, as `ZonedDateTime.new` resolves it |
| `.format`, `DateTime.parse`, `DateTime.parse_iso` | |

### Offset

| | |
| --- | --- |
| `Offset.utc()` | |
| `Offset.of_hours(h)` → result, `Offset.of_hm(h, m)` → result, `Offset.of_seconds(s)` → result | `of_hm(-3, 30)` is -03:30. Use `of_seconds(-1800)` for -00:30 |
| `.seconds` | the offset in seconds, positive east of Greenwich |
| `Offset.parse_iso(text)` → result | `Z`, `+05:30`, `+0530`, `+05` |

### OffsetDateTime

| | |
| --- | --- |
| `OffsetDateTime.of(year, month, day, hour, minute, second, o: Offset)` → result | |
| `OffsetDateTime.new(dt: DateTime, o: Offset)`, `dt.at_offset(o)` | |
| `OffsetDateTime.now_utc()` | |
| `OffsetDateTime.from_instant(i: Instant, o: Offset)`, `i.at_offset(o)` | |
| `.datetime`, `.offset`, `.date()`, `.time()` | the parts |
| `.to_instant()`, `.to_offset(o: Offset)`, `.to_utc()` | the same instant, maybe at another offset |
| `.in_zone(z: TimeZone)` | the same instant in a zone |
| `odt + d`, `odt + p`, `odt - d`, `odt - p` | keep the offset |
| `.duration_until(other: OffsetDateTime)` | between the two instants |
| `.format`, `OffsetDateTime.parse`, `OffsetDateTime.parse_iso` | `parse_iso` reads RFC 3339 |

`==` compares parts, so the same instant at two offsets is not `==`. Compare `.to_instant()`s to
ask whether two values are the same instant. `<` orders by instant first.

### Instant

| | |
| --- | --- |
| `Instant.now()` | from the system clock, to the microsecond |
| `Instant.from_unix(s)`, `.from_unix_millis(ms)`, `.from_unix_micros(us)`, `.from_unix_nanos(ns)` | |
| `.unix_seconds()`, `.unix_millis()`, `.unix_micros()`, `.unix_nanos()` | rounded down, so they are negative before 1970 |
| `.secs`, `.nanos` | the seconds since 1970, and nanoseconds from 0 to 999999999 |
| `i + d`, `i - d`, `.duration_since(earlier: Instant)`, `.elapsed()` | |
| `.at_offset(o: Offset)`, `.to_utc()` | an `OffsetDateTime` |
| `.in_zone(z: TimeZone)` | a `ZonedDateTime` |
| `.format` (in UTC), `Instant.parse`, `Instant.parse_iso` | |

### Duration

| | |
| --- | --- |
| `Duration.zero()`, `Duration.of_days(n)`, `of_hours`, `of_minutes`, `of_seconds`, `of_millis`, `of_micros`, `of_nanos` | a day is exactly 24 hours |
| `Duration.of_seconds_float(x: float)` | |
| `.secs`, `.nanos` | seconds, rounded down, and nanoseconds from 0 to 999999999: -1.5 s is secs -2, nanos 500000000 |
| `a + b`, `a - b`, `-a`, `a * k`, `a / k`, `.abs()` | exact. `/` truncates toward zero to the nanosecond |
| `.whole_days()`, `whole_hours`, `whole_minutes`, `whole_seconds`, `whole_millis`, `whole_micros`, `whole_nanos` | truncated toward zero |
| `.as_seconds_float()` | |
| `.is_zero()`, `.is_negative()` | |
| `Duration.parse_iso(text)` → result | `PT1H30M`, `P2DT0.5S`, `-PT10S` |

### Period

| | |
| --- | --- |
| `Period.of(years, months, days)`, `Period.zero()`, `of_years`, `of_months`, `of_weeks`, `of_days` | |
| `.years`, `.months`, `.days` | |
| `a + b`, `a - b`, `-a`, `a * k`, `.is_zero()` | part by part, without carrying months into years |
| `Period.parse_iso(text)` → result | `P1Y2M3D`, `P2W`, `-P1M`, `P1Y-2M` |

### TimeZone

| | |
| --- | --- |
| `TimeZone.get(name)` → result | `"America/Chicago"` and any other IANA zone, `"UTC"`, `"+05:30"`, or `"localtime"` |
| `TimeZone.local()` | the system's zone; see below |
| `TimeZone.utc()`, `TimeZone.fixed(o: Offset)` | |
| `TimeZone.posix(spec)` → result | a POSIX TZ string, as `"CST6CDT,M3.2.0,M11.1.0"` |
| `TimeZone.from_tzif(name, data: bytes)` → result | a TZif file (RFC 8536), such as one from `/usr/share/zoneinfo` |
| `.name` | |
| `.offset_at(i: Instant)`, `.abbreviation_at(i)`, `.is_dst_at(i)` | `-06:00`, `"CST"`, `false` |
| `.resolve(dt: DateTime)` | a `LocalTime`: what the wall clock time means here |

`get` reads the zone from the system's copy of the IANA database: the directory `TZDIR` names,
or else the first of `/usr/share/zoneinfo`, `/usr/lib/zoneinfo`, `/usr/share/lib/zoneinfo`, and
`/etc/zoneinfo`. It reads the file each time, so get a zone once and reuse it. `local` uses `TZ`
if it is set (a zone name, a path to a TZif file, or a POSIX TZ string), and then
`/etc/localtime`, which it names by where the link points. It falls back to UTC.

### LocalTime and Disambiguation

When the clocks go forward an hour, the wall clock times in that hour never happen. When they go
back, the times in that hour happen twice. `zone.resolve(dt)` says which case applies:

```stone
pub enum LocalTime:
    Unique(at: OffsetDateTime)
    Ambiguous(earlier: OffsetDateTime, later: OffsetDateTime)
    Gap(before: Offset, after: Offset)
```

`ZonedDateTime.from_local` takes a `Disambiguation` that picks one instant, with the meanings
JavaScript's Temporal gives them:

| | skipped time, as 02:30 when 02:00 becomes 03:00 | repeated time, as 01:30 when 02:00 becomes 01:00 |
| --- | --- | --- |
| `Compatible` | 03:30, moved later by the gap's length | the earlier instant |
| `Earlier` | 01:30, moved earlier by the gap's length | the earlier instant |
| `Later` | 03:30 | the later instant |
| `Reject` | an `err` | an `err` |

### ZonedDateTime

| | |
| --- | --- |
| `ZonedDateTime.of(year, month, day, hour, minute, second, zone: TimeZone)` → result | `Compatible` |
| `ZonedDateTime.new(dt: DateTime, zone)`, `dt.in_zone(zone)` | `Compatible` |
| `ZonedDateTime.from_local(dt, zone, how: Disambiguation)` → result | an `err` only for `Reject` |
| `ZonedDateTime.from_instant(i: Instant, zone)`, `i.in_zone(zone)`, `odt.in_zone(zone)` | |
| `ZonedDateTime.now(zone)`, `ZonedDateTime.now_local()` | |
| `.datetime`, `.offset`, `.zone`, `.date()`, `.time()` | the parts. `.offset` is always the zone's offset then |
| `.to_instant()`, `.to_offset_datetime()`, `.in_zone(other: TimeZone)` | the same instant |
| `.abbreviation()`, `.is_dst()` | `"CST"`, `false` |
| `zdt + d`, `zdt - d` | `d` later in exact time |
| `zdt + p`, `zdt - p`, `.add_days(n)` | on the wall clock. A skipped time moves later, and a repeated one keeps the offset if it can |
| `.duration_until(other: ZonedDateTime)` | between the two instants |
| `.format(pattern)` | `%Z` writes the abbreviation |
| `ZonedDateTime.parse(text, pattern, zone)` → result | an offset in the text must be the zone's, and picks between repeated times |
| `ZonedDateTime.parse_iso(text)` → result | RFC 9557: `2026-11-06T19:13:31-06:00[America/Chicago]`, with the offset optional |

`==` compares parts, zone included. `<` orders by instant, then wall clock time, then the zone's
name.

## Formatting and parsing

### ISO 8601

`print` and `str` write ISO 8601, and each type's `parse_iso` reads it strictly:

- Dates are `YYYY-MM-DD`. Years outside 0000 to 9999 have a sign: `+12026-01-02`, `-0044-03-15`.
- Times are `hh:mm:ss`, with a fraction of 3, 6, or 9 digits if needed. `parse_iso` also reads
  `hh:mm`, and fractions of 1 to 9 digits after `.` or `,`.
- `T`, `t`, or a space separates a date and a time.
- Offsets are `Z` or `+hh:mm`. `parse_iso` also reads `z`, `+hhmm`, and `+hh`.
- A `ZonedDateTime` adds its zone's name in brackets, as RFC 9557 does:
  `2026-11-06T19:13:31-06:00[America/Chicago]`.

### Patterns

`format(pattern)` replaces each specifier in the pattern with a part of the value, and
`parse(text, pattern)` reads text written that way. Any other character must match exactly.

| Specifier | Meaning | Example |
| --- | --- | --- |
| `%Y` | year, at least 4 digits | `2026` |
| `%C`, `%y` | century, and year in the century | `20`, `26` |
| `%m` | month | `11` |
| `%d`, `%e` | day of the month, zero- or space-padded | `06`, `" 6"` |
| `%j` | day of the year | `310` |
| `%B`, `%b` (`%h`) | month name, full and short | `November`, `Nov` |
| `%A`, `%a` | weekday name, full and short | `Friday`, `Fri` |
| `%u`, `%w` | weekday number, Monday = 1 to 7, and Sunday = 0 to 6 | `5`, `5` |
| `%G`, `%g`, `%V` | ISO week-based year, its last two digits, and ISO week | `2026`, `26`, `45` |
| `%U`, `%W` | week of the year, starting Sunday or Monday (format only) | `44` |
| `%H`, `%I` | hour, 24-hour and 12-hour | `19`, `07` |
| `%M`, `%S` | minute, second | `13`, `31` |
| `%f` | nanoseconds, 9 digits. Parsing reads 1 to 9 digits as a fraction | `500000000` |
| `%3f`, `%6f`, `%9f` | milliseconds, microseconds, nanoseconds | `500` |
| `%p`, `%P` | `AM` or `PM`, and `am` or `pm`. Parsing ignores case | `PM` |
| `%z`, `%:z` | offset | `-0600`, `-06:00` |
| `%Z` | a `ZonedDateTime`'s abbreviation, else `UTC` for offset 0 or the offset. Parsing reads `UTC`, `GMT`, or an offset | `CST`, `-06:00` |
| `%s` | seconds since 1970-01-01T00:00:00Z | `1794014011` |
| `%F` | `%Y-%m-%d` | `2026-11-06` |
| `%T`, `%R` | `%H:%M:%S`, `%H:%M` | `19:13:31` |
| `%D` (`%x`) | `%m/%d/%y` | `11/06/26` |
| `%X` | `%H:%M:%S` | |
| `%c` | `%a %b %e %H:%M:%S %Y` | `Fri Nov  6 19:13:31 2026` |
| `%n`, `%t` | a newline and a tab. Parsing skips any whitespace | |
| `%%` | `%` | |

A `-` after `%` drops the padding: `%-d` writes `6` and `%-I` writes `7`.

Names are in English. A specifier that needs a part the value lacks, such as `%H` on a `Date`,
stops `format`. In `parse`, parts of the pattern the type has no room for are read and then
ignored. A `Date` can be read from `"2026-11-06 19:00"` with `"%F %H:%M"`.

When parsing:

- Unsigned `%Y` reads up to 4 digits, so `%Y%m%d` reads `20261106`. With a sign, it reads up to 9.
- `%y` without `%C` is 1969 to 2068, as in POSIX.
- A date can come from `%Y %m %d`, from `%Y %j`, or from `%G %V %u`. A weekday read alongside
  is checked against the date.
- Minutes and seconds left out are 0. A `DateTime` needs both a date and an hour.
- An `OffsetDateTime` or `Instant` needs an offset (`%z`, `%:z`, `%Z`) or `%s`.

## Limits

- **Time zones come from the system.** `TimeZone.get` reads the IANA database the operating
  system ships, so its rules are as current as the system's. Windows has no such database, so
  there only `UTC`, fixed offsets, `TimeZone.posix`, and `TimeZone.from_tzif` work, unless
  `TZDIR` names a copy of the database, and `TimeZone.local()` is UTC unless `TZ` is set. Zones
  with leap seconds (`right/...`) are not supported.
- **No leap seconds.** `23:59:60` is not a valid time, and every day has 86400 seconds.
- **Microsecond clock.** `Instant.now()` comes from stone's `time.now()`, a float. At today's
  dates that float holds the time to about a quarter of a microsecond, so `now` rounds to the
  microsecond.
- English names only.

## Development

```sh
stone test            # every test, interpreted
stone test --build    # every test, compiled to native code
stone fmt --check
cd examples && stone run tour.stn
```

`lib.stn` holds every public type, because stone has no re-exports. The `internal/` modules work on
plain ints and strings:

- `civil.stn` does calendar arithmetic.
- `text.stn` pads numbers and holds names.
- `fmt.stn` formats with strftime patterns.
- `parse.stn` reads strptime patterns and ISO 8601.
- `tz.stn` reads TZif files and POSIX TZ strings, and finds a zone's offsets.

Their functions are `pub` only so `lib.stn` can call them. Programs should use the types instead.

## License

Apache-2.0
