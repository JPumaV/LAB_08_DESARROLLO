import reflex as rx
from app.states.state import State, Tarea


def tarjeta_tarea(tarea: Tarea) -> rx.Component:
    """A card component for displaying a task."""
    return rx.el.div(
        rx.el.p(tarea["titulo"], class_name="font-medium text-sm text-gray-800"),
        class_name="bg-white p-4 rounded-lg border border-gray-200 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-200 cursor-pointer",
    )


def columna_kanban(
    nombre: str, estado: str, tareas_filtradas: rx.Var[list[Tarea]]
) -> rx.Component:
    """A column in the Kanban board."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name=rx.match(
                    estado,
                    ("Pendiente", "w-2 h-2 rounded-full bg-yellow-500 mr-2"),
                    ("En Progreso", "w-2 h-2 rounded-full bg-teal-500 mr-2"),
                    ("Completadas", "w-2 h-2 rounded-full bg-green-500 mr-2"),
                    "w-2 h-2 rounded-full bg-gray-500 mr-2",
                )
            ),
            rx.el.h2(
                nombre,
                class_name="font-semibold text-gray-700 text-sm tracking-wide uppercase",
            ),
            rx.el.span(
                rx.el.strong(tareas_filtradas.length()),
                class_name="ml-2 text-xs font-bold text-gray-400 bg-gray-200 rounded-full px-2 py-0.5",
            ),
            class_name="flex items-center p-3 border-b border-gray-200",
        ),
        rx.el.div(
            rx.foreach(tareas_filtradas, tarjeta_tarea),
            class_name="p-3 space-y-3 h-full overflow-y-auto",
        ),
        class_name="flex flex-col flex-1 min-w-[300px] bg-gray-50 rounded-xl border border-gray-200 max-h-[70vh]",
    )