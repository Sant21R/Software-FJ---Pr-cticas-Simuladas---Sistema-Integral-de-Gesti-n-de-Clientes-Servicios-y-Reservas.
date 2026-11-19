#Software FJ - Ejercicio 1: Sistema Integral de Gestión de Clientes, Servicios y Reservas 

# Integrantes:
# - Santiago Ruiz Martínez 
# - James Dario Acosta López (Responde pero aun no aporta)
# - David Felipe Hidalgo Narvaez (No responde ni aporta)
# - Dayana Nathaly Narvaez Andrade (No responde ni aporta)
# - Yeferson Quintero (Responde y aporta la sección de )

# Tutor: Ing. Juan Pablo Arango Cardona


# En un equipo conformado por cinco (5) estudiantes, deberán desarrollar 
# un sistema integral orientado a objetos, sin uso de bases de datos, 
# capaz de gestionar clientes, servicios y reservas para una empresa 
# llamada Software FJ que ofrece varios tipos de servicios (reservas de 
# salas, alquiler de equipos y asesorías especializadas). El objetivo de esta 
# tarea es construir una aplicación estable, modular y extensible que 
# implemente de forma rigurosa los principios de abstracción, herencia, 
# polimorfismo, encapsulación y manejo avanzado de excepciones, 
# garantizando que el sistema siga funcionando aun cuando se presenten 
# errores durante su ejecución. 

# El sistema debe incluir clases abstractas, clases derivadas, métodos 
# sobrecargados, manejo de listas internas y validaciones estrictas, 
# demostrando un diseño orientado a objetos completamente funcional. La 
# información no debe almacenarse en bases de datos; toda la gestión 
# debe hacerse mediante objetos, listas y manejo de archivos únicamente 
# para el registro de eventos y errores. 

# Como parte esencial de la tarea, el sistema deberá incorporar manejo 
# robusto de excepciones, incluyendo excepciones personalizadas, uso
# de bloques try/except, try/except/else, try/except/finally, y 
# encadenamiento de excepciones. Cada error detectado debe registrarse 
# en un archivo de logs, manteniendo la aplicación activa y estable en 
# todo momento. El sistema debe ser capaz de manejar errores 
# provenientes de datos inválidos, parámetros faltantes, operaciones no 
# permitidas, intentos de reserva incorrectos, servicios no disponibles, 
# cálculos inconsistentes y cualquier otra situación que pueda 
# comprometer la operación normal de la aplicación. 

# El trabajo debe basarse en una arquitectura orientada a objetos, incluyendo al menos:
# • Una clase abstracta que represente entidades generales del sistema. 
# • Una clase Cliente con validaciones robustas y encapsulación de datos personales. 
# • Una clase abstracta Servicio y al menos tres servicios especializados que hereden de ella, implementando polimorfismo y métodos sobrescritos para calcular costos, describir servicios y validar parámetros. 
# • Una clase Reserva que integre cliente, servicio, duración y estado, e implemente confirmación, cancelación y procesamiento con manejo de excepciones. 
# • Métodos sobrecargados (por ejemplo, diferentes variantes del cálculo de costos con impuestos, descuentos o parámetros opcionales). 
# • Un archivo de logs donde se registren todos los errores y eventos relevantes.

# El sistema, sin utilizar ningún motor de base de datos, debe simular al 
# menos 10 operaciones completas, incluyendo registros válidos e 
# inválidos de clientes, creación correcta e incorrecta de servicios, y 
# reservas exitosas y fallidas, demostrando la capacidad del programa 
# para continuar funcionando ante errores graves y manejar excepciones 
# de manera controlada y profesional. 

# El equipo debe entregar un único proyecto completamente funcional, 
# organizado, documentado y capaz de ejecutarse sin interrupciones, 
# demostrando la correcta aplicación de la programación orientada a 
# objetos y el manejo avanzado de excepciones en un entorno sin base de 
# datos. 

import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
import logging
import math
import os


# Archivo de logs
try:
    CARPETA = os.path.dirname(os.path.abspath(__file__))
    ARCHIVO_LOG = os.path.join(CARPETA, "Software FJ.log")
    manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
except OSError:
    ARCHIVO_LOG = os.path.join(os.path.expanduser("~"), "Software FJ.log")
    manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")

manejador.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.DEBUG)
logger.addHandler(manejador)



# Excepciones

