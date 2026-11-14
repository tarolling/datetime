# Changelog

## 0.2.1 (unreleased)

This release needs stone 0.4.6. The API is unchanged.

### Changed

- The oldest supported stone is now 0.4.6, for its constants, bitwise operators, and lints. The
  package's fixed limits are constants now, so each use compiles to its value instead of a call.
- CI fails on any warning, with `stone check --deny warnings`.

## 0.2.0 (2026-11-08)

Time zones, and arithmetic with operators. This release needs stone 0.4.5.

### Added

- `TimeZone`, read from the system's IANA time zone database with `TimeZone.get("America/Chicago")`
  (or from `TZDIR`), and also from a POSIX TZ string (`TimeZone.posix`), a TZif file's bytes
  (`TimeZone.from_tzif`), or a fixed offset. `TimeZone.local()` is the system's zone, from `TZ`
  or `/etc/localtime`. A zone gives its offset, abbreviation, and daylight saving time at any
  instant, with POSIX rules for the years past its last listed change.
- `ZonedDateTime`, a date and time in a zone, written and read as RFC 9557
  (`2026-11-06T19:13:31-06:00[America/Chicago]`), with `format` writing the abbreviation for `%Z`.
  Adding a `Duration` moves through exact time, and adding a `Period` moves the wall clock.
- `LocalTime` (from `zone.resolve(dt)`) says whether a wall clock time happens once, twice, or
  never in a zone, and `Disambiguation` picks an instant for the last two cases, as in Temporal.
- `in_zone(zone)` on `Instant`, `OffsetDateTime`, and `DateTime`, plus `Date.today(zone)` and
  `DateTime.now(zone)`.
- Operators: `+` and `-` add durations and periods to every date and time type, durations add,
  subtract, negate, and multiply and divide by an int, and periods add, subtract, negate, and
  multiply by an int.

### Changed

- The oldest supported stone is now 0.4.5, for its operator traits, its fixes to compiled
  programs that read files as bytes, and its fix to compiled macOS programs that could start with
  garbage in their globals and crash.
- `add`, `sub`, `neg`, `mul`, and `div` are now the operator traits' methods. `d.add(e)` still
  works and means `d + e`.

### Removed

- `add_period` on `Date`, `DateTime`, and `OffsetDateTime`: write `d + p`.

## 0.1.0 (2026-11-07)

The first release.

- Types `Date`, `Time`, `DateTime`, `Offset`, `OffsetDateTime`, `Instant`, `Duration`, `Period`,
  and `Weekday`, for years -999999 to 999999 with nanosecond precision.
- Calendar arithmetic: days, weeks, months (clamped to the month's last day), years, and periods.
  Exact duration arithmetic, including multiplication and division.
- ISO 8601 / RFC 3339 output from `print` and `str`, and strict reading with `parse_iso`.
- strftime-style `format(pattern)` and strptime-style `parse(text, pattern)`.
- `Instant.now()`, `Date.today_utc()`, `DateTime.now_utc()`, and `OffsetDateTime.now_utc()` from
  the system clock.
