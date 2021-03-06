Introduction
============

``ftw.calendar`` is a calendar view based on fullcalendar (http://arshaw.com/fullcalendar).

Features
========

- Generic: ftw.calendar doesn't care about the event objects, it only needs
  a collection in which the resulting brains have a start and a end attribute.
  If the calendar view is on an other content type than a collection, it will
  show all events (types defined in portal_calendar) below this context.

- Lightweight: the only requirement (apart from plone of course) is simplejson.
  Optionally, if you want to enable resizing of events and the drag and drop functionality,
  you can install jquery.ui but it is not required.

- Internationalized: currently ftw.calendar is available
  in german, english and czech. Feel free to add more translations.

- Integrated: ftw.calendar cares about your calendar settings.
  First day of the week is respected and displayed accordingly.

Usage
=====

- Add ``ftw.calendar`` to your buildout configuration:

::

    [instance]
    eggs +=
        ftw.calendar

- Install the generic import profile.


Use the ``ftwcalendar_view`` as the new default view on any collection.
The default events-collection in a new plone site should work well,
you probably should remove the date criterions though,
since fullcalendar needs to be able to set them according to the selected month.

Troubleshooting
===============

Often there are javascript-errors just after installing and trying the calendar view.
Normally these are due to javascript caching and can be easily solved
by enabling javascript debugging in the js_registry.

Credits
=======

Many thanks to Adam Shaw for jq.fullcalendar.


Compatibility
-------------

Runs with `Plone <http://www.plone.org/>`_ `4.1`, `4.2`.


Links
=====

- Main github project repository: https://github.com/4teamwork/ftw.calendar
- Issue tracker: https://github.com/4teamwork/ftw.calendar/issues
- Package on pypi: http://pypi.python.org/pypi/ftw.calendar
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.calendar


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.calendar`` is licensed under GNU General Public License, version 2.

