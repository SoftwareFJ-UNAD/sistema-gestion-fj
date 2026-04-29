"""
MÓDULO DE SERVICIOS CONCRETOS
===============================
Implementa las tres clases de servicios específicos que heredan de la
clase abstracta Servicio: ReservaSalas, AlquilerEquipos y Asesoria.

Cada servicio tiene su propia lógica de cálculo de costos y descripción,
demostrando el principio de POLIMORFISMO.

Autor: Victor Morales
Fecha: 2025
"""

from clases.servicio import Servicio
from clases.excepciones import CostoInconsistenteError, ServicioNoDisponibleError
from clases.logger import LoggerSistema


class ReservaSalas(Servicio):
    """
    SERVICIO DE RESERVA DE SALAS
    =============================
    Representa la reserva de espacios físicos (salas de reuniones,
    conferencias, auditorios, etc.)
    
    Fórmula de costo:
        costo = precio_base * duración * (1 - descuento/100)
    
    Reglas de negocio:
        - Descuento permitido: 0% a 50%
        - Si no se especifica descuento, se aplica 0%
    """
    
    def calcular_costo(self, duracion, **kwargs):
        """
        Calcula el costo de reserva de una sala.
        
        Parámetros:
        -----------
        duracion : float - Horas de reserva
        **kwargs : dict - Parámetros opcionales
            - descuento (float): Porcentaje de descuento (0-50)
        
        Retorna:
        --------
        float - Costo total con descuento aplicado (redondeado a 2 decimales)
        
        Excepciones:
        ------------
        CostoInconsistenteError - Si el descuento está fuera del rango permitido
        """
        # Validación común (duración positiva, no excede máximo, etc.)
        self.validar_parametros(duracion)
        
        # Calcular costo base
        costo_base = self.precio_base * duracion
        
        # Aplicar descuento si existe en los parámetros
        if "descuento" in kwargs:
            descuento = kwargs["descuento"]
            
            # Validar que descuento sea numérico
            if not isinstance(descuento, (int, float)):
                raise CostoInconsistenteError(
                    f"El descuento debe ser numérico (recibido: {type(descuento).__name__})"
                )
            
            # Validar rango de descuento (0% a 50%)
            if descuento < 0 or descuento > 50:
                raise CostoInconsistenteError(
                    f"El descuento debe estar entre 0% y 50% (solicitado: {descuento}%)"
                )
            
            # Aplicar descuento
            costo_final = costo_base * (1 - descuento / 100)
            
            # Registrar en log
            LoggerSistema.registrar_evento(
                f"ReservaSalas: {duracion}h, base ${costo_base:.2f}, "
                f"descuento {descuento}% = ${costo_final:.2f}"
            )
        else:
            # Sin descuento
            costo_final = costo_base
            LoggerSistema.registrar_evento(
                f"ReservaSalas: {duracion}h, base ${costo_base:.2f}, sin descuento"
            )
        
        # Validación de seguridad: costo no puede ser negativo
        if costo_final < 0:
            raise CostoInconsistenteError(
                f"Costo negativo calculado: ${costo_final:.2f}. Revise los parámetros."
            )
        
        return round(costo_final, 2)
    
    def describir(self):
        """
        Descripción del servicio de reserva de salas.
        
        Retorna:
        --------
        str - Descripción con emoji para mejor visualización
        """
        return f"📌 Reserva de Salas - {self.nombre}: ${self.precio_base}/hora. Ideal para reuniones y eventos."


