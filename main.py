"""
SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS
==============================================================
SOFTWARE FJ - DEMOSTRACIÓN COMPLETA

Este programa demuestra la aplicación de:
1. Programación Orientada a Objetos (POO):
   - Abstracción (clase abstracta Servicio)
   - Herencia (ReservaSalas, AlquilerEquipos, Asesoria)
   - Polimorfismo (método calcular_costo diferente en cada servicio)
   - Encapsulación (properties en Cliente)

2. Manejo avanzado de excepciones:
   - Excepciones personalizadas
   - Bloques try/except/else/finally
   - Encadenamiento de excepciones

3. Logging de eventos y errores

4. Sin bases de datos (solo listas en memoria)

Autor: Victor Morales
Fecha: 2025
"""

import os
import sys

# Agregar el directorio actual al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from clases.cliente import Cliente
from clases.servicios_concretos import ReservaSalas, AlquilerEquipos, Asesoria
from clases.reserva import Reserva
from clases.logger import LoggerSistema
from clases.excepciones import (
    DatosClienteInvalidosError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    CostoInconsistenteError,
    DuracionInvalidaError
)


def mostrar_separador(titulo):
    """
    Muestra un separador visual en consola para organizar la salida.
    
    Parámetros:
    -----------
    titulo : str - Título de la sección a mostrar
    """
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70)


def mostrar_operacion(numero, descripcion):
    """
    Muestra el número y descripción de una operación.
    
    Parámetros:
    -----------
    numero : int - Número de la operación
    descripcion : str - Descripción de lo que se va a demostrar
    """
    print(f"\n--- OPERACIÓN {numero} ---")
    print(f"📝 {descripcion}")
    print("-" * 50)


