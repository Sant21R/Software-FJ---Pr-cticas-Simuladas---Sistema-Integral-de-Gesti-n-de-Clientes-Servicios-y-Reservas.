#Software FJ - Ejercicio 1: Sistema Integral de Gestión de Clientes, Servicios y Reservas 

# Integrantes:
# - Santiago Ruiz Martínez
# - James Dario Acosta López
# - David Felipe Hidalgo Narvaez
# - Dayana Nathaly Narvaez Andrade 
# - Yeferson Quintero

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
# • Una clase abstracta Servicio y al menos tres servicios especializados que hereden de ella, implementando polimorfismo y métodos sobrescritos para calcular costos, describir servicios y validar información. 
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



# Excepciomes personalizadas para el sistema Software FJ

class SoftwareFJError(Exception):
    """Excepción general del sistema (las demás heredan de esta)."""

class ClienteInvalidoError(SoftwareFJError):
    """Se usa cuando los datos de un cliente no son válidos."""

class ServicioInvalidoError(SoftwareFJError):
    """Se usa cuando los datos de un servicio no son válidos."""

class ParametroFaltanteError(SoftwareFJError):
    """Se usa cuando falta un dato obligatorio."""

class ServicioNoDisponibleError(SoftwareFJError):
    """Se usa cuando el servicio no está disponible."""

class ReservaError(SoftwareFJError):
    """Se usa cuando hay un problema con una reserva."""

class OperacionNoPermitidaError(ReservaError):
    """Se usa cuando se intenta realizar una operación no permitida."""

class CalculoInconsistenteError(SoftwareFJError):
    """Se usa cuando hay un cálculo inconsistente en el sistema."""

# Clase abstracta

class EntidadBase(ABC):
    """Todas las entidades (Cliente, Servicio, Reserva) heredan de esta clase."""

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

# gestión de clientes sin base de datos.
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
        if valor is None:
            raise ParametroFaltanteError(f"El campo {campo} es obligatorio.")

        if isinstance(valor, (int, float)) and not isinstance(valor, bool):
            valor = str(valor)

        if not isinstance(valor, str):
            raise ParametroFaltanteError(f"El campo {campo} debe ser texto válido.")

        valor = valor.strip()
        if not valor:
            raise ParametroFaltanteError(f"El campo {campo} es obligatorio.")

        return valor

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


# Tkinter Ventana principal con pestañas para Clientes, Servicios, Reservas y Log

class VentanaPrincipal:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Software FJ - Clientes, Servicios y Reservas")
        self.ventana.geometry("800x500")

        titulo = tk.Label(self.ventana, text="Software FJ",
                        font=("Arial", 18, "bold"))
        titulo.pack(pady=10)

        # Pestañas Pedientes
        self.pestanas = ttk.Notebook(self.ventana)
        self.pestanas.pack(fill="both", expand=True, padx=10, pady=5)

        self.gestor_clientes = GestorClientes()
        self.crear_pestana_clientes()
        self.crear_pestana_pendiente("Servicios", "(Servicio, Sala, Equipo, Asesoría)")
        self.crear_pestana_pendiente("Reservas", "(clase Reserva y simulación)")
        self.crear_pestana_log()

        logger.info("Ventana principal iniciada.")

    # formulario de clientes dentro de la interfaz existente.
    def crear_pestana_clientes(self):
        marco = ttk.Frame(self.pestanas, padding=12)
        self.pestanas.add(marco, text="Clientes")
        campos = (("Identificación", "identificacion"), ("Nombre", "nombre"),
                  ("Correo", "correo"), ("Teléfono", "telefono"))
        self.entradas_clientes = {}
        for fila, (etiqueta, clave) in enumerate(campos):
            ttk.Label(marco, text=etiqueta).grid(row=fila, column=0, sticky="w", pady=4)
            entrada = ttk.Entry(marco, width=38)
            entrada.grid(row=fila, column=1, sticky="ew", padx=8, pady=4)
            self.entradas_clientes[clave] = entrada

        botones = ttk.Frame(marco)
        botones.grid(row=4, column=0, columnspan=2, sticky="w", pady=8)
        ttk.Button(botones, text="Registrar", command=self.registrar_cliente).pack(side="left", padx=4)
        ttk.Button(botones, text="Buscar por ID", command=self.buscar_cliente).pack(side="left", padx=4)
        ttk.Button(botones, text="Mostrar todos", command=self.mostrar_clientes).pack(side="left", padx=4)

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
            messagebox.showinfo("Clientes", "Cliente registrado correctamente.")
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
            messagebox.showinfo("Clientes", "No se encontró un cliente con esa identificación.")

    def mostrar_clientes(self):
        self.actualizar_tabla_clientes(self.gestor_clientes.listar())

    def actualizar_tabla_clientes(self, clientes):
        for item in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(item)
        for cliente in clientes:
            self.tabla_clientes.insert("", tk.END, values=(
                cliente.id, cliente.nombre, cliente.correo, cliente.telefono
            ))

    def crear_pestana_pendiente(self, nombre, quien):
        """Pestaña vacía que el compañero correspondiente debe completar."""
        marco = tk.Frame(self.pestanas)
        tk.Label(marco, text="Esta pendiente por hacer: " + quien, font=("Arial", 12)).pack(pady=40)
        self.pestanas.add(marco, text=nombre)
        return marco

    def crear_pestana_log(self):
        """Pestaña para ver el log y probar que los errores se controlan."""
        marco = tk.Frame(self.pestanas)
        self.pestanas.add(marco, text="Registro (log)")

        botones = tk.Frame(marco)
        botones.pack(pady=5)
        tk.Button(botones, text="Probar error controlado",
                command=self.probar_error).pack(side="left", padx=5)
        tk.Button(botones, text="Actualizar log",
                command=self.mostrar_log).pack(side="left", padx=5)

        self.texto_log = tk.Text(marco, height=18, state="disabled")
        self.texto_log.pack(fill="both", expand=True, padx=5, pady=5)

    def probar_error(self):
        """Demuestra try / except / else / finally y encadenamiento."""
        try:
            try:
                numero = int("abc")                      
            except ValueError as e:
                raise ServicioInvalidoError("La tarifa no es un número") from e
        except SoftwareFJError as e:
            logger.error("Error controlado: %s | causa: %r", e, e.__cause__)
            messagebox.showerror("Error controlado", str(e))
        else:
            logger.info("No hubo errores en la prueba.")
        finally:
            logger.info("Prueba de errores finalizada.")
            self.mostrar_log()

    def mostrar_log(self):
        """Lee el archivo de log y lo muestra en pantalla."""
        try:
            with open(ARCHIVO_LOG, encoding="utf-8") as archivo:
                contenido = archivo.read()
        except OSError as e:
            contenido = "No se pudo leer el log: " + str(e)
        self.texto_log.config(state="normal")
        self.texto_log.delete("1.0", "end")
        self.texto_log.insert("end", contenido)
        self.texto_log.see("end")
        self.texto_log.config(state="disabled")

    def iniciar(self):
        self.ventana.mainloop()

# Software FJ

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.iniciar()