"""
MÓDULO DE EXCEPCIONES PERSONALIZADAS
=====================================
Este módulo define todas las excepciones específicas del sistema.
Cada excepción hereda de la clase base 'Exception' para permitir
un manejo diferenciado de errores según el tipo de situación.

Autor: Victor Morales
Fecha: 2025
"""


class DatosClienteInvalidosError(Exception):
    """
    Excepción lanzada cuando los datos de un cliente NO superan las validaciones.
    
    Casos de uso:
    - Nombre con menos de 3 caracteres
    - Email con formato incorrecto (falta @ o dominio)
    - Teléfono con letras o menos de 7 dígitos
    """
    pass


class ServicioNoDisponibleError(Exception):
    """
    Excepción lanzada cuando se solicita un servicio que NO existe
    o que no está disponible por alguna razón de negocio.
    
    Casos de uso:
    - Nivel de asesoría inválido (ej: 'experto' cuando solo hay básico/intermedio/avanzado)
    - Servicio eliminado del catálogo
    """
    pass


class ReservaInvalidaError(Exception):
    """
    Excepción lanzada cuando una reserva está en un estado incorrecto
    para la operación que se intenta realizar.
    
    Casos de uso:
    - Intentar confirmar una reserva ya cancelada
    - Intentar cancelar una reserva ya completada
    - Fecha de reserva en formato incorrecto
    """
    pass


class CostoInconsistenteError(Exception):
    """
    Excepción lanzada cuando el cálculo de costo produce un valor inválido.
    
    Casos de uso:
    - Descuento fuera del rango permitido (0-50%)
    - Impuesto fuera del rango permitido (0-30%)
    - Resultado de cálculo negativo
    """
    pass


class DuracionInvalidaError(Exception):
    """
    Excepción lanzada cuando la duración de un servicio no es válida.
    
    Casos de uso:
    - Duración negativa o cero
    - Duración que excede el máximo permitido (24 horas)
    - Tipo de dato incorrecto (string en lugar de número)
    """
    pass