import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { Aviso } from "../componentes/Aviso.jsx"
import { FormularioCliente } from "../componentes/FormularioCliente.jsx"

const VACIO = { nombres: "", email: "", telefono: "" }

export function Registro({ casos }) {
  const navigate = useNavigate()
  const [valores, setValores] = useState(VACIO)
  const [errores, setErrores] = useState({})
  const [aviso, setAviso] = useState("")
  const [enviando, setEnviando] = useState(false)

  async function guardar() {
    setAviso("")
    setErrores({})
    setEnviando(true)
    try {
      await casos.crear(valores)
      navigate("/", { state: { aviso: "Cliente registrado" } })
    } catch (fallo) {
      setErrores(fallo.errores || {})
      if (!fallo.errores) setAviso(fallo.message)
    } finally {
      setEnviando(false)
    }
  }

  return (
    <section>
      <h2>Registro</h2>
      <Aviso texto={aviso} tipo="error" />
      <FormularioCliente
        valores={valores}
        errores={errores}
        enviando={enviando}
        textoBoton="Registrar"
        onChange={(nombre, valor) => setValores((actual) => ({ ...actual, [nombre]: valor }))}
        onSubmit={guardar}
      />
      <p>
        <Link to="/">Volver al listado</Link>
      </p>
    </section>
  )
}
