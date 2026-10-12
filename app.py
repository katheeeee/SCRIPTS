import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


COLOR_TEXTO = "#2f4858"
COLOR_RECTA = "#457b9d"
COLOR_PUNTO = "#e76f51"
COLOR_INTERP = "#2a9d8f"
COLOR_AMARILLO = "#e9c46a"
COLOR_MORADO = "#8e7dbe"
COLOR_BORDE = "#a8dadc"
COLOR_BANDA = "#e8f1f5"
COLOR_GRID = "#c9d6df"

CSS = """
<style>
    .stApp { background-color: #f7f9fc; }
    h1, h2, h3 { color: #2f4858; }
    .card {
        background-color: #ffffff;
        border-left: 6px solid #a8dadc;
        border-radius: 10px;
        padding: 14px 18px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    }
    .card-title {
        font-size: 0.80rem;
        color: #6b7c8c;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .card-value {
        font-size: 1.6rem;
        color: #2f4858;
        font-weight: 600;
        margin: 4px 0 0 0;
    }
    .step-num {
        display: inline-block;
        background-color: #e8f1f5;
        color: #457b9d;
        font-weight: 600;
        border-radius: 50%;
        width: 26px;
        height: 26px;
        line-height: 26px;
        text-align: center;
        margin-right: 8px;
    }
    .step-title { color: #2f4858; font-weight: 600; }
</style>
"""


def fmt(valor):
    if valor is None:
        return "no definido"
    if not math.isfinite(valor):
        return "no definido"
    if float(valor) == 0:
        valor = 0.0
    if float(valor).is_integer():
        return str(int(valor))
    return f"{valor:.10g}"


