import reflex as rx
from app.states.state import State
from app.components.kanban import columna_kanban


def index() -> rx.Component:
    """The main view of the Kanban board."""
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.h1("Kanban Board", class_name="text-3xl font-bold text-gray-900"),
                rx.el.button(
                    rx.icon("filter", class_name="mr-2 h-4 w-4"),
                    rx.cond(
                        State.mostrar_solo_pendientes,
                        "Mostrar Todas",
                        "Mostrar Solo Pendientes",
                    ),
                    on_click=State.toggle_mostrar_pendientes,
                    class_name="flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-colors shadow-sm border border-gray-300 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500",
                ),
                class_name="flex justify-between items-center mb-8",
            ),
            rx.el.div(
                rx.cond(
                    State.mostrar_solo_pendientes,
                    columna_kanban("Pendiente", "Pendiente", State.tareas_pendientes),
                    rx.el.div(
                        columna_kanban(
                            "Pendiente", "Pendiente", State.tareas_pendientes
                        ),
                        columna_kanban(
                            "En Progreso", "En Progreso", State.tareas_en_progreso
                        ),
                        columna_kanban(
                            "Completadas", "Completadas", State.tareas_completadas
                        ),
                        class_name="flex flex-1 gap-6",
                    ),
                ),
                class_name="flex w-full gap-6",
            ),
            class_name="container mx-auto py-8 px-4",
        ),
        class_name="min-h-screen bg-gray-100 font-['Raleway']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)