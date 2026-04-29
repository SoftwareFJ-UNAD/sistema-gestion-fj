"""
MÓDULO DE LA CLASE CLIENTE
===========================
Define la clase Cliente con encapsulación de datos personales
y validaciones robustas para nombre, email y teléfono.

Los datos se validan mediante properties (getters/setters) que
protegen el estado interno del objeto y lanzan excepciones
personalizadas cuando los datos son inválidos.

Autor: Victor Morales
Fecha: 2025
"""

import re  # Expresiones regulares para validar formato de email
from clases.excepciones import DatosClienteInvalidosError
from clases.logger import LoggerSistema


class Cliente:
    """
    Clase que representa un cliente del sistema Software FJ.
    
    Atributos privados (encapsulación):
    - _nombre: str
    - _email: str
    - _telefono: str
    
    Los datos se asignan mediante setters que validan cada valor antes
    de almacenarlo, garantizando la integridad de la información.
    """
    
    def __init__(self, nombre, email, telefono):
        """
        Constructor de la clase Cliente.
        
        Parámetros:
        -----------
        nombre : str - Nombre completo (mínimo 3 caracteres)
        email : str  - Correo electrónico (formato usuario@dominio.com)
        telefono : str - Teléfono (solo números, mínimo 7 dígitos)
        
        Excepciones:
        ------------
        DatosClienteInvalidosError - Si algún dato no pasa la validación
        """
        # Inicializar atributos privados como None
        self._nombre = None
        self._email = None
        self._telefono = None
        
        # Usar los setters para asignar y validar
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        
        # Registrar en log la creación exitosa del cliente
        LoggerSistema.registrar_evento(f"Cliente creado exitosamente: {self._nombre}")
    
    # ==================== PROPIEDAD NOMBRE ====================
    
    @property
    def nombre(self):
        """Getter: devuelve el nombre del cliente."""
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        """
        Setter: asigna y valida el nombre del cliente.
        
        Validaciones:
        - No puede estar vacío
        - Debe tener al menos 3 caracteres
        """
        # Validación: nombre no vacío
        if not valor:
            raise DatosClienteInvalidosError("El nombre no puede estar vacío")
        
        # Validación: nombre con longitud mínima
        if len(valor.strip()) < 3:
            raise DatosClienteInvalidosError(
                f"El nombre debe tener al menos 3 caracteres (recibido: '{valor}')"
            )
        
        # Asignación después de validar
        self._nombre = valor.strip()
    
    # ==================== PROPIEDAD EMAIL ====================
    
    @property
    def email(self):
        """Getter: devuelve el email del cliente."""
        return self._email
    
    @email.setter
    def email(self, valor):
        """
        Setter: asigna y valida el email del cliente.
        
        Validaciones:
        - Formato válido usando expresión regular
        - Debe contener @ y un dominio con punto
        """
        if not valor:
            raise DatosClienteInvalidosError("El email no puede estar vacío")
        
        # Expresión regular para validar formato de email
        # Patrón: usuario@dominio.extension
        patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(patron_email, valor.strip()):
            raise DatosClienteInvalidosError(
                f"Email inválido: '{valor}'. Formato requerido: usuario@dominio.com"
            )
        
        self._email = valor.strip().lower()  # Convertir a minúsculas por consistencia
    
    # ==================== PROPIEDAD TELEFONO ====================
    
    @property
    def telefono(self):
        """Getter: devuelve el teléfono del cliente."""
        return self._telefono
    
    @telefono.setter
    def telefono(self, valor):
        """
        Setter: asigna y valida el teléfono del cliente.
        
        Validaciones:
        - Solo caracteres numéricos
        - Mínimo 7 dígitos (estándar colombiano)
        """
        if not valor:
            raise DatosClienteInvalidosError("El teléfono no puede estar vacío")
        
        # Eliminar espacios, guiones y paréntesis para validación
        valor_limpio = valor.strip().replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
        
        # Verificar que solo contenga números
        if not valor_limpio.isdigit():
            raise DatosClienteInvalidosError(
                f"Teléfono inválido: '{valor}'. Debe contener solo números"
            )
        
        # Verificar longitud mínima
        if len(valor_limpio) < 7:
            raise DatosClienteInvalidosError(
                f"Teléfono inválido: debe tener al menos 7 dígitos (tiene {len(valor_limpio)})"
            )
        
        self._telefono = valor_limpio
    
    # ==================== MÉTODOS ADICIONALES ====================
    
    def __str__(self):
        """
        Representación en string del cliente para mostrar en consola.
        
        Retorna:
        --------
        str: Formato "Nombre (Email)"
        """
        return f"{self._nombre} ({self._email})"
    
    def obtener_resumen(self):
        """
        Devuelve un diccionario con los datos del cliente.
        Útil para exportar información a reportes o JSON.
        
        Retorna:
        --------
        dict: Diccionario con nombre, email y teléfono
        """
        return {
            "nombre": self._nombre,
            "email": self._email,
            "telefono": self._telefono
        }