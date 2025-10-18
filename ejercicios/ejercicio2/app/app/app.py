import reflex as rx
from app.state import KanbanState
from app.components import kanban_column, add_task_dialog, task_counters


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Tablero Kanban", class_name="text-4xl font-extrabold text-gray-900"
                ),
                rx.el.button(
                    rx.icon("plus", class_name="mr-2"),
                    "Añadir Tarea",
                    on_click=KanbanState.toggle_add_task_dialog,
                    class_name="flex items-center bg-emerald-600 text-white px-6 py-3 rounded-lg font-semibold shadow-[0px_6px_0px_rgba(0,0,0,0)] hover:shadow-[0px_12px_0px_rgba(0,0,0,0)] active:shadow-[0px_12px_0px_rgba(0,0,0,0)] hover:bg-emerald-700 transition-all duration-300",
                ),
                class_name="flex justify-between items-center mb-8",
            ),
            rx.el.div(
                kanban_column("Pendiente", KanbanState.pending_tasks),
                kanban_column("En Progreso", KanbanState.in_progress_tasks),
                kanban_column("Completada", KanbanState.completed_tasks),
                class_name="flex flex-col md:flex-row gap-6",
            ),
            task_counters(),
            add_task_dialog(),
            class_name="container mx-auto p-4 md:p-8",
        ),
        class_name="font-['Lato'] bg-gray-50 min-h-screen",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)
