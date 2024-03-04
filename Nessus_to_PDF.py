import xml.etree.ElementTree as ET
import pandas as pd
import pdfkit
from pathlib import Path

# Configuración de pdfkit para usar wkhtmltopdf
# Asegúrate de ajustar la ruta al ejecutable wkhtmltopdf en tu sistema
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

# Ruta al archivo .nessus
nessus_file_path = 'NetworkScan.nessus'

# Parsear el archivo .nessus
tree = ET.parse(nessus_file_path)
root = tree.getroot()

# Lista para almacenar los datos extraídos
data = []

# Extraer los datos de cada ReportItem en el archivo .nessus
for report_host in root.findall('.//ReportHost'):
    host_name = report_host.get('name')
    for report_item in report_host.findall('.//ReportItem'):
        item_data = {'Host': host_name}
        item_data.update(report_item.attrib)  # Añade todos los atributos del ReportItem

        # Extraer los elementos secundarios como tags y sus textos
        for child in report_item:
            item_data[child.tag] = child.text

        data.append(item_data)

# Convertir los datos a un DataFrame
df = pd.DataFrame(data)

# Guardar el DataFrame como HTML
html_file_path = 'nessus_report.html'
df.to_html(html_file_path)

# Convertir el HTML a PDF
output_pdf_path = 'nessus_report.pdf'
pdfkit.from_file(html_file_path, output_pdf_path, configuration=config)

print(f"El informe PDF ha sido creado: {Path(output_pdf_path).resolve()}")