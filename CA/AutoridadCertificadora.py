import os
import datetime
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from cryptography.x509.oid import NameOID

# Importamos nuestro gestor de archivos seguro
from FIO.fio import GestorArchivos

class AutoridadCertificadora:
    def __init__(self, nombre_ca="TFG Root CA", directorio_base="datos_ca"):
        self.nombre_ca = nombre_ca
        self.directorio_base = directorio_base
        
        # Rutas maestras
        self.ruta_clave_privada = os.path.join(self.directorio_base, "ca_key.pem")
        self.ruta_certificado = os.path.join(self.directorio_base, "ca_cert.pem")

    def inicializar_ca(self):
        """
        Crea la identidad de la CA maestra si no existe.
        """
        print("[PKI] Inicializando nueva Autoridad Certificadora Maestra...")
        
        # Si ya existe, no hacemos nada para no sobrescribir la CA original
        if os.path.exists(self.ruta_clave_privada) and os.path.exists(self.ruta_certificado):
            print("[PKI] La CA ya existe. No se sobrescribirá nada.")
            return

        # 1. Generar clave privada de la CA
        private_key = ec.generate_private_key(ec.SECP256R1())
        
        # 2. Crear certificado autofirmado para la CA
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, self.nombre_ca),
            x509.NameAttribute(NameOID.COMMON_NAME, f"{self.nombre_ca} Root"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=3650) # 10 años
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True
        ).sign(private_key, hashes.SHA256())

        # 3. Guardar de forma segura usando el gestor FIO
        GestorArchivos.escribir_bytes(
            self.ruta_clave_privada,
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )
        GestorArchivos.escribir_bytes(
            self.ruta_certificado,
            cert.public_bytes(serialization.Encoding.PEM)
        )
        
        print("[PKI] Autoridad Certificadora creada con éxito.")

    def emitir_certificado(self, ruta_csr, nombre_archivo_salida):
        """
        Firma una petición (CSR) y devuelve un certificado oficial.
        """
        print(f"[PKI] Procesando petición CSR desde: {ruta_csr}")
        
        # 1. Cargar datos de la CA leyendo de forma segura
        key_bytes = GestorArchivos.leer_bytes(self.ruta_clave_privada)
        ca_private_key = serialization.load_pem_private_key(key_bytes, password=None)
        
        cert_bytes = GestorArchivos.leer_bytes(self.ruta_certificado)
        ca_cert = x509.load_pem_x509_certificate(cert_bytes)
        
        # 2. Cargar el CSR del usuario
        csr_bytes = GestorArchivos.leer_bytes(ruta_csr)
        csr = x509.load_pem_x509_csr(csr_bytes)
        
        if not csr.is_signature_valid:
            raise ValueError("[ERROR] La firma del CSR no es válida.")

        # 3. Construir el nuevo certificado
        cert_builder = x509.CertificateBuilder().subject_name(
            csr.subject
        ).issuer_name(
            ca_cert.subject
        ).public_key(
            csr.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.now(datetime.timezone.utc)
        ).not_valid_after(
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365) # 1 año para usuarios
        ).add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True
        )

        # 4. Firmar el certificado con la clave maestra de la CA
        certificado_final = cert_builder.sign(ca_private_key, hashes.SHA256())
        
        # 5. Guardar el certificado generado
        ruta_salida = os.path.join(self.directorio_base, nombre_archivo_salida)
        GestorArchivos.escribir_bytes(
            ruta_salida,
            certificado_final.public_bytes(serialization.Encoding.PEM)
        )
        
        print(f"[PKI] ¡Certificado emitido y firmado! Guardado en: {ruta_salida}")
        return ruta_salida