import os
from xml.etree import ElementTree

import requests
from unidecode import unidecode
from zeep import Client, Transport

import estafeta
from estafeta.core.error import EstafetaWrongData, EstafetaEmptyField


class EstafetaClient(object):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    @property
    def user(self):
        if estafeta.user is not None:
            return estafeta.user
        raise EstafetaEmptyField("User is not assigned")

    @property
    def id(self):
        if estafeta.id is not None:
            return estafeta.id
        raise EstafetaEmptyField("Id is not assigned")

    @property
    def password(self):
        if estafeta.password is not None:
            return estafeta.password
        raise EstafetaEmptyField("Password is not assigned")

    @property
    def account_number(self):
        if estafeta.account_number is not None:
            return estafeta.account_number
        raise EstafetaEmptyField("Account Number is not assigned")

    @property
    def url_label(self):
        if estafeta.production is not None:
            if type(estafeta.production) is bool:
                return estafeta.core.__url_label__[estafeta.production]
            raise EstafetaWrongData("Production variable have to be boolean")
        raise EstafetaEmptyField("Production variable is mandatory to retrieve a URL")

    @property
    def url_tracking(self):
        if estafeta.production is not None:
            if type(estafeta.production) is bool:
                return estafeta.core.__url_tracking__[estafeta.production]
            raise EstafetaWrongData("Production variable have to be boolean")
        raise EstafetaEmptyField("Production variable is mandatory to retrieve a URL")

    @property
    def url_quote(self):
        if estafeta.production is not None:
            if type(estafeta.production) is bool:
                return estafeta.core.__url_quote__[estafeta.production]
            raise EstafetaWrongData("Production variable have to be boolean")
        raise EstafetaEmptyField("Production variable is mandatory to retrieve a URL")

    @classmethod
    def __validate_label__(cls, data):
        error = ''

        instance = EstafetaClient()

        # Validates the mandatory fields in the data
        for name in ['paperType', 'labelDescriptionList']:
            if not name in data:
                error += name + ', '
        if error is not '':
            raise EstafetaWrongData('Fields \"{}\" are mandatory'.format(error[:-2]))

        # Validates the mandatory fields in labelDescriptionList dict
        labelDescriptionList = data.pop('labelDescriptionList')
        for name in ['content', 'deliveryToEstafetaOffice', 'destinationInfo', 'numberOfLabels', 'officeNum',
                     'parcelTypeId', 'returnDocument', 'serviceTypeId', 'valid', 'weight', 'originZipCodeForRouting', ]:
            if not name in labelDescriptionList:
                error += name + ', '
            elif error is '' and type(labelDescriptionList[name]) is str:
                labelDescriptionList[name] = unidecode(labelDescriptionList[name])
        if error is not '':
            raise EstafetaWrongData('In LabelDescription, the fields \"{}\" are mandatory'.format(error[:-2]))

        # Validates the mandatory fields in destinationInfo
        destinationInfo = labelDescriptionList.pop('destinationInfo')
        for name in ['address1', 'city', 'contactName', 'corporateName', 'neighborhood', 'state', 'valid', 'zipCode', ]:
            if not name in destinationInfo:
                error += name + ', '
            elif error is '' and type(destinationInfo[name]) is str:
                destinationInfo[name] = unidecode(destinationInfo[name])
        if error is not '':
            raise EstafetaWrongData('In DestinationInfo, the fields \"{}\" are mandatory'.format(error[:-2]))
        # Fills no mandatory fields
        for name in ['address2', 'phoneNumber', 'cellPhone']:
            destinationInfo[name] = unidecode(destinationInfo.get(name, ''))
        if 'customerNumber' not in destinationInfo:
            destinationInfo['customerNumber'] = estafeta.account_number
        destinationInfo = open(os.path.dirname(__file__) + '/wsdl/shipment_info.xml').read().format(
            data=destinationInfo,
            shipment_info='destinationInfo'
        )

        # Validates the mandatory fields in originInfo
        originInfo = labelDescriptionList.pop('originInfo', '')
        if originInfo is not '':
            for name in ['address1', 'city', 'contactName', 'corporateName', 'neighborhood', 'state', 'valid',
                         'zipCode', ]:
                if not name in originInfo:
                    error += name + ', '
                elif error is '' and type(originInfo[name]) is str:
                    originInfo[name] = unidecode(originInfo[name])
            if error is not '':
                raise EstafetaWrongData('In OriginInfo, the fields \"{}\" are mandatory'.format(error[:-2]))
            for name in ['address2', 'phoneNumber', 'cellPhone']:
                originInfo[name] = unidecode(originInfo.get(name, ''))
            if 'customerNumber' not in originInfo:
                originInfo['customerNumber'] = unidecode(estafeta.account_number)
            originInfo = open(os.path.dirname(__file__) + '/wsdl/shipment_info.xml').read().format(data=originInfo, shipment_info='originInfo')

        return open(os.path.dirname(__file__) + '/wsdl/create_label.xml').read().format(
            data=labelDescriptionList,
            customerNumber=instance.account_number,
            username=instance.user,
            password=instance.password,
            id=instance.id,
            paperType=data['paperType'],
            originInfo=originInfo,
            destinationInfo=destinationInfo,
        )

    @classmethod
    def generate_label(cls, data=None):
        if type(data) is not dict:
            raise EstafetaWrongData("Data have to be a dictionary")
        wsdl = cls.__validate_label__(data=data)
        headers = {
            'content-type': 'text/xml',
            'SOAPAction': 'http://axis.frontend.hydra.hotelbeds.com/getHotelValuedAvail'
        }
        instance = EstafetaClient()
        r = requests.post(url=instance.url_label, data=wsdl, headers=headers, verify=False)
        tree = ElementTree.fromstring(r.content)
        body = tree.find('{http://schemas.xmlsoap.org/soap/envelope/}Body')
        elements = body.findall('multiRef')
        res = dict()
        for element in elements:
            if element.attrib['id'] is 'id1':
                continue
            for child in element:
                res[child.tag] = child.text
        return res

    @classmethod
    def __valid_track__(cls, data=None):

        error = ''

        # Validates data
        for name in ['searchType', 'searchConfiguration']:
            if name not in data:
                error += name + ', '
        if error is not '':
            raise EstafetaWrongData('Fields \"{}\" are mandatory'.format(error[:-2]))

        # Validates searchType
        searchType = data.pop('searchType')
        if 'type' not in searchType:
            raise EstafetaWrongData('In searchType, the field type is mandatory')
        if searchType['type'] is 'R':
            if 'waybillRange' not in searchType:
                raise EstafetaWrongData('In searchType, when type has the value \'R\', waybillRange field is mandatory.')
            stype = searchType.pop('waybillRange')
            for name in ['initialWaybill', 'finalWaybill']:
                if name not in stype:
                    error += name + ', '
            if error is not '':
                raise EstafetaWrongData('In waybillRange, fields \"{}\" are mandatory'.format(error[:-2]))
        elif searchType['type'] is 'L':
            if 'waybillList' not in searchType:
                raise EstafetaWrongData('In searchType, when type has the value \'L\', waybillList field is mandatory.')
            stype = searchType.pop('waybillList')
            for name in ['waybillType', 'waybills']:
                if name not in stype:
                    error += name + ', '
            if error is not '':
                raise EstafetaWrongData('In waybillList, fields \"{}\" are mandatory'.format(error[:-2]))
        else:
            raise EstafetaWrongData('In searchType, the field type can only have \'R\' or \'L\' as parameter')

        # Validates searchConfiguration
        searchConfiguration = data.pop('searchConfiguration')
        for name in ['includeDimensions', 'includeWaybillReplaceData', 'includeReturnDocumentData',
                     'includeMultipleServiceData', 'includeInternationalData', 'includeSignature',
                     'includeCustomerInfo']:
            searchConfiguration[name] = searchConfiguration.get(name, 0)

        # Validates historyConfiguration
        historyConfiguration = searchConfiguration.pop('historyConfiguration', {})
        if 'includeHistory' not in historyConfiguration:
            historyConfiguration['includeHistory'] = 0
            historyConfiguration['historyType'] = ''
        else:
            if type(historyConfiguration['includeHistory']) is not int:
                raise EstafetaWrongData('In historyConfiguration, the field includeHistory can only be an integer')
            if 1 < historyConfiguration['includeHistory'] < 0:
                raise EstafetaWrongData('In historyConfiguration, the field includeHistory can only be an 1 or 0')
            if 'historyType' not in historyConfiguration:
                if historyConfiguration['includeHistory'] is 1:
                    raise EstafetaWrongData(
                        'In historyConfiguration, the field historyType can not be empty when includeHistory is 1'
                    )

        # Validates filterType
        filter = searchConfiguration.pop('filterType', {})
        if 'filterInformation' not in filter:
            filter['filterInformation'] = 0
            filter['filterType'] = ''
        else:
            if type(filter['filterInformation']) is not int:
                raise EstafetaWrongData('In filter, the field filterInformation can only be an integer')
            if 1 < filter['filterInformation'] < 0:
                raise EstafetaWrongData('In filter, the field filterInformation can only be an 1 or 0')
            if 'filterType' not in filter:
                if filter['filterInformation'] is 1:
                    raise EstafetaWrongData(
                        'In filterType, the field filterType can not be empty when filterInformation is 1'
                    )

        instance = EstafetaClient()

        transport = Transport()
        transport.session.verify = False
        client = Client(instance.url_tracking, transport=transport)

        filter = client.get_type('ns0:Filter')(**filter)
        historyConfiguration = client.get_type('ns0:HistoryConfiguration')(**historyConfiguration)
        searchConfiguration['historyConfiguration'] = historyConfiguration
        searchConfiguration['filterType'] = filter
        searchConfiguration = client.get_type('ns0:SearchConfiguration')(**searchConfiguration)

        searchTypeList = ['waybillRange', 'WaybillRange'] if searchType['type'] is 'R' else ['waybillList',
                                                                                             'WaybillList']
        stype = client.get_type('ns0:%s' % searchTypeList[1])(**stype)
        searchType[searchTypeList[0]] = stype
        searchType = client.get_type('ns0:SearchType')(**searchType)

        client.transport.session.close()

        return {
            'searchType': searchType,
            'searchConfiguration': searchConfiguration,
        }

    @classmethod
    def track_package(cls, data=None):
        if type(data) is not dict:
            raise EstafetaWrongData("Data have to be a dictionary")

        wsdl = cls.__valid_track__(data=data)
        instance = EstafetaClient()

        transport = Transport()
        transport.session.verify = False
        client = Client(instance.url_tracking, transport=transport)

        wsdl['suscriberId'] = instance.id
        wsdl['login'] = instance.user
        wsdl['password'] = instance.password
        response = client.service.ExecuteQuery(**wsdl)
        client.transport.session.close()
        return response

    @classmethod
    def __valid_quote__(cls, data=None):

        error = ''

        for name in ['esFrecuencia', 'esLista', 'esPaquete', 'datosOrigen', 'datosDestino']:
            if name not in data:
                error += name + ', '
        if error is not '':
            raise EstafetaWrongData('Fields \"{}\" are mandatory'.format(error[:-2]))

        if data['esPaquete']:
            for name in ['alto', 'largo', 'ancho', 'peso']:
                if name not in data:
                    error += name + ', '
            if error is not '':
                raise EstafetaWrongData('When \'esPaquete\' is True, fields \"{}\" ara mandatory'.format(error[:-2]))
        else:
            for name in ['alto', 'largo', 'ancho', 'peso']:
                data[name] = 0

        instance = EstafetaClient()

        transport = Transport()
        transport.session.verify = False
        client = Client(instance.url_quote, transport=transport)

        data['tipoEnvio'] = client.get_type("ns0:TipoEnvio")(
            EsPaquete=data.pop('esPaquete'),
            Largo=data.pop('largo'),
            Alto=data.pop('alto'),
            Ancho=data.pop('ancho'),
            Peso=data.pop('peso'),
        )

        return data

    @classmethod
    def quote(cls, data=None):
        if type(data) is not dict:
            raise EstafetaWrongData("Data have to be a dictionary")
        wsdl = cls.__valid_quote__(data=data)
        instance = EstafetaClient()

        transport = Transport()
        transport.session.verify = False
        client = Client(instance.url_quote, transport=transport)

        wsdl['idusuario'] = instance.id
        wsdl['usuario'] = instance.user
        wsdl['contra'] = instance.password

        response = client.service.FrecuenciaCotizador(**wsdl)
        client.transport.session.close()

        return response[0]