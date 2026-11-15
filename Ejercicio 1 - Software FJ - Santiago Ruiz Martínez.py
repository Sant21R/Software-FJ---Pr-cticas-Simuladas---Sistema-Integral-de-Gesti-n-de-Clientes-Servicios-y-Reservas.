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

        self.gestor_clientes = GestorClientes()
        self.gestor_servicios = GestorServicios()
        self.crear_pestana_clientes()
        self.crear_pestana_servicios()

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

    def iniciar(self):
        self.ventana.mainloop()
            
# Software FJ

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.iniciar()