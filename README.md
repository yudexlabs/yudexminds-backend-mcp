# FastAPI + MCP Server YudexMinds

Una aplicación FastAPI que expone tanto una API REST como un servidor MCP (Model Context Protocol), ejecutándose en un entorno Docker containerizado.

## 🚀 Características

- **API REST**: Endpoints FastAPI para operaciones CRUD y lógica de negocio
- **Servidor MCP**: Protocolo de comunicación para modelos de IA
- **Docker Compose**: Orquestación de contenedores para desarrollo y producción
- **Documentación automática**: Swagger UI y ReDoc integrados
- **Configuración flexible**: Variables de entorno para diferentes entornos

## 📋 Requisitos previos

- Docker >= 20.10
- Docker Compose >= 2.0
- Python 3.11+ (para desarrollo local)

## 🛠️ Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone <[repository-url](https://github.com/yudexlabs/yudexminds-backend-mcp)>
cd mcp-server-ideas
```

### 2. Configurar variables de entorno

Copia el archivo de ejemplo y ajusta las variables según tu entorno:

```bash
cp .env.example .env
```

### 3. Ejecutar con Docker Compose

#### Desarrollo

```bash
docker-compose up --build
```

## 🏗️ Estructura del proyecto

```
├── app/
|   ├── auth_api.py          # Autenticación API
|   ├── auth_mcp.py          # Autenticación MCP
│   ├── config.py            # Configuración
│   └── main.py              # Punto de entrada FastAPI
|
|── nginx/
|   └── config               # Configuración Nginx
|
├── docker-compose.yml       # Docker Compose
├── Dockerfile
├── requirements.txt
├── claude_desktop_config.json
└── README.md
```

## 🔌 Endpoints disponibles

### API REST

La API estará disponible en `http://localhost:8000`

- **Documentación Swagger**: `http://localhost:8000/docs`
- **Documentación ReDoc**: `http://localhost:8000/redoc`

## 🐳 Comandos Docker útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Acceder al contenedor de la aplicación
docker-compose exec app bash

# Detener todos los servicios
docker-compose down

# Limpiar volúmenes y redes
docker-compose down -v --remove-orphans

# Reconstruir sin caché
docker-compose build --no-cache
```

## 🧪 Testing

### Ejecutar tests localmente

```bash
# Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Ejecutar tests
pytest tests/

# Con coverage
pytest --cov=app tests/
```

## 📊 Monitoreo y logs

### Logs de la aplicación

```bash
# Ver logs de todos los servicios
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs app

# Seguir logs en tiempo real
docker-compose logs -f app
```
