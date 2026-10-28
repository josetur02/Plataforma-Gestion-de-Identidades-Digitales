import os
from EXCEPCIONES.errores import ArchivoNoEncontradoError, TamanoExcedidoError

class GestorArchivos:
    LIMITE_TAMANO_MB = 50 

    @staticmethod
    def verificar_existencia(ruta):
        if not os.path.exists(ruta):
            raise ArchivoNoEncontradoError(ruta)
        return True

    @staticmethod
    def verificar_tamano(ruta, limite_mb=LIMITE_TAMANO_MB):
        GestorArchivos.verificar_existencia(ruta)
        tamano_bytes = os.path.getsize(ruta)
        tamano_mb = tamano_bytes / (1024 * 1024)
        
        if tamano_mb > limite_mb:
            # Usamos nuestro error personalizado de seguridad
            raise TamanoExcedidoError(tamano_mb, limite_mb)
        return True

    @staticmethod
    def leer_bytes(ruta):
        """Lee archivos binarios (claves, certificados, firmas)."""
        GestorArchivos.verificar_tamano(ruta)
        with open(ruta, 'rb') as f:
            return f.read()

    @staticmethod
    def escribir_bytes(ruta, contenido):
        """Guarda datos matemáticos puros en el disco."""
        directorio = os.path.dirname(ruta)
        if directorio:
            os.makedirs(directorio, exist_ok=True)

        with open(ruta, 'wb') as f:
            f.write(contenido)
        return ruta

    @staticmethod
    def leer_texto(ruta, encoding='utf-8'):
        """Lee archivos de texto plano (contratos, JSON)."""
        GestorArchivos.verificar_tamano(ruta)
        with open(ruta, 'r', encoding=encoding) as f:
            return f.read()
    
    @staticmethod
    def escribir_texto(ruta, contenido, encoding='utf-8'):
        """Guarda archivos de texto legible en el disco."""
        directorio = os.path.dirname(ruta)
        if directorio:
            os.makedirs(directorio, exist_ok=True)
            
        with open(ruta, 'w', encoding=encoding) as f:
            f.write(contenido)
        return ruta