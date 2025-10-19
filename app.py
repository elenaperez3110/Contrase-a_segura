import re
import streamlit as st

st.set_page_config(page_title="Validador de Contraseñas", page_icon="🔐", layout="centered")

# --- Parámetros y utilidades ---
SPECIALS = "¡!¿?@#&%"  # exactamente los que pides

UPPER_RE = re.compile(r"[A-Z]")
LOWER_RE = re.compile(r"[a-z]")
DIGIT_RE = re.compile(r"\d")
SPECIAL_RE = re.compile(rf"[{re.escape(SPECIALS)}]")  # escapa por seguridad

def validar_contrasena(pwd: str):
    """Devuelve un dict con cada condición y el total cumplido."""
    condiciones = {
        "longitud": 5 < len(pwd) < 17,
        "mayuscula": bool(UPPER_RE.search(pwd)),
        "minuscula": bool(LOWER_RE.search(pwd)),
        "numero": bool(DIGIT_RE.search(pwd)),
        "especial": bool(SPECIAL_RE.search(pwd)),
    }
    total = sum(condiciones.values())
    return condiciones, total

def mensaje_por_total(total: int):
    if total == 5:
        return "Contraseña fuerte", "success"
    elif total == 4:
        return "Contraseña débil", "warning"
    else:
        return "Contraseña no válida", "error"

# --- UI ---
st.title("🔐 Validador de Contraseñas")
st.caption("Reglas: 6–16 caracteres, al menos una mayúscula, una minúscula, un número y un especial de: ¡ ! ¿ ? @ # & %")

pwd = st.text_input("Introduce tu contraseña:", type="password")

if st.button("Validar", type="primary") or pwd:
    condiciones, total = validar_contrasena(pwd)
    mensaje, alert_type = mensaje_por_total(total)

    # Alerta principal
    getattr(st, alert_type)(mensaje)

    # Checklist de condiciones
    st.subheader("Detalle de validación")
    def checkmark(ok): return "✅" if ok else "❌"
    st.write(f"{checkmark(condiciones['longitud'])} Longitud entre 6 y 16 caracteres")
    st.write(f"{checkmark(condiciones['mayuscula'])} Contiene al menos **una mayúscula**")
    st.write(f"{checkmark(condiciones['minuscula'])} Contiene al menos **una minúscula**")
    st.write(f"{checkmark(condiciones['numero'])} Contiene al menos **un número**")
    st.write(f"{checkmark(condiciones['especial'])} Contiene al menos **un carácter especial** de `{SPECIALS}`")

    # Sugerencia básica si no es fuerte
    if total < 5:
        faltan = [k for k, v in condiciones.items() if not v]
        recomendaciones = {
            "longitud": "Usa una longitud entre 6 y 16 caracteres.",
            "mayuscula": "Añade al menos una letra mayúscula (A–Z).",
            "minuscula": "Añade al menos una letra minúscula (a–z).",
            "numero": "Añade al menos un dígito (0–9).",
            "especial": f"Añade al menos un carácter especial de: {SPECIALS}",
        }
        st.info("Mejoras sugeridas:\n\n- " + "\n- ".join(recomendaciones[f] for f in faltan))

# Pie de página
st.caption("Este validador no almacena contraseñas.")
