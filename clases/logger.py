"""
Módulo para manejo de logging (registro de eventos y errores).
"""

import datetime
import os

class LoggerSistema:
    RUTA_LOG = "logs/eventos.log"
    
    @staticmethod
    def _asegurar_directorio():
        directorio = os.path.dirname(LoggerSistema.RUTA_LOG)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
    
    @staticmethod
    def registrar_evento(mensaje, nivel="INFO"):
        LoggerSistema._asegurar_directorio()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LoggerSistema.RUTA_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(f"[{timestamp}] [{nivel}] {mensaje}\n")
