import unittest

import estafeta
from estafeta import EstafetaClient


class CoreTests(unittest.TestCase):

    def setUp(self):
        super().setUp()

    def create_core(self):
        estafeta_client = EstafetaClient()

        with self.assertRaises(estafeta.core.EstafetaEmptyField):
            print(estafeta_client.password)

        estafeta.user = 'Usuario1'
        estafeta.password = '1GCvGIu$'
        estafeta.id = '25'

        with self.assertRaises(estafeta.core.EstafetaEmptyField):
            print(estafeta_client.url_tracking)
        with self.assertRaises(estafeta.core.EstafetaEmptyField):
            print(estafeta_client.url_label)

        estafeta.production = False

        self.assertEqual(estafeta_client.url_tracking, 'https://trackingqa.estafeta.com/Service.asmx?wsdl')
        self.assertEqual(estafeta_client.url_label,
                         'https://labelqa.estafeta.com/EstafetaLabel20/services/EstafetaLabelWS?wsdl')

        estafeta.production = True

        self.assertEqual(estafeta_client.url_tracking, 'https://trackingqa.estafeta.com/Service.asmx?wsdl')
        self.assertEqual(estafeta_client.url_label,
                         'https://label.estafeta.com/EstafetaLabel20/services/EstafetaLabelWS?wsdl')

        self.assertEqual(estafeta_client.user, 'Usuario1')
        self.assertNotEqual(estafeta_client.user, '1GCvGIu$')
        self.assertEqual(estafeta_client.password, '1GCvGIu$')
        self.assertEqual(estafeta_client.id, '25')
