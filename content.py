"""
Block-based content system for the CFD Explorer info panels.

Block constructors return plain dicts; render_blocks() converts them to Dash components.
"""

import uuid

from dash import html, dcc
import dash_bootstrap_components as dbc


# ─── Block constructors ────────────────────────────────────────────────────────

def collapsible(title, *children):
    """Expanding/collapsing section that can contain any other blocks."""
    return {"type": "collapsible", "title": title, "children": list(children)}


def latex(expr):
    """Display-mode LaTeX equation rendered via MathJax."""
    return {"type": "latex", "expr": expr}


def image_text(src, caption, img_side="left"):
    """Side-by-side image and text. img_side: 'left' or 'right'."""
    return {"type": "image_text", "src": src, "caption": caption, "img_side": img_side}


def bullets(*items):
    """Bullet list of strings."""
    return {"type": "bullets", "items": list(items)}


def paragraph(content):
    """Plain text paragraph."""
    return {"type": "text", "content": content}


# ─── Renderer ──────────────────────────────────────────────────────────────────

_TEXT_STYLE = {"color": "#bbb", "fontSize": "0.92rem", "lineHeight": "1.6"}


def render_blocks(blocks):
    """Convert a list of block descriptors into Dash components."""
    components = []
    for block in blocks:
        btype = block["type"]

        if btype == "text":
            components.append(
                html.P(block["content"], style={**_TEXT_STYLE, "margin": "0 0 0.6rem"})
            )

        elif btype == "latex":
            components.append(
                dcc.Markdown(
                    f"$$\n{block['expr']}\n$$",
                    mathjax=True,
                    style={"overflowX": "auto", "margin": "0.5rem 0", "textAlign": "center"},
                )
            )

        elif btype == "bullets":
            components.append(
                html.Ul(
                    [html.Li(item, style=_TEXT_STYLE) for item in block["items"]],
                    style={"paddingLeft": "1.4rem", "margin": "0.4rem 0 0.8rem"},
                )
            )

        elif btype == "image_text":
            img_col = dbc.Col(
                html.Img(
                    src=block["src"],
                    style={"width": "100%", "borderRadius": "6px",
                           "border": "1px solid #2d2d4a"},
                ),
                width=5,
            )
            txt_col = dbc.Col(html.P(block["caption"], style=_TEXT_STYLE), width=7)
            cols = (
                [img_col, txt_col]
                if block.get("img_side", "left") == "left"
                else [txt_col, img_col]
            )
            components.append(dbc.Row(cols, className="align-items-center mb-3"))

        elif btype == "collapsible":
            uid = str(uuid.uuid4())
            components.append(
                dbc.Accordion(
                    dbc.AccordionItem(
                        html.Div(
                            render_blocks(block["children"]),
                            style={"padding": "0.25rem 0"},
                        ),
                        title=block["title"],
                        item_id=f"{uid}-item",
                    ),
                    id=f"{uid}-acc",
                    start_collapsed=True,
                    className="mb-2",
                )
            )

    return components


# ─── General / home page content ──────────────────────────────────────────────

