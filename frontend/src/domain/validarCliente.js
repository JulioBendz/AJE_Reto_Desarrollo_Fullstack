function correoValido(email) {
  const arroba = email.indexOf("@")
  if (arroba <= 0 || arroba !== email.lastIndexOf("@")) return false
  const dominio = email.slice(arroba + 1)
  const punto = dominio.lastIndexOf(".")
  return punto > 0 && punto < dominio.length - 1 && !email.includes(" ")
}

export function validarCliente(datos) {
  const nombres = (datos.nombres ?? "").trim()
  const email = (datos.email ?? "").trim()
  const telefono = (datos.telefono ?? "").trim()
  const errores = {}

  if (!nombres) errores.nombres = "El nombre es obligatorio"
  else if (nombres.length > 255) errores.nombres = "El nombre admite hasta 255 caracteres"

  if (!email) errores.email = "El correo es obligatorio"
  else if (email.length > 255 || !correoValido(email)) errores.email = "El correo no es válido"

  if (telefono.length > 50) errores.telefono = "El teléfono admite hasta 50 caracteres"

  return {
    valido: Object.keys(errores).length === 0,
    errores,
    datos: { nombres, email, telefono: telefono || null },
  }
}
