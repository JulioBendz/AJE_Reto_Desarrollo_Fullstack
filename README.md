# Reto de Desarrollo Fullstack

Aplicación CRUD de clientes con frontend React, backend, API pública de Retool y PostgreSQL. El alcance está cerrado en la especificación; el avance se anota aparte.

- Especificación: [docs/spec/reto-desarrollo-fullstack.md](docs/spec/reto-desarrollo-fullstack.md)
- Stack: [docs/adr/0001-stack-del-reto.md](docs/adr/0001-stack-del-reto.md)
- Seguimiento: [docs/seguimiento.md](docs/seguimiento.md)

Stack fijado: React 18, FastAPI, SQLAlchemy, Requests, Pycircuitbreaker, PostgreSQL 17 y Docker Compose.

El contenedor se levanta con **Docker Engine** dentro de Ubuntu en WSL. Es el Docker gratuito. No se usa Docker Desktop.

## Base de datos local

Ubuntu ya queda instalado con `wsl --install` en un PowerShell de administrador. Después de reiniciar Windows, abre la aplicación **Ubuntu**. La contraseña que pide `sudo` es la de ese usuario Linux, no la de Windows.

Estos comandos instalan Docker Engine y el plugin de Compose:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
```

| Comando | Qué hace |
|---|---|
| `sudo apt-get update` | Actualiza la lista de paquetes de Ubuntu. |
| `sudo apt-get install -y ca-certificates curl` | Instala lo necesario para descargar la clave de Docker. `-y` acepta sin preguntar. |
| `sudo install -m 0755 -d /etc/apt/keyrings` | Crea la carpeta donde se guarda esa clave. |
| `sudo curl ... docker.asc` | Descarga la clave oficial del repositorio de Docker. |
| `sudo chmod a+r ...` | Permite que el sistema lea la clave. |
| `echo "deb ..." \| sudo tee ...` | Agrega el repositorio estable de Docker Engine a Ubuntu. |
| `sudo apt-get update` | Vuelve a leer la lista, ahora con ese repositorio. |
| `sudo apt-get install -y docker-ce ... docker-compose-plugin` | Instala el motor gratuito y `docker compose`. |
| `sudo usermod -aG docker $USER` | Permite usar Docker sin `sudo` en la siguiente sesión. |

Cierra Ubuntu, ábrelo de nuevo y levanta la base:

```bash
sudo service docker start
cd /mnt/e/julio-bendezu/AJE_Reto_Desarrollo_Fullstack
docker compose up -d
docker compose exec postgres psql -U postgres -d retoDB -c "\d cliente"
```

| Comando | Qué hace |
|---|---|
| `sudo service docker start` | Arranca el motor. Hay que repetirlo después de cada encendido de la laptop. |
| `cd /mnt/e/...` | Entra a la carpeta del proyecto. El disco `E:` de Windows se ve en Ubuntu como `/mnt/e`. |
| `docker compose up -d` | Crea PostgreSQL 17, el backend y la pantalla. `-d` los deja corriendo en segundo plano. |
| `docker compose exec ... \d cliente` | Muestra las columnas de `cliente`. Usuario y contraseña locales: `postgres` / `postgres`. Puerto: `5432`. |

## Pruebas del backend

Comprueban los cinco endpoints, el id aleatorio, la baja lógica y los códigos 201, 200, 204, 400, 404, 409 y 503.

La mayoría usa un repositorio en memoria y un Retool falso: no escribe en PostgreSQL ni llama a internet. Dos pruebas sí usan la base `retoDB`, así que el contenedor tiene que estar levantado. El circuito de Retool se prueba interceptando la red, sin salir a `retoolapi.dev`.

El recorrido real, Retool y después PostgreSQL, se hace con el servidor en marcha: desde Swagger o desde la pantalla.

```bash
cd backend
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\pytest
```

## Configuración local

Las URLs y credenciales de esta máquina van en `backend/.env`. Ese archivo no se sube a Git. La plantilla que sí se versiona es `backend/.env.example`.

```powershell
cd backend
copy .env.example .env
```

Abre `backend/.env` y reemplaza solo el valor de `RETOOL_API_URL`. No la pegues en el código.

### Cómo obtener la URL de Retool

1. Entra a [https://retool.com/api-generator](https://retool.com/api-generator).
2. En **Build Your Dataset** crea las columnas del cliente. Pon los títulos `nombres`, `email` y `telefono`. El tipo puede ser texto. El spec permite que el payload externo no coincida exactamente con la tabla.
3. En **Configuration**, el nombre del API ponlo `clientes`. La cantidad de filas puede ser 50.
4. Pulsa **Generate API**.
5. En la pantalla siguiente copia **Endpoint URL**. Se ve así: `https://retoolapi.dev/AbC123/clientes`. Copia esa base, sin un número final como `/1`.
6. Pégala en `backend/.env`:

