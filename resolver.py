import json
import os

# Configuración de rutas absolutas dinámicas para evitar errores de directorio
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "data", "syscall_db.json")
CONFIG_PATH = os.path.join(SCRIPT_DIR, "data", "config.json")

# Diccionario de localización interna para los textos de la interfaz de la consola
LOC_STRINGS = {
    "en": {
        "welcome": "==========================================================",
        "title":   "   🎛️  PS2 SYSCALL RESOLVER & HAL GENERATOR V1.1",
        "inputs":  "• Supported inputs: Hexadecimal (0x4b), Decimal (75) or Names (pad).",
        "missing": "• If a syscall is missing, add it to data/syscall_db.json",
        "lang_tip":"• Type 'lang' to toggle between English and Español.",
        "exit_tip":"• Type 'salir' or 'exit' to quit the tool.",
        "prompt":  "🔍 MIPS Syscall / Token -> ",
        "bye":     "👋 Closing tool. Configuration saved.",
        "found":   "📍 CAPTURED ENTRY",
        "fn_name": "Func Name",
        "fn_sig":  "C Signature",
        "fn_desc": "Purpose",
        "error":   "❌ Token '{val}' not found in the JSON database.\n",
        "switched":"🌐 UI language set to: ENGLISH."
    },
    "es": {
        "welcome": "==========================================================",
        "title":   "   🎛️  RESOLVEDOR DE SYSCALLS Y GENERADOR HAL PS2 V1.1",
        "inputs":  "• Inputs soportados: Hexadecimal (0x4b), Decimal (75) o Nombres (pad).",
        "missing": "• Si una syscall no existe, puedes añadirla a data/syscall_db.json",
        "lang_tip":"• Escribe 'lang' para alternar entre Inglés y Español.",
        "exit_tip":"• Escribe 'salir' o 'exit' para cerrar la herramienta.",
        "prompt":  "🔍 MIPS Syscall / Token -> ",
        "bye":     "👋 Cerrando herramienta. Configuración guardada.",
        "found":   "📍 REGISTRO CAPTURADO",
        "fn_name": "Función SDK",
        "fn_sig":  "Firma Port",
        "fn_desc": "Propósito",
        "error":   "❌ Token '{val}' no localizado en la base de datos JSON.\n",
        "switched":"🌐 Idioma de la interfaz configurado en: ESPAÑOL."
    }
}

def load_config():
    """Lee el archivo de configuración para recordar el idioma elegido en el pasado."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config.get("language", "en")
        except json.JSONDecodeError as e:
            # ¡PARCHE DE SEGURIDAD! Te avisa en vivo si el JSON tiene un comentario ilegal o error de comas
            print(f"⚠️  [CONFIG ERROR] data/config.json tiene un error de sintaxis: {e}")
            print("💡 Recuerda: El formato JSON estándar NO admite comentarios '//'.")
        except Exception as e:
            pass
    return "en"

def save_config(lang):
    """Guarda persistentemente la elección del idioma en la PC para el futuro."""
    try:
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump({"language": lang}, f, indent=2)
    except Exception as e:
        print(f"Error saving config: {e}")

def load_database():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error reading database: {e}")
            return {}
    return {}

def print_header(lang):
    text = LOC_STRINGS[lang]
    print(text["welcome"])
    print(text["title"])
    print(text["welcome"])
    print(text["inputs"])
    print(text["missing"])
    print(text["lang_tip"])
    print(text["exit_tip"])
    print("═"*60 + "\n")

def main():
    db = load_database()
    current_lang = load_config()
    print_header(current_lang)

    while True:
        text = LOC_STRINGS[current_lang]
        try:
            user_input = input(text["prompt"]).strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{text['bye']}")
            break

        if not user_input:
            continue

        low_input = user_input.lower()
        if low_input in ["salir", "exit"]:
            print(text["bye"])
            break

        # CONMUTADOR DE IDIOMA DINÁMICO EN VIVO
        if low_input == "lang":
            current_lang = "es" if current_lang == "en" else "en"
            save_config(current_lang)
            print(f"\n{LOC_STRINGS[current_lang]['switched']}\n")
            continue

        found_entries = {}

        # 1. Búsqueda por texto (Nombre parcial de la función del SDK de Sony)
        if not user_input.isdigit() and not any(low_input.startswith(p) for p in ["0x", "a", "b", "c", "d", "e", "f"]):
            for hex_id, data in db.items():
                if low_input in data["name"].lower():
                    found_entries[hex_id] = data
        else:
            # 2. Búsqueda numérica (Hexadecimal o Decimal)
            target_hex = ""
            try:
                if low_input.startswith("0x"):
                    target_hex = hex(int(user_input, 16))
                elif any(c in low_input for c in ["a", "b", "c", "d", "e", "f"]):
                    target_hex = hex(int(user_input, 16))
                else:
                    target_hex = hex(int(user_input, 10))
            except ValueError:
                pass

            if target_hex in db:
                found_entries[target_hex] = db[target_hex]

        # Desplegar las coincidencias aplicando los filtros de idioma elegidos
        if found_entries:
            for hex_id, info in found_entries.items():
                dec_id = int(hex_id, 16)
                # Selecciona la clave de descripción bilingüe adecuada (desc_en o desc_es)
                desc_key = f"desc_{current_lang}"
                description = info.get(desc_key, info.get("desc_en", ""))

                print("\n" + "═"*60)
                print(f"{text['found']}: {hex_id} (Decimal: {dec_id})")
                print(f"🔹 {text['fn_name']}:  {info['name']}")
                print(f"🔹 {text['fn_sig']}:   {info['return']} {info['name']}({info['args']});")
                print(f"🔹 {text['fn_desc']}:    {description}")
                print("═"*60 + "\n")
        else:
            print(text["error"].format(val=user_input))

if __name__ == "__main__":
    main()
