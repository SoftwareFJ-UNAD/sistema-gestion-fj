"""
MÓDULO DE LOGGING (REGISTRO DE EVENTOS Y ERRORES)
==================================================
"""

import datetime
import os


class LoggerSistema:
    """
    Clase estática para el registro de eventos del sistema.
    """
    
    RUTA_LOG = "logs/eventos.log"
    
    @staticmethod
    def _asegurar_directorio():
        """Método privado: asegura que el directorio 'logs/' exista."""
        directorio = os.path.dirname(LoggerSistema.RUTA_LOG)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
    
    @staticmethod
    def limpiar_log():
        """Limpia el contenido del archivo de log."""
        LoggerSistema._asegurar_directorio()
        with open(LoggerSistema.RUTA_LOG, "w", encoding="utf-8") as archivo:
            archivo.write("")
        print("📝 Log limpiado")
    
    @staticmethod
    def registrar_evento(mensaje, nivel="INFO"):
        """Registra un evento en el archivo de log."""
        LoggerSistema._asegurar_directorio()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LoggerSistema.RUTA_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(f"[{timestamp}] [{nivel}] {mensaje}\n")