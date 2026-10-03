import { existsSync, readFileSync, writeFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"

const ruta = join(dirname(fileURLToPath(import.meta.url)), "coverage", "lcov.info")
if (!existsSync(ruta)) {
  process.exit(0)
}

const lineas = readFileSync(ruta, "utf8").split(/\r?\n/).map((linea) => {
  if (!linea.startsWith("SF:")) {
    return linea
  }
  const archivo = linea.slice(3).replaceAll("\\", "/")
  if (archivo.startsWith("frontend/")) {
    return `SF:${archivo}`
  }
  if (archivo.startsWith("src/")) {
    return `SF:frontend/${archivo}`
  }
  return `SF:${archivo}`
})

writeFileSync(ruta, `${lineas.join("\n").replace(/\n$/, "")}\n`)
