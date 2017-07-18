import unittest

import estafeta
from estafeta.core.error import EstafetaWrongData


class LabelTests(unittest.TestCase):

    def setUp(self):
        super().setUp()

        estafeta.user = 'prueba1'
        estafeta.password = 'lAbeL_K_11'
        estafeta.id = '28'
        estafeta.account_number = '0000000'
        estafeta.production = False

    def test_label(self):
        data = {
            'paperType': 1,
            'labelDescriptionList': {
                'content': 'Vasos termicos',
                'deliveryToEstafetaOffice': False,
                'destinationCountryId': 'MX',
                'serviceTypeId': '70',
                'officeNum': 130,
                'valid': True,
                'parcelTypeId': 4,  # 1 es sobre, 4 es paquete
                'numberOfLabels': 1,
                'returnDocument': False,
                'weight': 10.0,
                'originZipCodeForRouting': '45222',
                'destinationInfo': {
                    'address1': 'Ruben Rodriguez 416',
                    'address2': 'San Andres',
                    'city': 'Guadalajara',
                    'contactName': 'Luis Angel Iniguez Hernandez',
                    'corporateName': 'Luis Angel Iniguez Hernandez',
                    'neighborhood': 'San Andres',
                    'phoneNumber': '3311975232',
                    'state': 'Jalisco',
                    'zipCode': '44810',
                    'valid': True,
                },
                'originInfo': {
                    'address1': 'Av Vallarta 9992',
                    'address2': 'Rancho Contento',
                    'city': 'Zapopan',
                    'contactName': 'Juanpu Toledo',
                    'corporateName': 'Argosystems',
                    'neighborhood': 'Rancho Contento',
                    'phoneNumber': '36440510',
                    'state': 'Jalisco',
                    'zipCode': '45222',
                    'valid': True,
                }
            }
        }

        response = estafeta.EstafetaClient.generate_label(data=data)
        self.assertEqual(bool(response), True)
        self.assertEqual(response['resultCode'], '0')

    def test_label_accents(self):
        data = {
            'paperType': 1,
            'labelDescriptionList': {
                'content': 'Vasos térmicos',
                'deliveryToEstafetaOffice': False,
                'destinationCountryId': 'MX',
                'serviceTypeId': '70',
                'officeNum': 130,
                'valid': True,
                'parcelTypeId': 4,  # 1 es sobre, 4 es paquete
                'numberOfLabels': 1,
                'returnDocument': False,
                'weight': 10.0,
                'originZipCodeForRouting': '45222',
                'destinationInfo': {
                    'address1': 'Rubén Rodriguez 416',
                    'address2': 'San Andrés',
                    'city': 'Guadalajara',
                    'contactName': 'Luis Angel Iñiguez Hernández',
                    'corporateName': 'Luis Angel I{iguez Hernández',
                    'neighborhood': 'San Andrés',
                    'phoneNumber': '3311975232',
                    'state': 'Jalisco',
                    'zipCode': '44810',
                    'valid': True,
                },
                'originInfo': {
                    'address1': 'Av Vallarta 9992',
                    'address2': 'Rancho Contento',
                    'city': 'Zapopan',
                    'contactName': 'Juanpu Toledo',
                    'corporateName': 'Argosystems',
                    'neighborhood': 'Rancho Contento',
                    'phoneNumber': '36440510',
                    'state': 'Jalisco',
                    'zipCode': '45222',
                    'valid': True,
                }
            }
        }

        response = estafeta.EstafetaClient.generate_label(data=data)
        self.assertEqual(bool(response), True)
        self.assertEqual(response['resultCode'], '0')

    def test_only_destination(self):
        data = {
            'paperType': 1,
            'labelDescriptionList': {
                'content': 'Vasos termicos',
                'deliveryToEstafetaOffice': False,
                'destinationCountryId': 'MX',
                'serviceTypeId': '70',
                'officeNum': 130,
                'valid': True,
                'parcelTypeId': 4,  # 1 es sobre, 4 es paquete
                'numberOfLabels': 1,
                'returnDocument': False,
                'weight': 10.0,
                'originZipCodeForRouting': '45222',
                'destinationInfo': {
                    'address1': 'Ruben Rodriguez 416',
                    'address2': 'San Andres',
                    'city': 'Guadalajara',
                    'contactName': 'Luis Angel Iniguez Hernandez',
                    'corporateName': 'Luis Angel Iniguez Hernandez',
                    'neighborhood': 'San Andres',
                    'phoneNumber': '3311975232',
                    'state': 'Jalisco',
                    'zipCode': '44810',
                    'valid': True,
                }
            }
        }

        response = estafeta.EstafetaClient.generate_label(data=data)
        self.assertEqual(bool(response), True)
        self.assertEqual(response['resultCode'], '0')

    def test_wrong_postal_code(self):
        data = {
            'paperType': 1,
            'labelDescriptionList': {
                'content': 'Vasos termicos',
                'deliveryToEstafetaOffice': False,
                'destinationCountryId': 'MX',
                'serviceTypeId': '70',
                'officeNum': 130,
                'valid': True,
                'parcelTypeId': 4,  # 1 es sobre, 4 es paquete
                'numberOfLabels': 1,
                'returnDocument': False,
                'weight': 10.0,
                'originZipCodeForRouting': '00000',
                'destinationInfo': {
                    'address1': 'Ruben Rodriguez 416',
                    'address2': 'San Andres',
                    'city': 'Guadalajara',
                    'contactName': 'Luis Angel Iniguez Hernandez',
                    'corporateName': 'Luis Angel Iniguez Hernandez',
                    'neighborhood': 'San Andres',
                    'phoneNumber': '3311975232',
                    'state': 'Jalisco',
                    'zipCode': '00000',
                    'valid': True,
                }
            }
        }

        response = estafeta.EstafetaClient.generate_label(data=data)
        print(response, type(response), bool(response))
        self.assertEqual(bool(response), True)
        self.assertEqual(response['resultCode'], '2')

    def test_wrong_data(self):
        data = {
            'paperType': 1,
            'labelDescriptionList': {
                'content': 'Vasos termicos',
                'deliveryToEstafetaOffice': False,
                'destinationCountryId': 'MX',
                'serviceTypeId': '7000',
                'officeNum': 130,
                'valid': True,
                'parcelTypeId': 6,  # 1 es sobre, 4 es paquete
                'numberOfLabels': 1,
                'returnDocument': False,
                'weight': 10.0,
                'originZipCodeForRouting': '45222',
                'destinationInfo': {
                    'address1': 'Ruben Rodriguez 416',
                    'address2': 'San Andres',
                    'city': 'Guadalajara',
                    'contactName': 'Luis Angel Iniguez Hernandez',
                    'corporateName': 'Luis Angel Iniguez Hernandez',
                    'neighborhood': 'San Andres',
                    'phoneNumber': '3311975232',
                    'state': 'Jalisco',
                    'zipCode': '44810',
                    'valid': True,
                }
            }
        }

        response = estafeta.EstafetaClient.generate_label(data=data)
        print(response)
        self.assertEqual(bool(response), True)
        self.assertEqual(response['resultCode'], '1000')

    def test_empty(self):
        with self.assertRaises(EstafetaWrongData):
            response = estafeta.EstafetaClient.generate_label(data=None)
        with self.assertRaises(EstafetaWrongData):
            response = estafeta.EstafetaClient.generate_label(data='JuanpiToledo')

    def test_empty_fields(self):
        with self.assertRaises(EstafetaWrongData):
            data = {
                'paperType': 1,
                'labelDescriptionList': {
                    'deliveryToEstafetaOffice': False,
                    'officeNum': 130,
                    'valid': True,
                    'parcelTypeId': 6,  # 1 es sobre, 4 es paquete
                    'numberOfLabels': 1,
                    'returnDocument': False,
                    'weight': 10.0,
                    'originZipCodeForRouting': '45222',
                    'destinationInfo': {
                        'address2': 'San Andres',
                        'city': 'Guadalajara',
                        'corporateName': 'Luis Angel Iniguez Hernandez',
                        'neighborhood': 'San Andres',
                        'phoneNumber': '3311975232',
                        'state': 'Jalisco',
                    }
                }
            }
            response = estafeta.EstafetaClient.generate_label(data=data)
