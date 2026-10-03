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

  it("rechaza campos ausentes, largos y correos mal formados", () => {
    const ausente = validarCliente({})
    expect(ausente.errores.nombres).toBeTruthy()
    expect(ausente.errores.email).toBeTruthy()

    const largo = validarCliente({
      nombres: "a".repeat(256),
      email: `${"a".repeat(250)}@b.com`,
      telefono: "1".repeat(51),
    })
    expect(largo.errores.nombres).toBeTruthy()
    expect(largo.errores.email).toBeTruthy()
    expect(largo.errores.telefono).toBeTruthy()

    for (const email of ["@ejemplo.com", "ana@@ejemplo.com", "ana@ejemplo.", "ana @ejemplo.com", "ana@.com"]) {
      expect(validarCliente({ nombres: "Ana", email, telefono: null }).errores.email).toBeTruthy()
    }
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

  it("lista, obtiene y actualiza a traves del api", async () => {
    const api = {
      listar: vi.fn().mockResolvedValue([]),
      obtener: vi.fn().mockResolvedValue({ id: 4 }),
      actualizar: vi.fn().mockResolvedValue({ id: 4 }),
    }
    const casos = crearCasos(api)

    await casos.listar()
    await casos.obtener(4)
    await casos.actualizar(4, { nombres: "Ana", email: "ana@ejemplo.com", telefono: "" })

    expect(api.listar).toHaveBeenCalled()
    expect(api.obtener).toHaveBeenCalledWith(4)
    expect(api.actualizar).toHaveBeenCalledWith(4, { nombres: "Ana", email: "ana@ejemplo.com", telefono: null })
  })

  it("elimina por el id del cliente", async () => {
    const api = { eliminar: vi.fn().mockResolvedValue(null) }
    await crearCasos(api).eliminar(4)
    expect(api.eliminar).toHaveBeenCalledWith(4)
  })
})
