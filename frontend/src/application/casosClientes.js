import { validarCliente } from "../domain/validarCliente.js"

function rechazarSiEsInvalido(datos) {
  const resultado = validarCliente(datos)
  if (resultado.valido) return resultado.datos
  const error = new Error("Datos de entrada inválidos")
  error.errores = resultado.errores
  throw error
}

export function crearCasos(api) {
  return {
    listar() {
      return api.listar()
    },
    obtener(id) {
      return api.obtener(id)
    },
    async crear(datos) {
      return api.crear(rechazarSiEsInvalido(datos))
    },
    async actualizar(id, datos) {
      return api.actualizar(id, rechazarSiEsInvalido(datos))
    },
    eliminar(id) {
      return api.eliminar(id)
    },
  }
}