class SoftwareFJError(Exception):
    """Excepción general del sistema (las demás se heredan de esta)."""

class ClienteInvalidoError(SoftwareFJError):
    """Se usa para los datos de un cliente que no son válidos."""

class ServicioInvalidoError(SoftwareFJError):
    """Se usa para cuando los datos de un servicio no son válidos."""

class ParametroFaltanteError(SoftwareFJError):
    """Se usa para cuando falta un dato obligatorio."""

class ServicioNoDisponibleError(SoftwareFJError):
    """Se usa para cuando el servicio no está disponible."""

class ReservaError(SoftwareFJError):
    """Se usa para cuando hay un problema con una reserva."""

class OperacionNoPermitidaError(ReservaError):
    """Se usa para cuando se intenta realizar una operación no permitida."""

class CalculoInconsistenteError(SoftwareFJError):
    """Se usa para cuando hay un cálculo inconsistente en el sistema."""

# Clases abstractas

class EntidadBase(ABC):
    """Las entidades (Cliente, Servicio, Reserva) se heredan de esta clase"""

    def __init__(self):
        self._id = None          

    @property
    def id(self):
        return self._id

    @abstractmethod
    def describir(self):
        """Cada clase hija debe explicar cómo se describe."""
        pass

    def __str__(self):
        return self.describir()

# gestión de clientes sin usar base de datos
class Cliente(EntidadBase):
    """Representa a un cliente y protege sus datos mediante propiedades."""

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__()
        self._id = self._validar_texto(identificacion, "Identificación")
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @staticmethod
    def _validar_texto(valor, campo):
        if not isinstance(valor, str) or not valor.strip():
            raise ParametroFaltanteError(f"El campo {campo} es obligatorio.")
        return valor.strip()

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        nombre = self._validar_texto(valor, "nombre")
        if len(nombre) < 2:
            raise ClienteInvalidoError("El nombre debe tener al menos dos caracteres.")
        self._nombre = nombre

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        correo = self._validar_texto(valor, "correo")
        if correo.count("@") != 1 or "." not in correo.split("@")[-1] or " " in correo:
            raise ClienteInvalidoError("Ingresa un correo electrónico válido.")
        self._correo = correo

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        telefono = self._validar_texto(valor, "teléfono")
        if not telefono.isdigit() or not 7 <= len(telefono) <= 15:
            raise ClienteInvalidoError("El teléfono debe tener entre 7 y 15 dígitos.")
        self._telefono = telefono

    def describir(self):
        return f"{self.nombre} | ID: {self.id} | {self.correo} | {self.telefono}"


class GestorClientes:
    """Almacena clientes en memoria; no usa bases de datos."""

    def __init__(self):
        self._clientes = []

    def registrar(self, identificacion, nombre, correo, telefono):
        if self.buscar(identificacion) is not None:
            raise ClienteInvalidoError("Ya existe un cliente con esa identificación.")
        cliente = Cliente(identificacion, nombre, correo, telefono)
        self._clientes.append(cliente)
        logger.info("Cliente registrado con identificación: %s", cliente.id)
        return cliente

    def buscar(self, identificacion):
        return next((c for c in self._clientes if c.id == str(identificacion).strip()), None)

    def listar(self):
        return list(self._clientes)