HOME_CONTENT = [
    paragraph(
        "Nuestra aplicación permite visualizar la dinámica de fluidos computacionales mediante gráficas con las cuales "
        "el usuario puede interactuar mediante los parámetros. Presenta ecuaciones en 1D y 2D como también visualización de "
        "las ecuaciones de Navier-Stokes."
    ),
    collapsible(
        "¿Qué es la dinámica de Fluidos Computacional?",
        paragraph(
            "La dinámica de fluidos computacional es la ciencia de usar computadoras para analizar y predecir los flujos de líquidos y gases "
            "mediante ecuaciones y análisis. Esta ciencia incorpora varios elementos de la física y está presente en nuestra vida diaria desde "
            "las vibraciones de nuestra voz hasta el vuelo de un avión. Es por esto que resulta tan importante generar contenido que permita su "
            "mejor comprensión al público en general."
        ),
    ),
    collapsible(
        "Historia de la dinámica de fluidos computacional",
        paragraph(
            "Al inicio del siglo 20, se empezaron a usar las ecuaciones de Navier-Stokes, estas ecuaciones son vitales y representan "
            "el inicio de la ciencia de la dinámica de fluidos computacionales al ofrecer los planos teóricos del comportamiento de los fluidos. "
            "La aparición de las primeras computadoras en los años 50 y 60 fue el punto de inflexión en esta ciencia; se empezaron a resolver "
            "problemas complejos, algunos incluso considerados imposibles de resolver en la época. Los métodos numéricos ayudaron a los investigadores "
            "a dividir estos problemas en elementos y analizar las propiedades de los fluidos de manera más sencilla. En la actualidad, la gran capacidad "
            "de cómputo permite resolver problemas aún más complejos en un menor tiempo, como analizar un avión en pleno vuelo."
        ),
    ),
    collapsible(
        "Aplicaciones generales",
        bullets(
            "Desarrollo aeroespacial y defensa: Modelado del flujo del viento alrededor de un avión para predecir el impulso.",
            "Industria automotriz: Predicción de qué tan eficiente es el enfriado del motor, ajuste de sensores, acústica, modelado de la batería, etc.",
            "Energías renovables: Medición de la eficiencia del hidrógeno con respecto a otros combustibles, análisis de almacenamiento de energía y de consumo energético.",
            "Salud: Análisis del flujo de la sangre y el oxígeno en la sangre, medición de eficiencia de nuevos medicamentos.",
            "Marina: Propulsión naval, resistencia del casco de un barco y simulación de la interacción de las olas con la nave.",
        ),
    ),
    collapsible(
        "Tipos de ecuaciones",
        paragraph("Las ecuaciones están organizadas por orden de complejidad:"),
        bullets(
            "Convección lineal en 1D",
            "Convección no lineal en 1D",
            "Ecuación de difusión en 1D",
            "Ecuación de Burgers en 1D",
            "Laplace y Poisson en 2D",
            "Ecuaciones de convección y difusión en 2D",
            "Ecuaciones de Navier-Stokes: Cavity flow y Channel flow",
        ),
    ),
    collapsible(
        "Ecuaciones de Navier-Stokes",
        paragraph(
            "Esta es la segunda ley de Newton aplicada al fluido: la fuerza es igual a la masa por la aceleración."
        ),
        latex(
            r"\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} "
            r"= -\frac{1}{\rho}\nabla p + \nu \nabla^2 \mathbf{u}"
        ),
        latex(r"\nabla \cdot \mathbf{u} = 0"),
        paragraph(
            "Lo que hace a estas ecuaciones complejas es que son no lineales, y es por esto que la dinámica de fluidos computacional requiere la "
            "aplicación iterativa de métodos numéricos."
        ),
    ),
    collapsible(
        "Referencias",
        bullets(
            "Ansys. (s.f.). What is Computational Fluid Dynamics (CFD)?. Simulation Topics. https://www.ansys.com/simulation-topics/what-is-computational-fluid-dynamics",
            "PTC. (s.f.). Computational Fluid Dynamics. CAD software solutions. https://www.ptc.com/en/technologies/cad/simulation-and-analysis/computational-fluid-dynamics",
            "Volupe. (s.f.). Basic CFD Concepts — A Practical Introduction to Computational Fluid Dynamics. https://volupe.com/support/basic-cfd-concepts-fluid-dynamics/",
        ),
    ),
]


# ─── Per-equation info blocks ──────────────────────────────────────────────────

