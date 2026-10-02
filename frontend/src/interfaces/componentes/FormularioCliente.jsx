export function FormularioCliente({ valores, errores, enviando, textoBoton, onChange, onSubmit }) {
  function campo(evento) {
    onChange(evento.target.name, evento.target.value)
  }

  return (
    <form
      noValidate
      onSubmit={(evento) => {
        evento.preventDefault()
        onSubmit()
      }}
    >
      <label htmlFor="nombres">Nombres</label>
      <input
        id="nombres"
        name="nombres"
        value={valores.nombres}
        onChange={campo}
        maxLength={255}
        aria-invalid={Boolean(errores.nombres)}
      />
      {errores.nombres ? <p className="campo-error">{errores.nombres}</p> : null}

      <label htmlFor="email">Correo</label>
      <input
        id="email"
        name="email"
        type="email"
        value={valores.email}
        onChange={campo}
        maxLength={255}
        aria-invalid={Boolean(errores.email)}
      />
      {errores.email ? <p className="campo-error">{errores.email}</p> : null}

      <label htmlFor="telefono">Teléfono</label>
      <input
        id="telefono"
        name="telefono"
        value={valores.telefono}
        onChange={campo}
        maxLength={50}
        aria-invalid={Boolean(errores.telefono)}
      />
      {errores.telefono ? <p className="campo-error">{errores.telefono}</p> : null}

      <button type="submit" disabled={enviando}>
        {enviando ? "Guardando…" : textoBoton}
      </button>
    </form>
  )
}
