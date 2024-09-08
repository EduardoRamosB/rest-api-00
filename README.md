# Albergue Tail-World

Backend utilizando Django Rest Framework para la gestión de un albergue de animales. El proyecto está dividido en tres aplicaciones principales:

- `accounts`: Maneja todo lo relacionado con los usuarios y sus roles (admin, voluntarios y adoptadores).
- `shelter`: Maneja todo lo relacionado con el albergue, incluidos los animales y las adopciones.
- `kpis`: Proporciona indicadores del rendimiento del albergue.

## Requisitos

- Python 3.10 o superior
- PostgreSQL

## Configuración del entorno

1. **Clona el repositorio:**

   ```bash
   git clone git@github.com:EduardoRamosB/rest-api-00.git
   cd rest-api-00


2. **Crea y activa un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate # En Windows usa venv\Scripts\activate

   
3. **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
   
4. **Configura la base de datos:**
   ```bash
    Crea una base de datos en PostgreSQL llamada backend02_env.

    psql -U postgres -c "CREATE DATABASE backend02_env;"

5. **Configura la base de datos:**
    ```bash
    Configura el archivo .env:
    Crea un archivo .env en la raíz del proyecto con el siguiente contenido:

    DJANGO_SECRET_KEY=poner_aqui_tu_secret_key
    DEBUG=True
    DATABASE_ENGINE=django.db.backends.postgresql
    DATABASE_NAME=backend02_env
    DATABASE_USER=postgres
    DATABASE_PASSWORD=poner_aqui_tu_password
    DATABASE_HOST=localhost
    DATABASE_PORT=5432

    Asegúrate de reemplazar poner_aqui_tu_secret_key y poner_aqui_tu_password con valores apropiados.

6. **Aplica las migraciones:**
    ```bash
    python manage.py migrate

7. **Crea un superusuario para acceder al panel de administración::**
    ```bash
    python manage.py createsuperuser
   
8. **Ejecuta el servidor de desarrollo:**
    ```bash
    python manage.py runserver
   
## Pruebas
1. **pytest**
    ```bash
   Para ejecutar las pruebas del proyecto, utiliza:
   pytest accounts
   pytest shelter

## Notas
Asegúrate de que PostgreSQL esté en ejecución y accesible en localhost con el puerto 5432.
Si necesitas modificar la configuración de la base de datos o del entorno, edita el archivo .env en la raíz del proyecto.
