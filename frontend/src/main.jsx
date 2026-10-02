import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { BrowserRouter } from "react-router-dom"
import { crearCasos } from "./application/casosClientes.js"
import { apiClientes } from "./infrastructure/apiClientes.js"
import { App } from "./interfaces/App.jsx"
import "./index.css"

const casos = crearCasos(apiClientes)

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <App casos={casos} />
    </BrowserRouter>
  </StrictMode>,
)
