# Padron_AFIP_Script_LS
Este repositorio contiene un script en Python para consultar el padrón de AFIP y verificar una lista de CUITs en Excel.

## Características

- **Carga de archivos**: Selecciona un archivo Excel con CUITs y el archivo de texto del padrón AFIP, que sale del siguiente sitio: https://www.afip.gob.ar/genericos/cInscripcion/archivoCompleto.asp
- **Procesamiento de datos**: Compara registros y genera un informe de coincidencias y no coincidencias.
- **Formato de salida**: Exporta un archivo Excel con dos hojas: "Encontrados" y "No Encontrados", según el diseño de registro del padrón mencionado previamente.

## Requisitos

- Python 3.x
- Pandas
- Tkinter

## Uso

- Prepara un archivo Excel con la lista de CUITs que deseas verificar. Asegúrate de que la columna que contiene los CUITs se llame "CUIT".
- Descarga el archivo de texto del padrón de AFIP desde el sitio de AFIP.
- Consulta el diseño de registro y observaciones en la misma página.
- Ejecuta el script.

 ## Consideraciones adicionales:
- El script puede sobrescribir archivos existentes si no se selecciona un nombre único para el archivo de reporte.
- NO AUTORIZO el uso comercial de este script. En tal caso, solicito amablemente me contactes de manera privada.
- ADAPTACIONES: Agradezco los créditos correspondientes, siempre y cuando se cumpla la condición anterior.
- AVISOS: Agradezco los avisos al respecto del uso del script, si funciona, si hay errores, sugerencias para mejoras, etc.
