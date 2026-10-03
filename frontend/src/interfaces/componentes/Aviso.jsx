export function Aviso({ texto, tipo = "ok" }) {
  if (!texto) return null
  return (
    <p className={tipo === "error" ? "aviso aviso-error" : "aviso aviso-ok"} role="status">
      {texto}
    </p>
  )
}