INFO_1D_DIFFUSION = [
    paragraph(
        "También conocida como la ecuación de calor, describe la difusión, "
        "que es la distribución de las partículas en un sistema determinado, "
        "donde hay regiones con mayor concentración que otras."
    ),
    latex(r"\frac{\partial u}{\partial t} = \nu \frac{\partial^2 u}{\partial x^2}"),
    collapsible(
        "¿Cómo se relaciona con CFD?",
        paragraph(
            "Representa el término viscoso de las ecuaciones de fluidos. "
            "En CFD, sirve para probar esquemas numéricos implícitos y explícitos de disipación."
        ),
    ),
    collapsible(
        "Variables",
        bullets(
            "nx — nodos en X",
            "nt — intervalos",
            "ν — Coeficiente de difusión",
            "σ — CFL ≤ 0.49",
        ),
    ),
    collapsible(
        "Aplicaciones",
        bullets(
            "Un ejemplo de sus aplicaciones es predecir la dispersión de los "
            "contaminantes en un lago a lo largo del tiempo.",
        ),
    ),
    collapsible(
        "Referencias",
        bullets(
            "Study Smarter. (2024, 10 de junio). Difusión. "
            "https://www.studysmarter.es/resumenes/ingenieria/termodinamica-de-ingenieria/ecuacion-de-difusion/",
        ),
    ),
]

INFO_1D_LINEAR_CONVECTION = [
    paragraph(
        "Muestra la transferencia del calor a través de un fluido; "
        "este viaja a través del movimiento de la masa de dicho fluido."
    ),
    latex(r"\frac{\partial u}{\partial t} + c \frac{\partial u}{\partial x} = 0"),
    collapsible(
        "¿Cómo se relaciona con CFD?",
        paragraph(
            "Es la base para entender cómo viaja la información en una malla computacional. "
            "Ayuda a estudiar el número de Courant (CFL) y la estabilidad numérica."
        ),
    ),
    collapsible(
        "Variables",
        bullets(
            "nx — nodos en X",
            "nt — intervalos",
            "c — Velocidad de propagación de la onda",
            "σ — CFL ≤ 1",
        ),
    ),
    collapsible(
        "Aplicaciones",
        bullets(
            "Las empresas de gas o petróleo inyectan un químico rastreador en una tubería. "
            "Usan esta ecuación en un modelo de una sola dimensión (la línea del tubo) para calcular cuánto tiempo tardará el químico en "
            "llegar a los sensores río abajo y detectar si hubo una pérdida de presión o fuga en el trayecto.",
        ),
    ),
    collapsible(
        "Referencias",
        bullets(
            "Study Smarter. (2024, 12 de junio). Convección. "
            "https://www.studysmarter.es/resumenes/ingenieria/termodinamica-de-ingenieria/conveccion/",
        ),
    ),
]

INFO_1D_NONLINEAR_CONVECTION = [
    paragraph(
        "A diferencia de la convección lineal, la velocidad del fluido no es una constante externa, "
        "está acoplada al movimiento, "
        "lo que genera que la velocidad de propagación cambia con el flujo."
    ),
    latex(r"\frac{\partial u}{\partial t} + u \frac{\partial u}{\partial x} = 0"),
    collapsible(
        "¿Cómo se relaciona con CFD?",
        paragraph(
            "Este término no lineal es el causante de la turbulencia y el caos en los fluidos. "
            "Es el problema matemático más complejo de Navier-Stokes ya que introduce fenómenos "
            "de choque donde zonas rápidas alcanzan a las lentas."
        ),
    ),
    collapsible(
        "Variables",
        bullets(
            "nx — nodos en X",
            "nt — intervalos",
            "c — velocidad de propagación de la onda",
            "σ — CFL ≤ 1",
        ),
    ),
    collapsible(
        "Aplicaciones",
        paragraph(
            "Aunque nació para fluidos, se usa formalmente en ingeniería civil para diseñar el flujo de tráfico "
            "en túneles o puentes de un solo carril. "
            "Permite predecir en qué punto exacto un frenado ligero causará un embotellamiento masivo kilómetros atrás."
        ),
    ),
    collapsible(
        "Referencias",
        bullets(
            "Study Smarter. (2024, 12 de junio). Convección. "
            "https://www.studysmarter.es/resumenes/ingenieria/termodinamica-de-ingenieria/conveccion/",
        ),
    ),
]

