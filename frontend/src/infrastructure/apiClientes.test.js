import { afterEach, describe, expect, it, vi } from "vitest"
import { apiClientes } from "./apiClientes.js"

function respuesta(status, cuerpo) {
  return {
    status,
    ok: status >= 200 && status < 300,
    json: async () => cuerpo,
  }
}

afterEach(() => {
  vi.unstubAllGlobals()
})

describe("apiClientes", () => {
  it("lista, crea, actualiza y elimina", async () => {
    const fetch = vi
      .fn()
      .mockResolvedValueOnce(respuesta(200, [{ id: 1 }]))
      .mockResolvedValueOnce(respuesta(201, { id: 4 }))
      .mockResolvedValueOnce(respuesta(200, { id: 4, nombres: "Ana" }))
      .mockResolvedValueOnce(respuesta(204, null))
    vi.stubGlobal("fetch", fetch)

    await expect(apiClientes.listar()).resolves.toEqual([{ id: 1 }])
    await expect(apiClientes.crear({ nombres: "Ana" })).resolves.toEqual({ id: 4 })
    await expect(apiClientes.actualizar(4, { nombres: "Ana" })).resolves.toEqual({ id: 4, nombres: "Ana" })
    await expect(apiClientes.eliminar(4)).resolves.toBeNull()
    expect(fetch.mock.calls.map(([url, opciones]) => [url, opciones.method || "GET"])).toEqual([
      ["http://127.0.0.1:8000/api/clientes", "GET"],
      ["http://127.0.0.1:8000/api/clientes", "POST"],
      ["http://127.0.0.1:8000/api/clientes/4", "PUT"],
      ["http://127.0.0.1:8000/api/clientes/4", "DELETE"],
    ])
  })

  it("traduce un fallo del backend y una red caida", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(respuesta(409, { detalle: "El email ya esta registrado" })))
    await expect(apiClientes.obtener(3)).rejects.toThrow("El email ya esta registrado")

    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("fallo")))
    await expect(apiClientes.listar()).rejects.toThrow("No se pudo contactar al backend")

    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ status: 500, ok: false, json: async () => { throw new Error("no-json") } }))
    await expect(apiClientes.listar()).rejects.toThrow("No se pudo completar la operación")
  })
})
