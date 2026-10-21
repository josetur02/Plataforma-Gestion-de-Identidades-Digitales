from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from HANDLER.handler import HandlerSobreDigital
from FIO.fio import GestorArchivos

# Importamos nuestro sistema de auditoría
from LOGGER.logger import AuditorZeroTrust

class Firmador:
    def __init__(self):
        self.handler = HandlerSobreDigital()
        self.logger = AuditorZeroTrust() # Inicializamos el auditor

    def firmar_y_empaquetar(self, ruta_archivo, clave_privada, ruta_certificado_usuario, ruta_salida):
        self.logger.info("FIRMADOR", f"Procesando documento para firma: {ruta_archivo}")
        
        # 1. Leer archivo original y certificado de forma segura
        contenido = GestorArchivos.leer_bytes(ruta_archivo)
        certificado_bytes = GestorArchivos.leer_bytes(ruta_certificado_usuario)

        # 2. Calcular firma matemática
        firma_bytes = clave_privada.sign(
            contenido,
            ec.ECDSA(hashes.SHA256())
        )

        # 3. Delegar la creación del archivo al Handler
        ruta_final = self.handler.empaquetar(contenido, firma_bytes, certificado_bytes, ruta_salida)
        
        # Registramos el éxito en el log en lugar de usar un simple print
        self.logger.info("FIRMADOR", f"Éxito. Sobre digital guardado en: {ruta_final}")
        return ruta_final