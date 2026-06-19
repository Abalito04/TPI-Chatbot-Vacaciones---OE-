# TPI Organizacion Empresarial - Chatbot de vacaciones

Este proyecto simula un chatbot administrativo para gestionar solicitudes de vacaciones en una organizacion ficticia llamada NovaTech SRL.

## Proceso elegido

Gestion de solicitud de vacaciones del personal.

El bot permite:

- Identificar al empleado por legajo.
- Consultar saldo disponible de dias.
- Registrar una solicitud.
- Validar fechas y cantidad de dias.
- Derivar automaticamente a aprobacion de RR. HH. cuando corresponde.
- Manejar errores de entrada del usuario.

## Stack propuesto

- Lenguaje: Python
- Plataforma simulada: consola, adaptable a Telegram Bot API, WhatsApp Business API o web.
- Persistencia: archivos CSV como base de datos simulada.
- Gestion de estados: maquina de estados implementada en `bot.py`.

## Como ejecutar

Desde esta carpeta:

```bash
python bot.py
```

## Archivos

- `bot.py`: simulador funcional del chatbot.
- `data/empleados.csv`: base de datos simulada de empleados y saldos.
- `data/solicitudes.csv`: registro de solicitudes generadas.
- `docs/bpmn_as_is.mmd`: diagrama del proceso manual actual.
- `docs/bpmn_to_be.mmd`: diagrama del proceso automatizado con bot.

## Flujo principal

1. El usuario inicia el bot.
2. Ingresa su legajo.
3. El bot consulta la base de empleados.
4. El usuario carga fecha de inicio y cantidad de dias.
5. El bot valida datos y saldo.
6. Si corresponde, registra la solicitud.
7. Si hay errores, informa el problema y permite reintentar o finalizar.

