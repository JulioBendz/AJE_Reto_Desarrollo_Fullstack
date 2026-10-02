import { describe, expect, it, vi } from "vitest"
import { crearCasos } from "../application/casosClientes.js"
import { validarCliente } from "./validarCliente.js"

describe("validarCliente", () => {
  it("recorta nombre y telefono", () => {
    const resultado = validarCliente({ nombres: " Ana Ruiz ", email: "ana@ejemplo.com", telefono: " 999 " })
    expect(resultado.valido).toBe(true)
    expect(resultado.datos).toEqual({ nombres: "Ana Ruiz", email: "ana@ejemplo.com", telefono: "999" })
  })

  it("rechaza el nombre vacio y un correo invalido", () => {
    const resultado = validarCliente({ nombres: "  ", email: "no-es-email", telefono: "" })
    expect(resultado.valido).toBe(false)
    expect(resultado.errores.nombres).toBeTruthy()
    expect(resultado.errores.email).toBeTruthy()
  })
})

describe("casos de clientes", () => {
  it("no llama al api si el alta es invalida", async () => {
    const api = { crear: vi.fn() }
    await expect(crearCasos(api).crear({ nombres: "", email: "x", telefono: "" })).rejects.toThrow(
      "Datos de entrada inválidos",
    )
    expect(api.crear).not.toHaveBeenCalled()
  })

  it("elimina por el id del cliente", async () => {
    const api = { eliminar: vi.fn().mockResolvedValue(null) }
    await crearCasos(api).eliminar(4)
    expect(api.eliminar).toHaveBeenCalledWith(4)
  })
})