def tarjeta(titulo, valor, color=COLOR_BORDE):
    st.markdown(
        f"""
        <div class="card" style="border-left-color:{color};">
            <p class="card-title">{titulo}</p>
            <p class="card-value">{valor}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def paso(numero, titulo, expresion):
    with st.container(border=True):
        st.markdown(
            f'<span class="step-num">{numero}</span>'
            f'<span class="step-title">{titulo}</span>',
            unsafe_allow_html=True,
        )
        st.latex(expresion)


def interpolar(x0, y0, x1, y1, x):
    m = (y1 - y0) / (x1 - x0)
    p = y0 + m * (x - x0)
    return m, p


def calcular_errores(valor_real, aproximado):
    absoluto = abs(valor_real - aproximado)
    if valor_real == 0:
        return absoluto, None, None
    relativo = absoluto / abs(valor_real)
    porcentual = relativo * 100
    return absoluto, relativo, porcentual


def grafica(x0, y0, x1, y1, x, p):
    xmin, xmax = sorted([x0, x1])
    margen = max((xmax - xmin) * 0.35, 1.0)
    xs = np.linspace(xmin - margen, xmax + margen, 200)
    m = (y1 - y0) / (x1 - x0)
    ys = y0 + m * (xs - x0)

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    ax.axvspan(xmin, xmax, color=COLOR_BANDA, zorder=0,
               label="Intervalo de interpolación")
    ax.plot(xs, ys, color=COLOR_RECTA, linewidth=2,
            label="Recta interpolante", zorder=3)
    ax.plot([x0, x1], [y0, y1], "o", color=COLOR_PUNTO, markersize=9,
            label="Puntos conocidos", zorder=4)
    ax.plot([x], [p], "o", color=COLOR_INTERP, markersize=10,
            label="Punto interpolado", zorder=4)
    ax.axvline(x, color=COLOR_GRID, linestyle=":", linewidth=1, zorder=1)

    caja = dict(boxstyle="round,pad=0.3", fc="#ffffff", ec="#dce5ec")
    ax.annotate(f"({fmt(x0)}, {fmt(y0)})", (x0, y0),
                textcoords="offset points", xytext=(8, 8),
                color=COLOR_PUNTO, bbox=caja)
    ax.annotate(f"({fmt(x1)}, {fmt(y1)})", (x1, y1),
                textcoords="offset points", xytext=(8, -16),
                color=COLOR_PUNTO, bbox=caja)
    ax.annotate(f"({fmt(x)}, {fmt(p)})", (x, p),
                textcoords="offset points", xytext=(8, 8),
                color=COLOR_INTERP, bbox=dict(boxstyle="round,pad=0.3",
                                              fc="#ffffff", ec=COLOR_INTERP))

    ax.set_title("Interpolación lineal", color=COLOR_TEXTO, fontsize=13)
    ax.set_xlabel("x")
    ax.set_ylabel("P(x)")
    ax.grid(True, linestyle=":", alpha=0.5, color=COLOR_GRID)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="best", framealpha=0.9)
    fig.tight_layout()
    return fig


def cargar_ejemplo():
    st.session_state.update(
        {"x0": 2.0, "y0": 10.0, "x1": 6.0, "y1": 30.0, "x": 4.0,
         "usar_error": True, "valor_real": 21.0}
    )


def main():
    st.set_page_config(page_title="Interpolación lineal", layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)

    st.title("Interpolación lineal")
    st.caption(
        "Métodos Numéricos · estimación de un valor intermedio entre dos "
        "puntos conocidos"
    )

    defaults = {
        "x0": 2.0, "y0": 10.0, "x1": 6.0, "y1": 30.0, "x": 4.0,
        "usar_error": False, "valor_real": 21.0,
    }
    for clave, valor in defaults.items():
        if clave not in st.session_state:
            st.session_state[clave] = valor

    with st.container(border=True):
        st.subheader("Panel de entrada")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("**Punto 1**")
            e1, e2 = st.columns(2)
            with e1:
                x0 = st.number_input("x₀", step=1.0, key="x0")
            with e2:
                y0 = st.number_input("y₀", step=1.0, key="y0")
        with col_p2:
            st.markdown("**Punto 2**")
            e3, e4 = st.columns(2)
            with e3:
                x1 = st.number_input("x₁", step=1.0, key="x1")
            with e4:
                y1 = st.number_input("y₁", step=1.0, key="y1")

        col_x, col_err = st.columns(2)
        with col_x:
            x = st.number_input("x a interpolar", step=1.0, key="x")
        with col_err:
            usar_error = st.checkbox(
                "Calcular error con un valor real f(x)", key="usar_error"
            )

        valor_real = None
        if usar_error:
            valor_real = st.number_input(
                "Valor real f(x)", step=1.0, key="valor_real"
            )

        b1, b2 = st.columns([1, 1])
        with b1:
            st.button("Calcular", type="primary", width="stretch")
        with b2:
            st.button(
                "Cargar ejemplo", type="secondary",
                on_click=cargar_ejemplo, width="stretch",
            )

    if not all(math.isfinite(v) for v in (x0, y0, x1, y1, x)):
        st.error("Todas las entradas deben ser números finitos (sin NaN ni infinito).")
        st.stop()

    if math.isclose(x0, x1, rel_tol=1e-9, abs_tol=1e-12):
        st.error("Los puntos deben tener x₀ ≠ x₁. Con x₀ = x₁ la pendiente no está definida.")
        st.stop()

    m, p = interpolar(x0, y0, x1, y1, x)

    xmin, xmax = sorted([x0, x1])
    if x < xmin or x > xmax:
        st.warning(
            f"El valor x = {fmt(x)} está fuera del intervalo "
            f"[{fmt(xmin)}, {fmt(xmax)}]. Se trata de una extrapolación, "
            "no de una interpolación."
        )

    st.subheader("Resultados")
    r1, r2, r3 = st.columns(3)
    with r1:
        tarjeta("Valor aproximado P(x)", fmt(p), COLOR_INTERP)
    with r2:
        tarjeta("Pendiente m", fmt(m), COLOR_RECTA)
    with r3:
        tarjeta("Intervalo", f"[{fmt(xmin)}, {fmt(xmax)}]", COLOR_AMARILLO)

    izq, der = st.columns([1, 1])

    with izq:
        st.subheader("Solución paso a paso")
        paso(1, "Fórmula general",
             r"P(x) = y_0 + \frac{y_1 - y_0}{x_1 - x_0}\,(x - x_0)")
        paso(2, "Cálculo de la pendiente",
             r"m = \frac{y_1 - y_0}{x_1 - x_0} = "
             r"\frac{" + fmt(y1) + r" - (" + fmt(y0) + r")}{"
             + fmt(x1) + r" - (" + fmt(x0) + r")} = "
             r"\frac{" + fmt(y1 - y0) + r"}{" + fmt(x1 - x0) + r"} = " + fmt(m))
        paso(3, "Sustitución en la fórmula",
             r"P(x) = " + fmt(y0) + r" + (" + fmt(m) + r")\,\bigl("
             + fmt(x) + r" - (" + fmt(x0) + r")\bigr)")
        paso(4, "Operaciones intermedias",
             r"P(x) = " + fmt(y0) + r" + (" + fmt(m) + r")\bigl("
             + fmt(x - x0) + r"\bigr) = " + fmt(y0) + r" + "
             + fmt(m * (x - x0)))
        paso(5, "Resultado final", r"P(" + fmt(x) + r") = " + fmt(p))

    with der:
        st.subheader("Gráfica")
        fig = grafica(x0, y0, x1, y1, x, p)
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Tabla resumen")
    filas = [
        ("x₀", fmt(x0)),
        ("y₀", fmt(y0)),
        ("x₁", fmt(x1)),
        ("y₁", fmt(y1)),
        ("Pendiente m", fmt(m)),
        ("x solicitado", fmt(x)),
        ("P(x) interpolado", fmt(p)),
    ]
    destacadas = {"P(x) interpolado"}

    errores = None
    if usar_error and valor_real is not None:
        errores = calcular_errores(valor_real, p)
        absoluto, relativo, porcentual = errores
        filas.append(("Valor real f(x)", fmt(valor_real)))
        filas.append(("Error absoluto", fmt(absoluto)))
        filas.append(("Error relativo",
                      "no definido" if relativo is None else fmt(relativo)))
        filas.append(("Error porcentual",
                      "no definido" if porcentual is None else f"{fmt(porcentual)} %"))
        destacadas.update({"Error absoluto", "Error relativo", "Error porcentual"})

    tabla = pd.DataFrame(filas, columns=["Parámetro", "Valor"])

    def resaltar(fila):
        if fila["Parámetro"] in destacadas:
            return ["background-color: #e8f1f5; font-weight: 600;"] * len(fila)
        return [""] * len(fila)

    estilo = (
        tabla.style
        .apply(resaltar, axis=1)
        .set_properties(subset=["Valor"],
                        **{"text-align": "right", "font-family": "monospace"})
    )
    st.dataframe(estilo, hide_index=True, width="stretch")

    st.subheader("Análisis del error")
    if not usar_error:
        st.info(
            "No se proporcionó un valor real f(x). Sin un valor de referencia "
            "solo puede calcularse la aproximación P(x); el error verdadero no "
            "es calculable."
        )
        return

    absoluto, relativo, porcentual = errores
    e1, e2, e3 = st.columns(3)
    with e1:
        tarjeta("Error absoluto", fmt(absoluto), COLOR_PUNTO)
    with e2:
        tarjeta("Error relativo",
                "no definido" if relativo is None else fmt(relativo), COLOR_AMARILLO)
    with e3:
        tarjeta("Error porcentual",
                "no definido" if porcentual is None else f"{fmt(porcentual)} %",
                COLOR_MORADO)

    if valor_real == 0:
        st.warning(
            "El valor real f(x) = 0. El error absoluto sí está definido, pero el "
            "error relativo y porcentual no se pueden calcular porque implican "
            "dividir entre cero."
        )
    else:
        st.latex(r"E_a = |f(x) - P(x)| = |" + fmt(valor_real) + r" - ("
                 + fmt(p) + r")| = " + fmt(absoluto))
        st.latex(r"E_r = \frac{|f(x) - P(x)|}{|f(x)|} = \frac{" + fmt(absoluto)
                 + r"}{" + fmt(abs(valor_real)) + r"} = " + fmt(relativo))
        st.latex(r"E_\% = E_r \times 100 = " + fmt(porcentual) + r"\,\%")


main()
