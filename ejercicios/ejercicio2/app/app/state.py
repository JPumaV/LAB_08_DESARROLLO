import reflex as rx
from typing import TypedDict, Literal, cast
import uuid

Estado = Literal["Pendiente", "En Progreso", "Completada"]


class Task(TypedDict):
    id: str
    title: str
    description: str
    estado: Estado


class KanbanState(rx.State):
    tasks: list[Task] = [
        {
            "id": str(uuid.uuid4()),
            "title": "Configurar el entorno de desarrollo",
            "description": "Instalar todas las dependencias y configurar la base de datos.",
            "estado": "Completada",
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Diseñar la interfaz de usuario",
            "description": "Crear mockups y prototipos para el tablero Kanban.",
            "estado": "En Progreso",
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Implementar la funcionalidad de arrastrar y soltar",
            "description": "Añadir la capacidad de mover tareas entre columnas.",
            "estado": "Pendiente",
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Desarrollar el backend",
            "description": "Crear los endpoints de la API para gestionar tareas.",
            "estado": "En Progreso",
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Escribir pruebas unitarias",
            "description": "Asegurar que todos los componentes funcionen correctamente.",
            "estado": "Pendiente",
        },
    ]
    show_add_task_dialog: bool = False
    new_task_title: str = ""
    new_task_description: str = ""
    dragged_task_id: str | None = None

    @rx.var
    def task_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {"Pendiente": 0, "En Progreso": 0, "Completada": 0}
        for task in self.tasks:
            estado = task["estado"]
            if estado in counts:
                counts[estado] += 1
        return counts

    @rx.var
    def pending_tasks(self) -> list[Task]:
        return [task for task in self.tasks if task["estado"] == "Pendiente"]

    @rx.var
    def in_progress_tasks(self) -> list[Task]:
        return [task for task in self.tasks if task["estado"] == "En Progreso"]

    @rx.var
    def completed_tasks(self) -> list[Task]:
        return [task for task in self.tasks if task["estado"] == "Completada"]

    @rx.event
    def toggle_add_task_dialog(self):
        self.show_add_task_dialog = not self.show_add_task_dialog
        if not self.show_add_task_dialog:
            self.new_task_title = ""
            self.new_task_description = ""

    @rx.event
    def add_task(self):
        if self.new_task_title and self.new_task_description:
            new_task: Task = {
                "id": str(uuid.uuid4()),
                "title": self.new_task_title,
                "description": self.new_task_description,
                "estado": "Pendiente",
            }
            self.tasks.append(new_task)
            self.show_add_task_dialog = False
            self.new_task_title = ""
            self.new_task_description = ""

    @rx.event
    def start_drag(self, task_id: str):
        self.dragged_task_id = task_id

    @rx.event
    def drop_on_column(self, new_estado: Estado):
        if self.dragged_task_id is not None:
            updated_tasks = []
            for task in self.tasks:
                if task["id"] == self.dragged_task_id:
                    task["estado"] = new_estado
                updated_tasks.append(task)
            self.tasks = updated_tasks
            self.dragged_task_id = None