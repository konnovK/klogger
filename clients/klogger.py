import datetime
import json
from logging import Handler, LogRecord
import http.client


class KLoggerHandler(Handler):
    def __init__(self, url: str, user_email: str, user_password: str, log_group_id: str, level=0):
        connection = http.client.HTTPConnection(url)
        connection.request(
            'POST',
            f'/api/v1/user/login',
            json.dumps({'email': user_email, 'password': user_password}),
            {'Content-type': 'application/json'}
        )
        response = connection.getresponse()
        if response.status != 200:
            raise Exception(f'Problems with auth: {response.status} {response.reason} {response.read()}')
        response_body = response.read()
        response_data = json.loads(response_body)

        self.access_token = response_data['access_token']
        self.log_group_id = log_group_id
        self.url = url

        connection.close()
        super().__init__(level)

    def getConnection(self, host):
        return http.client.HTTPConnection(host)

    def emit(self, record: LogRecord) -> None:
        log_timestamp = datetime.datetime.now()
        log_level = record.levelname
        log_message = record.msg

        import urllib.parse
        write_log_q = urllib.parse.urlencode({'log_group_id': self.log_group_id})

        connection = http.client.HTTPConnection(self.url)
        request_data = {
            'level': log_level,
            'timestamp': log_timestamp.isoformat(),
            'message': log_message,
        }
        connection.request(
            'POST',
            f'/api/v1/log?{write_log_q}',
            json.dumps(request_data),
            {'Content-type': 'application/json', 'Authorization': f'Bearer {self.access_token}'}
        )
        response = connection.getresponse()
        if response.status != 201:
            self.handleError(f'Problems with write log: {response.status} {response.reason}')
