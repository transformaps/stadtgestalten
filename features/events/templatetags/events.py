import calendar as python_calendar
import datetime
import itertools

import django.utils.formats
import django.utils.timezone
from django import template
from django.core import urlresolvers

register = template.Library()


class Calendar(python_calendar.LocaleHTMLCalendar):
    def __init__(self, event_dict, firstweekday=0, locale=None):
        super().__init__(firstweekday, locale)
        self.today = datetime.date.today()
        self.events = event_dict

    def formatday(self, thedate, themonth):
        events = self.events.get(thedate, [])
        url = ''
        if len(events) == 1:
            url = events[0].get_absolute_url()
        elif len(events) > 1:
            url = urlresolvers.reverse(
                    'day-events', args=['{{:%{}}}'.format(c).format(thedate) for c in 'Ybd'])
        return {
                'day': thedate.day,
                'events': events,
                'in_month': thedate.month == themonth,
                'today': thedate == self.today,
                'url': url,
                }

    def formatmonthname(self, theyear, themonth):
        with python_calendar.different_locale(self.locale):
            return '%s %s' % (python_calendar.month_name[themonth], theyear)

    def formatmonthweeks(self, theyear, themonth):
        return [self.formatweek(week, themonth)
                for week in self.monthdatescalendar(theyear, themonth)]

    def formatweek(self, theweek, themonth):
        return [self.formatday(d, themonth) for d in theweek]

    def formatweekday(self, day):
        with python_calendar.different_locale(self.locale):
            return python_calendar.day_abbr[day]

    def formatweekheader(self):
        return [self.formatweekday(i) for i in self.iterweekdays()]


@register.inclusion_tag('events/_calendar.html', takes_context=True)
def calendar(context, associations, size='preview'):
    request = context.get('request')
    around = django.utils.timezone.now()
    around = around.replace(
            day=1,
            month=int(request.GET.get('month', around.month)),
            year=int(request.GET.get('year', around.year)))
    event_associations = associations.filter_events()
    calendar_associations = event_associations.filter(
            content__time__gt=around-datetime.timedelta(weeks=6),
            content__time__lt=around+datetime.timedelta(weeks=6)
            ).order_by('content__time')
    calendar_event_dict = {date: list(events) for date, events in itertools.groupby(
        calendar_associations, key=lambda a: a.container.time.date())}
    calendar = Calendar(calendar_event_dict)
    last_month = around.replace(day=1) + datetime.timedelta(days=-1)
    next_month = around.replace(day=1) + datetime.timedelta(days=31)
    context.update({
            'days': calendar.formatweekheader(),
            'prev_month': last_month,
            'month': calendar.formatmonthname(around.year, around.month),
            'next_month': next_month,
            'weeks': calendar.formatmonthweeks(around.year, around.month),
            'size': size,
            })
    return context


@register.filter
def day_preview(associations):
    return ', '.join([
        '{} {}'.format(django.utils.formats.time_format(
            django.utils.timezone.localtime(a.container.time)), a.container.title)
        for a in associations])


@register.simple_tag(takes_context=True)
def event_time(context, event):
    context['event'] = event
    time_str = context.template.engine.get_template('events/_time.html').render(context)
    return time_str.strip()


@register.inclusion_tag('events/_sidebar_calendar.html', takes_context=True)
def sidebar_calendar(
        context, associations, group=None, preview_length=5, show_group=True,
        hide_buttons=False):
    upcoming = associations.filter_upcoming().order_by('content__time')[:preview_length]
    context.update({
        'associations': associations,
        'group': group,
        'hide_buttons': hide_buttons,
        'show_group': show_group,
        'upcoming': upcoming,
    })
    return context


@register.filter
def upcoming_events(events, preview_length):
    return events.upcoming(preview_length)
