# API Libros - Documentación del Proyecto

## Descripción

Este proyecto es una API desarrollada en Python que interactúa con una base de datos PostgreSQL. La API está diseñada para gestionar libros y autores, y está contenida en un entorno Docker para facilitar su despliegue y escalabilidad. Utilizamos **Poetry** para la gestión de dependencias y PostgreSQL como base de datos. Todo el proyecto está configurado para correr con un solo comando utilizando Docker Compose.

## Estructura del Proyecto

```
├── deployment/
│   ├── Dockerfile       # Definición de la imagen Docker para la API
│   ├── migrations/      # Migraciones de base de datos para PostgreSQL
├── src/
│   └── app.py           # Código principal de la API
├── pyproject.toml       # Archivo de configuración de dependencias gestionado por Poetry
├── poetry.lock          # Archivo de bloqueo de dependencias
├── docker-compose.yml   # Archivo de configuración para Docker Compose
└── README.md            # Documentación del proyecto
```

## Requisitos

Antes de comenzar, asegúrate de tener instalados los siguientes programas:

- Docker
- Docker Compose

## Configuración de la Aplicación

### Variables de entorno

En el archivo `docker-compose.yml`, las siguientes variables de entorno son utilizadas:

- `ENVIRONMENT`: define el entorno en el que se ejecuta la aplicación (`production`, `development`, etc.)
- `DATABASE_HOST`: el host donde se encuentra la base de datos (en este caso, el contenedor `db`).
- `DATABASE_PORT`: el puerto utilizado para conectarse a la base de datos (5432 por defecto).
- `DATABASE_USER`: nombre de usuario para la base de datos (`app_admin`).
- `DATABASE_PASSWORD`: contraseña para la base de datos (`app_admin`).
- `DATABASE_NAME`: nombre de la base de datos utilizada (`libros`).

## Instrucciones de Instalación

1. **Clonar el repositorio**

   Clona este repositorio en tu máquina local:

   ```bash
   git clone 
   cd api-libros
   ```

2. **Construir los contenedores**

   Usa Docker Compose para construir y desplegar los contenedores de la API y la base de datos:

   ```bash
   docker-compose up --build
   ```

   Este comando realizará lo siguiente:
   - Construirá la imagen de la API definida en el `Dockerfile`.
   - Inicializará la base de datos PostgreSQL y aplicará cualquier migración en el directorio `deployment/migrations`.

3. **Acceder a la API**

   La API estará disponible en el puerto `9000`. Puedes acceder a ella utilizando `http://localhost:9000`.

4. **Acceder a PostgreSQL**

   Si necesitas acceder a la base de datos directamente, puedes usar las siguientes credenciales:

   - **Host**: `localhost`
   - **Puerto**: `5432`
   - **Usuario**: `app_admin`
   - **Contraseña**: `app_admin`
   - **Base de datos**: `libros`

## Endpoints

La API expone los siguientes endpoints para gestionar autores y libros:

### Autores
- `GET /autores`: Lista todos los autores.
- `POST /autores`: Añade un nuevo autor.
- `GET /autores/{id}`: Obtiene los detalles de un autor por su ID.
- `PUT /autores/{id}`: Actualiza los detalles de un autor por su ID.
- `DELETE /autores/{id}`: Elimina un autor por su ID (No se puede eliminar si tiene libros asociados).

### Libros
- `GET /libros`: Lista todos los libros.
- `POST /libros`: Añade un nuevo libro.
- `GET /libros/{id}`: Obtiene los detalles de un libro por su ID.
- `PUT /libros/{id}`: Actualiza los detalles de un libro por su ID.
- `DELETE /libros/{id}`: Elimina un libro por su ID.

## Validaciones

- **Campos requeridos**: Se validan todos los campos requeridos para crear o actualizar tanto autores como libros.
- **Restricción de eliminación de autores**: No se permite eliminar un autor si tiene libros asociados.

## Detalles del Dockerfile

El `Dockerfile` define cómo se construye el contenedor de la API. Aquí te doy un desglose rápido de los pasos principales:

1. **Base de la imagen**:
   Utilizamos la imagen oficial de Python `python:3.12`.

2. **Instalación de dependencias**:
   Utilizamos Poetry para gestionar las dependencias del proyecto y las instalamos en la imagen Docker.

3. **Configuración del contenedor**:
   - Copiamos los archivos del proyecto al directorio `/app` dentro del contenedor.
   - Exponemos el puerto `9000` para la API.
   - Finalmente, el contenedor se ejecuta con el comando `CMD ["python", "app.py"]`.

## Volúmenes

- `postgres_data`: Se utiliza para persistir los datos de PostgreSQL, asegurando que los datos no se pierdan cuando el contenedor se detiene o reinicia.
- `./deployment/migrations`: Directorio que contiene las migraciones de base de datos.

## Redes

- `app-network`: Una red de tipo `bridge` que permite la comunicación entre los contenedores de la aplicación y la base de datos.

## Comandos Útiles

- **Construir y levantar los contenedores**:

  ```bash
  docker-compose up --build
  ```

- **Detener los contenedores**:

  ```bash
  docker-compose down
  ```

- **Ejecutar un shell dentro del contenedor de la aplicación**:

  ```bash
  docker exec -it <nombre_contenedor_app> /bin/bash
  ```

## Mantenimiento

Si necesitas agregar nuevas dependencias al proyecto, puedes hacerlo editando el archivo `pyproject.toml`. Después, ejecuta el siguiente comando dentro del contenedor de la aplicación:

```bash
poetry add <nueva_dependencia>
```

## Contribuciones

Si deseas contribuir al proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama con el nombre de tu feature (`git checkout -b feature/nueva-feature`).
3. Haz commit de tus cambios (`git commit -m 'Agrega nueva feature'`).
4. Haz push a la rama (`git push origin feature/nueva-feature`).
5. Abre un Pull Request.

