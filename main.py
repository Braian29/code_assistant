import os
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json

# Cargar variables de entorno (incluyendo GROQ_API_KEY)
load_dotenv()

def load_files_from_directory(directory_path, extensions=None):
    """
    Carga todos los archivos desde la carpeta especificada, filtrando por extensiones.
    """
    project_files = []
    folder_path = Path(directory_path)
    for file_path in folder_path.rglob('*'):
        if file_path.is_file() and (not extensions or file_path.suffix in extensions):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    project_files.append({"file_name": str(file_path), "content": content})
            except Exception as e:
                print(f"Error leyendo {file_path}: {e}")
    return project_files

def process_files_with_langchain(files):
    """
    Divide los archivos en fragmentos para analizarlos con LangChain.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_chunks = []
    for file in files:
        chunks = splitter.split_text(file["content"])
        all_chunks.extend({"file_name": file["file_name"], "content": chunk} for chunk in chunks)
    return all_chunks

def get_prompt_template():
    """
    Define un prompt para analizar el código.
    """
    system_message = SystemMessagePromptTemplate.from_template(
        "Eres un asistente experto en desarrollo de software. Ayudas a analizar código y proponer mejoras."
    )
    human_message = HumanMessagePromptTemplate.from_template(
        "Analiza el siguiente fragmento de código de {file_name} y sugiere mejoras:\n\n{content}"
    )
    return ChatPromptTemplate.from_messages([system_message, human_message])

def analyze_chunks_with_groq(chunks, groq_api_key, model_name="llama3-70b-8192"):
    """
    Analiza los fragmentos usando el modelo Groq.
    """
    groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name=model_name)
    prompt_template = get_prompt_template()
    sequence = RunnableSequence(prompt_template | groq_chat)
    
    results = []
    for chunk in chunks:
        try:
            # Ejecuta la cadena y extrae la respuesta.
            result = sequence.invoke({
                "file_name": chunk["file_name"],
                "content": chunk["content"]
            })
            # Convertir el resultado en texto si es necesario
            if hasattr(result, 'content'):
                analysis_text = result.content  # Extraer contenido textual
            else:
                analysis_text = str(result)  # Serializar cualquier otro formato
            results.append({"file_name": chunk["file_name"], "analysis": analysis_text})
        except Exception as e:
            print(f"Error analizando {chunk['file_name']}: {e}")
    return results

def save_results_to_file(results, output_file="analysis_results.json"):
    """
    Guarda los resultados del análisis en un archivo JSON.
    """
    serializable_results = []
    for result in results:
        try:
            # Asegurarse de que los datos sean serializables
            serializable_results.append({
                "file_name": result["file_name"],
                "analysis": result["analysis"]
            })
        except Exception as e:
            print(f"Error procesando resultado para guardar: {e}")

    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(serializable_results, file, indent=4, ensure_ascii=False)
        print(f"Resultados guardados en {output_file}")
    except Exception as e:
        print(f"Error guardando resultados: {e}")



def main():
    """
    Punto de entrada principal de la aplicación.
    """
    groq_api_key = os.getenv("GROQ_API_KEY") or input("Ingresa tu GROQ_API_KEY: ")
    directory_path = input("Ingresa la ruta de la carpeta de tu proyecto: ")
    extensions = input("Filtrar por extensiones (separadas por coma, ej: .py,.txt) o dejar vacío: ")
    extensions = [ext.strip() for ext in extensions.split(',')] if extensions else None

    files = load_files_from_directory(directory_path, extensions)
    print(f"Se han cargado {len(files)} archivos.")

    chunks = process_files_with_langchain(files)
    print(f"Se han dividido los archivos en {len(chunks)} fragmentos.")

    results = analyze_chunks_with_groq(chunks, groq_api_key)
    save_results_to_file(results)

    for result in results:
        print(f"Análisis de {result['file_name']}:\n{result['analysis']}\n{'='*50}")

if __name__ == "__main__":
    main()