class Servicio(EntidadBase, ABC):
    """Base para los servicios ofrecidos por Software FJ."""

    def __init__(self, nombre, tarifa_hora):
        super().__init__()
        self.nombre = self._validar_texto(nombre, "nombre del servicio")
        self.tarifa_hora = tarifa_hora

    @staticmethod
    def _validar_texto(valor, campo):
        if not isinstance(valor, str) or not valor.strip():
            raise ServicioInvalidoError(f"El campo {campo} es obligatorio.")
        return valor.strip()

    @staticmethod
    def _validar_numero(valor, campo, minimo=0, exclusivo=False):
        try:
            if isinstance(valor, bool):
                raise ValueError
            numero = float(valor)
        except (TypeError, ValueError) as error:
            raise ServicioInvalidoError(f"El campo {campo} debe ser numérico.") from error

        if not math.isfinite(numero) or (numero <= minimo if exclusivo else numero < minimo):
            condicion = "mayor que cero" if exclusivo and minimo == 0 else f"igual o mayor que {minimo}"
            raise ServicioInvalidoError(f"El campo {campo} debe ser {condicion}.")
        return numero

    @staticmethod
    def _validar_entero_positivo(valor, campo):
        try:
            if isinstance(valor, bool):
                raise ValueError
            numero_decimal = float(valor)
            if not math.isfinite(numero_decimal) or not numero_decimal.is_integer():
                raise ValueError
            numero = int(numero_decimal)
        except (TypeError, ValueError) as error:
            raise ServicioInvalidoError(f"El campo {campo} debe ser un número entero positivo.") from error
        if numero <= 0:
            raise ServicioInvalidoError(f"El campo {campo} debe ser un número entero positivo.")
        return numero

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @tarifa_hora.setter
    def tarifa_hora(self, valor):
        self._tarifa_hora = self._validar_numero(
            valor, "tarifa por hora", minimo=0, exclusivo=True
        )

    @property
    @abstractmethod
    def tipo(self):
        """Nombre legible del tipo de servicio."""
        pass

    @property
    @abstractmethod
    def detalle(self):
        """Dato específico que caracteriza al servicio."""
        pass

    @abstractmethod
    def validar_parametros(self, cantidad=1):
        """Valida las condiciones particulares del servicio."""
        pass

    @abstractmethod
    def _calcular_costo_base(self, duracion_horas, cantidad):
        """Calcula el costo antes de impuestos y descuentos."""
        pass

    def calcular_costo(self, duracion_horas, impuesto=0, descuento=0, cantidad=1):
        duracion = self._validar_numero(duracion_horas, "duración", minimo=0, exclusivo=True)
        impuesto = self._validar_numero(impuesto, "impuesto")
        descuento = self._validar_numero(descuento, "descuento")
        if impuesto > 100 or descuento > 100:
            raise ServicioInvalidoError("El impuesto y el descuento deben estar entre 0 y 100.")
        cantidad = self._validar_entero_positivo(cantidad, "cantidad")
        self.validar_parametros(cantidad)

        subtotal = self._calcular_costo_base(duracion, cantidad)
        return round(subtotal * (1 - descuento / 100) * (1 + impuesto / 100), 2)


class Sala(Servicio):
    """Sala que se alquila por hora y tiene una capacidad definida."""

    def __init__(self, nombre, tarifa_hora, capacidad):
        super().__init__(nombre, tarifa_hora)
        self._capacidad = self._validar_entero_positivo(capacidad, "capacidad")

    @property
    def tipo(self):
        return "Sala"

    @property
    def detalle(self):
        return f"{self._capacidad} personas"

    def validar_parametros(self, cantidad=1):
        self._validar_entero_positivo(cantidad, "cantidad de salas")

    def _calcular_costo_base(self, duracion_horas, cantidad):
        return self.tarifa_hora * duracion_horas * cantidad

    def describir(self):
        return f"{self.nombre} | Sala para {self._capacidad} personas | ${self.tarifa_hora:.2f}/hora"


class Equipo(Servicio):
    """Equipo disponible para alquiler por hora."""

    def __init__(self, nombre, tarifa_hora, unidades_disponibles):
        super().__init__(nombre, tarifa_hora)
        self._unidades_disponibles = self._validar_entero_positivo(
            unidades_disponibles, "unidades disponibles"
        )

    @property
    def tipo(self):
        return "Alquiler de equipos"

    @property
    def detalle(self):
        return f"{self._unidades_disponibles} unidades disponibles"

    def validar_parametros(self, cantidad=1):
        cantidad = self._validar_entero_positivo(cantidad, "cantidad de equipos")
        if cantidad > self._unidades_disponibles:
            raise ServicioNoDisponibleError(
                f"Solo hay {self._unidades_disponibles} unidades de {self.nombre} disponibles."
            )

    def _calcular_costo_base(self, duracion_horas, cantidad):
        return self.tarifa_hora * duracion_horas * cantidad

    def describir(self):
        return (
            f"{self.nombre} | {self._unidades_disponibles} unidades disponibles | "
            f"${self.tarifa_hora:.2f}/hora por unidad"
        )


