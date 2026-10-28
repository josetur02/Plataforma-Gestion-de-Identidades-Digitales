"""
******************************************************************************
*
*  Universidad de Cádiz (UCA)
*  Escuela Superior de Ingeniería
*
*  Trabajo de Fin de Grado (TFG)
*
*  TÍTULO:
*  "Sistema de Firma Digital Basado en Criptografía de Curva Elíptica (ECC)"
*
*  AUTOR:
*  [Tu Nombre]
*
*  DIRECTOR:
*  [Nombre del Tutor]
*
*  DESCRIPCIÓN:
*  Módulo ERRNO (Gestión de Excepciones). 
*  Define la jerarquía de errores personalizados de la plataforma para 
*  estandarizar la captura de fallos, ocultar detalles técnicos a posibles 
*  atacantes y facilitar la auditoría del sistema (Zero Trust).
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
# No hay dependencias externas. Este módulo provee las clases base.

"""
******************************************************************************
*                     CLASE BASE DE LA PLATAFORMA
******************************************************************************
"""

class Errores(Exception):
    """
    Clase base para todos los errores personalizados de la plataforma.
    Proporciona un código de error y un mensaje descriptivo.
    """
    def __init__(self, codigo: str, mensaje: str):
        self.codigo = codigo
        self.mensaje = mensaje
        super().__init__(f"[{self.codigo}] {self.mensaje}")

