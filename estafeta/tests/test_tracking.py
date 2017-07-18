import unittest

import estafeta


class TrackingTests(unittest.TestCase):

    def setUp(self):
        super().setUp()

        estafeta.user = 'Usuario1'
        estafeta.password = '1GCvGIu$'
        estafeta.id = '25'
        estafeta.account_number = '0000000'
        estafeta.production = False

    def test_tracking_w_history(self):

        data = {
            'searchType': {
                'type': 'L',
                'waybillList': {
                    'waybillType': 'G',
                    'waybills': '6015013271610680252912',
                },
            },
            'searchConfiguration': {
                'historyConfiguration': {
                    'includeHistory': 1,
                    'historyType': 'ALL',
                },
                'filterType': {
                    'filterInformation': 0,
                },
            }
        }

        response = estafeta.EstafetaClient.track_package(data=data)
        for tracking_data in response['trackingData']['TrackingData']:
            self.assertEqual(tracking_data['waybill'], '6015013271610680252912')

    def test_tracking_short(self):

        data = {
            'searchType': {
                'type': 'L',
                'waybillList': {
                    'waybillType': 'R',
                    'waybills': '1346061292',
                },
            },
            'searchConfiguration': {
                'historyConfiguration': {
                    'includeHistory': 1,
                    'historyType': 'ALL',
                },
                'filterType': {
                    'filterInformation': 0,
                },
            }
        }

        response = estafeta.EstafetaClient.track_package(data=data)
        for tracking_data in response['trackingData']['TrackingData']:
            self.assertEqual(tracking_data['waybill'], '6015013271610680252912')

    def test_wrong_type(self):
        #1346061292

        data = {
            'searchType': {
                'type': 'R',
                'waybillList': {
                    'waybillType': 'R',
                    'waybills': '1346061292',
                },
            },
            'searchConfiguration': {
                'historyConfiguration': {
                    'includeHistory': 1,
                    'historyType': 'ALL',
                },
                'filterType': {
                    'filterInformation': 0,
                },
            }
        }

        with self.assertRaises(estafeta.core.EstafetaWrongData):
            response = estafeta.EstafetaClient.track_package(data=data)
