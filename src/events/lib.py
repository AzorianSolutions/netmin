import datetime


class Graylog:

    @staticmethod
    def get_network_messages(source: str, event_type: str, start: datetime.datetime, end: datetime.datetime,
                             limit: int = 10):
        import os
        from grapi.grapi import Grapi

        token = os.getenv('NM_GRAYLOG_TOKEN')
        graylog_url: str = os.getenv('MN_GRAYLOG_URL', 'https://graylog.example.com')
        if not graylog_url.endswith('/'):
            graylog_url += '/'

        url = f'{graylog_url}api/search/universal/absolute'
        api = Grapi(url, token)

        message: str = ''
        if event_type == 'link-down':
            message = 'link down'
        if event_type == 'link-up':
            message = 'link up'
        if event_type == 'link-fcs-error':
            message = 'fcs error on link'

        query: str = 'message:"' + message + '"'

        if len(str(source).strip()):
            query += ' && source:' + source

        params: dict = {
            'query': query,
            'fields': 'source,message,timestamp',
            'from': start.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'to': end.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'limit': limit,
        }

        messages = []
        result = api.send('get', **params)

        for item in result.json()['messages']:
            dt: datetime.datetime = datetime.datetime.strptime(item['message']['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
            item['message']['timestamp'] = dt
            messages.append(item['message'])

        return messages
