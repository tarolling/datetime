# Changelog

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
