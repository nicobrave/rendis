from decouple import config
import re
from google.cloud import vision
import os

# Inicializar Google Vision Client (asegúrate de tener configuradas las credenciales)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config('GOOGLE_APPLICATION_CREDENTIALS')
client = vision.ImageAnnotatorClient()

def process_receipt(image_file):
    try:
        content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        if not texts:
            raise ValueError("No se pudo extraer texto de la imagen")

        extracted_text = texts[0].description
        print(f"Texto extraído completo: {extracted_text}")

        # Inicializar valores por defecto
        provider_name = "N/A"
        detail = ""
        document_number = "N/A"
        document_date = "N/A"
        total_amount = "N/A"

        # Dividir el texto en líneas para buscar los valores necesarios
        lines = extracted_text.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()

            # Buscar el nombre del proveedor (Razón Social Empresa)
            if "razón social" in line_lower or "señor(es):" in line_lower:
                provider_name = lines[i].strip()  # Capturamos el nombre del proveedor

            # Buscar detalles o descripción de los productos
            if "descripcion" in line_lower or "detalle" in line_lower:
                # Tomamos las siguientes líneas para capturar todos los detalles
                j = i + 1
                while j < len(lines) and not re.search(r'total', lines[j].lower()):
                    detail += lines[j].strip() + "; "  # Concatenamos cada línea de detalle
                    j += 1

            # Buscar el número de documento
            if "n°" in line_lower or "factura" in line_lower:
                numero_match = re.search(r'\d+', line_lower)
                if numero_match:
                    document_number = numero_match.group(0)

            # Buscar la fecha de emisión
            if "fecha emision" in line_lower or "fecha emisión" in line_lower:
                date_match = re.search(r'(\d{1,2} de [A-Za-z]+ del \d{4})', line)
                if date_match:
                    document_date = date_match.group(0)

            # Buscar el monto total
            if "total" in line_lower:
                total_match = re.search(r'(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)', line_lower)
                if total_match:
                    total_amount = total_match.group(0).replace(',', '.')

        # Retornar los datos extraídos
        return {
            "provider_name": provider_name,
            "detail": detail.strip('; '),  # Remover el último punto y coma
            "document_number": document_number,
            "document_date": document_date,
            "total_amount": total_amount
        }

    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        raise e