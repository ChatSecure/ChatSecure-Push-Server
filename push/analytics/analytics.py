import keen
import rollbar
import sys
import os
import logging


logger = logging.getLogger("django")


def event(event_name, extra_data_dict={}):
    """
    Log an event to the analytics backend
    """
    keen_enabled = len(os.environ.get("KEEN_PROJECT_ID", '')) > 0
    if keen_enabled:
        keen.add_event(event_name, extra_data_dict)
    logger.info('%s: %s', event_name, extra_data_dict)


def exception(request=None, extra_data=None):
    """
    Log an exception to the logging backend
    """
    rollbar.report_exc_info(sys.exc_info(), request=request, extra_data=extra_data)
