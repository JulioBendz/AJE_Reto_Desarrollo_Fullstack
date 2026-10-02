import { useEffect, useState } from "react"
import { Link, useNavigate, useParams } from "react-router-dom"
import { Aviso } from "../componentes/Aviso.jsx"
import { FormularioCliente } from "../componentes/FormularioCliente.jsx"

export function Edicion({ casos }) {
  const { id } = useParams()
  const navigate = useNavigate()
  const [valores, setValores] = useState(null)
  const [errores, setErrores] = useState({})
  const [aviso, setAviso] = useState("")
  const [enviando, setEnviando] = useState(false)

  useEffect(() => {
    casos
      .obtener(id)
      .then((cliente) =>
        setValores({
          nombres: cliente.nombres,
          email: cliente.email,
          telefono: cliente.telefono || "",
        }),
      )
      .catch((fallo) => setAviso(fallo.message))
  }, [casos, id])

  async function guardar() {
    setAviso("")
    setErrores({})
    setEnviando(true)
    try {
      await casos.actualizar(id, valores)
      navigate("/", { state: { aviso: "Cliente actualizado" } })
    } catch (fallo) {
      setErrores(fallo.errores || {})
      if (!fallo.errores) setAviso(fallo.message)
    } finally {
      setEnviando(false)
    }
  }

  return (
    <section>
      <h2>Edición</h2>
      <Aviso texto={aviso} tipo="error" />
      {valores ? (
        <FormularioCliente
          valores={valores}
          errores={errores}
          enviando={enviando}
          textoBoton="Guardar cambios"
          onChange={(nombre, valor) => setValores((actual) => ({ ...actual, [nombre]: valor }))}
          onSubmit={guardar}
        />
      ) : null}
      <p>
        <Link to="/">Volver al listado</Link>
      </p>
    </section>
  )
}
