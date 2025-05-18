# Detector de Anomalías - Contugas

Este repositorio contiene dos componentes principales:
1. Una aplicación web para detectar anomalías en tiempo real
2. El código de entrenamiento del modelo de detección de anomalías

## Estructura del Proyecto

```
contugas_grupo_22/
├── web_app/                    # Aplicación web
│   ├── app.py                 # Aplicación principal Flask
│   ├── requirements.txt       # Dependencias de la aplicación web
│   ├── templates/            # Plantillas HTML
│   ├── static/              # Archivos estáticos (CSS, JS, imágenes)
│   │   ├── css/           # Hojas de estilo
│   │   ├── js/           # Scripts de JavaScript
│   │   └── images/       # Imágenes (incluyendo logo.png)
│   ├── model/              # Modelo entrenado
│   ├── Dockerfile          # Configuración de Docker
│   └── docker-compose.yml  # Configuración de Docker Compose
│
├── model_training/            # Entrenamiento del modelo
│   ├── requirements.txt      # Dependencias para entrenamiento
│   ├── notebooks/           # Jupyter notebooks para EDA
│   ├── src/                # Módulos Python
│   │   ├── features.py    # Procesamiento de características
│   │   ├── ingestion.py  # Carga de datos
│   │   ├── labeling.py   # Etiquetado de datos
│   │   ├── metrics.py    # Métricas de evaluación
│   │   ├── detectors.py  # Implementación de detectores
│   │   └── evaluation.py # Evaluación de modelos
│   ├── data/              # Datos
│   │   ├── raw/         # Datos sin procesar
│   │   └── processed/   # Datos procesados
│   ├── train.py          # Script de entrenamiento
│   └── evaluate.py       # Script de evaluación
│
└── README.md                  # Este archivo
```

## Características Principales

- Interfaz web intuitiva con el logo oficial de Contugas
- Detección de anomalías en tiempo real
- Soporte para múltiples clientes
- Visualización clara de resultados
- Implementación en Docker para fácil despliegue
- Documentación completa y mantenible

## Instalación de la Aplicación Web

### Opción 1: Usando Docker (Recomendado)

Esta es la forma más sencilla y recomendada de ejecutar la aplicación, ya que funciona igual en Windows y Linux.

#### Requisitos Previos
- Docker Desktop
  - Windows: [Descargar Docker Desktop para Windows](https://www.docker.com/products/docker-desktop/)
  - Linux: [Instrucciones de instalación para Linux](https://docs.docker.com/engine/install/)
- Git (opcional)
  - Windows: [Git para Windows](https://gitforwindows.org/)
  - Linux: `sudo apt-get install git` (Ubuntu/Debian) o `sudo yum install git` (CentOS/RHEL)

#### Pasos de Instalación

1. Clona o descarga este repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd contugas_grupo_22/web_app
   ```

2. Inicia Docker Desktop y espera a que el servicio esté activo
   - Windows: Busca "Docker Desktop" en el menú inicio
   - Linux: El servicio debería iniciar automáticamente, o usa `systemctl start docker`

3. Construye y ejecuta la aplicación:
   ```bash
   docker-compose up --build
   ```

4. Accede a la aplicación en http://localhost:5000

### Opción 2: Instalación Manual

#### Windows

1. Instala Python 3.9:
   - Descarga el instalador de [python.org](https://www.python.org/downloads/release/python-390/)
   - Durante la instalación, marca la opción "Add Python to PATH"

2. Abre PowerShell y navega al directorio:
   ```powershell
   cd contugas_grupo_22/web_app
   ```

3. Crea y activa el entorno virtual:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

4. Instala las dependencias:
   ```powershell
   pip install -r requirements.txt
   ```

5. Ejecuta la aplicación:
   ```powershell
   python app.py
   ```

#### Linux

1. Instala Python 3.9 y pip:
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install python3.9 python3.9-venv python3-pip

   # CentOS/RHEL
   sudo yum install python39 python39-devel python39-pip
   ```

2. Navega al directorio:
   ```bash
   cd contugas_grupo_22/web_app
   ```

3. Crea y activa el entorno virtual:
   ```bash
   python3.9 -m venv venv
   source venv/bin/activate
   ```

4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

5. Ejecuta la aplicación:
   ```bash
   python app.py
   ```

## Uso de la Aplicación

1. Accede a la aplicación web en tu navegador: http://localhost:5000

2. En el formulario, ingresa los siguientes datos:
   - Fecha y Hora: Selecciona la fecha y hora de la medición
   - Cliente: Selecciona el cliente de la lista desplegable
   - Volumen: Ingresa el valor del volumen medido
   - Presión: Ingresa el valor de la presión medida
   - Temperatura: Ingresa el valor de la temperatura medida

3. Haz clic en "Enviar" para procesar los datos

4. La aplicación mostrará si se detectó una anomalía o si los valores son normales

## Interfaz y Personalización

La aplicación cuenta con una interfaz personalizada que incluye:

1. Logo oficial de Contugas en la parte superior de la página
2. Esquema de colores corporativo
3. Diseño responsivo para diferentes dispositivos
4. Navegación intuitiva y amigable

Para modificar elementos visuales:
- El logo se encuentra en `web_app/static/images/logo.png`
- Los estilos CSS están en `web_app/static/css/`
- Las plantillas HTML en `web_app/templates/`

## Solución de Problemas

### Docker

#### Windows
- Asegúrate de que Docker Desktop esté corriendo (icono de la ballena en la barra de tareas)
- Si Docker no inicia, verifica que WSL2 esté instalado y actualizado
- Para reiniciar Docker: Botón derecho en el icono > Restart

#### Linux
- Verifica el estado de Docker: `systemctl status docker`
- Si Docker no está corriendo: `systemctl start docker`
- Asegúrate de que tu usuario esté en el grupo docker: `sudo usermod -aG docker $USER`

### Instalación Manual

#### Windows
- Si Python no es reconocido: Verifica que esté en el PATH del sistema
- Si hay errores de permisos: Ejecuta PowerShell como administrador
- Para problemas con pip: `python -m pip install --upgrade pip`

#### Linux
- Problemas de permisos: `chmod +x venv/bin/activate`
- Si faltan dependencias: `sudo apt-get install python3.9-dev` (Ubuntu/Debian)
- Errores de compilación: `sudo apt-get install build-essential`

### Problemas Comunes
- Puerto 5000 en uso: Cambia el puerto en `docker-compose.yml` o usa `python app.py --port 5001`
- Errores de memoria en Docker: Aumenta la memoria asignada en Docker Desktop
- Problemas de red: Verifica la configuración del firewall

## Mantenimiento y Actualización

### Docker
```bash
# Actualizar la aplicación
git pull
docker-compose down
docker-compose up --build

# Limpiar recursos no utilizados
docker system prune
```

### Manual
```bash
# Actualizar la aplicación
git pull
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

## Soporte

Si encuentras algún problema:
1. Revisa la sección de Solución de Problemas
2. Verifica los logs de la aplicación
3. Contacta al equipo de soporte
