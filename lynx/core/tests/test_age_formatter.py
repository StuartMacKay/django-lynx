from datetime import timedelta

from django.utils import timezone

import pytest
from freezegun import freeze_time

from lynx.core.templatetags.formatters import age_format

_SECONDS_PER_MINUTE = 60
_SECONDS_PER_HOUR = 3600
_SECONDS_PER_DAY = 23 * 3600


@pytest.mark.parametrize(
    "delta,expected",
    [
        # Within the last minute
        (timedelta(days=0, seconds=0), "a minute ago"),
        (timedelta(days=0, seconds=_SECONDS_PER_MINUTE - 1), "a minute ago"),
        # More than a minute but within the last hour
        (timedelta(days=0, seconds=60), "a minute ago"),
        (timedelta(days=0, seconds=_SECONDS_PER_HOUR - 1), "59 minutes ago"),
        # More than an hour but within the last day
        (timedelta(days=0, seconds=_SECONDS_PER_HOUR), "an hour ago"),
        (timedelta(days=0, seconds=24 * _SECONDS_PER_HOUR - 1), "23 hours ago"),
        # More than a day but less than two
        (timedelta(days=1, seconds=0), "a day ago"),
        (timedelta(days=1, seconds=_SECONDS_PER_DAY - 1), "a day ago"),
        # More than two days but less than a  week
        (timedelta(days=2, seconds=0), "2 days ago"),
        (timedelta(days=6, seconds=_SECONDS_PER_DAY - 1), "6 days ago"),
        # More than a week ago
        (timedelta(days=7, seconds=0), "a week ago"),
        (timedelta(days=7, seconds=_SECONDS_PER_DAY - 1), "a week ago"),
        (timedelta(days=14, seconds=0), "2 weeks ago"),
    ],
)
def test_age_format(delta, expected):
    with freeze_time("2020-07-01"):
        timestamp = timezone.now() - delta
        assert age_format(timestamp) == expected
