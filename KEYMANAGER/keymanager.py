import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from cryptography.x509.oid import NameOID

# Importamos el FIO, las Excepciones y el nuevo Logger
from FIO.fio import GestorArchivos
from EXCEPCIONES.errores import FormatoClaveInvalidoError
from LOGGER.logger import AuditorZeroTrust

class KeyManager:
    def __init__(self, directorio_base="datos_usuario"):
        self.directorio_base = directorio_base
        self.logger = AuditorZeroTrust() # Inicializamos el auditor

    def generar_par_claves(self):
        self.logger.info("KEYMANAGER", "Generando par de claves ECC (SECP256R1)...")
        private_key = ec.generate_private_key(ec.SECP256R1())
        return private_key

    def guardar_clave_privada(self, private_key, nombre_archivo="mi_clave_privada.pem"):
        ruta_completa = os.path.join(self.directorio_base, nombre_archivo)
        
        pem_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        GestorArchivos.escribir_bytes(ruta_completa, pem_bytes)
        self.logger.info("KEYMANAGER", f"Clave privada guardada en: {ruta_completa}")
        return ruta_completa

    def cargar_clave_privada(self, ruta_archivo="mi_clave_privada.pem"):
        ruta_completa = os.path.join(self.directorio_base, ruta_archivo)

        contenido_bytes = GestorArchivos.leer_bytes(ruta_completa)
        
        try:
            private_key = serialization.load_pem_private_key(
                contenido_bytes,
                password=None
            )
        except ValueError:
            raise FormatoClaveInvalidoError()
            
        self.logger.info("KEYMANAGER", f"Clave privada cargada con éxito desde {ruta_completa}")
        return private_key

    def generar_csr(self, private_key, nombre_empleado, nombre_empresa, nombre_archivo="mi_peticion.csr"):
        self.logger.info("KEYMANAGER", f"Generando CSR para {nombre_empleado}...")
        
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, nombre_empresa),
            x509.NameAttribute(NameOID.COMMON_NAME, nombre_empleado),
        ])

        csr = x509.CertificateSigningRequestBuilder().subject_name(
            subject
        ).sign(private_key, hashes.SHA256())

        ruta_completa = os.path.join(self.directorio_base, nombre_archivo)
        GestorArchivos.escribir_bytes(ruta_completa, csr.public_bytes(serialization.Encoding.PEM))
            
        self.logger.info("KEYMANAGER", f"CSR guardada en: {ruta_completa}")
        return csr, ruta_completa