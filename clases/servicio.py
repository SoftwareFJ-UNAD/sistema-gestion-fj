"""
MÓDULO DE LA CLASE ABSTRACTA SERVICIO
=======================================
Define el contrato (interfaz) que deben cumplir todos los servicios
del sistema. Esta clase no puede instanciarse directamente; solo sirve
como plantilla para las clases hijas (ReservaSalas, AlquilerEquipos, Asesoria).

Principios POA aplicados:
- ABSTRACCIÓN: Se definen métodos abstractos que las hijas deben implementar
- POLIMORFISMO: Cada servicio concreto implementa calcular_costo() de forma diferente

Autor: Victor Morales
Fecha: 2025
"""

from abc import ABC, abstractmethod  # Para definir clases y métodos abstractos
from clases.excepciones import DuracionInvalidaError, CostoInconsistenteError
from clases.logger import LoggerSistema


class Servicio(ABC):
    """
    CLASE ABSTRACTA: Representa un servicio genérico del sistema.
    No se puede instanciar directamente (lanzaría TypeError).
    
    Atributos:
    ----------
    nombre : str - Nombre descriptivo del servicio
    precio_base : float - Precio base por unidad de tiempo (hora)
    DURACION_MAXIMA : int - Constante de clase (24 horas máximo)
    """
    
    # Constante de clase: límite máximo de duración para cualquier servicio
    DURACION_MAXIMA = 24  # Horas
    
    def __init__(self, nombre, precio_base):
        """
        Constructor de la clase abstracta Servicio.
        
        Parámetros:
        -----------
        nombre : str - Nombre del servicio
        precio_base : float - Precio base por hora
        
        Nota: Este constructor es llamado por las clases hijas usando super()
        """
        self.nombre = nombre
        self.precio_base = precio_base
        
        # Registro en log de la creación del servicio
        LoggerSistema.registrar_evento(
            f"Servicio creado: {self.__class__.__name__} - '{nombre}' (${precio_base}/hora)"
        )
    
    def validar_parametros(self, duracion):
        """
        MÉTODO CONCRETO: Valida parámetros comunes a todos los servicios.
        
        Validaciones:
        - duracion debe ser numérica (int o float)
        - duracion debe ser positiva (> 0)
        - duracion no puede exceder DURACION_MAXIMA (24 horas)
        
        Parámetros:
        -----------
        duracion : int/float - Duración del servicio en horas
        
        Retorna:
        --------
        bool - True si la validación es exitosa
        
        Excepciones:
        ------------
        DuracionInvalidaError - Si algún parámetro no supera la validación
        """
        # Validación: tipo de dato correcto
        if not isinstance(duracion, (int, float)):
            raise DuracionInvalidaError(
                f"La duración debe ser numérica (recibido: {type(duracion).__name__})"
            )
        
        # Validación: duración positiva
        if duracion <= 0:
            raise DuracionInvalidaError(
                f"La duración debe ser positiva (recibido: {duracion})"
            )
        
        # Validación: no exceder el máximo permitido
        if duracion > self.DURACION_MAXIMA:
            raise DuracionInvalidaError(
                f"La duración no puede exceder {self.DURACION_MAXIMA} horas "
                f"(solicitado: {duracion}h)"
            )
        
        return True  # Retorna True si todas las validaciones pasan
    
    @abstractmethod
    def calcular_costo(self, duracion, **kwargs):
        """
        MÉTODO ABSTRACTO: Calcula el costo total del servicio.
        
        Cada clase hija DEBE implementar este método con su propia lógica.
        
        Parámetros:
        -----------
        duracion : int/float - Duración en horas
        **kwargs : dict - Parámetros adicionales variables según el servicio
            - ReservaSalas: descuento (float)
            - AlquilerEquipos: impuesto (float), dias (bool)
            - Asesoria: nivel (str), descuento_fidelidad (float)
        
        Retorna:
        --------
        float - Costo total calculado
        
        Excepciones:
        ------------
        CostoInconsistenteError - Si el cálculo produce valor inválido
        """
        pass  # Implementado por las clases hijas
    
    @abstractmethod
    def describir(self):
        """
        MÉTODO ABSTRACTO: Retorna una descripción textual del servicio.
        
        Cada clase hija DEBE implementar este método.
        
        Retorna:
        --------
        str - Descripción amigable del servicio para mostrar al usuario
        """
        pass  # Implementado por las clases hijas
    
    def __str__(self):
        """
        Representación en string del servicio.
        
        Retorna:
        --------
        str - Formato: "NombreClase: nombre ($precio_base/hora base)"
        """
        return f"{self.__class__.__name__}: {self.nombre} (${self.precio_base}/hora base)"