class Asesoria(Servicio):
    """Asesoría especializada que se cobra por hora."""

    def __init__(self, nombre, tarifa_hora, especialidad):
        super().__init__(nombre, tarifa_hora)
        self._especialidad = self._validar_texto(especialidad, "especialidad")

    @property
    def tipo(self):
        return "Asesoría especializada"

    @property
    def detalle(self):
        return self._especialidad

    def validar_parametros(self, cantidad=1):
        self._validar_entero_positivo(cantidad, "cantidad de asesorías")

    def _calcular_costo_base(self, duracion_horas, cantidad):
        return self.tarifa_hora * duracion_horas * cantidad

    def describir(self):
        return f"{self.nombre} | Especialidad: {self._especialidad} | ${self.tarifa_hora:.2f}/hora"


class GestorServicios:
    """Almacena y consulta servicios en memoria."""

    def __init__(self):
        self._servicios = []

    def registrar(self, servicio):
        if not isinstance(servicio, Servicio):
            raise ServicioInvalidoError("Solo se pueden registrar servicios válidos.")
        servicio._id = f"S{len(self._servicios) + 1:03d}"
        self._servicios.append(servicio)
        logger.info("Servicio registrado: %s (%s)", servicio.id, servicio.tipo)
        return servicio

    def buscar(self, identificacion):
        return next((servicio for servicio in self._servicios if servicio.id == str(identificacion).strip()), None)

    def listar(self):
        return list(self._servicios)

class Reserva(EntidadBase):

    ESTADOS = ("Pendiente", "Confirmada", "Cancelada", "Procesada")

    def __init__(self, cliente, servicio, duracion, cantidad=1):
        super().__init__()

        if not isinstance(cliente, Cliente):
            raise ReservaError("Debe seleccionar un cliente válido.")

        if not isinstance(servicio, Servicio):
            raise ReservaError("Debe seleccionar un servicio válido.")

        try:
            self._duracion = Servicio._validar_numero( duracion, "duración", minimo=0, exclusivo=True)

            self._cantidad = Servicio._validar_entero_positivo( cantidad, "cantidad")

            servicio.validar_parametros(self._cantidad)

        except SoftwareFJError as error:
            raise ReservaError("No fue posible crear la reserva.") from error

        self._cliente = cliente
        self._servicio = servicio
        self._estado = "Pendiente"

        self._costo = servicio.calcular_costo( self._duracion, cantidad=self._cantidad)

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
     def cantidad(self):
         return self._cantidad

    def confirmar(self):
        if self._estado != "Pendiente":
            raise OperacionNoPermitidaError("Solo se pueden confirmar reservas pendientes.")

        self._estado = "Confirmada"
        logger.info("Reserva %s confirmada.", self.id)

    def cancelar(self):
        if self._estado in ("Cancelada", "Procesada"):
            raise OperacionNoPermitidaError( "No se puede cancelar esta reserva.")

        self._estado = "Cancelada"
        logger.info("Reserva %s cancelada.", self.id)

    def procesar(self):
        if self._estado != "Confirmada":
            raise OperacionNoPermitidaError( "La reserva debe estar confirmada.")

        self._estado = "Procesada"
        logger.info("Reserva %s procesada.", self.id)

    def describir(self):
        return (
            f"Reserva {self.id} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} horas | "
            f"Estado: {self.estado} | "
            f"Costo: ${self.costo:,.2f}" )

class GestorReservas:

    def __init__(self):
        self._reservas = []
        self._contador = 1

    def registrar(self, cliente, servicio, duracion, cantidad=1):
        try:
            reserva = Reserva( cliente, servicio, duracion, cantidad)
            reserva._id = f"R{self._contador:03d}"
            self._contador += 1
            self._reservas.append(reserva)

        except SoftwareFJError as error:
            logger.error( "Error al registrar reserva: %s",error,exc_info=True )
            raise
        else:
            logger.info("Reserva %s registrada.", reserva.id)
            return reserva

        finally:
            logger.info("Finalizó el registro de reserva.")

    def buscar(self, identificacion):
        return next(
            (r for r in self._reservas
            if r.id == str(identificacion).strip()),
            None)
    def listar(self):
        return list(self._reservas)

    def confirmar(self, identificacion):
        reserva = self.buscar(identificacion)

        if reserva is None:
            raise ReservaError("La reserva no existe.")

        reserva.confirmar()
        return reserva

    def cancelar(self, identificacion):
        reserva = self.buscar(identificacion)

        if reserva is None:
            raise ReservaError("La reserva no existe.")

        reserva.cancelar()
        return reserva

    def procesar(self, identificacion):
        reserva = self.buscar(identificacion)

        if reserva is None:
            raise ReservaError("La reserva no existe.")

        reserva.procesar()
        return reserva
        