INFO_BURGERS_1D = [
    paragraph(
        "Modelo de movimiento turbulento de fluidos propuesto por J.M. Burgers, "
        "siendo publicados todos sus artículos respecto al modelo en 1948 (Beck, 1948). "
        "La ecuación de Burgers combina la convección no lineal con la difusión viscosa."
    ),
    collapsible(
        "Solución exacta",
        paragraph(
            "La transformación de Cole-Hopf linealiza la ecuación de Burgers. "
            "La solución analítica se calcula con SymPy y se muestra junto al resultado numérico."
        ),
        latex(r"u(x,t) = -2\nu \frac{\partial}{\partial x} \ln \phi(x,t)"),
    ),
    collapsible(
        "Interpretación física",
        bullets(
            "La convección de la curva representa dispersión de la energía cinética del fluido.",
            "Una mayor difusión suaviza la dispersión de la energía.",
            "Mayor viscosidad → difusión más suave. Menor viscosidad → cambios bruscos en la ecuación.",
        ),
    ),
    collapsible(
        "Parámetros",
        bullets(
            "nx — Cantidad de puntos a representar en el eje x",
            "nt — Cantidad de unidades de tiempo consideradas en el desplazamiento de la ecuación",
            "ν (viscosidad cinemática) — Controla la fuerza de dispersión de la ecuación",
        ),
    ),
    collapsible(
        "Usos/aplicaciones de la ecuación",
        bullets(
            "Simplificación de la ecuación de Navier-Stokes.",
            "Modelo de referencia para analizar otras Ecuaciones Diferenciales Parciales.",
            "Caracterización de otras leyes de conservación escalares viscosas.",
        )
    ),
    collapsible(
        "Referencias",
        bullets(
            "Beck, M. (s.f.). Burgers Equation. Heriot-Watt University. https://math.bu.edu/people/mabeck/Beck2012_burgers.pdf"
        )
    )
]

INFO_2D_LAPLACE = [
    paragraph(
        "La ecuación de Laplace permite modelar flujos potenciales en campos de velocidad sin circulación."
    ),
    latex(r"\frac{\partial^2 p}{\partial x^2} + \frac{\partial^2 p}{\partial y^2} = 0"),
    collapsible(
        "¿Cómo se relaciona con CFD?",
        paragraph(
            "Es la parte más importante del flujo potencial (fluidos ideales, no viscosos e irrotacionales). "
            "Permite calcular campos de velocidad complejos de manera rápida usando funciones de corriente "
            "antes de recurrir a simulaciones más complejas."
        ),
    ),
    collapsible(
        "Variables",
        bullets(
            "nx — cuadrículas en x",
            "ny — cuadrículas en y",
            "Tolerancia de convergencia — Umbral para detener la iteración",
        ),
    ),
    collapsible(
        "Aplicaciones",
        bullets(
            "Este modelo es útil para estudiar flujos laminares alrededor de objetos sumergidos, "
            "como al diseñar cascos de barcos, donde se busca minimizar la resistencia al fluido.",
        ),
    ),
    collapsible(
        "Referencias",
        bullets(
            "Study Smarter. (2024, 5 de septiembre). Ecuaciones de Laplace. "
            "https://www.studysmarter.es/resumenes/ingenieria/ingenieria-quimica/ecuaciones-de-laplace/",
        ),
    ),
]

INFO_2D_POISSON = [
    paragraph(
        "La ecuación de Poisson en física es fundamental, "
        "ya que relaciona la densidad de carga de un sistema con el campo de potencial que genera."
    ),
    latex(r"\frac{\partial^2 p}{\partial x^2} + \frac{\partial^2 p}{\partial y^2} = b(x,y)"),
    collapsible(
        "¿Cómo se relaciona con CFD?",
        paragraph(
            "Es crucial para resolver fluidos incompresibles, como el agua o el aire a baja velocidad. "
            "En algoritmos clásicos de CFD la presión no tiene una ecuación directa, "
            "así que se construye una ecuación de Poisson para la presión. En cada paso de tiempo, "
            "se resuelve esta ecuación para asegurar que el campo de velocidades respete la conservación de la masa."
        ),
    ),
    collapsible(
        "Variables",
        bullets(
            "nx — cuadrículas en x",
            "ny — cuadrículas en y",
            "nt — contador de iteraciones",
        ),
    ),
    collapsible(
        "Aplicaciones",
        paragraph(
            "En un simulador de CFD, cuando el agua pasa a través de las aspas de una bomba, la velocidad del fluido cambia constantemente. "
            "La ecuación de Poisson se usa para calcular el mapa de presiones dentro de la bomba. Si la presión baja demasiado en una zona, "
            "el agua puede hervir de golpe y destruir el metal de la bomba."
        ),
    ),
    collapsible(
        "Referencias",
        bullets(
            "Study Smarter. (2024, 20 de junio). Ecuación de Poisson. "
            "https://www.studysmarter.es/resumenes/fisica/electromagnetismo/ecuacion-de-poisson/",
        ),
    ),
]

