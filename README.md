# Proyecto: Análisis Automático de Código con LangChain y Groq

## Descripción
Este proyecto automatiza el análisis de código fuente utilizando **LangChain** para la segmentación de texto y **Groq** para el procesamiento mediante modelos de lenguaje avanzados. El objetivo es analizar archivos de un directorio, dividirlos en fragmentos manejables y sugerir mejoras o insights sobre el código utilizando un modelo de IA.

## Características
- **Carga de Archivos**: Lee todos los archivos de una carpeta especificada, filtrando por extensiones si es necesario.
- **Fragmentación Inteligente**: Divide el contenido en fragmentos utilizando el divisor de texto `RecursiveCharacterTextSplitter` de LangChain.
- **Análisis con Groq**: Integra Groq para procesar cada fragmento y generar sugerencias o análisis detallados.
- **Resultados JSON**: Exporta los resultados en un archivo JSON para facilitar su revisión o posterior análisis.

## Dependencias
Asegúrate de instalar las dependencias antes de ejecutar el proyecto:

```bash
pip install langchain langchain-groq python-dotenv
```

## Uso

### Configuración
1. Crea un archivo `.env` en la raíz del proyecto con tu clave de API de Groq:

   ```env
   GROQ_API_KEY=tu_clave_api
   ```

### Ejecución
1. Ejecuta el script principal:

   ```bash
   python main.py
   ```

2. Ingresa la ruta de la carpeta que contiene los archivos que deseas analizar.
3. Opcionalmente, filtra los archivos por extensión (por ejemplo, `.py, .txt`).
4. El script procesará los archivos y generará un archivo JSON con los resultados en la raíz del proyecto, por defecto llamado `analysis_results.json`.

### Archivos de Resultado
Los análisis se guardan en un archivo JSON en el siguiente formato:

```json
[
    {
        "file_name": "ruta/del/archivo.py",
        "analysis": "Sugerencias e insights generados para el fragmento del código."
    }
]
```

## Estructura del Proyecto

- **`main.py`**: Script principal que gestiona el flujo de trabajo.
- **`load_files_from_directory`**: Función para cargar archivos de una carpeta.
- **`process_files_with_langchain`**: Divide los archivos en fragmentos manejables.
- **`analyze_chunks_with_groq`**: Envía los fragmentos a Groq para su análisis.
- **`save_results_to_file`**: Guarda los resultados en un archivo JSON.

## Contribuciones
Si deseas contribuir:
1. Realiza un fork del repositorio.
2. Crea una rama para tus cambios.
3. Envía un pull request con tus mejoras.

## Licencia
Este proyecto está disponible bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto
Si tienes preguntas o comentarios, no dudes en contactarme a través de [correo o perfil de GitHub]. 
