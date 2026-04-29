"""
Módulo de excepciones personalizadas para el sistema FJ.
"""

class DatosClienteInvalidosError(Exception):
    """Excepción lanzada cuando los datos de un cliente son inválidos."""
    pass

class ServicioNoDisponibleError(Exception):
    """Excepción lanzada cuando un servicio no está disponible."""
    pass

class ReservaInvalidaError(Exception):
    """Excepción lanzada cuando una reserva es inválida."""
    pass

class CostoInconsistenteError(Exception):
    """Excepción lanzada cuando el cálculo de costo es inválido."""
    pass

class DuracionInvalidaError(Exception):
    """Excepción lanzada cuando la duración no es válida."""
    pass
