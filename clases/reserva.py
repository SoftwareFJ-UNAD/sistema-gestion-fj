"""
MÓDULO DE LA CLASE RESERVA
===========================
Define la clase Reserva que integra un cliente con un servicio,
gestionando el ciclo de vida completo de una reserva: creación,
confirmación, cancelación y finalización.

ESTADOS POSIBLES:
-----------------
- PENDIENTE:   Estado inicial cuando se crea la reserva
- CONFIRMADA:  Después de confirmar y calcular el costo
- CANCELADA:   Cuando el usuario cancela antes de completar
- COMPLETADA:  Cuando el servicio fue prestado exitosamente

DEMOSTRACIÓN DE MANEJO DE EXCEPCIONES:
---------------------------------------
- Uso de try/except para capturar errores en cálculo de costos
- Uso de else para código que solo se ejecuta si no hay error
- Uso de finally para código que se ejecuta siempre
- Encadenamiento de excepciones con 'raise from'

Autor: Victor Morales
Fecha: 2025
"""

import datetime  # Para manejar fechas y timestamps
from clases.excepciones import ReservaInvalidaError
from clases.logger import LoggerSistema


class Reserva:
    """
    Clase que representa una reserva de un servicio para un cliente.
    
    Atributos:
    ----------
    cliente : Cliente - Objeto cliente que hace la reserva
    servicio : Servicio - Objeto servicio a reservar
    duracion : float - Duración en horas
    estado : str - Estado actual (PENDIENTE, CONFIRMADA, CANCELADA, COMPLETADA)
    costo : float - Costo total (None antes de confirmar)
    fecha_reserva : str - Fecha de la reserva (YYYY-MM-DD)
    fecha_confirmacion : datetime - Momento exacto de confirmación
    historial_cambios : list - Registro de todos los cambios de estado
    """
    
    # Lista de estados válidos (constante de clase)
    ESTADOS_VALIDOS = ["PENDIENTE", "CONFIRMADA", "CANCELADA", "COMPLETADA"]
    
    def __init__(self, cliente, servicio, duracion, fecha=None):
        """
        Constructor de la clase Reserva.
        
        Parámetros:
        -----------
        cliente : Cliente - Objeto cliente que hace la reserva
        servicio : Servicio - Objeto servicio a reservar
        duracion : float - Duración en horas
        fecha : str, opcional - Fecha en formato YYYY-MM-DD.
                Si no se proporciona, usa la fecha actual.
        
        Excepciones:
        ------------
        ReservaInvalidaError - Si el formato de fecha es incorrecto
        """
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self._estado = "PENDIENTE"  # Estado inicial
        self.costo = None  # Aún sin calcular
        self.fecha_confirmacion = None  # Se seteará al confirmar
        self.historial_cambios = []  # Registro de cambios de estado
        
        # Establecer la fecha de la reserva
        self._establecer_fecha(fecha)
        
        # Registrar el cambio de estado inicial
        self._registrar_cambio_estado("PENDIENTE", "Creación de la reserva")
        
        # Registrar en log la creación
        LoggerSistema.registrar_evento(
            f"Nueva reserva creada: Cliente={cliente.nombre}, "
            f"Servicio={servicio.nombre}, Duración={duracion}h, Fecha={self.fecha_reserva}"
        )
    
    def _establecer_fecha(self, fecha_str):
        """
        MÉTODO PRIVADO: Establece la fecha de la reserva con validación.
        
        Parámetros:
        -----------
        fecha_str : str o None - Fecha en formato YYYY-MM-DD
        
        Excepciones:
        ------------
        ReservaInvalidaError - Si el formato de fecha es incorrecto
        """
        if fecha_str is None:
            # Si no se proporciona fecha, usar la fecha actual
            self.fecha_reserva = datetime.date.today().strftime("%Y-%m-%d")
            return
        
        try:
            # Intentar parsear la fecha para validar formato
            datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
            self.fecha_reserva = fecha_str
        except ValueError:
            raise ReservaInvalidaError(
                f"Formato de fecha inválido: '{fecha_str}'. "
                f"Use el formato YYYY-MM-DD (ejemplo: 2025-05-15)"
            )
    
    def _registrar_cambio_estado(self, nuevo_estado, razon):
        """
        MÉTODO PRIVADO: Registra un cambio de estado en el historial.
        
        Parámetros:
        -----------
        nuevo_estado : str - Nuevo estado de la reserva
        razon : str - Motivo del cambio de estado
        """
        self.historial_cambios.append({
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "estado_anterior": self._estado if hasattr(self, '_estado') else None,
            "estado_nuevo": nuevo_estado,
            "razon": razon
        })
    
    @property
    def estado(self):
        """Getter: devuelve el estado actual de la reserva."""
        return self._estado
    
    def confirmar(self):
        """
        CONFIRMA LA RESERVA
        ===================
        Calcula el costo del servicio y cambia el estado a CONFIRMADA.
        
        Este método DEMUESTRA el manejo avanzado de excepciones con:
        - try: Intenta calcular el costo
        - except: Captura errores del cálculo
        - else: Solo se ejecuta si no hubo excepción
        - finally: Se ejecuta SIEMPRE (haya o no error)
        
        Retorna:
        --------
        float - Costo total de la reserva
        
        Excepciones:
        ------------
        ReservaInvalidaError - Si la reserva no está en estado PENDIENTE
        """
        print(f"\n--- Confirmando reserva para {self.cliente.nombre} ---")
        
        # Validar que la reserva esté en estado PENDIENTE
        if self._estado != "PENDIENTE":
            error_msg = (
                f"No se puede confirmar una reserva en estado '{self._estado}'. "
                f"Solo se confirman reservas PENDIENTES."
            )
            LoggerSistema.registrar_evento(error_msg, "ERROR")
            raise ReservaInvalidaError(error_msg)
        
        try:
            # INTENTAR: Calcular el costo usando el servicio
            print("Calculando costo del servicio...")
            self.costo = self.servicio.calcular_costo(self.duracion)
            
        except Exception as e:
            # EXCEPT: Capturar CUALQUIER error ocurrido en el cálculo
            LoggerSistema.registrar_evento(
                f"Error al calcular costo para reserva de {self.cliente.nombre}: {str(e)}",
                "ERROR"
            )
            # Re-lanzar la excepción con encadenamiento (raise from)
            raise ReservaInvalidaError(
                f"No se pudo calcular el costo: {str(e)}"
            ) from e
        
        else:
            # ELSE: Se ejecuta SOLO si NO hubo excepción en el try
            print(f"Costo calculado exitosamente: ${self.costo:.2f}")
            self._estado = "CONFIRMADA"
            self.fecha_confirmacion = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._registrar_cambio_estado("CONFIRMADA", "Confirmación exitosa")
            
            LoggerSistema.registrar_evento(
                f"Reserva CONFIRMADA: Cliente={self.cliente.nombre}, "
                f"Servicio={self.servicio.nombre}, Costo=${self.costo:.2f}"
            )
            
            print(f"✅ Reserva confirmada exitosamente. Costo total: ${self.costo:.2f}")
            return self.costo
        
        finally:
            # FINALLY: Se ejecuta SIEMPRE, haya o no excepción
            print(f"--- Fin del proceso de confirmación para {self.cliente.nombre} ---")
    
    def cancelar(self, razon="Cancelado por el usuario"):
        """
        CANCELA LA RESERVA
        ==================
        Cambia el estado a CANCELADA (solo si está PENDIENTE o CONFIRMADA).
        
        Parámetros:
        -----------
        razon : str - Motivo de la cancelación (opcional)
        
        Excepciones:
        ------------
        ReservaInvalidaError - Si la reserva ya está CANCELADA o COMPLETADA
        """
        # Validar que se pueda cancelar
        if self._estado in ["CANCELADA", "COMPLETADA"]:
            error_msg = f"No se puede cancelar una reserva en estado '{self._estado}'"
            LoggerSistema.registrar_evento(error_msg, "ERROR")
            raise ReservaInvalidaError(error_msg)
        
        estado_anterior = self._estado
        self._estado = "CANCELADA"
        self._registrar_cambio_estado("CANCELADA", razon)
        
        LoggerSistema.registrar_evento(
            f"Reserva CANCELADA: {self.cliente.nombre} - {self.servicio.nombre}. "
            f"Razón: {razon}"
        )
        
        print(f"❌ Reserva cancelada. Estado anterior: {estado_anterior}")
    
    def completar(self):
        """
        MARCA LA RESERVA COMO COMPLETADA
        =================================
        Cambia el estado a COMPLETADA (solo si está CONFIRMADA).
        
        Excepciones:
        ------------
        ReservaInvalidaError - Si la reserva no está CONFIRMADA
        """
        if self._estado != "CONFIRMADA":
            raise ReservaInvalidaError(
                f"Solo se pueden completar reservas CONFIRMADAS "
                f"(estado actual: {self._estado})"
            )
        
        self._estado = "COMPLETADA"
        self._registrar_cambio_estado("COMPLETADA", "Servicio prestado exitosamente")
        
        LoggerSistema.registrar_evento(
            f"Reserva COMPLETADA: {self.cliente.nombre} - {self.servicio.nombre}"
        )
        
        print(f"✅ Reserva marcada como completada")
    
    def obtener_info_completa(self):
        """
        Obtiene toda la información de la reserva en un diccionario.
        
        Útil para exportar datos a JSON, generar reportes o mostrar
        información detallada en la interfaz de usuario.
        
        Retorna:
        --------
        dict - Diccionario con todos los datos de la reserva
        """
        return {
            "cliente": self.cliente.obtener_resumen(),
            "servicio": {
                "nombre": self.servicio.nombre,
                "tipo": self.servicio.__class__.__name__,
                "descripcion": self.servicio.describir()
            },
            "duracion_horas": self.duracion,
            "fecha": self.fecha_reserva,
            "estado": self._estado,
            "costo": self.costo,
            "fecha_confirmacion": self.fecha_confirmacion,
            "historial_cambios": len(self.historial_cambios),
            "detalle_cambios": self.historial_cambios
        }
    
    def __str__(self):
        """
        Representación en string de la reserva.
        
        Retorna:
        --------
        str - Formato amigable para mostrar en consola
        """
        costo_str = f"${self.costo:.2f}" if self.costo else "Pendiente"
        return f"📅 {self.cliente.nombre} | {self.servicio.nombre} | {self.duracion}h | {self._estado} | {costo_str}"
    
    def __repr__(self):
        """
        Representación técnica de la reserva (para depuración).
        
        Retorna:
        --------
        str - Formato que permite reconstruir el objeto
        """
        return f"Reserva(cliente={self.cliente.nombre!r}, servicio={self.servicio.nombre!r}, duracion={self.duracion}, estado={self._estado!r})"