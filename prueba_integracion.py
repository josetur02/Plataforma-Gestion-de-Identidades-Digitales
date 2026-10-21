from KEYMANAGER.keymanager import KeyManager
from CA.AutoridadCertificadora import AutoridadCertificadora
import os
from SIGN.firma_manager import Firmador
from VALIDADOR.validador import Validador

def simular_flujo_completo():
    print("=== INICIANDO SISTEMA ZERO TRUST ===\n")
    
    # ---------------------------------------------------------
    # FASE 1: IDENTIDADES (CA y Empleado)
    # ---------------------------------------------------------
    print("--- FASE 1: GENERACIÓN DE IDENTIDADES ---")
    km = KeyManager(directorio_base="datos_empleado")
    pki = AutoridadCertificadora(nombre_ca="Acme Corp Root CA", directorio_base="datos_servidor")
    
    pki.inicializar_ca()
    
    clave_empleado = km.generar_par_claves()
    km.guardar_clave_privada(clave_empleado, "clave_empleado.pem")
    
    _, ruta_csr = km.generar_csr(
        private_key=clave_empleado, 
        nombre_empleado="Ana Torres", 
        nombre_empresa="Acme Corp", 
        nombre_archivo="peticion_ana.csr"
    )
    
    ruta_cert_ana = pki.emitir_certificado(ruta_csr, "certificado_ana.crt")

    # ---------------------------------------------------------
    # FASE 2: CREACIÓN Y FIRMA DEL DOCUMENTO
    # ---------------------------------------------------------
    print("\n--- FASE 2: FIRMA DE DOCUMENTO ---")
    # 1. Creamos un contrato de prueba
    ruta_contrato = "contrato_prueba.txt"
    with open(ruta_contrato, "w") as f:
        f.write("Yo, Ana Torres, apruebo la transferencia de 10.000 euros.")
    
    # 2. Ana usa el Módulo de Firma
    firmador = Firmador()
    ruta_sobre_digital = firmador.firmar_y_empaquetar(
        ruta_archivo=ruta_contrato,
        clave_privada=clave_empleado,
        ruta_certificado_usuario=ruta_cert_ana,
        ruta_salida="contrato_oficial.json"
    )

    # ---------------------------------------------------------
    # FASE 3: VALIDACIÓN DEL RECEPTOR
    # ---------------------------------------------------------
    print("\n--- FASE 3: VALIDACIÓN (Zero Trust) ---")
    # 1. Juan recibe el JSON y usa el Validador pasándole el certificado de la empresa
    ruta_ca_maestra = os.path.join("datos_servidor", "ca_cert.pem")
    validador = Validador(ruta_ca_maestra=ruta_ca_maestra)
    
    # 2. El sistema comprueba si puede confiar en el archivo
    validador.validar_sobre_digital(ruta_sobre=ruta_sobre_digital)

    print("\n=== PRUEBA COMPLETADA ===")

if __name__ == "__main__":
    simular_flujo_completo()