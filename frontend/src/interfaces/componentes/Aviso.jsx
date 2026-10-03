export function Aviso({ texto, tipo = "ok" }) {
  if (!texto) return null
  return (
    <output className={tipo === "error" ? "aviso aviso-error" : "aviso aviso-ok"}>{texto}</output>
  )
}
