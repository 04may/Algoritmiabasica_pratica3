#!/bin/bash
# ejecuta.sh
# Este script prepara el entorno para ejecutar el programa de búsqueda con retroceso.
# Verifica la existencia de Python3 y pip3, crea un entorno virtual,
# instala las dependencias necesarias y establece los permisos adecuados.

# Verificar que Python3 está instalado
if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: Python3 no está instalado. Por favor, instale Python3 e intente nuevamente."
    exit 1
fi

# Verificar que pip3 está instalado
if ! command -v pip3 >/dev/null 2>&1; then
    echo "Error: pip3 no está instalado. Por favor, instale pip3 e intente nuevamente."
    exit 1
fi

# Crear el entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar el entorno virtual
source venv/bin/activate

# Actualizar pip a la última versión
echo "Actualizando pip..."
pip install --upgrade pip

# Instalar los paquetes necesarios
echo "Instalando paquetes necesarios: numpy..."
pip install numpy

# Asegurar que el script principal sea ejecutable (se asume que se llama retroceso.py)
chmod +x retroceso.py

echo "¡El entorno está listo!"
echo "Ahora puede ejecutar el programa con el siguiente comando:"
echo "  python retroceso.py"
echo "O directamente:"
echo "  ./retroceso.py"