```env
RETOOL_API_URL=https://retoolapi.dev/AbC123/clientes
```

`DATABASE_URL` ya apunta al PostgreSQL local del `docker compose`. No hace falta cambiarla. Esa cadena vive solo en `.env`; el código la lee y no la repite.

## Contrato del API

Con la base levantada, desde `backend`:

```powershell
.\.venv\Scripts\uvicorn app.main:aplicacion --reload
```

Swagger queda en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). El contrato OpenAPI 3 está en [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json).

`CORS_ORIGINS` lista los orígenes del navegador que pueden llamar al API. En local son la pantalla de Vite (`5173`) y la pantalla del contenedor (`8080`). No van en el código.

## Pantalla en desarrollo

Con el API en el puerto 8000, desde `frontend`:

```powershell
npm install
npm run dev
```

La consulta abre en [http://127.0.0.1:5173](http://127.0.0.1:5173). Habla solo con `/api/clientes`. La plantilla del destino es `frontend/.env.example` (`VITE_API_URL`). Si no existe `frontend/.env`, el valor por defecto es `http://127.0.0.1:8000`.

## Los tres contenedores

Para el despliegue que pide el reto, detén el `uvicorn` y el `npm run dev` si siguen ocupando los puertos 8000 y 5173. En Ubuntu:

```bash
sudo service docker start
cd /mnt/e/julio-bendezu/AJE_Reto_Desarrollo_Fullstack
docker compose up -d --build
```

| Dirección | Qué es |
|---|---|
| [http://127.0.0.1:8080](http://127.0.0.1:8080) | Pantalla servida por el contenedor |
| [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) | Swagger del backend en contenedor |
| `localhost:5432` | PostgreSQL |

El backend del contenedor usa el nombre `postgres` para llegar a la base. Esa dirección está en `docker-compose.yml` y reemplaza el `127.0.0.1` de `backend/.env`, que sirve cuando el API corre en Windows.

## Calidad con SonarQube

El servidor de análisis no forma parte de los tres contenedores de la aplicación. Se levanta aparte:

```bash
cd /mnt/e/julio-bendezu/AJE_Reto_Desarrollo_Fullstack
docker compose -f docker-compose.sonar.yml up -d
```

Cuando [http://127.0.0.1:9000](http://127.0.0.1:9000) responda, un servidor recién creado entra con `admin` / `admin` y obliga a cambiar esa contraseña. En esta máquina el cambio ya está hecho. La clave queda solo en `sonar-admin.local`, fuera del repositorio.

En el IDE, el plugin que nombra el reto es **SonarQube for IDE**. Conéctalo así:

1. En [http://127.0.0.1:9000](http://127.0.0.1:9000), avatar → My Account → Security → Generate Tokens. Tipo User Token, nombre `cursor`. Copia el token; no lo subas al repositorio.
2. En Cursor, `Ctrl+Shift+P` → **SonarQube: Focus on SonarQube View**.
3. En ese panel, **Add SonarQube Server Connection**. URL `http://127.0.0.1:9000`, el token y un nombre, por ejemplo `Reto local`.
4. **Bind this workspace to a SonarQube project** y elige `Reto clientes` (`aje-reto-clientes`).

Esa conexión subraya en el editor las reglas del servidor. La puerta de calidad la sigue calculando el scanner, no el plugin.

Las pruebas con cobertura, desde cada carpeta. Pytest escribe `.coverage` (dato interno) y `coverage.xml` (lo que lee Sonar). Vitest escribe `frontend/coverage/lcov.info`.

```powershell
cd backend
.\.venv\Scripts\python -m pytest --cov=app --cov-report=term-missing --cov-report=xml
cd ..\frontend
npm test -- --coverage
```

El informe de Python queda con la ruta `backend/app`, que es la que el scanner encuentra desde la raíz. Luego, en Ubuntu:

```bash
bash escanear-sonar.sh
```

El scanner usa `sonar-project.properties` y el token de `sonar-token.local`. Ninguno de los dos tokens se guarda en el repositorio.
