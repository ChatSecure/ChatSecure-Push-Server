import keen


def log(event_name, extra_data_dict={}):
    keen.add_event(event_name, extra_data_dict)
