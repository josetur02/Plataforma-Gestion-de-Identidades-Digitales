import json
import base64
import binascii

from FIO.fio import GestorArchivos
from EXCEPCIONES.errores import PaqueteCorruptoError, DecodificacionBase64Error

class HandlerSobreDigital:
    @staticmethod
    def empaquetar(contenido_bytes, firma_bytes, certificado_bytes, ruta_salida):
        """Convierte los datos binarios a texto seguro (Base64) y crea el JSON."""
        sobre = {
            "documento_base64": base64.b64encode(contenido_bytes).decode('utf-8'),
            "firma_base64": base64.b64encode(firma_bytes).decode('utf-8'),
            "certificado_adjunto_base64": base64.b64encode(certificado_bytes).decode('utf-8')
        }
        
        # Convertimos el diccionario a una cadena de texto JSON
        texto_json = json.dumps(sobre, indent=4)
        
        # Delegamos la escritura al gestor de archivos
        GestorArchivos.escribir_texto(ruta_salida, texto_json)
        return ruta_salida

    @staticmethod
    def desempaquetar(ruta_sobre):
        """Abre el JSON de forma segura y devuelve los bytes originales."""
        texto_json = GestorArchivos.leer_texto(ruta_sobre)
        
        # 1. Comprobamos la integridad del archivo (¿Es un JSON válido? ¿Tiene las 3 piezas?)
        try:
            sobre = json.loads(texto_json)
            doc_b64 = sobre["documento_base64"]
            firma_b64 = sobre["firma_base64"]
            cert_b64 = sobre["certificado_adjunto_base64"]
        except (json.JSONDecodeError, KeyError):
            raise PaqueteCorruptoError()
            
        # 2. Comprobamos la integridad de los datos (¿El Base64 está intacto?)
        try:
            contenido_bytes = base64.b64decode(doc_b64)
            firma_bytes = base64.b64decode(firma_b64)
            certificado_bytes = base64.b64decode(cert_b64)
        except (ValueError, binascii.Error):
            raise DecodificacionBase64Error()
        
        return contenido_bytes, firma_bytes, certificado_bytes