# MeteoAnalyzer

## Descripción

Aplicación para el consumo y visualización de estadísticas de datos meteorológicos por ciudad utilizando la API de [Open-Meteo](https://open-meteo.com/en/docs).

---

Incluye:
- Modelo de base de datos relacional
- Proceso ejecutable de consulta de datos meteorológicos de ciudades por rango de fechas
- API para consulta de estadísticas relacionadas con temperaturas y precipitaciones de las ciudades

## Base de Datos (PostgreSQL +  DjangoORM)

El modelo de datos se compone de **2 tablas principales** relacionadas entre sí:

---

### 1. `cities`

| Campo       | Tipo       | Constraints              | Descripción                           |
|-------------|------------|--------------------------|---------------------------------------|
| `id`        | PK (int)   | NOT NULL, PRIMARY KEY    | Identificador único de la ciudad.     |
| `name`      | Char(100)  | NOT NULL                 | Nombre de la ciudad.                  |
| `latitude`  | Float      | Entre `-90.0` y `90.0`   | Latitud de la ciudad.                 |
| `longitude` | Float      | Entre `-180.0` y `180.0` | Longitud de la ciudad.                |

- **Constraints adicionales**: 
- UNIQUE (`name`, `latitude`, `longitude`).  


#### `weather_data`

Tabla que almacena los registros horarios de temperatura y precipitación para una ciudad y fecha concreta.

| Campo           | Tipo       | Constraints            | Descripción                                          |
|-----------------|------------|------------------------|------------------------------------------------------|
| `id`            | PK (int)   | NOT NULL, PRIMARY KEY  | Identificador único del registro.                    |
| `city_id`       | FK (int)   | FOREIGN KEY → `cities` | Ciudad a la que pertenece el dato meteorológico.     |
| `date_time`     | DateTime   | NOT NULL               | Fecha y hora del dato meteorológico.                 |
| `temperature`   | Float      | NULLABLE               | Temperatura en grados Celsius.                       |
| `precipitation` | Float      | NULLABLE               | Precipitación en milímetros.                         |

- **Constraints adicionales**: 
- UNIQUE INDEX (`city`, `date_time`).  

## Proceso de carga de datos meteorológicos

La aplicación incluye un **management command de Django** para cargar datos de temperatura y precipitación desde la API de [Open-Meteo](https://open-meteo.com/en/docs) y almacenarlos en la base de datos.

---

### Uso

El comando puede ser invocado escribiendo `python manage.py load_meteo_data_for_city`. Pero debido a que la aplicación reside en un contenedor **Docker** orquestado por **Docker Compose**, la llamada real sería la siguiente:

````bash
 docker compose exec backend python manage.py load_meteo_data_for_city {{city_name}} {{start_date}} {{end_date}} [--strategy={{strategy}} --index={{index}}]
````

#### Argumentos

| Nombre del Argumento | Tipo                                                                  | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|----------------------|-----------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| city_name            | Posicional (Obligatorio)                                              | Nombre de la ciudad a consultar                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| start_date           | Posicional (Obligatorio)                                              | Fecha de inicio de la consulta en formato YYYY-MM-DD. No puede ser menor que start_date.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| end_date             | Posicional (Obligatorio)                                              | Fecha de fin de la consulta en formato YYYY-MM-DD                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| --strategy           | Opcional                                                              | Estrategia que seguir en el caso de que la búsqueda devuelva múltiples ciudades con el mismo nombre. Valores permitidos: <br/> - `first`(por defecto): Escoge la ciudad en la primera posición <br/> - `all`: Procesa todas las ciudades recibidas para el rango de fechas dado <br/> - `select`: En medio de la ejecución muestra las opciones recibidas al usuario y solicita un input para seleccionar <br/> - `index`: El usuario pre-establecerá un índice para seleccionar la ciudad. Por ejemplo, si el índice es 2, el comando procesará la ciudad en la posición 2 de la lista recibida (es importante recordar que la posición dos no corresponde con la segunda, sino con la tercera, ya que los índices comienzan desde 0) |
| --index              | Opcional (Requerido si --strategy=index, ignorado en los demás casos) | Valor entero positivo o 0. Corresponde con el índice de la estrategia `index`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |


## API REST (Django)

Como ya se ha mencionado, la aplicación expone una API REST que permite consultar estadísticas meteorológicas almacenadas en la base de datos.  
Todas las respuestas se devuelven en formato **JSON**.

---

### Endpoints disponibles

| Método | Endpoint                 | Descripción                                                                                                                                                                                                                                                      | Query Params                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Respuestas relevantes                           |
|--------|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| GET    | `/stats/temperature/`    | Devuelve estadísticas de **temperatura** para una ciudad en un rango de fechas (media, media diaria, máximos, mínimos y umbrales).                                                                                                                               | - `city` (string, requerido, sin formato) <br/> - `start_date` (string, requerido, formato YYYY-MM-DD y menor o igual que `end_date` <br/> - `end_date` (string, requerido, formato YYYY-MM-DD) <br/> - `upper_threshold` (number, no requerido, 30.0 por defecto) <br/> - `lower_threshold` (number, no requerido, 0.0 por defecto) <br/> - `latitude` (number, no requerido, sirve para afinar la identificación de ciudad, rango [-90,90]) <br/> - `longitude` (number, no requerido, sirve para afinar la identificación de ciudad, rango [-180,180]) | - `200 OK` → lista de `CityTemperatureSchema`   |
| GET    | `/stats/precipitation/`  | Devuelve estadísticas de **precipitación** para una ciudad en un rango de fechas (total, total diario, promedio, días con precipitaciones y máximo).                                                                                                             | - `city` (string, requerido, sin formato) <br/> - `start_date` (string, requerido, formato YYYY-MM-DD y menor o igual que `end_date` <br/> - `end_date` (string, requerido, formato YYYY-MM-DD) <br/> - `latitude` (number, no requerido, sirve para afinar la identificación de ciudad, rango [-90,90]) <br/> - `longitude` (number, no requerido, sirve para afinar la identificación de ciudad, rango [-180,180])                                                                                                                                      | - `200 OK` → lista de `CityPrecipitationSchema` |
| GET    | `/stats/all/`            | Devuelve estadísticas **globales** de todas las ciudades en todas las fechas (fecha más antigua registrada, fecha más reciente registrada, temperatura media, precipitación total, días con precipitación, precipitación máxima y temperaturas máxima y mínima). | —                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | - `200 OK` → `AllCitiesWeatherSchema`           |


> **Nota:** Adicionalmente, aquellas llamadas con *query parameters* son susceptibles de devolver un *400 Bad Request* si alguno de estos no cumple con su formato esperado.

### Esquemas

#### CityTemperatureSchema
  ```json
  {
    "latitude": -3.12,
    "longitude": -70.23,
    "temperature": {
      "average": 23.1,
      "average_by_day": {
        "YYYY-MM-DD": 23.1
      },
      "max": {
        "value": 33.1,
        "date": "2018-01-10T17:00"
      },
      "min": {
        "value": 13.1,
        "date": "2018-01-10T22:00"
      },
      "hours_above_threshold": 5,
      "hours_below_threshold": 2
    }
  }
  ```
  
#### CityPrecipitationSchema
  ```json
  {
    "latitude": -3.12,
    "longitude": -70.23,
    "precipitation": {
      "total": 0.1,
      "total_by_day": {
        "YYYY-MM-DD": 0.1
      },
      "days_with_precipitation": 1,
      "max": {
        "value": 0.1,
        "date": "2018-01-10T17:00"
      },
      "average": 0.1
    }
  }
  ```
  
#### AllCitiesWeatherSchema
  ```json
  {
    " {{ CITY_NAME }}": ["{{ CityWeatherSchema }}"]
  }
  ```
  
#### CityWeatherSchema
  ```json
  {
    "start_date": "2018-01-10T17:00",
    "end_date": "2020-01-10T17:00",
    "temperature_average": 10.1,
    "precipitation_total": 0.1,
    "days_with_precipitation": 12,
    "precipitation_max": {
      "value": 0.1,
      "date": "2018-01-10T17:00"
    },
    "temperature_max": {
      "value": 30.1,
      "date": "2018-01-10T17:00"
    },
    "temperature_min": {
      "value": -0.1,
      "date": "2018-01-10T17:00"
    }
  }
  ```

### Documentación interactiva (OpenAPI)

Para explorar y probar la API, el proyecto incluye una interfaz de documentación generada automáticamente con **Swagger UI** mediante la librería [`drf_yasg`](https://github.com/axnsan12/drf-yasg).

- Mientras esté levantado el servidor en local, la documentación estará disponible en:  
    [Swagger UI (OpenAPI)](http://localhost:8000/docs/)

## Ejecución de Servicios

La aplicación se despliega mediante **Docker Compose**.  
Se incluyen dos servicios principales: la base de datos PostgreSQL y el backend en Django.

### Servicios y Perfiles

| Servicio   | Descripción                 |
|------------|-----------------------------|
| `database` | Base de datos PostgreSQL    |
| `backend`  | API Django (MeteoAnalyzer)  |

### Comandos útiles

#### Manejar aplicación

> **Nota:** Se recomienda añadir el flag `--build` la primera vez que se ejecute `docker compose up` para asegurar la correcta construcción de las imágenes.

- Levantar **toda la aplicación**:
  ```bash
  docker compose up [--build]
  ```
- Bajar **toda la aplicación**:
  ```bash
  docker compose down
  ```
- Levantar solo la **base de datos**:
  ```bash
  docker compose database up [--build]
  ```
- Bajar la **base de datos**:
  ```bash
  docker compose database down
  ```

#### Utilidades

- Ejecutar tests del backend:
  ```bash
  docker compose exec backend python manage.py test
  ```
  
### Variables de entorno

> **Nota:** Hay un fichero `.env.example` en la raíz del proyecto que puede copiarse como `.env` para ejecutar directamente con `docker-compose.yml`.  
> 
> De no existir este fichero, habría que asegurarse de cargar estas variables de entorno manualmente en el sistema.

| Variable                      | Descripción                                                                  | Ejemplo                                           | Backend |  Database  |
|-------------------------------|------------------------------------------------------------------------------|---------------------------------------------------|:-------:|:----------:|
| `SECRET_KEY`                  | Clave secreta de Django (para sesiones, CSRF, seguridad).                    | `django-insecure-xyz123`                          |    ✅    |     ❌      |
| `POSTGRES_USER`               | Usuario de la base de datos PostgreSQL.                                      | `database`                                        |    ✅    |     ✅      |
| `POSTGRES_PASSWORD`           | Contraseña de la base de datos PostgreSQL.                                   | `database`                                        |    ✅    |     ✅      |
| `POSTGRES_DB`                 | Nombre de la base de datos PostgreSQL.                                       | `database`                                        |    ✅    |     ✅      |
| `POSTGRES_PORT`               | Puerto de la base de datos PostgreSQL.                                       | `5432`                                            |    ✅    |     ✅      |
| `BACKEND_HOST`                | Host definido para exponer la API Django.                                    | `0.0.0.0`                                         |    ✅    |     ❌      |
| `BACKEND_PORT`                | Puerto definido para exponer la API Django.                                  | `8000`                                            |    ✅    |     ❌      |
| `DEBUG`                       | Activa el modo debug de Django (solo para desarrollo, **no en producción**). | `True`                                            |    ✅    |     ❌      |
| `OPEN_METEO_CITY_ENDPOINT`    | Endpoint de Open-Meteo para obtener información de ciudades.                 | `https://geocoding-api.open-meteo.com/v1/search`  |    ✅    |     ❌      |
| `OPEN_METEO_WEATHER_ENDPOINT` | Endpoint de Open-Meteo para obtener datos meteorológicos históricos.         | `https://archive-api.open-meteo.com/v1/archive`   |    ✅    |     ❌      |
