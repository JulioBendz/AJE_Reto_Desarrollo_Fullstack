import { useEffect, useState } from "react"
import { Link, useLocation, useNavigate } from "react-router-dom"
import { Aviso } from "../componentes/Aviso.jsx"

function formatearFecha(valor) {
  const fecha = new Date(valor)
  if (Number.isNaN(fecha.getTime())) return valor
  return fecha.toLocaleString("es-PE")
}

export function Consulta({ casos }) {
  const location = useLocation()
  const navigate = useNavigate()
  const [clientes, setClientes] = useState([])
  const [aviso, setAviso] = useState("")
  const [error, setError] = useState("")

  async function cargar() {
    try {
      setClientes(await casos.listar())
      setError("")
    } catch (fallo) {
      setError(fallo.message)
    }
  }

  useEffect(() => {
    cargar()
  }, [])

  useEffect(() => {
    if (!location.state?.aviso) return
    setAviso(location.state.aviso)
    navigate(location.pathname, { replace: true, state: null })
  }, [location.pathname, location.state, navigate])

  async function eliminar(id) {
    setAviso("")
    setError("")
    try {
      await casos.eliminar(id)
      setAviso("Cliente eliminado")
      setClientes(await casos.listar())
    } catch (fallo) {
      setError(fallo.message)
    }
  }

  return (
    <section>
      <div className="encabezado-seccion">
        <h2>Consulta</h2>
        <Link to="/registro">Registrar cliente</Link>
      </div>
      <Aviso texto={aviso} />
      <Aviso texto={error} tipo="error" />
      {clientes.length === 0 ? <p>No hay clientes activos.</p> : null}
      {clientes.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Nombres</th>
              <th>Correo</th>
              <th>Teléfono</th>
              <th>Registro</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {clientes.map((cliente) => (
              <tr key={cliente.id}>
                <td>{cliente.nombres}</td>
                <td>{cliente.email}</td>
                <td>{cliente.telefono || "—"}</td>
                <td>{formatearFecha(cliente.fecha_creacion)}</td>
                <td className="acciones">
                  <Link to={`/clientes/${cliente.id}/editar`}>Editar</Link>
                  <button type="button" onClick={() => eliminar(cliente.id)}>
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}
    </section>
  )
}
