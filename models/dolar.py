import xml.etree.ElementTree as ET
import requests
from odoo.http import Controller,route,request
from odoo import api, fields, models, tools,http, _

class TRMService(models.Model):
    _name = 'trm.service'

    trm_value = fields.Float(string='TRM Value')

    @api.model
    def update_trm_value(self):
        soap_body = """
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:act="http://action.trm.services.generic.action.superfinanciera.nexura.sc.com.co/">
                <soapenv:Header/>
                <soapenv:Body>
                    <act:queryTCRM></act:queryTCRM>
                </soapenv:Body>
            </soapenv:Envelope>
        """

        headers = {
            'Content-Type': 'text/xml',
        }

        response = requests.post(
            'https://www.superfinanciera.gov.co/SuperfinancieraWebServiceTRM/TCRMServicesWebService/TCRMServicesWebService',
            headers=headers,
            data=soap_body
        )
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            value_element = root.find('.//value')
            if value_element is not None:
                trm_value = float(value_element.text)
                trm_service_record = self.env['trm.service'].sudo().search([], limit=1)
                if trm_service_record:
                    trm_service_record.write({'trm_value': trm_value})
                else:
                    self.env['trm.service'].sudo().create({'trm_value': trm_value})
            else:
                raise ValueError("No se encontró el valor de la TRM en la respuesta XML")
        else:
            raise ConnectionError(f"Error al realizar la solicitud: {response.status_code}")

class MyWebController(http.Controller):
    @http.route('/get_trm_value', type='http', auth='public', website=True)
    def get_trm_value(self, **kwargs):
        trm_service_record = request.env['trm.service'].sudo().search([], order='id desc', limit=1)
        if trm_service_record:
            trm_value = trm_service_record.trm_value
            return str(trm_value)
        else:
            return "No se encontró ningún valor de TRM en la base de datos"

