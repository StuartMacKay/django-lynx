from django import template
from django.utils import timezone
from django.utils.translation import gettext, ngettext_lazy

register = template.Library()


@register.filter(expects_localtime=True)
def age_format(value):

    weeks = days = hours = minutes = 0
    delta = timezone.now() - value

    # TODO Passing dates in the future raises AssertionError but should we
    #      consider returning a value string instead, e.g. "one week from now".

    assert delta.days >= 0 and delta.seconds >= 0, "Value is in the future: %s" % value

    if delta.days:
        weeks = int(delta.days / 7)
        days = delta.days
    else:
        hours = int(delta.seconds / 3600)
        minutes = int(delta.seconds / 60)

    if weeks:
        return ngettext_lazy("a week ago", "%(n)d weeks ago", weeks) % {"n": weeks}
    elif days:
        return ngettext_lazy("a day ago", "%(n)d days ago", days) % {"n": days}
    elif hours:
        return ngettext_lazy("an hour ago", "%(n)d hours ago", hours) % {"n": hours}
    elif minutes:
        return ngettext_lazy("a minute ago", "%(n)d minutes ago", minutes) % {
            "n": minutes
        }
    else:
        # We don't need precision (or accuracy) so round up seconds to a minute.
        return gettext("a minute ago")
