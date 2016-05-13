import keen
import rollbar
import sys


def event(event_name, extra_data_dict={}):
    """
    Log an event to the analytics backend
    """
    keen.add_event(event_name, extra_data_dict)


def exception(request=None, extra_data=None):
    """
    Log an exception to the logging backend
    """
    rollbar.report_exc_info(sys.exc_info(), request=request, extra_data=extra_data)
