from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import uuid4


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
EMPLEADOS_CSV = DATA_DIR / "empleados.csv"
SOLICITUDES_CSV = DATA_DIR / "solicitudes.csv"


@dataclass
class Empleado:
    legajo: str
    nombre: str
    area: str
    dias_disponibles: int
    activo: bool


def cargar_empleados() -> dict[str, Empleado]:
    empleados: dict[str, Empleado] = {}
    with EMPLEADOS_CSV.open(newline="", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            empleados[fila["legajo"]] = Empleado(
                legajo=fila["legajo"],
                nombre=fila["nombre"],
                area=fila["area"],
                dias_disponibles=int(fila["dias_disponibles"]),
                activo=fila["activo"].strip().lower() == "si",
            )
    return empleados


def registrar_solicitud(
    empleado: Empleado,
    fecha_inicio: str,
    dias_solicitados: int,
    estado: str,
    observacion: str,
) -> None:
    with SOLICITUDES_CSV.open("a", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(
            [
                str(uuid4())[:8],
                empleado.legajo,
                empleado.nombre,
                fecha_inicio,
                dias_solicitados,
                estado,
                observacion,
            ]
        )


def pedir_opcion() -> str:
    print("\nOpciones: solicitar | saldo | salir")
    return input("Bot: ¿Que queres hacer? ").strip().lower()


def pedir_legajo(empleados: dict[str, Empleado]) -> Empleado | None:
    legajo = input("Bot: Ingresa tu legajo: ").strip()
    empleado = empleados.get(legajo)

    if empleado is None:
        print("Bot: No encontre ese legajo. Verifica el numero o comunicate con RR. HH.")
        return None

    if not empleado.activo:
        print("Bot: El legajo existe, pero figura como inactivo. Derivo la consulta a RR. HH.")
        return None

    print(f"Bot: Hola {empleado.nombre}. Area: {empleado.area}.")
    return empleado


def pedir_fecha() -> str | None:
    fecha = input("Bot: Ingresa fecha de inicio (AAAA-MM-DD): ").strip()
    try:
        fecha_inicio = datetime.strptime(fecha, "%Y-%m-%d").date()
    except ValueError:
        print("Bot: La fecha no tiene el formato correcto. Usa AAAA-MM-DD.")
        return None

    if fecha_inicio < datetime.now().date():
        print("Bot: La fecha no puede ser anterior al dia actual.")
        return None

    return fecha


def pedir_dias() -> int | None:
    valor = input("Bot: Ingresa cantidad de dias solicitados: ").strip()
    try:
        dias = int(valor)
    except ValueError:
        print("Bot: Necesito un numero entero. Ejemplo: 5.")
        return None

    if dias <= 0:
        print("Bot: La cantidad de dias debe ser mayor a cero.")
        return None

    return dias


def flujo_saldo(empleados: dict[str, Empleado]) -> None:
    empleado = pedir_legajo(empleados)
    if empleado:
        print(f"Bot: Tenes {empleado.dias_disponibles} dias disponibles.")


def flujo_solicitud(empleados: dict[str, Empleado]) -> None:
    empleado = pedir_legajo(empleados)
    if empleado is None:
        return

    fecha_inicio = pedir_fecha()
    if fecha_inicio is None:
        return

    dias_solicitados = pedir_dias()
    if dias_solicitados is None:
        return

    if empleado.dias_disponibles == 0:
        print("Bot: No tenes dias disponibles. La solicitud no puede generarse.")
        registrar_solicitud(
            empleado,
            fecha_inicio,
            dias_solicitados,
            "rechazada",
            "Sin saldo disponible",
        )
        return

    if dias_solicitados > empleado.dias_disponibles:
        print(
            "Bot: La cantidad solicitada supera tu saldo. "
            f"Saldo actual: {empleado.dias_disponibles} dias."
        )
        registrar_solicitud(
            empleado,
            fecha_inicio,
            dias_solicitados,
            "rechazada",
            "Dias solicitados mayores al saldo",
        )
        return

    if dias_solicitados > 10:
        estado = "pendiente_rrhh"
        observacion = "Requiere aprobacion especial por superar 10 dias"
        print("Bot: La solicitud queda pendiente de aprobacion especial de RR. HH.")
    else:
        estado = "aprobada"
        observacion = "Aprobacion automatica por saldo suficiente"
        print("Bot: Solicitud aprobada automaticamente.")

    registrar_solicitud(empleado, fecha_inicio, dias_solicitados, estado, observacion)
    print("Bot: La solicitud fue registrada en la base de datos.")


def main() -> None:
    empleados = cargar_empleados()
    print("Bot: Bienvenido al asistente de vacaciones de NovaTech SRL.")

    while True:
        opcion = pedir_opcion()

        if opcion == "solicitar":
            flujo_solicitud(empleados)
        elif opcion == "saldo":
            flujo_saldo(empleados)
        elif opcion == "salir":
            print("Bot: Gracias. Hasta luego.")
            break
        else:
            print("Bot: No entendi la opcion. Escribi solicitar, saldo o salir.")


if __name__ == "__main__":
    main()

