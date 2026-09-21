# 🎛️ PS2 Syscall Resolver & HAL Generator

A lightweight, standalone cross-platform diagnostic tool designed to accelerate the native porting and decompilation of PlayStation 2 titles (such as *Ratchet & Clank 2*). It automatically translates MIPS R5900 Emotion Engine Kernel Syscalls and SIF tokens into portable C/C++ hardware abstraction layer signatures.

*Una herramienta de diagnóstico ligera e independiente diseñada para acelerar el port nativo y la decompilación de títulos de PlayStation 2 (como Ratchet & Clank 2). Traduce automáticamente las Syscalls del Kernel del Emotion Engine MIPS R5900 y los tokens SIF en firmas portables de la capa de abstracción de hardware en C/C++.*

---

## 🌐 Features / Características

* **Bilingüe Nativo (EN/ES):** Persistent configuration file (`data/config.json`) remembers your language choice. Type `lang` to toggle.
* *Soporte Bilingüe:* Archivo de configuración persistente que recuerda tu idioma. Escribe `lang` para cambiarlo.
* **Hybrid Search Engine:** Instantly lookup entries by Hexadecimal (`0x4B`), Decimal (`75`), or partial SDK names (`pad`, `sema`).
* *Motor de Búsqueda Híbrido:* Busca instantáneamente por Hexadecimal, Decimal o coincidencia de nombres del SDK.
* **Expandable Database:** Clean, human-readable JSON format (`data/syscall_db.json`) allowing manual additions.
* *Base de Datos Expandible:* Formato JSON limpio que permite añadir nuevos registros manualmente.

---

## 📂 Repository Structure / Estructura del Repositorio

```text
ps2-syscall-resolver/
├── data/
│   ├── config.json         # Stores user language preferences (en / es)
│   └── syscall_db.json     # Bilinguial hardware syscall database
├── .gitignore              # Excludes Python bytecode and cache files
├── README.md               # Tool documentation (This file)
└── resolver.py             # Main interactive CLI script
```

---

## 🚀 Getting Started / Guía de Inicio

### Requirements / Requisitos
* Python 3.8 or superior / *Python 3.8 o superior.*
* Absolute path robust / *Ejecutable desde cualquier terminal mediante rutas absolutas.*

### Running the Tool / Ejecución
Open your terminal in the repository directory and execute:
*Abre la terminal en el directorio del repositorio y ejecuta:*

```bash
python resolver.py
```

### Usage Examples / Ejemplos de Uso

| User Input / Entrada | Resolved Entity / Resultado | Generated Output / Salida Generada |
| :--- | :--- | :--- |
| `0x4b` o `75` | `GetOsdConfigParam` | C Signature & BIOS parameter translation / *Firma en C y propósito.* |
| `pad` | `scePadInit`, `scePadPortOpen` | List of all registered gamepad stubs / *Lista de stubs de mandos.* |
| `lang` | *UI Toggle* | Switches the tool between English and Español / *Alterna el idioma.* |

---

## ⚠️ Important JSON Rule / Regla Crítica del JSON

> [!WARNING]
> **Do NOT add comments (`//`) inside `data/config.json` or `data/syscall_db.json`.** 
> The standard JSON specification strictly forbids comments. Doing so will corrupt the files and force the script to default to English. Use `"_comment": "your text"` instead.
> 
> ***NO añadas comentarios (`//`) dentro de los archivos JSON.***
> *La especificación oficial de JSON prohíbe los comentarios. Hacerlo corromperá los archivos y forzará al script a arrancar en Inglés. Usa `_comment` si deseas dejar notas.*

---

## 📝 License / Licencia
MIT - Feel free to expand the database for your own hardware research and native ports.
*MIT - Siéntete libre de expandir la base de datos para tus propios laboratorios de hardware.*
