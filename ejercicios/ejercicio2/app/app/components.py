import reflex as rx
from app.state import KanbanState, Task, Estado


def task_card(task: Task) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(task["title"], class_name="font-semibold text-gray-800 text-base"),
            rx.el.p(task["description"], class_name="text-sm text-gray-600 mt-1"),
            class_name="p-4 bg-white rounded-lg shadow-[0px_1px_3px_rgba(0,0,0,0.12)] hover:shadow-[0px_4px_8px_rgba(0,0,0,0.15)] transition-shadow duration-300 cursor-grab active:cursor-grabbing",
        ),
        draggable=True,
        custom_attrs={"onDragStart": KanbanState.start_drag(task["id"])},
    )


def kanban_column(title: Estado, tasks: list[Task]) -> rx.Component:
    column_colors = {
        "Pendiente": "bg-gray-100 border-gray-300",
        "En Progreso": "bg-blue-100 border-blue-300",
        "Completada": "bg-emerald-100 border-emerald-300",
    }
    header_colors = {
        "Pendiente": "text-gray-700",
        "En Progreso": "text-blue-700",
        "Completada": "text-emerald-700",
    }
    return rx.el.div(
        rx.el.h2(
            f"{title} ({tasks.length()})",
            class_name=f"text-lg font-bold p-4 border-b-2 {header_colors[title]} {column_colors[title]} rounded-t-xl tracking-wider",
        ),
        rx.el.div(
            rx.foreach(tasks, task_card), class_name="p-4 space-y-4 min-h-[200px]"
        ),
        custom_attrs={
            "onDragOver": rx.event.prevent_default,
            "onDrop": KanbanState.drop_on_column(title),
        },
        class_name=f"w-full md:w-1/3 bg-gray-50 rounded-xl shadow-[0px_1px_3px_rgba(0,0,0,0.12)] border {column_colors[title]} transition-shadow duration-300",
    )


def add_task_dialog() -> rx.Component:
    return rx.cond(
        KanbanState.show_add_task_dialog,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Añadir Nueva Tarea",
                        class_name="text-2xl font-bold text-gray-800 mb-6",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Título",
                            class_name="text-sm font-semibold text-gray-700 mb-2",
                        ),
                        rx.el.input(
                            default_value=KanbanState.new_task_title,
                            on_change=KanbanState.set_new_task_title.debounce(300),
                            placeholder="Ej. Finalizar el informe",
                            class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Descripción",
                            class_name="text-sm font-semibold text-gray-700 mb-2",
                        ),
                        rx.el.textarea(
                            default_value=KanbanState.new_task_description,
                            on_change=KanbanState.set_new_task_description.debounce(
                                300
                            ),
                            placeholder="Ej. Incluir gráficos de ventas del último trimestre",
                            class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 h-24",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancelar",
                            on_click=KanbanState.toggle_add_task_dialog,
                            class_name="px-4 py-2 rounded-lg bg-gray-200 text-gray-800 font-medium hover:bg-gray-300 transition-colors",
                        ),
                        rx.el.button(
                            "Añadir Tarea",
                            on_click=KanbanState.add_task,
                            class_name="px-4 py-2 rounded-lg bg-emerald-600 text-white font-medium hover:bg-emerald-700 transition-colors",
                        ),
                        class_name="flex justify-end gap-4",
                    ),
                    class_name="bg-white p-8 rounded-xl shadow-lg w-[90vw] max-w-lg z-50",
                    on_click=rx.event.stop_propagation,
                ),
                class_name="fixed inset-0 flex items-center justify-center bg-black/30 z-40",
                on_click=KanbanState.toggle_add_task_dialog,
            )
        ),
    )


def task_counters() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Resumen de Tareas",
            class_name="text-xl font-bold text-gray-800 mb-4 text-center",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Pendientes", class_name="text-base font-semibold text-gray-700"
                ),
                rx.el.p(
                    KanbanState.task_counts["Pendiente"],
                    class_name="text-3xl font-bold text-gray-500",
                ),
                class_name="p-6 bg-white rounded-xl shadow-[0px_1px_3px_rgba(0,0,0,0.12)] text-center w-full",
            ),
            rx.el.div(
                rx.el.p(
                    "En Progreso", class_name="text-base font-semibold text-blue-700"
                ),
                rx.el.p(
                    KanbanState.task_counts["En Progreso"],
                    class_name="text-3xl font-bold text-blue-500",
                ),
                class_name="p-6 bg-white rounded-xl shadow-[0px_1px_3px_rgba(0,0,0,0.12)] text-center w-full",
            ),
            rx.el.div(
                rx.el.p(
                    "Completadas", class_name="text-base font-semibold text-emerald-700"
                ),
                rx.el.p(
                    KanbanState.task_counts["Completada"],
                    class_name="text-3xl font-bold text-emerald-500",
                ),
                class_name="p-6 bg-white rounded-xl shadow-[0px_1px_3px_rgba(0,0,0,0.12)] text-center w-full",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6",
        ),
        class_name="mt-12 w-full",
    )