# Interfaz gráfica con Tkinter

class VentanaPrincipal:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Software FJ")
        self.ventana.geometry("800x500")

        titulo = tk.Label(self.ventana, text="Software FJ x Grupo 322",
                        font=("Arial", 18, "bold"))
        titulo.pack(pady=10)

        # Pestañas
        self.pestanas = ttk.Notebook(self.ventana)
        self.pestanas.pack(fill="both", expand=True, padx=10, pady=5)

        # Gestores del sistema
        self.gestor_clientes = GestorClientes()
        self.gestor_servicios = GestorServicios()
        self.gestor_reservas = GestorReservas()  

        # Creación de pestañas
        self.crear_pestana_clientes()
        self.crear_pestana_servicios()
        self.crear_pestana_reservas() 

        logger.info("Ventana principal iniciada.")

    # formulario de clientes
    def crear_pestana_clientes(self):
        marco = ttk.Frame(self.pestanas, padding=12)
        self.pestanas.add(marco, text="CLIENTES")
        campos = (("Identificación:", "identificacion"), ("Nombre:", "nombre"),
                ("Correo:", "correo"), ("Teléfono:", "telefono"))
        self.entradas_clientes = {}
        for fila, (etiqueta, clave) in enumerate(campos):
            ttk.Label(marco, text=etiqueta).grid(row=fila, column=0, sticky="w", pady=4)
            entrada = ttk.Entry(marco, width=38)
            entrada.grid(row=fila, column=1, sticky="ew", padx=8, pady=4)
            self.entradas_clientes[clave] = entrada

        botones = ttk.Frame(marco)
        botones.grid(row=4, column=0, columnspan=2, sticky="w", pady=8)
        ttk.Button(botones, text="Registrar datos", command=self.registrar_cliente).pack(side="left", padx=4)
        ttk.Button(botones, text="Buscar ID", command=self.buscar_cliente).pack(side="left", padx=4)
        ttk.Button(botones, text="Mostrar todos los datos", command=self.mostrar_clientes).pack(side="left", padx=4)

        self.tabla_clientes = ttk.Treeview(
            marco, columns=("id", "nombre", "correo", "telefono"), show="headings", height=7
        )
        for columna, ancho in (("id", 100), ("nombre", 160), ("correo", 220), ("telefono", 120)):
            self.tabla_clientes.heading(columna, text=columna.capitalize())
            self.tabla_clientes.column(columna, width=ancho, minwidth=75)
        self.tabla_clientes.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=8)
        marco.columnconfigure(1, weight=1)
        marco.rowconfigure(5, weight=1)

    def registrar_cliente(self):
        datos = {clave: entrada.get() for clave, entrada in self.entradas_clientes.items()}
        try:
            self.gestor_clientes.registrar(**datos)
        except SoftwareFJError as error:
            logger.warning("Registro de cliente rechazado: %s", error)
            messagebox.showerror("Datos de cliente", str(error))
        else:
            messagebox.showinfo("Clientes", "REGISTRO EXITOSO: Cliente registrado correctamente.")
            for entrada in self.entradas_clientes.values():
                entrada.delete(0, tk.END)
            self.mostrar_clientes()

    def buscar_cliente(self):
        identificacion = self.entradas_clientes["identificacion"].get().strip()
        if not identificacion:
            messagebox.showwarning("Clientes", "Escribe la identificación que deseas buscar.")
            return
        cliente = self.gestor_clientes.buscar(identificacion)
        self.actualizar_tabla_clientes([cliente] if cliente else [])
        if cliente is None:
            messagebox.showinfo("Clientes", "REGISTRO FALLIDO: No se encontró un cliente con esa identificación.")

    def mostrar_clientes(self):
        self.actualizar_tabla_clientes(self.gestor_clientes.listar())

    def actualizar_tabla_clientes(self, clientes):
        for item in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(item)
        for cliente in clientes:
            self.tabla_clientes.insert("", tk.END, values=(
                cliente.id, cliente.nombre, cliente.correo, cliente.telefono
            ))

    def crear_pestana_servicios(self):
        marco = ttk.Frame(self.pestanas, padding=12)
        self.pestanas.add(marco, text="SERVICIOS")

        ttk.Label(marco, text="Tipo de servicio").grid(row=0, column=0, sticky="w", pady=4)
        self.tipo_servicio = tk.StringVar(value="Sala")
        selector = ttk.Combobox(
            marco, textvariable=self.tipo_servicio,
            values=("Sala", "Alquiler de equipos", "Asesoría especializada"),
            state="readonly", width=34
        )
        selector.grid(row=0, column=1, sticky="ew", padx=8, pady=4)
        selector.bind("<<ComboboxSelected>>", self.actualizar_campo_detalle)

        ttk.Label(marco, text="Nombre").grid(row=1, column=0, sticky="w", pady=4)
        self.entrada_nombre_servicio = ttk.Entry(marco, width=38)
        self.entrada_nombre_servicio.grid(row=1, column=1, sticky="ew", padx=8, pady=4)

        ttk.Label(marco, text="Tarifa por hora").grid(row=2, column=0, sticky="w", pady=4)
        self.entrada_tarifa_servicio = ttk.Entry(marco, width=38)
        self.entrada_tarifa_servicio.grid(row=2, column=1, sticky="ew", padx=8, pady=4)

        self.etiqueta_detalle_servicio = ttk.Label(marco, text="Capacidad (personas)")
        self.etiqueta_detalle_servicio.grid(row=3, column=0, sticky="w", pady=4)
        self.entrada_detalle_servicio = ttk.Entry(marco, width=38)
        self.entrada_detalle_servicio.grid(row=3, column=1, sticky="ew", padx=8, pady=4)

        botones = ttk.Frame(marco)
        botones.grid(row=4, column=0, columnspan=2, sticky="w", pady=8)
        ttk.Button(botones, text="Registrar servicio", command=self.registrar_servicio).pack(side="left", padx=4)
        ttk.Button(botones, text="Mostrar todos", command=self.mostrar_servicios).pack(side="left", padx=4)

        self.tabla_servicios = ttk.Treeview(
            marco, columns=("id", "tipo", "nombre", "tarifa", "detalle"),
            show="headings", height=7
        )
        for columna, titulo, ancho in (
            ("id", "ID", 75), ("tipo", "Tipo", 160), ("nombre", "Nombre", 140),
            ("tarifa", "Tarifa/hora", 100), ("detalle", "Detalle", 180)
        ):
            self.tabla_servicios.heading(columna, text=titulo)
            self.tabla_servicios.column(columna, width=ancho, minwidth=70)
        self.tabla_servicios.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=8)
        marco.columnconfigure(1, weight=1)
        marco.rowconfigure(5, weight=1)

    def actualizar_campo_detalle(self, evento=None):
        etiquetas = {
            "Sala": "Capacidad (personas)",
            "Alquiler de equipos": "Unidades disponibles",
            "Asesoría especializada": "Especialidad"
        }
        self.etiqueta_detalle_servicio.config(text=etiquetas[self.tipo_servicio.get()])
        self.entrada_detalle_servicio.delete(0, tk.END)

    def registrar_servicio(self):
        nombre = self.entrada_nombre_servicio.get()
        tarifa = self.entrada_tarifa_servicio.get()
        detalle = self.entrada_detalle_servicio.get()
        tipo = self.tipo_servicio.get()
        try:
            if tipo == "Sala":
                servicio = Sala(nombre, tarifa, detalle)
            elif tipo == "Alquiler de equipos":
                servicio = Equipo(nombre, tarifa, detalle)
            else:
                servicio = Asesoria(nombre, tarifa, detalle)
            self.gestor_servicios.registrar(servicio)
        except SoftwareFJError as error:
            logger.warning("Registro de servicio rechazado: %s", error)
            messagebox.showerror("Datos del servicio", str(error))
        else:
            messagebox.showinfo("Servicios", "REGISTRO EXITOSO: Servicio registrado correctamente.")
            self.entrada_nombre_servicio.delete(0, tk.END)
            self.entrada_tarifa_servicio.delete(0, tk.END)
            self.entrada_detalle_servicio.delete(0, tk.END)
            self.mostrar_servicios()

    def mostrar_servicios(self):
        for item in self.tabla_servicios.get_children():
            self.tabla_servicios.delete(item)
        for servicio in self.gestor_servicios.listar():
            self.tabla_servicios.insert("", tk.END, values=(
                servicio.id, servicio.tipo, servicio.nombre,
                f"${servicio.tarifa_hora:,.2f}", servicio.detalle
            ))

    # PESTAÑA DE RESERVAS

    def crear_pestana_reservas(self):

        marco = ttk.Frame(self.pestanas, padding=12)
        self.pestanas.add(marco, text="RESERVAS")

        ttk.Label( marco,text="GESTIÓN DE RESERVAS",font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Seleccionar cliente
        ttk.Label(marco, text="Cliente:").grid(
            row=1, column=0, sticky="w", pady=5)

        self.combo_cliente = ttk.Combobox(
            marco, state="readonly", width=35)
        self.combo_cliente.grid(
            row=1, column=1, sticky="ew", padx=8, pady=5)

        # Seleccionar servicio
        ttk.Label(marco, text="Servicio:").grid(
            row=2, column=0, sticky="w", pady=5)

        self.combo_servicio = ttk.Combobox(
            marco, state="readonly", width=35)
        self.combo_servicio.grid(
            row=2, column=1, sticky="ew", padx=8, pady=5
        )

        # Duración
        ttk.Label(marco, text="Duración (horas):").grid(
            row=3, column=0, sticky="w", pady=5)

        self.entrada_duracion = ttk.Entry(marco)
        self.entrada_duracion.grid(
            row=3, column=1, sticky="ew", padx=8, pady=5)

        # Cantidad
        ttk.Label(marco, text="Cantidad:").grid(
            row=4, column=0, sticky="w", pady=5)

        self.entrada_cantidad = ttk.Entry(marco)
        self.entrada_cantidad.insert(0, "1")
        self.entrada_cantidad.grid(
            row=4, column=1, sticky="ew", padx=8, pady=5)

        # Botones principales
        botones = ttk.Frame(marco)
        botones.grid(
            row=5, column=0, columnspan=2, pady=10)

        ttk.Button(botones,text="Actualizar listas",
            command=self.actualizar_listas_reservas).pack(side="left", padx=4)

        ttk.Button(botones,text="Registrar reserva",
            command=self.registrar_reserva).pack(side="left", padx=4)

        ttk.Button( botones,text="Mostrar reservas",
            command=self.mostrar_reservas).pack(side="left", padx=4)

        # Tabla de reservas
        self.tabla_reservas = ttk.Treeview(marco,columns=("id", "cliente", "servicio",
                "duracion", "cantidad", "estado", "costo"), show="headings",height=8)

        columnas = [ ("id", "ID", 65),
            ("cliente", "Cliente", 120),
            ("servicio", "Servicio", 120),
            ("duracion", "Horas", 65),
            ("cantidad", "Cantidad", 75),
            ("estado", "Estado", 100),
            ("costo", "Costo", 100)]

        for columna, titulo, ancho in columnas:
            self.tabla_reservas.heading(
                columna, text=titulo)
            self.tabla_reservas.column(
                columna, width=ancho, minwidth=55)

        self.tabla_reservas.grid(
            row=6, column=0, columnspan=2,
            sticky="nsew", pady=10)

        # Botones para cambiar estado
        acciones = ttk.Frame(marco)
        acciones.grid(row=7, column=0, columnspan=2, pady=8)

        ttk.Button(acciones,text="Confirmar",command=self.confirmar_reserva).pack(side="left", padx=5)

        ttk.Button(acciones,text="Cancelar",command=self.cancelar_reserva).pack(side="left", padx=5)

        ttk.Button(acciones,text="Procesar", command=self.procesar_reserva).pack(side="left", padx=5)

        marco.columnconfigure(1, weight=1)
        marco.rowconfigure(6, weight=1)

        self.actualizar_listas_reservas()

    # ACTUALIZAR CLIENTES Y SERVICIOS
    

    def actualizar_listas_reservas(self):

        clientes = self.gestor_clientes.listar()
        servicios = self.gestor_servicios.listar()

        self.combo_cliente["values"] = [
            f"{c.id} - {c.nombre}" for c in clientes]

        self.combo_servicio["values"] = [
            f"{s.id} - {s.nombre}" for s in servicios]

        if clientes:
            self.combo_cliente.current(0)
        else:
            self.combo_cliente.set("")

        if servicios:
            self.combo_servicio.current(0)
        else:
            self.combo_servicio.set("")

    # REGISTRAR RESERVA
    def registrar_reserva(self):

        try: cliente_seleccionado = self.combo_cliente.get()
            servicio_seleccionado = self.combo_servicio.get()

            if not cliente_seleccionado or not servicio_seleccionado:
                raise ParametroFaltanteError(
                    "Debe seleccionar un cliente y un servicio.")

            id_cliente = cliente_seleccionado.split(" - ")[0]
            id_servicio = servicio_seleccionado.split(" - ")[0]

            cliente = self.gestor_clientes.buscar(id_cliente)
            servicio = self.gestor_servicios.buscar(id_servicio)

            if cliente is None:
                raise ReservaError("El cliente no existe.")

            if servicio is None:
                raise ReservaError("El servicio no existe.")

            duracion = self.entrada_duracion.get()
            cantidad = self.entrada_cantidad.get()

            reserva = self.gestor_reservas.registrar(
                cliente, servicio, duracion, cantidad) except SoftwareFJError as error:

            logger.error("Error al registrar reserva: %s",
                error, exc_info=True )
            messagebox.showerror("Error", str(error))

        except Exception as error:

            logger.critical(
                "Error inesperado: %s",
                error, exc_info=True)
            messagebox.showerror(
                "Error inesperado",
                "Ocurrió un error al registrar la reserva.")
        else:
            messagebox.showinfo(
                "Reserva registrada",
                f"Reserva {reserva.id} creada correctamente.\n\n"
                f"Cliente: {cliente.nombre}\n"
                f"Servicio: {servicio.nombre}\n"
                f"Costo: ${reserva.costo:,.2f}")

            self.entrada_duracion.delete(0, tk.END)
            self.entrada_cantidad.delete(0, tk.END)
            self.entrada_cantidad.insert(0, "1")
            self.mostrar_reservas()

    # MOSTRAR RESERVAS

    def mostrar_reservas(self):

        for item in self.tabla_reservas.get_children():
            self.tabla_reservas.delete(item)

        for reserva in self.gestor_reservas.listar():

            self.tabla_reservas.insert("",tk.END,values=(
                    reserva.id,
                    reserva.cliente.nombre,
                    reserva.servicio.nombre,
                    reserva.duracion,
                    reserva.cantidad,
                    reserva.estado,
                    f"${reserva.costo:,.2f}"))

    # OBTENER RESERVA SELECCIONADA

    def obtener_reserva_seleccionada(self):

        seleccion = self.tabla_reservas.selection()

        if not seleccion:
            raise ParametroFaltanteError(
                "Debe seleccionar una reserva.")

        valores = self.tabla_reservas.item(
            seleccion[0], "values")

        reserva = self.gestor_reservas.buscar(valores[0])

        if reserva is None:
            raise ReservaError("La reserva no existe.")

        return reserva

    # CONFIRMAR RESERVA

    def confirmar_reserva(self):

        try:
            reserva = self.obtener_reserva_seleccionada()
            self.gestor_reservas.confirmar(reserva.id)

        except SoftwareFJError as error:

            logger.error(
                "Error al confirmar reserva: %s",
                error, exc_info=True)
            messagebox.showerror("Error", str(error))

        else:

            messagebox.showinfo(
                "Reservas",
                "Reserva confirmada correctamente.")
            self.mostrar_reservas()

    # CANCELAR RESERVA

    def cancelar_reserva(self):

        try:
            reserva = self.obtener_reserva_seleccionada()
            self.gestor_reservas.cancelar(reserva.id)

        except SoftwareFJError as error:

            logger.error(
                "Error al cancelar reserva: %s",
                error, exc_info=True)

            messagebox.showerror("Error", str(error))

        else:

            messagebox.showinfo(
                "Reservas",
                "Reserva cancelada correctamente.")

            self.mostrar_reservas()

    # PROCESAR RESERVA

    def procesar_reserva(self):

        try:
            reserva = self.obtener_reserva_seleccionada()
            self.gestor_reservas.procesar(reserva.id)

        except SoftwareFJError as error:

            logger.error(
                "Error al procesar reserva: %s",
                error, exc_info=True)

            messagebox.showerror("Error", str(error))

        else:

            messagebox.showinfo(
                "Reservas",
                "Reserva procesada correctamente.")

            self.mostrar_reservas()
    def iniciar(self):
        self.ventana.mainloop()
            
# Software FJ

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.iniciar()