INFO_2D_DIFFUSION = [
    paragraph(
        "También conocida como la ecuación de calor, describe la difusión, "
        "que es la distribución de las partículas en un sistema determinado, "
        "donde hay regiones con mayor concentración que otras."
    ),
    latex(
        r"\frac{\partial u}{\partial t} = \nu \left("
        r"\frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2}\right)"
    ),
    collapsible(
        "¿Cómo se relaciona con CFD?",
        paragraph(
            "Representa el término viscoso de las ecuaciones de fluidos. "
            "En CFD, sirve para probar esquemas numéricos implícitos y explícitos de disipación."
        ),
    ),
    collapsible(
        "Variables",
        bullets(
            "nx — nodos en x",
            "ny — nodos en y",
            "nt — Intervalos",
            "ν — Coeficiente de difusión",
            "σ — CFL",
        ),
    ),
    collapsible(
        "Aplicaciones",
        paragraph(
            "Los ingenieros de hardware usan esta ecuación en un plano 2D para ver cómo el calor "
            "generado por los transistores se esparce por la placa de circuito, "
            "permitiendo determinar dónde posicionar los ventiladores o disipadores de calor."
        ),
    ),
    collapsible(
        "Referencias",
        bullets(
            "Study Smarter. (2024, 10 de junio). Difusión. "
            "https://www.studysmarter.es/resumenes/ingenieria/termodinamica-de-ingenieria/ecuacion-de-difusion/",
        ),
    ),
]

INFO_2D_LINEAR_CONVECTION = [
    paragraph(
        "Muestra la transferencia del calor a través de un fluido; este viaja a través del movimiento de la masa de dicho fluido."
    ),
    latex(
        r"\frac{\partial u}{\partial t} "
        r"+ c\frac{\partial u}{\partial x} + c\frac{\partial u}{\partial y} = 0"
    ),
    collapsible(
        "¿Cómo se relaciona con CFD?",
        paragraph(
            "Es la base para entender cómo viaja la información en una malla computacional. "
            "Ayuda a estudiar el número de Courant (CFL) y la estabilidad numérica."
        ),
    ),
    collapsible(
        "Variables",
        bullets(
            "nx, ny — nodos en X y Y",
            "nt — intervalos",
            "c — Velocidad de onda en ambas direcciones",
            "σ — CFL ≤ 1",
        ),
    ),
    collapsible(
        "Aplicaciones",
        bullets(
            "Cuando un volcán hace erupción, los meteorólogos usan esta ecuación en un mapa 2D "
            "para predecir hacia dónde se moverá la nube de ceniza en las próximas horas basándose en la velocidad del viento, "
            "permitiendo cerrar aeropuertos a tiempo.",
        ),
    ),
    collapsible(
        "Referencias",
        bullets(
            "Study Smarter. (2024, 12 de junio). Convección. "
            "https://www.studysmarter.es/resumenes/ingenieria/termodinamica-de-ingenieria/conveccion/",
        ),
    ),
]

