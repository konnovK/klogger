import datetime
from logging import Handler, LogRecord
import requests


class KLoggerHandler(Handler):
    def __init__(self, url: str, user_email: str, user_password: str, log_group_id: str, level=0) -> None:
        r = requests.post(f'{url}/api/v1/user/login', json={'email': user_email, 'password': user_password})
        if r.status_code != 200:
            raise Exception(f'Problems with auth: {r.json()}')
        response_data = r.json()
        self.url = url
        self.log_group_id = log_group_id
        self.access_token = response_data['access_token']
        super().__init__(level)

    def emit(self, record: LogRecord) -> None:
        log_timestamp = datetime.datetime.now()
        log_level = record.levelname
        log_message = record.msg

        r = requests.post(
            f'{self.url}/api/v1/log',
            params={'log_group_id': self.log_group_id},
            headers={'Authorization': f'Bearer {self.access_token}'},
            json={
                'level': log_level,
                'timestamp': log_timestamp.isoformat(),
                'message': log_message,
            }
        )
        if r.status_code != 201:
            self.handleError(record)