class AlquilerEquipos(Servicio):
    """
    SERVICIO DE ALQUILER DE EQUIPOS
    =================================
    Representa el alquiler de equipos tecnológicos (laptops, proyectores, etc.)
    
    Fórmula de costo:
        costo = precio_base * duración_horas * (1 + impuesto/100)
    
    Reglas de negocio:
        - Impuesto estándar: 19% (IVA Colombia)
        - Puede recibir duración en días (se convierte a horas, 1 día = 8 horas)
        - Impuesto permitido: 0% a 30%
    """
    
    IMPUESTO_DEFAULT = 19  # IVA estándar en Colombia
    
    def calcular_costo(self, duracion, **kwargs):
        """
        Calcula el costo de alquiler de equipos.
        
        Parámetros:
        -----------
        duracion : float - Duración (en horas o días según 'dias')
        **kwargs : dict - Parámetros opcionales
            - impuesto (float): Porcentaje de impuesto (0-30)
            - dias (bool): Si es True, la duración se interpreta en días
        
        Retorna:
        --------
        float - Costo total con impuesto aplicado (redondeado a 2 decimales)
        """
        # Convertir días a horas si es necesario
        if kwargs.get("dias", False):
            # 1 día = 8 horas laborables
            duracion_horas = duracion * 8
            LoggerSistema.registrar_evento(
                f"AlquilerEquipos: {duracion} días convertidos a {duracion_horas} horas"
            )
        else:
            duracion_horas = duracion
        
        # Validación común
        self.validar_parametros(duracion_horas)
        
        # Calcular costo base
        costo_base = self.precio_base * duracion_horas
        
        # Obtener impuesto (usar el proporcionado o el valor por defecto)
        impuesto = kwargs.get("impuesto", self.IMPUESTO_DEFAULT)
        
        # Validar que impuesto sea numérico
        if not isinstance(impuesto, (int, float)):
            raise CostoInconsistenteError(
                f"El impuesto debe ser numérico (recibido: {type(impuesto).__name__})"
            )
        
        # Validar rango de impuesto (0% a 30%)
        if impuesto < 0 or impuesto > 30:
            raise CostoInconsistenteError(
                f"El impuesto debe estar entre 0% y 30% (solicitado: {impuesto}%)"
            )
        
        # Aplicar impuesto
        costo_final = costo_base * (1 + impuesto / 100)
        
        # Registrar en log
        LoggerSistema.registrar_evento(
            f"AlquilerEquipos: {duracion_horas}h, base ${costo_base:.2f}, "
            f"impuesto {impuesto}% = ${costo_final:.2f}"
        )
        
        return round(costo_final, 2)
    
    def describir(self):
        """
        Descripción del servicio de alquiler de equipos.
        
        Retorna:
        --------
        str - Descripción con emoji y detalle de impuesto
        """
        return f"🖥️ Alquiler de Equipos - {self.nombre}: ${self.precio_base}/hora. Incluye IVA del {self.IMPUESTO_DEFAULT}%."


class Asesoria(Servicio):
    """
    SERVICIO DE ASESORÍA ESPECIALIZADA
    ====================================
    Representa asesorías o consultorías con diferentes niveles de especialización.
    
    Fórmula de costo:
        costo = (precio_base * duración + cargo_nivel) * (1 - descuento_fidelidad/100)
    
    Reglas de negocio:
        - Niveles: básico ($0 extra), intermedio ($50 extra), avanzado ($100 extra)
        - Descuento por fidelidad: 0% a 20%
    """
    
    # Diccionario con los cargos extra por nivel de especialización
    NIVELES = {
        "basico": 0,      # Sin costo adicional
        "intermedio": 50, # $50 extra
        "avanzado": 100   # $100 extra
    }
    
    def calcular_costo(self, duracion, **kwargs):
        """
        Calcula el costo de una asesoría.
        
        Parámetros:
        -----------
        duracion : float - Horas de asesoría
        **kwargs : dict - Parámetros opcionales
            - nivel (str): 'basico', 'intermedio' o 'avanzado'
            - descuento_fidelidad (float): Descuento adicional (0-20%)
        
        Retorna:
        --------
        float - Costo total con cargos y descuentos (redondeado a 2 decimales)
        
        Excepciones:
        ------------
        ServicioNoDisponibleError - Si el nivel de asesoría no existe
        CostoInconsistenteError - Si el descuento está fuera del rango
        """
        # Validación común
        self.validar_parametros(duracion)
        
        # Obtener nivel (por defecto 'basico')
        nivel = kwargs.get("nivel", "basico").lower()
        
        # Validar que el nivel exista en el diccionario
        if nivel not in self.NIVELES:
            raise ServicioNoDisponibleError(
                f"Nivel de asesoría inválido: '{nivel}'. "
                f"Niveles válidos: {list(self.NIVELES.keys())}"
            )
        
        # Calcular costo base
        costo_base = self.precio_base * duracion
        
        # Obtener cargo extra según el nivel
        cargo_extra = self.NIVELES[nivel]
        
        # Sumar base y cargo extra
        costo_subtotal = costo_base + cargo_extra
        
        # Aplicar descuento por fidelidad
        descuento = kwargs.get("descuento_fidelidad", 0)
        
        # Validar rango de descuento (0% a 20%)
        if descuento < 0 or descuento > 20:
            raise CostoInconsistenteError(
                f"El descuento por fidelidad debe estar entre 0% y 20% "
                f"(solicitado: {descuento}%)"
            )
        
        # Aplicar descuento
        costo_final = costo_subtotal * (1 - descuento / 100)
        
        # Registrar en log
        LoggerSistema.registrar_evento(
            f"Asesoria: {duracion}h, nivel={nivel}, cargo_extra=${cargo_extra}, "
            f"descuento={descuento}%, costo_final=${costo_final:.2f}"
        )
        
        return round(costo_final, 2)
    
    def describir(self):
        """
        Descripción del servicio de asesoría.
        
        Retorna:
        --------
        str - Descripción con emoji y detalle de niveles
        """
        return (f"🎓 Asesoría Especializada - {self.nombre}: ${self.precio_base}/hora + "
                f"cargo según nivel (Básico:$0, Intermedio:$50, Avanzado:$100)")