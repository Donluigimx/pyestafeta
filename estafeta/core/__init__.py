
from estafeta.core.client import EstafetaClient

user = None
password = None
id = None
account_number = None
production = None

from estafeta.core.error import EstafetaWrongData, EstafetaEmptyField

__url_label__ = [
    'https://labelqa.estafeta.com/EstafetaLabel20/services/EstafetaLabelWS?wsdl',
    'https://label.estafeta.com/EstafetaLabel20/services/EstafetaLabelWS?wsdl',
]

__url_tracking__ = [
    'https://trackingqa.estafeta.com/Service.asmx?wsdl',
    'https://tracking.estafeta.com/Service.asmx?wsdl',
]

__url_quote__ = [
    'http://frecuenciacotizador.estafeta.com/Service.asmx?wsdl',
    'http://frecuenciacotizador.estafeta.com/Service.asmx?wsdl',
]
