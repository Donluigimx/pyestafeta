import unittest

import estafeta
from estafeta import EstafetaClient
from estafeta.core import EstafetaWrongData


class QuoteTests(unittest.TestCase):

    def setUp(self):
        super().setUp()

        estafeta.user = 'AdminUser'
        estafeta.password = ',1,B(vVi'
        estafeta.id = '1'
        estafeta.production = False

    def test_quote(self):

        data = {
            'esFrecuencia': False,
            'esLista': True,
            'esPaquete': True,
            'peso': 10,
            'largo': 10,
            'alto': 10,
            'ancho': 10,
            'datosOrigen': "44810",
            'datosDestino': "06100",
        }

        response = estafeta.EstafetaClient.quote(data=data)
        print(response)

        self.assertEqual(response['Error'], '000')

        data = {
            'esFrecuencia': False,
            'esLista': True,
            'esPaquete': False,
            'datosOrigen': "44810",
            'datosDestino': "06100",
        }

        response = estafeta.EstafetaClient.quote(data=data)

        print(response)
        self.assertEqual(response['Error'], '000')

    def test_wrong_quote(self):
        with self.assertRaises(EstafetaWrongData):
            data = {
                'esFrecuencia': False,
                'esLista': True,
                'esPaquete': True,
                'listaOrigen': "44810",
                'listaDestino': "06100",
            }

            response = estafeta.EstafetaClient.quote(data=data)

            # self.assertNotEqual(response['Error'], '000')
