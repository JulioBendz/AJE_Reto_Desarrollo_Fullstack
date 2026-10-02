const base = (import.meta.env.VITE_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "")

async function pedir(ruta, opciones = {}) {
  let respuesta
  try {
    respuesta = await fetch(`${base}${ruta}`, {
      ...opciones,
      headers: {
        Accept: "application/json",
        ...(opciones.body ? { "Content-Type": "application/json" } : {}),
      },
    })
  } catch {
    const error = new Error("No se pudo contactar al backend")
    error.estado = 0
    throw error
  }

  if (respuesta.status === 204) return null
  const cuerpo = await respuesta.json().catch(() => ({}))
  if (!respuesta.ok) {
    const error = new Error(cuerpo.detalle || "No se pudo completar la operación")
    error.estado = respuesta.status
    throw error
  }
  return cuerpo
}

export const apiClientes = {
  listar: () => pedir("/api/clientes"),
  obtener: (id) => pedir(`/api/clientes/${id}`),
  crear: (datos) => pedir("/api/clientes", { method: "POST", body: JSON.stringify(datos) }),
  actualizar: (id, datos) => pedir(`/api/clientes/${id}`, { method: "PUT", body: JSON.stringify(datos) }),
  eliminar: (id) => pedir(`/api/clientes/${id}`, { method: "DELETE" }),
}
