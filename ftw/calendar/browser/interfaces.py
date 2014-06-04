from zope.interface import Interface


class IFtwCalendarLayer(Interface):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IFtwCalendarModifier(Interface):
    """A hook to to adjust the info returned for an event appearing in the calendar."""

    def __call__(brain, info):
        """May mutate info based on info in brain. Returns nothing."""
