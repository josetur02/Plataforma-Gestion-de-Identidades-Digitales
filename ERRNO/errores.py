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
*  Módulo Errno. 
*  Gestión de errores y excepciones.
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

class Errores(Exception):
    """
    Clase base para todos los posibles errores.
    Proporciona un código de error y un mensaje descriptivo.
    """
    def __init__(self, codigo: str, mensaje: str):
        self.codigo = codigo
        self.mensaje = mensaje
        super().__init__(f"[{self.codigo}] {self.mensaje}")


"""
******************************************************************************
*                     ERRORES MÓDULO FIO
******************************************************************************
"""

class FIO_Errno(Errores): pass

class RutaNoEncontradaError(FIO_Errno):
    """
    Error lanzado cuando una ruta no es encontrada.
    """
    def __init__(self, ruta: str):
        super().__init__("ERR-FIO-001", f"La ruta requerida no existe: {ruta}")

class TamanoExcedidoError(FIO_Errno):
    """
    Error lanzado cuando un archivo excede el tamaño permitido.
    """
    def __init__(self, tamano_mb: float, limite_mb: int):
        super().__init__("ERR-FIO-002", f"Archivo demasiado grande ({tamano_mb:.2f} MB). Límite de seguridad: {limite_mb} MB.")

class ArchivoNoEncontradoError(FIO_Errno):
    """
    Error lanzado cuando un archivo no es encontrado.
    """
    def __init__(self, ruta: str):
        super().__init__("ERR-FIO-003", f"El archivo requerido no existe: {ruta}")