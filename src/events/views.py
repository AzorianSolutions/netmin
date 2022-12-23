from django.shortcuts import render


def index(request):
    from datetime import datetime, timedelta
    from events.lib import Graylog

    event_types = [
        {'type': '', 'label': 'Choose an option...'},
        {'type': 'link-down', 'label': 'Link Down'},
        {'type': 'link-up', 'label': 'Link Up'},
        {'type': 'link-fcs-error', 'label': 'Link FCS Error'},
    ]

    default_from: datetime = datetime.now() - timedelta(days=1)
    default_to: datetime = datetime.now()

    params: dict = {
        's': request.GET['s'] if 's' in request.GET else '',
        'from': request.GET['from'] if 'from' in request.GET else default_from.strftime('%m/%d/%Y %I:%M %p'),
        'to': request.GET['to'] if 'to' in request.GET else default_to.strftime('%m/%d/%Y %I:%M %p'),
        'min': request.GET['min'] if 'min' in request.GET else '1',
        'et': request.GET['et'] if 'et' in request.GET else 'link-down',
        'l': request.GET['l'] if 'l' in request.GET else '10000',
    }

    messages = Graylog.get_network_messages(source=params['s'], event_type=params['et'],
                                            start=datetime.strptime(params['from'], '%m/%d/%Y %I:%M %p'),
                                            end=datetime.strptime(params['to'], '%m/%d/%Y %I:%M %p'),
                                            limit=params['l'])

    message_index: dict = {}

    for message in messages:
        index_key: str = message['source'] + '-' + message['message']

        if index_key not in message_index:
            message_index[index_key] = {'total': 0, 'latest_ts': '', 'source': message['source'],
                                        'message': message['message'],
                                        'messages': []}

        message_index[index_key]['total'] += 1
        message_index[index_key]['messages'].append(message)

        if message_index[index_key]['latest_ts'] == '' or message['timestamp'] > message_index[index_key]['latest_ts']:
            message_index[index_key]['latest_ts'] = message['timestamp']

    filter_keys = []
    for key in message_index:
        if message_index[key]['total'] < int(params['min']):
            filter_keys.append(key)

    for key in filter_keys:
        message_index.pop(key)

    data: dict = {
        'graylog_messages': messages,
        'message_index': message_index.values(),
        'params': params,
        'event_types': event_types,
    }

    return render(request, 'events/index.jinja2', data)
