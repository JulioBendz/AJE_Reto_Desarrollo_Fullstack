const CORREO = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export function validarCliente(datos) {
  const nombres = (datos.nombres ?? "").trim()
  const email = (datos.email ?? "").trim()
  const telefono = (datos.telefono ?? "").trim()
  const errores = {}

  if (!nombres) errores.nombres = "El nombre es obligatorio"
  else if (nombres.length > 255) errores.nombres = "El nombre admite hasta 255 caracteres"

  if (!email) errores.email = "El correo es obligatorio"
  else if (email.length > 255 || !CORREO.test(email)) errores.email = "El correo no es válido"

  if (telefono.length > 50) errores.telefono = "El teléfono admite hasta 50 caracteres"

  return {
    valido: Object.keys(errores).length === 0,
    errores,
    datos: { nombres, email, telefono: telefono || null },
  }
}
