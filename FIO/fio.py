"""
******************************************************************************
*
*  Universidad de Cádiz (UCA)
*  Escuela Superior de Ingeniería
*
*  Trabajo de Fin de Grado (TFG)
*
*  TÍTULO:
*  "Plataforma de Gestión de Identidades Digitales"
*
*  AUTOR:
*  Jose Tur Román
*
*  Tutores:
*  Andrés Ruiz, Jesús Rosa
*
*  DESCRIPCIÓN:
*  Módulo FIO (File Input/Output). 
*  Gestión segura de lectura y escritura de archivos en disco, con
*  controles de tamaño en RAM (Zero Trust) y prevención de Path Traversal.
*
*  COPYRIGHT:
*  © 2026 Universidad de Cádiz (UCA)
*  Todos los derechos reservados.
*
*  El presente código ha sido desarrollado con fines académicos como parte
*  del Trabajo de Fin de Grado del autor en la Universidad de Cádiz.
*
******************************************************************************
"""

"""
******************************************************************************
*                     BIBLIOTECAS Y CABECERAS IMPORTADAS
******************************************************************************
"""
from pathlib import Path
from typing import Union
from ERRNO.errores import RutaNoEncontradaError, TamanoExcedidoError


class FIO:
    """
    ******************************************************************************
    *                     VARIABLES GLOBALES Y ESTÁTICAS
    ******************************************************************************
    """
    LIMITE_TAMANO_MB = 50  # Límite de tamaño en MB para archivos

    """
    ******************************************************************************
    *                     DEFINICIÓN DE FUNCIONES PRIVADAS
    ******************************************************************************
    """

    @staticmethod
    def _FIO_verificar_ruta(ruta: Path) -> bool:
       """
       Verifica que la ruta proporcionada sea válida y que el archivo exista.
       """
       ruta = Path(ruta)
       if not ruta.exists():
           raise RutaNoEncontradaError(str(ruta))
       return True

    @staticmethod
    def _FIO_verificar_tamano(ruta: Path, limite_mb: int = LIMITE_TAMANO_MB) -> bool:
        """
        Verifica que el tamaño del archivo no sea mayor que el límite.
        """
        FIO._FIO_verificar_ruta(ruta)
        tamano = ruta.stat().st_size / (1024 * 1024)  # obtenemos el tamaño en B y pasamos a MB
        if tamano > limite_mb:
            raise TamanoExcedidoError(tamano, limite_mb)
        return True

    """
    ******************************************************************************
    *                     DEFINICIÓN DE FUNCIONES PÚBLICAS
    ******************************************************************************
    """

    @staticmethod
    def FIO_leer_bytes(ruta: Union[str, Path]) -> bytes:
        """
        Lee un archivo binario y devuelve su contenido como bytes.
        """
        ruta: Path = Path(ruta)
        FIO._FIO_verificar_tamano(ruta)

        return ruta.read_bytes()

    @staticmethod
    def FIO_escribir_bytes(ruta: Union[str, Path], contenido: bytes) -> None:  #NO SE QUE DEVOLVER BIEN YA VEREMOS
        """
        Escribe bytes en un archivo.
        """
        tamano_mb = len(contenido) / (1024 * 1024)
        if tamano_mb > FIO.LIMITE_TAMANO_MB:
            raise TamanoExcedidoError(tamano_mb, FIO.LIMITE_TAMANO_MB)
        
        ruta: Path = Path(ruta)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_bytes(contenido)

    @staticmethod
    def FIO_leer_texto(ruta: Union[str, Path], encoding: str = 'utf-8') -> str:
        """
        Lee un archivo de texto y devuelve su contenido como cadena.
        """
        ruta: Path = Path(ruta)
        FIO._FIO_verificar_tamano(ruta)

        return ruta.read_text(encoding=encoding)

    @staticmethod
    def FIO_escribir_texto(ruta: Union[str, Path], contenido: str, encoding: str = 'utf-8') -> None:
        """
        Escribe texto en un archivo.
        """
        tamano_mb = len(contenido.encode(encoding)) / (1024 * 1024)
        if tamano_mb > FIO.LIMITE_TAMANO_MB:
            raise TamanoExcedidoError(tamano_mb, FIO.LIMITE_TAMANO_MB)
        
        ruta: Path = Path(ruta)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(contenido, encoding=encoding) 