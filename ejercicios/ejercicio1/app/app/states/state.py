import reflex as rx
from typing import TypedDict


class Tarea(TypedDict):
    titulo: str
    estado: str


class State(rx.State):
    """The app state."""

    mostrar_solo_pendientes: bool = False
    tareas: list[Tarea] = [
        {"titulo": "Diseñar la nueva landing page", "estado": "Pendiente"},
        {"titulo": "Desarrollar la API de autenticación", "estado": "En Progreso"},
        {"titulo": "Configurar el pipeline de CI/CD", "estado": "Completadas"},
        {"titulo": "Escribir la documentación de la API", "estado": "Pendiente"},
        {"titulo": "Investigar sobre WebSockets", "estado": "Pendiente"},
        {"titulo": "Corregir bug en el módulo de pagos", "estado": "En Progreso"},
        {"titulo": "Desplegar la versión 1.2 en producción", "estado": "Completadas"},
    ]

    @rx.event
    def toggle_mostrar_pendientes(self):
        """Toggle the filter for showing only pending tasks."""
        self.mostrar_solo_pendientes = not self.mostrar_solo_pendientes

    @rx.var
    def tareas_pendientes(self) -> list[Tarea]:
        """Returns a list of pending tasks."""
        return [t for t in self.tareas if t["estado"] == "Pendiente"]

    @rx.var
    def tareas_en_progreso(self) -> list[Tarea]:
        """Returns a list of tasks in progress."""
        return [t for t in self.tareas if t["estado"] == "En Progreso"]

    @rx.var
    def tareas_completadas(self) -> list[Tarea]:
        """Returns a list of completed tasks."""
        return [t for t in self.tareas if t["estado"] == "Completadas"]