INFO_2D_NONLINEAR_CONVECTION = [
    paragraph(
        "A diferencia de la convección lineal, la velocidad del fluido no es una constante externa, "
        "está acoplada al movimiento, lo que genera que la velocidad de propagación cambia con el flujo."
    ),
    latex(
        r"\frac{\partial u}{\partial t} "
        r"+ u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y} = 0"
    ),
    latex(
        r"\frac{\partial v}{\partial t} "
        r"+ u\frac{\partial v}{\partial x} + v\frac{\partial v}{\partial y} = 0"
    ),
    collapsible(
        "¿Cómo se relaciona con CFD?",
        paragraph(
            "Este término no lineal es el causante de la turbulencia y el caos en los fluidos. "
            "Es el problema matemático más complejo de Navier-Stokes ya que introduce fenómenos "
            "de choque donde zonas rápidas alcanzan a las lentas."
        ),
    ),
    collapsible(
        "Variables",
        bullets(
            "nx, ny — nodos en X y Y",
            "nt — intervalos",
            "σ — número CFL",
        ),
    ),
    collapsible(
        "Aplicaciones",
        paragraph(
            "En las primeras etapas de diseño de un dron, se usa para calcular cómo el aire "
            "de alta velocidad que pasa por encima del dron choca e interactúa con el aire de baja velocidad del entorno, "
            "antes de que la fricción del aire empiece a importar."
        ),
    ),
    collapsible(
        "Referencias",
        bullets(
            "Study Smarter. (2024, 12 de junio). Convección. "
            "https://www.studysmarter.es/resumenes/ingenieria/termodinamica-de-ingenieria/conveccion/",
        ),
    ),
]

INFO_BURGERS_2D = [
    paragraph(
        "La ecuación de Burgers 2D incorpora la difusión viscosa a la convección no lineal en 2D. "
        "Ambas componentes de velocidad evolucionan simultáneamente bajo la misma estructura de EDP."
    ),
    latex(
        r"\frac{\partial u}{\partial t} + u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y} "
        r"= \nu\left(\frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2}\right)"
    ),
    latex(
        r"\frac{\partial v}{\partial t} + u\frac{\partial v}{\partial x} + v\frac{\partial v}{\partial y} "
        r"= \nu\left(\frac{\partial^2 v}{\partial x^2} + \frac{\partial^2 v}{\partial y^2}\right)"
    ),
    paragraph(
        "La ecuación anterior se discretiza para ser aproximada. Su forma resultante es la siguiente:"
    ),
    latex(
        r"\begin{split}& \frac{u_{i,j}^{n+1} - u_{i,j}^n}{\Delta t} + u_{i,j}^n \frac{u_{i,j}^n-u_{i-1,j}^n}{\Delta x} + v_{i,j}^n \frac{u_{i,j}^n - u_{i,j-1}^n}{\Delta y} = \\& \qquad \nu \left( \frac{u_{i+1,j}^n - 2u_{i,j}^n+u_{i-1,j}^n}{\Delta x^2} + \frac{u_{i,j+1}^n - 2u_{i,j}^n + u_{i,j-1}^n}{\Delta y^2} \right)\end{split}"
    ),
    latex(
        r"\begin{split} v_{i,j}^{n+1} = & v_{i,j}^n - \frac{\Delta t}{\Delta x} u_{i,j}^n (v_{i,j}^n - v_{i-1,j}^n) - \frac{\Delta t}{\Delta y} v_{i,j}^n (v_{i,j}^n - v_{i,j-1}^n) \\& + \frac{\nu \Delta t}{\Delta x^2}(v_{i+1,j}^n-2v_{i,j}^n+v_{i-1,j}^n) + \frac{\nu \Delta t}{\Delta y^2} (v_{i,j+1}^n - 2v_{i,j}^n + v_{i,j-1}^n)\end{split}"
    ),
    collapsible(
        "Interpretación física",
        paragraph("Dos efectos en competencia dan forma a la solución:"),
        bullets(
            "La convección representa la dispersión de la energía cinética del fluido.",
            "Una mayor difusión suaviza la dispersión de la energía.",
            "Mayor viscosidad → difusión más suave. Menor viscosidad → cambios bruscos en la ecuación.",
        ),
    ),
    collapsible(
        "Parámetros",
        bullets(
            "nx, ny — Cantidad de puntos a representar en los ejes (x, y) respectivamente",
            "nt — Cantidad de unidades de tiempo consideradas en el desplazamiento de la ecuación",
            "ν (viscosidad cinemática) — Controla la fuerza de dispersión de la ecuación",
            "σ — parámetro de estabilidad (recomendado usar valores pequeños)",
        ),
    ),
    collapsible(
        "Aplicaciones",
        paragraph(
            "Se usa para la ruptura de olas en ingeniería naval, así como para diseñar puertos, muelles o rompeolas. "
            "El software calcula cómo las olas del mar avanzan (convección) "
            "y cómo la fricción con el fondo marino o los bloques de concreto (difusión) las frena, "
            "prediciendo la fuerza con la que golpearán la estructura."
        ),
    ),
    collapsible(
        "Referencias",
        bullets(
            "Beck, M. (s.f.). Burgers Equation. Heriot-Watt University. https://math.bu.edu/people/mabeck/Beck2012_burgers.pdf"
        )
    )
]

