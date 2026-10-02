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
| `docker compose up -d` | Crea el contenedor de PostgreSQL 17, la base `retoDB` y la tabla `cliente`. `-d` lo deja corriendo en segundo plano. |
| `docker compose exec ... \d cliente` | Muestra las columnas de `cliente`. Usuario y contraseña locales: `postgres` / `postgres`. Puerto: `5432`. |

## Pruebas del backend

No requieren Docker. Comprueban los cinco endpoints, el id aleatorio, la baja lógica y los códigos 201, 200, 204, 400, 404, 409 y 503.

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
