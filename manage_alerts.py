#!/usr/bin/python3

import json
import datetime
from urllib.request import urlopen, Request
import time

import api_keys
from coinigy import CoinigyToken


class AlertManager:
    def __init__(self, coinigy_token, print_output=True):
        self._coinigy_token = coinigy_token
        self.print_output = print_output

    def get_old_alerts(self):
        # get old alerts
        headers = {'Content-Type': 'application/json', 'X-API-KEY': self._coinigy_token.token,
                   'X-API-SECRET': self._coinigy_token.secret}
        values = '{"exch_code": "BTRX"}'
        values = bytes(values, encoding='utf-8')
        request = Request('https://api.coinigy.com/api/v1/alerts', data=values, headers=headers)
        old_alerts = urlopen(request).read()
        old_alerts = old_alerts.decode("utf-8")
        old_alerts = json.loads(old_alerts)
        return old_alerts

    def _api_delete_alert(self, alert_id):
        """
        Api call to delete alert
        :param alert_id: srting, id of the alert to delete
        :return:
        """
        body = '{"alert_id": ' + alert_id + '}'
        body = bytes(body, encoding='utf-8')
        headers = {'Content-Type': 'application/json', 'X-API-KEY': self._coinigy_token.token, 'X-API-SECRET': self._coinigy_token.secret}
        request = Request('https://api.coinigy.com/api/v1/deleteAlert', data=body, headers=headers)
        response_body = urlopen(request).read()
        time.sleep(1)
        return response_body

    def delete_alerts_newer_than(self, newer_than):
        """
        Deletes all alerts created after 'newer_than'
        :param newer_than: datetime object
        :return:
        """

        old_alerts = self.get_old_alerts()

        for alert in old_alerts['data']['open_alerts']:
            if datetime.datetime.strptime(alert['alert_added'], '%Y-%m-%d %H:%M:%S') > newer_than:
                resp_body = self._api_delete_alert(alert['alert_id'])
                if self.print_output:
                    print(resp_body)

    def delete_scanner_alerts(self):
        """
        Deletes all alerts created by the scanner
        :return:
        """

        old_alerts = self.get_old_alerts()

        for alert in old_alerts['data']['open_alerts']:
            if "z_base_scanner" in alert['alert_note']:
                resp_body = self._api_delete_alert(alert['alert_id'])
                if self.print_output:
                    print(resp_body)


if __name__ == "__main__":
    ##############VARIABLES TO SET
    # from_date = datetime.datetime(year=2017, month=12, day=1, hour=23)
    ##############VARIABLES TO SET

    alerts = AlertManager(CoinigyToken(token=api_keys.coinigykey, secret=api_keys.coinigysec))

    # alerts.delete_alerts_newer_than(from_date)
    alerts_set = open("alerts_set.txt").readlines()
    [print(line) for line in alerts_set]
    input("Press enter to delete these alerts")
    # alerts_set = [notification_id.split("\t")[1] for notification_id in alerts_set]
    for notification_id in alerts_set:
        print(notification_id)
        notification_id = notification_id.split("\t")[1]
        alerts._api_delete_alert(notification_id)
