# from datetime import datetime
# from zoneinfo import ZoneInfo
# import uuid

# # Mapa base de errores SENCE (completa con el anexo oficial cuando lo tengas)
# ERRORES_SENCE = {
#     "1": "Token inválido.",
#     "2": "RUT OTEC inválido o no coincide.",
#     "3": "Curso no encontrado o inactivo.",
#     "4": "RUN del participante inválido.",
#     "5": "Intentos excedidos o sesión expirada.",
#     # Agrega más códigos según el Anexo de Errores...
# }

# def normalizar_rut_formato_envio(rut: str) -> str:
#     """
#     Devuelve RUT en formato xxxxxxxx-x (sin puntos). No valida DV.
#     Si necesitas validar DV, usa tu validador existente antes de llamar a SENCE.
#     """
#     r = (rut or "").upper().replace(".", "").replace("-", "").strip()
#     if len(r) < 2:
#         return r
#     return f"{r[:-1]}-{r[-1]}"

# def validar_largo(valor: str, max_len: int) -> bool:
#     return isinstance(valor, str) and 1 <= len(valor) <= max_len

# def generar_id_sesion_alumno() -> str:
#     """
#     Genera un identificador (máx 149 chars) para IdSesionAlumno.
#     """
#     raw = f"{uuid.uuid4()}-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
#     return raw[:149]

# def ahora_scl_str() -> str:
#     """
#     Retorna 'aaaa-mm-dd hh:mm:ss' en America/Santiago (por si necesitas registrar).
#     """
#     return datetime.now(ZoneInfo("America/Santiago")).strftime("%Y-%m-%d %H:%M:%S")

# def zona_horaria_scl() -> str:
#     return "America/Santiago"