INFO_CAVITY_FLOW = [
    paragraph(
        "El problema \"Lid-Driven Cavity\" plantea un contenedor cuadrado, delimitado a dos dimensiones y con su tapa o pared superior sometida a movimiento. "
        "Ha sido ampliamente estudiado en el ámbito de la mecánica de fluidos y se han propuesto numerosas soluciones diversas, entre las cuales están las ecuaciones de Navier-Stokes."
    ),
    collapsible(
        "Ecuaciones fundamentales",
        paragraph("Momento u (eje x):"),
        latex(
            r"\frac{\partial u}{\partial t} + u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y} "
            r"= -\frac{1}{\rho}\frac{\partial p}{\partial x} "
            r"+ \nu\left(\frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2}\right)"
        ),
        paragraph("Momento v (eje y):"),
        latex(
            r"\frac{\partial v}{\partial t} + u\frac{\partial v}{\partial x} + v\frac{\partial v}{\partial y} "
            r"= -\frac{1}{\rho}\frac{\partial p}{\partial y} "
            r"+ \nu\left(\frac{\partial^2 v}{\partial x^2} + \frac{\partial^2 v}{\partial y^2}\right)"
        ),
        paragraph("Ecuación de presión de Poisson (derivada de la ecuación de incompresibilidad):"),
        latex(
            r"\frac{\partial^2 p}{\partial x^2}+\frac{\partial^2 p}{\partial y^2} = -\rho\left(\frac{\partial u}{\partial x}\frac{\partial u}{\partial x}+2\frac{\partial u}{\partial y}\frac{\partial v}{\partial x}+\frac{\partial v}{\partial y}\frac{\partial v}{\partial y} \right)"
        ),
    ),
    collapsible(
        "Número de Reynolds",
        paragraph("El número de Reynolds caracteriza el régimen del flujo:"),
        latex(r"\text{Re} = \frac{U L}{\nu}"),
        paragraph(
            "Con velocidad de tapa U = 1 y longitud de cavidad L = 2, Re = 2/ν. "
            "Mayor Re → dominado por inercia (estructura de vórtice compleja); "
            "menor Re → dominado por viscosidad (vórtice primario simple)."
        ),
    ),
    collapsible(
        "Interpretación de resultados",
        bullets(
            "Zonas de presión: Los colores representan una escala para la presión del fluido en una región dada.",
            "Vectores de velocidad: Las flechas representan la dirección y magnitud del movimiento del fluido.",
            "Líneas de corriente: Las líneas curvas muestran la forma que adopta el movimiento del fluido.",
        ),
    ),
    collapsible(
        "Parámetros",
        bullets(
            "nx, ny — Coordenadas de espacio (x, y) para la caja delimitadora. Aumentar el tamaño suaviza el comportamiento del fluido, pero vuelve más costosa la operación.",
            "nt — Número de intervalos de tiempo a considerar en el cálculo",
            "nit — Cantidad de iteraciones a realizar para el cálculo de las zonas de presión. A mayor número de iteraciones, más preciso es el resultado.",
            "ρ — Densidad del fluido",
            "ν — Viscosidad cinemática",
            "dt — Tamaño de los intervalos de tiempo que se consideran para 'nt'",
        ),
    ),
    collapsible(
        "Aplicaciones",
        bullets(
            "Diseño de tanques de mezclado industrial.",
            "Diseño de sistemas de enfriamiento eléctrico.",
            "Analizar cómo circula el aire dentro de una habitación con una ventana abierta para la renovación de aire.",
        ),
    ),
    collapsible(
        "Referencias",
        bullets(
            "Sheposh, R. (2023). Navier-Stokes equation. EBSCO. https://www.ebsco.com/research-starters/mathematics/navier-stokes-equation",
            "Zhang, J., Xiao, B., Yang, W. (2022, 17 de noviembre). Numerical Study of Lid-Driven Square Cavity Flow with Embedded Circular Obstacles Using Spectral/hp Element Methods. MDPI. https://www.mdpi.com/2076-3417/12/22/11711",
            "Reusken, A. (2012, 06 de enero). Numerical Methods for the Navier-Stokes equations. RWTH Aachen University. https://www.igpm.rwth-aachen.de/Download/ws1112/numanaIV/NavierStokes.pdf",
        )
    )
]

