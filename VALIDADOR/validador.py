from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature
from cryptography import x509
from HANDLER.handler import HandlerSobreDigital
from FIO.fio import GestorArchivos

class Validador:
    def __init__(self, ruta_ca_maestra):
        """El validador necesita conocer el certificado de la CA para confiar en los usuarios."""
        self.handler = HandlerSobreDigital()
        
        # Lectura segura del certificado raíz
        cert_bytes = GestorArchivos.leer_bytes(ruta_ca_maestra)
        self.ca_cert = x509.load_pem_x509_certificate(cert_bytes)
        self.ca_public_key = self.ca_cert.public_key()

    def validar_sobre_digital(self, ruta_sobre):
        print(f"\n[VALIDADOR] Analizando paquete: {ruta_sobre}")
        
        contenido, firma_bytes, cert_bytes = self.handler.desempaquetar(ruta_sobre)
        cert_usuario = x509.load_pem_x509_certificate(cert_bytes)

        # --- PASO 1: VALIDAR A LA PERSONA (Cadena de Confianza) ---
        print("[VALIDADOR] Comprobando si el usuario pertenece a la empresa...")
        try:
            self.ca_public_key.verify(
                cert_usuario.signature,
                cert_usuario.tbs_certificate_bytes,
                ec.ECDSA(cert_usuario.signature_hash_algorithm)
            )
            print("  -> Identidad confirmada por la CA.")
        except InvalidSignature:
            print("  -> [ERROR] El certificado es FALSO o no pertenece a esta empresa.")
            return False

        # --- PASO 2: VALIDAR EL DOCUMENTO (Integridad) ---
        print("[VALIDADOR] Comprobando que el documento no ha sido modificado...")
        clave_publica_usuario = cert_usuario.public_key()
        try:
            clave_publica_usuario.verify(
                firma_bytes,
                contenido,
                ec.ECDSA(hashes.SHA256())
            )
            print("  -> Integridad confirmada.")
            print("[VALIDADOR] >>> RESULTADO: 100% VÁLIDO Y CONFIABLE <<<")
            return True
        except InvalidSignature:
            print("  -> [ERROR] El documento ha sido alterado tras la firma.")
            return False