# Padron_AFIP_Script_LS

Este repositorio contiene scripts en Python y Google Colab para consultar el padrón de AFIP y verificar una lista de CUITs contra el archivo maestro publicado por AFIP.

## Características

- **Carga de archivos**:
  - Excel con la lista de CUITs (columna “CUIT”).
  - Archivo de texto del padrón AFIP (descargado desde https://www.afip.gob.ar/genericos/cInscripcion/archivoCompleto.asp).
- **Procesamiento de datos**: compara registros según el diseño oficial de AFIP.
- **Salida en Excel**:
  - Hoja “Resumen” con estadísticas globales.
  - Hoja “Encontrados” con coincidencias completas (CUIT, denominación, impuestos, actividad, etc.).
  - Hoja “No Encontrados” con los CUITs no localizados. (Las versiones python copian el formato de tu listado de cuits, la versión HTML sólo reporta los cuits no encontrados)

## Versiones disponibles

- `padron_afip_ls.py`: versión para ejecutar localmente (requiere Python 3.x, pandas, tkinter).
- `padron_afip_colab.ipynb`: versión para ejecutar directamente en Google Colab, sin instalación local.
- `Padron_afip_check.HTML`: versión para ejecutar directamente en navegador web, sin instalación de ningún tipo. Tiene algunas variaciones en el reporte, pero nada del otro mundo.

## Requisitos

- Python 3.x  
- Librerías: `pandas`, `tkinter` 

## Uso

1. Descarga el archivo del padrón AFIP.  
2. Prepara tu Excel con CUITs (columna “CUIT”).  
3. Ejecuta el script:
   - En PC: `python padron_afip_ls.py`
   - En Colab: sube la notebook y tus archivos.  
4. El script generará un reporte Excel con tres hojas: **Resumen**, **Encontrados** y **No Encontrados**.

---

💡 Autor: *Leonardo Sola*  
