from decouple import config
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import re
import json
import os

# Configuración de Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Verificar si estamos en un entorno de Render con la variable de entorno cargada
credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if credentials_json and credentials_json.startswith('{'):
    # Si es una cadena JSON, estamos en Render
    credentials_info = json.loads(credentials_json)
    creds = Credentials.from_service_account_info(credentials_info)
else:
    # Si no, asume que estamos en desarrollo local y usa el archivo de credenciales
    creds = Credentials.from_service_account_file('secrets/credentials.json')

# Inicializar el cliente de Google Sheets con las credenciales correspondientes
service = build('sheets', 'v4', credentials=creds)

def save_to_google_sheets(uid, email, project_id, provider_name, document_type, detail, document_number, document_date, total_amount, google_sheet_url, sheet_name, item_number):
    try:
        # Extraer el ID de Google Sheets desde la URL
        sheet_id = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', google_sheet_url).group(1)

        # Asegurarse de que los valores numéricos estén formateados como decimales
        total_amount = float(total_amount) if total_amount != "N/A" else "N/A"

        # Datos a enviar (basado en las columnas solicitadas)
        values = [[
            item_number,  # ITEM (número secuencial)
            provider_name or "",  # PROOVEDOR (nombre del proveedor)
            document_type or "",  # TIPO DE PARTIDA (por defecto será "Factura")
            detail or "",  # DETALLE (descripción de la factura)
            document_number or "",  # NUMERO DOCUMENTO
            document_date or "",  # FECHA (fecha de emisión)
            "",  # ID PPTO (vacío)
            "",  # INGRESOS (vacío)
            total_amount,  # RENDICION (total amount)
            "",  # Columna1 (vacío)
            ""   # Columna2 (vacío)
        ]]
        body = {'values': values}

        # Llamada a Google Sheets API para guardar los datos
        result = service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range=f'{sheet_name}!A:L',  # Dinámico según la hoja
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()

        print(f"{result.get('updates', {}).get('updatedCells', 0)} celdas actualizadas.")
    except Exception as e:
        print(f"Error al guardar en Google Sheets: {e}")
