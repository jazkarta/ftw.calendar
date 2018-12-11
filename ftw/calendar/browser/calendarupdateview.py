from plone.app.querystring.queryparser import parseFormquery
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from DateTime import DateTime
from ftw.calendar.browser.interfaces import IFtwCalendarModifier
from zope.component import queryUtility

import simplejson as json


class CalendarupdateView(BrowserView):
    """
    Calendarupdate browser view
    """

    def __call__(self, *args, **kw):
        """Render JS Initialization code"""

        response = self.request.response
        context = self.context

        response.setHeader('Content-Type', 'application/x-javascript')

        args = {}
        if self.request.get('end'):
            args['start'] = {'query': DateTime(self.request.get('start')),
                             'range': 'min'}
        if self.request.get('end'):
            args['end'] = {'query': DateTime(self.request.get('end')),
                           'range': 'max'}

        if context.portal_type == 'Collection':
            rawquery = context.getRawQuery()
            query = parseFormquery(context, rawquery, sort_on=context.getSort_on())
            query.update(args)
            catalog = getToolByName(context, 'portal_catalog')
            brains = catalog(query)
        elif context.portal_type == 'Topic':
            brains = context.aq_inner.queryCatalog(REQUEST=self.request, **args)
        else:
            portal_calendar = getToolByName(context, 'portal_calendar')
            catalog = getToolByName(context, 'portal_catalog')
            brains = catalog(
                portal_type=portal_calendar.getCalendarTypes(),
                path={'depth': -1,
                      'query': '/'.join(context.getPhysicalPath())},
                **args
            )
        result = []
        memberid = self.context.portal_membership.getAuthenticatedMember().id

        modifier = queryUtility(IFtwCalendarModifier)

        for brain in brains:
            if memberid in brain.Creator:
                editable = True
            else:
                editable = False
            duration = (brain.end - brain.start) * 86400
            info = {
                "id": "UID_%s" % (brain.UID),
                "title": brain.Title,
                "start": brain.start.ISO8601(),
                "end": brain.end.ISO8601(),
                "url": brain.getURL(),
                "editable": editable,
                "allDay": duration >= 86340,
                "className": "state-" + str(brain.review_state) + (editable and " editable" or ""),
                "description": brain.Description
            }
            if modifier:
                modifier(brain, info)
            result.append(info)
        return json.dumps(result, sort_keys=True)


class CalendarDropView(BrowserView):

    def __call__(self):
        request = self.context.REQUEST

        event_uid = request.get('event')

        if event_uid:
            event_uid = event_uid.split('UID_')[1]
        brains = self.context.portal_catalog(UID=event_uid)

        obj = brains[0].getObject()
        startDate, endDate = obj.startDate, obj.endDate
        dayDelta, minuteDelta = float(request.get('dayDelta')), \
            float(request.get('minuteDelta'))

        startDate = startDate + dayDelta + minuteDelta / 1440.0
        endDate = endDate + dayDelta + minuteDelta / 1440.0

        obj.setStartDate(startDate)
        obj.setEndDate(endDate)
        obj.reindexObject()
        return True


class CalendarResizeView(BrowserView):

    def __call__(self):
        request = self.context.REQUEST
        event_uid = request.get('event')
        if event_uid:
            event_uid = event_uid.split('UID_')[1]
        brains = self.context.portal_catalog(UID=event_uid)
        obj = brains[0].getObject()
        endDate = obj.endDate
        dayDelta, minuteDelta = float(request.get('dayDelta')), \
            float(request.get('minuteDelta'))

        endDate = endDate + dayDelta + minuteDelta / 1440.0

        obj.setEndDate(endDate)
        obj.reindexObject()
        return True
