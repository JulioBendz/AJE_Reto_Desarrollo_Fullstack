import { Link, Route, Routes } from "react-router-dom"
import { Consulta } from "./paginas/Consulta.jsx"
import { Edicion } from "./paginas/Edicion.jsx"
import { Registro } from "./paginas/Registro.jsx"

export function App({ casos }) {
  return (
    <div className="pagina">
      <header>
        <p className="marca">Reto fullstack</p>
        <h1>Clientes</h1>
        <nav>
          <Link to="/">Consulta</Link>
          <Link to="/registro">Registro</Link>
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Consulta casos={casos} />} />
          <Route path="/registro" element={<Registro casos={casos} />} />
          <Route path="/clientes/:id/editar" element={<Edicion casos={casos} />} />
        </Routes>
      </main>
    </div>
  )
}
