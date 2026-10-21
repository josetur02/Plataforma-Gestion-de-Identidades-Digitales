import logging
import os
from datetime import datetime

class AuditorZeroTrust:
    _instancia = None

    def __new__(cls):
        # Implementamos el patrón Singleton para que solo haya 1 logger en toda la app
        if cls._instancia is None:
            cls._instancia = super(AuditorZeroTrust, cls).__new__(cls)
            cls._instancia._configurar_logger()
        return cls._instancia

    def _configurar_logger(self):
        self.logger = logging.getLogger("ZeroTrustLogger")
        self.logger.setLevel(logging.DEBUG)

        # Evitar que se dupliquen los logs si se inicializa varias veces
        if not self.logger.handlers:
            # 1. Formato estandarizado de los logs
            formato = logging.Formatter(
                fmt="[%(asctime)s] [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            # 2. Guardar en archivo físico (Auditoría permanente)
            directorio_logs = "logs"
            if not os.path.exists(directorio_logs):
                os.makedirs(directorio_logs)
                
            archivo_handler = logging.FileHandler(os.path.join(directorio_logs, "auditoria_seguridad.log"), encoding='utf-8')
            archivo_handler.setLevel(logging.INFO)
            archivo_handler.setFormatter(formato)

            # 3. Mostrar en la consola de comandos
            consola_handler = logging.StreamHandler()
            consola_handler.setLevel(logging.INFO)
            consola_handler.setFormatter(formato)

            self.logger.addHandler(archivo_handler)
            self.logger.addHandler(consola_handler)

    # Métodos de registro según la gravedad
    def info(self, modulo, mensaje):
        """Para operaciones exitosas (ej. Certificado emitido)."""
        self.logger.info(f"[{modulo}] {mensaje}")

    def advertencia(self, modulo, mensaje):
        """Para cosas extrañas pero no fatales (ej. Intentar crear CA que ya existe)."""
        self.logger.warning(f"[{modulo}] {mensaje}")

    def error(self, modulo, mensaje):
        """Para fallos del sistema o de formato (ej. Archivo no encontrado)."""
        self.logger.error(f"[{modulo}] {mensaje}")

    def critico(self, modulo, mensaje):
        """Para brechas de seguridad (ej. Firmas alteradas)."""
        self.logger.critical(f"[{modulo}] {mensaje} !!!BRECHA DE SEGURIDAD!!!")