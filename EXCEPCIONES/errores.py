class ZeroTrustBaseError(Exception):
    def __init__(self, codigo, mensaje):
        self.codigo = codigo
        self.mensaje = mensaje
        super().__init__(f"[{self.codigo}] {self.mensaje}")

# ==========================================
# ERRORES DE SISTEMA DE ARCHIVOS (FIO)
# ==========================================
class FIOError(ZeroTrustBaseError): pass

class ArchivoNoEncontradoError(FIOError):
    def __init__(self, ruta):
        super().__init__("ERR-FIO-001", f"El archivo requerido no existe: {ruta}")

class TamanoExcedidoError(FIOError):
    def __init__(self, tamano_mb, limite_mb):
        super().__init__("ERR-FIO-002", f"Archivo demasiado grande ({tamano_mb:.2f} MB). Límite de seguridad: {limite_mb} MB.")

# ==========================================
# ERRORES DE EMPAQUETADO (HANDLER)
# ==========================================
class HandlerError(ZeroTrustBaseError): pass

class PaqueteCorruptoError(HandlerError):
    def __init__(self):
        super().__init__("ERR-HND-001", "El archivo de firma no tiene un formato JSON válido o le faltan piezas.")

class DecodificacionBase64Error(HandlerError):
    def __init__(self):
        super().__init__("ERR-HND-002", "No se pudieron decodificar los datos en Base64. El archivo podría estar dañado.")

# ==========================================
# ERRORES DE CRIPTOGRAFÍA Y PKI (CA / KEYMANAGER)
# ==========================================
class CriptoError(ZeroTrustBaseError): pass

class FormatoClaveInvalidoError(CriptoError):
    def __init__(self):
        super().__init__("ERR-CRY-001", "El archivo no contiene una clave privada válida o está corrupto.")

class FirmaCSRInvalidaError(CriptoError):
    def __init__(self):
        super().__init__("ERR-CRY-002", "La firma de la petición (CSR) no coincide con la identidad solicitada.")

# ==========================================
# ERRORES DE SEGURIDAD CRÍTICA (VALIDADOR)
# ==========================================
class ValidacionSeguridadError(ZeroTrustBaseError): pass

class IdentidadFalsaError(ValidacionSeguridadError):
    def __init__(self):
        super().__init__("ERR-SEC-001", "CRÍTICO: El certificado del usuario NO pertenece a esta empresa (Fallo en la Cadena de Confianza).")

class DocumentoAlteradoError(ValidacionSeguridadError):
    def __init__(self):
        super().__init__("ERR-SEC-002", "CRÍTICO: La firma matemática no coincide. El documento HA SIDO MANIPULADO.")