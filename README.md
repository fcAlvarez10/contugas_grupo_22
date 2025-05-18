# Detector de Anomalías - Contugas

Esta aplicación web permite detectar anomalías en mediciones de volumen, presión y temperatura para diferentes clientes.

## Requisitos Previos

### Opción 1: Usando Docker (Recomendado)
- [Docker](https://www.docker.com/products/docker-desktop/)
- [Docker Compose](https://docs.docker.com/compose/install/) (viene incluido con Docker Desktop)

### Opción 2: Instalación Manual
- Python 3.9 o superior
- pip (gestor de paquetes de Python)

## Instalación

### Opción 1: Usando Docker (Recomendado)

1. Descarga o clona este repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd contugas_grupo_22
   ```

2. Construye y ejecuta la aplicación con Docker Compose:
   ```bash
   docker-compose up
   ```

3. ¡Listo! La aplicación estará disponible en http://localhost:5000

### Opción 2: Instalación Manual

1. Descarga o clona este repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd contugas_grupo_22
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   ```

3. Activa el entorno virtual:
   - En Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - En Linux/Mac:
     ```bash
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

6. Accede a la aplicación en http://localhost:5000

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

## Estructura del Proyecto

```
contugas_grupo_22/
├── app.py              # Aplicación principal Flask
├── requirements.txt    # Dependencias del proyecto
├── model/             # Directorio con el modelo entrenado
├── templates/         # Plantillas HTML
├── Dockerfile         # Configuración de Docker
└── docker-compose.yml # Configuración de Docker Compose
```

## Solución de Problemas

### Docker
- Si el puerto 5000 está ocupado, puedes cambiarlo en el archivo `docker-compose.yml`
- Para reiniciar la aplicación: `docker-compose restart`
- Para detener la aplicación: `docker-compose down`
- Para ver los logs: `docker-compose logs`

### Instalación Manual
- Si hay problemas con las dependencias, asegúrate de usar Python 3.9
- Verifica que todas las dependencias estén instaladas: `pip list`
- Para ver los logs, revisa la consola donde ejecutaste la aplicación

## Soporte

Si encuentras algún problema o necesitas ayuda, por favor:
1. Revisa la sección de Solución de Problemas
2. Verifica los logs de la aplicación
3. Contacta al equipo de soporte