INFO_CHANNEL_FLOW = [
    paragraph(
        "Simula el movimiento de un fluido situado en un canal donde: "
        "el fluido está en contacto con la atmósfera, su cantidad se mantiene constante en cualquier área dada del canal y "
        "es propulsado principalmente por gravedad y no por presión (Dias et al., 2016, p. 1). "
        "Lo anterior se resuelve por medio de la proyección de Chorin, mostrando la turbulencia presente a lo largo del canal."
    ),
    collapsible(
        "Ecuaciones gobernantes",
        paragraph("Mismo sistema de Navier-Stokes que el cavity flow, más una fuerza de cuerpo F en la dirección x:"),
        latex(
            r"\frac{\partial u}{\partial t} + \ldots = "
            r"-\frac{1}{\rho}\frac{\partial p}{\partial x} + \nu\nabla^2 u + F"
        ),
        paragraph("Condiciones de frontera periódicas en x: la salida se conecta de vuelta a la entrada, simulando un canal infinito."),
    ),
    collapsible(
        "Estado estacionario analítico (flujo de Poiseuille)",
        paragraph("El flujo completamente desarrollado tiene un perfil de velocidad parabólico:"),
        latex(r"u(y) = \frac{F}{2\nu}\,y\,(L_y - y)"),
        paragraph(
            "La simulación itera hasta que se alcanza este estado estacionario o se supera el número máximo de pasos."
        ),
    ),
    collapsible(
        "Parámetros",
        bullets(
            "nx, ny — nodos en X y Y",
            "nit — iteraciones de presión de Poisson por intervalo",
            "ρ — densidad",
            "ν — viscosidad cinemática",
            "F — magnitud de la fuerza del cuerpo",
            "dt — intervalo de tiempo",
            "Max Iterations — número máximo de intervalos antes de parar",
        ),
    ),
    collapsible(
        "Aplicaciones",
        bullets(
            "Cuando se diseñan ductos de aire en un edificio, los ingenieros usan simulaciones de channel flow para asegurarse de contar con la energía exacta para que el aire llegue a todas las oficinas.",
            "Calcular el costo de bombeo de un gasoducto dependiendo de la viscosidad.",
            "Uso en dispositivos cardiovasculares para evitar la mezcla de líquidos con la sangre.",
        ),
    ),
    collapsible(
        "Referencias",
        bullets(
            "Sheposh, R. (2023). Navier-Stokes equation. EBSCO. https://www.ebsco.com/research-starters/mathematics/navier-stokes-equation",
            "Zhang, J., Xiao, B., Yang, W. (2022, 17 de noviembre). Numerical Study of Lid-Driven Square Cavity Flow with Embedded Circular Obstacles Using Spectral/hp Element Methods. MDPI. https://www.mdpi.com/2076-3417/12/22/11711",
            "Reusken, A. (2012, 06 de enero). Numerical Methods for the Navier-Stokes equations. RWTH Aachen University. https://www.igpm.rwth-aachen.de/Download/ws1112/numanaIV/NavierStokes.pdf",
        )
    )
]
