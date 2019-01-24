
class IndexerSchedule():
    """ IndexerSchedule
    """
    """ IndexerSchedule
    """

    def __init__(self, interval, start_time=None):
        """
    :param interval:
           Required. A duration value that specifies an interval or period for indexer runs.
           The smallest allowed interval is five minutes; the longest is one day.
           It must be formatted as an XSD "dayTimeDuration" value
           (a restricted subset of an ISO 8601 duration value).
           The pattern for this is: "P[nD][T[nH][nM]]". Examples: PT15M for every 15 minutes,
           PT2H for every 2 hours.
    :param start_time: Optional.
           A UTC datetime when the indexer should start running.
       """
        self.interval = interval
        self.start_time = start_time

    def to_dict(self):
        """ to_dict
        """
        return {"interval": self.interval,
                "startTime": self.start_time}