def main():
    """
    Función principal del sistema.
    Ejecuta 12+ operaciones demostrativas que incluyen casos
    válidos e inválidos para demostrar el manejo robusto de excepciones.
    """
    
    print("\n" + "=" * 70)
    print("  🚀 SISTEMA INTEGRAL SOFTWARE FJ 🚀")
    print("  Gestión de Clientes, Servicios y Reservas")
    print("  POO + Manejo Avanzado de Excepciones")
    print("=" * 70)
    
    # Limpiar log al inicio de la ejecución
    LoggerSistema.limpiar_log()
    
    # Listas para almacenar objetos (simulan "base de datos" en memoria)
    clientes = []
    servicios = []
    reservas = []
    
    LoggerSistema.registrar_evento("=== INICIO DE EJECUCIÓN DEL SISTEMA ===")
    
    # ================================================================
    # CREACIÓN DE SERVICIOS DISPONIBLES
    # ================================================================
    mostrar_separador("CREACIÓN DE SERVICIOS BASE")
    
    # Crear instancias de los tres tipos de servicios
    servicio_sala = ReservaSalas("Sala Ejecutiva", 50)
    servicio_sala_vip = ReservaSalas("Sala VIP", 80)
    servicio_laptop = AlquilerEquipos("Laptop Gaming", 15)
    servicio_proyector = AlquilerEquipos("Proyector 4K", 20)
    servicio_python = Asesoria("Asesoría en Python", 40)
    servicio_poo = Asesoria("Asesoría en POO Avanzado", 60)
    
    # Almacenar en lista
    servicios.extend([servicio_sala, servicio_sala_vip, servicio_laptop, 
                     servicio_proyector, servicio_python, servicio_poo])
    
    print("\n📋 Servicios disponibles en el catálogo:")
    for s in servicios:
        print(f"   {s.describir()}")
    
    # ================================================================
    # OPERACIÓN 1: Creación de cliente VÁLIDO
    # ================================================================
    mostrar_operacion(1, "Creación de cliente con datos VÁLIDOS")
    try:
        cliente1 = Cliente("Ana María Rodríguez", "ana.rodriguez@email.com", "3105551234")
        clientes.append(cliente1)
        print(f"✅ Cliente creado exitosamente: {cliente1}")
    except DatosClienteInvalidosError as e:
        print(f"❌ Error: {e}")
    
    # ================================================================
    # OPERACIÓN 2: Cliente con email INVÁLIDO
    # ================================================================
    mostrar_operacion(2, "Cliente con email INVÁLIDO (sin @) - DEBE LANZAR EXCEPCIÓN")
    try:
        cliente2 = Cliente("Carlos Pérez", "carlos.email-invalido", "3115556789")
        clientes.append(cliente2)
        print(f"✅ Cliente creado: {cliente2}")
    except DatosClienteInvalidosError as e:
        print(f"❌ EXCEPCIÓN CAPTURADA (correcto): {e}")
    
    # ================================================================
    # OPERACIÓN 3: Cliente con teléfono INVÁLIDO
    # ================================================================
    mostrar_operacion(3, "Cliente con teléfono INVÁLIDO (contiene letras)")
    try:
        cliente3 = Cliente("Laura Gómez", "laura.gomez@email.com", "ABC123456")
        clientes.append(cliente3)
        print(f"✅ Cliente creado: {cliente3}")
    except DatosClienteInvalidosError as e:
        print(f"❌ EXCEPCIÓN CAPTURADA (correcto): {e}")
    
    # ================================================================
    # OPERACIÓN 4: Cliente con nombre MUY CORTO
    # ================================================================
    mostrar_operacion(4, "Cliente con nombre MUY CORTO (menos de 3 caracteres)")
    try:
        cliente4 = Cliente("Jo", "jo@email.com", "3125550000")
        clientes.append(cliente4)
        print(f"✅ Cliente creado: {cliente4}")
    except DatosClienteInvalidosError as e:
        print(f"❌ EXCEPCIÓN CAPTURADA (correcto): {e}")
    
    # ================================================================
    # OPERACIÓN 5: Segundo cliente VÁLIDO
    # ================================================================
    mostrar_operacion(5, "Segundo cliente VÁLIDO")
    try:
        cliente5 = Cliente("Pedro Martínez", "pedro.martinez@empresa.com", "3205557890")
        clientes.append(cliente5)
        print(f"✅ Cliente creado exitosamente: {cliente5}")
    except DatosClienteInvalidosError as e:
        print(f"❌ Error: {e}")
    
    # Mostrar resumen de clientes válidos
    print(f"\n📋 Clientes válidos registrados: {len(clientes)}")
    for c in clientes:
        print(f"   • {c}")
    
    # ================================================================
    # OPERACIÓN 6: Reserva VÁLIDA con descuento
    # ================================================================
    mostrar_operacion(6, "Reserva VÁLIDA: Sala Ejecutiva - 3 horas con descuento del 10%")
    try:
        reserva1 = Reserva(clientes[0], servicio_sala, 3, "2025-05-15")
        costo = reserva1.confirmar()
        reservas.append(reserva1)
        print(f"💰 Costo final: ${costo}")
    except Exception as e:
        print(f"❌ Error en reserva: {e}")
    
    # ================================================================
    # OPERACIÓN 7: Reserva INVÁLIDA (duración negativa)
    # ================================================================
    mostrar_operacion(7, "Reserva INVÁLIDA: Duración negativa (-2 horas)")
    try:
        reserva2 = Reserva(clientes[0], servicio_sala_vip, -2, "2025-05-16")
        costo = reserva2.confirmar()
        reservas.append(reserva2)
        print(f"💰 Costo: ${costo}")
    except DuracionInvalidaError as e:
        print(f"❌ EXCEPCIÓN CAPTURADA (correcto): {e}")
    
    # ================================================================
    # OPERACIÓN 8: Alquiler de equipos (con días)
    # ================================================================
    mostrar_operacion(8, "Reserva VÁLIDA: Alquiler de Laptop Gaming por 2 días")
    try:
        reserva3 = Reserva(clientes[0] if len(clientes) > 0 else cliente5, 
                          servicio_laptop, 16, "2025-05-20")
        costo_final = reserva3.confirmar()
        reservas.append(reserva3)
        print(f"💰 Reserva confirmada: ${costo_final}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # ================================================================
    # OPERACIÓN 9: Asesoría nivel avanzado con descuento
    # ================================================================
    mostrar_operacion(9, "Reserva VÁLIDA: Asesoría Python nivel avanzado + descuento 10%")
    try:
        reserva4 = Reserva(clientes[0], servicio_python, 2, "2025-05-25")
        costo_final = reserva4.confirmar()
        reservas.append(reserva4)
        print(f"💰 Costo final: ${costo_final}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # ================================================================
    # OPERACIÓN 10: Intentar confirmar reserva ya confirmada (error)
    # ================================================================
    mostrar_operacion(10, "Reserva INVÁLIDA: Intentar reconfirmar reserva ya CONFIRMADA")
    try:
        if len(reservas) > 0:
            reservas[0].confirmar()
        else:
            print("⚠️ No hay reservas para probar")
    except ReservaInvalidaError as e:
        print(f"❌ EXCEPCIÓN CAPTURADA (correcto - no se puede reconfirmar): {e}")
    
    # ================================================================
    # OPERACIÓN 11: Cancelación de reserva
    # ================================================================
    mostrar_operacion(11, "Cancelación de reserva (válida)")
    try:
        if len(reservas) > 1:
            reservas[1].cancelar(razon="Cambio de planes del cliente")
        else:
            print("⚠️ No hay suficientes reservas")
    except ReservaInvalidaError as e:
        print(f"❌ Error: {e}")
    
    # ================================================================
    # OPERACIÓN 12: Nivel de asesoría inválido
    # ================================================================
    mostrar_operacion(12, "Reserva INVÁLIDA: Nivel de asesoría inexistente ('experto')")
    try:
        costo_invalido = servicio_poo.calcular_costo(3, nivel="experto")
        print(f"💰 Costo calculado: ${costo_invalido}")
    except ServicioNoDisponibleError as e:
        print(f"❌ EXCEPCIÓN CAPTURADA (correcto): {e}")
    
    # ================================================================
    # DEMOSTRACIÓN DE TRY/FINALLY
    # ================================================================
    mostrar_operacion(13, "Demostración de try/except/finally")
    try:
        print("Intentando crear reserva con duración excesiva (100 horas)...")
        reserva_test = Reserva(clientes[0], servicio_sala, 100, "2025-06-01")
        reserva_test.confirmar()
    except DuracionInvalidaError as e:
        print(f"❌ Error capturado: {e}")
    finally:
        print("🔵 El bloque FINALLY se ejecuta SIEMPRE (para limpieza, cierre, etc.)")
        LoggerSistema.registrar_evento("Bloque finally ejecutado correctamente", "INFO")
    
    # ================================================================
    # DEMOSTRACIÓN DE POLIMORFISMO
    # ================================================================
    mostrar_separador("DEMOSTRACIÓN DE POLIMORFISMO")
    print("\n🔹 Diferentes servicios respondiendo al mismo mensaje 'describir()':")
    for s in servicios[:3]:
        print(f"   {s.describir()}")
    
    print("\n🔹 Diferentes formas de calcular costo en el mismo tipo de servicio:")
    print(f"   • Sin descuento: ${servicio_sala.calcular_costo(2):.2f}")
    print(f"   • Con descuento 15%: ${servicio_sala.calcular_costo(2, descuento=15):.2f}")
    print(f"   • Con descuento 25%: ${servicio_sala.calcular_costo(2, descuento=25):.2f}")
    
    # ================================================================
    # REPORTE FINAL
    # ================================================================
    mostrar_separador("REPORTE FINAL DEL SISTEMA")
    
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   • Clientes intentados: 5")
    print(f"   • Clientes válidos: {len(clientes)}")
    print(f"   • Servicios disponibles: {len(servicios)}")
    print(f"   • Reservas procesadas: {len(reservas)}")
    
    print("\n📋 DETALLE DE RESERVAS:")
    for i, r in enumerate(reservas, 1):
        print(f"   {i}. {r}")
    
    print("\n📁 Archivo de log generado en: logs/eventos.log")
    print("   Revise este archivo para ver el registro de todos los eventos y errores.")
    
    LoggerSistema.registrar_evento("=== FIN DE EJECUCIÓN DEL SISTEMA ===")
    
    print("\n" + "=" * 70)
    print("  🎉 SISTEMA EJECUTADO CON ÉXITO 🎉")
    print("  Todas las excepciones fueron manejadas correctamente")
    print("  El sistema demo MOSTRÓ 12+ operaciones (válidas e inválidas)")
    print("=" * 70)


if __name__ == "__main__":
    main()