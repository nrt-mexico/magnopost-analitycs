import os
from datetime import datetime
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, Dimension, Metric, DateRange

# Ruta del archivo JSON de la cuenta de servicio
SERVICE_ACCOUNT_FILE = 'C:/Users/leone/Desktop/Google Analytics/magnopost-820e5a16961c.json'

# ID de propiedad de GA4
PROPERTY_ID = '428595664'

# Autenticación con el archivo de la cuenta de servicio
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/analytics.readonly"])

# Crea el cliente de la API
client = BetaAnalyticsDataClient(credentials=credentials)

# Define el rango de fechas (por ejemplo, los últimos 7 días)
date_range = DateRange(start_date="7daysAgo", end_date="today")

# Define la consulta con las dimensiones y métricas correctas
request = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    dimensions=[Dimension(name="date")],  # Define la dimensión como "date"
    metrics=[Metric(name="activeUsers"), Metric(name="sessions"), Metric(name="averageSessionDuration")],  # Métricas
    date_ranges=[date_range]  # Añadimos el rango de fechas
)

# Ejecuta la consulta
response = client.run_report(request)

# Creamos una lista para almacenar las filas con la fecha convertida
resultados = []

# Procesa los resultados de la API
for row in response.rows:
    # Obtener la fecha en formato YYYYMMDD
    fecha = row.dimension_values[0].value
    
    # Convertir la fecha de 'YYYYMMDD' a 'YYYY/MM/DD'
    fecha_formateada = datetime.strptime(fecha, '%Y%m%d').strftime('%Y/%m/%d')
    
    # Obtener métricas
    usuarios_activos = row.metric_values[0].value
    sesiones = row.metric_values[1].value
    duracion_sesion_segundos = float(row.metric_values[2].value)
    
    # Convertir la duración de la sesión de segundos a minutos
    duracion_sesion_minutos = duracion_sesion_segundos / 60
    
    # Almacenar el resultado
    resultados.append({
        'fecha': fecha_formateada,
        'usuarios_activos': usuarios_activos,
        'sesiones': sesiones,
        'duracion_sesion': duracion_sesion_minutos
    })

# Ordenamos los resultados para que la fecha actual sea la primera
resultados.sort(key=lambda x: (x['fecha'] != datetime.today().strftime('%Y/%m/%d'), x['fecha']))

# Imprime los resultados
for resultado in resultados:
    print(f"Fecha: {resultado['fecha']}")
    print(f"Usuarios Activos: {resultado['usuarios_activos']}")
    print(f"Sesiones: {resultado['sesiones']}")
    print(f"Duración media de la sesión: {resultado['duracion_sesion']:.2f} minutos")
    print("------------------------------------------------")
