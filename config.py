# import os

# # === CONFIGURACIÓN SENCE ===
# SENCE_LOGIN_URL = "https://sistemas.sence.cl/rce/Registro/IniciarSesion"
# SENCE_LINEA_CAPACITACION = 3  # 3 = Impulsa Personas

# # OTEC (usa variables de entorno en producción)
# OTEC_RUT = os.getenv("OTEC_RUT", "77558994-9")  # Formato xxxxxxxx-x (sin puntos)
# OTEC_TOKEN = os.getenv("OTEC_TOKEN", "EF80CC96-21C0-495F-9446-161057474609")  # 36 chars

# # Dominio base para armar UrlRetoma / UrlError (sin slash final)
# OTEC_BASE_URL = os.getenv("OTEC_BASE_URL", "http://localhost:3000")

# # Flask
# SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

# # A dónde redirigir tras éxito (por ejemplo, a tu panel/sala del curso)
# SUCCESS_REDIRECT_ENDPOINT = os.getenv("SUCCESS_REDIRECT_URL", "https://aulavirtual.iccapacitacionlaboral.cl/login/index.php")
# ERROR_REDIRECT_ENDPOINT   = os.getenv("ERROR_REDIRECT_ENDPOINT",   "login_sence_form")
