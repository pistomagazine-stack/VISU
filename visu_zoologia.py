import streamlit as st
import random
from pathlib import Path
import base64
import unicodedata

# Configuración de la página
st.set_page_config(
    page_title="Visu Máster - Biología UCM",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS definitivos y menú lateral flotante personalizado
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');

        /* Fondo general con degradado */
        .stApp {
            background: linear-gradient(to bottom, #FF0000 0%, #FF0000 25%, #000000 100%);
            background-attachment: fixed;
            color: #FFFFFF;
            font-family: 'Montserrat', sans-serif;
            text-transform: uppercase;
            padding-bottom: 120px !important;
        }

        /* Ocultar completamente la barra lateral nativa de Streamlit */
        [data-testid="stSidebar"] {
            display: none !important;
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
        }
        
        button[kind="header"], [data-testid="collapsedControl"], [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }

        /* Contenedor fijo del logotipo en la esquina superior izquierda */
        .logo-wrapper {
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 99999;
            width: 75px;
            height: 75px;
            border-radius: 14px;
            overflow: hidden;
            background: transparent;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .logo-wrapper img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            display: block;
        }

        /* Flecha de apertura: fija fuera del panel y sin caja */
        .toggle-btn-wrapper {
            position: fixed;
            top: 20px;
            left: 95px; /* Justo al terminar el logotipo: 20px + 75px */
            z-index: 1000000;
            width: 30px;
            height: 75px;
            display: flex;
            align-items: center;
            justify-content: flex-start;
        }

        .toggle-btn-wrapper a {
            color: #FFFFFF !important;
            text-decoration: none !important;
            font-size: 2.8rem;
            font-weight: 300;
            line-height: 1;
            cursor: pointer;
        }

        .toggle-btn-wrapper a:hover,
        .sidebar-close:hover {
            color: #FF0000 !important;
        }

        body:has(#customSidebar:target) .toggle-btn-wrapper {
            display: none !important;
        }

        /* Flecha de cierre dentro de la cabecera del panel */
        .sidebar-close {
            color: #FFFFFF !important;
            text-decoration: none !important;
            font-size: 2.8rem;
            font-weight: 300;
            line-height: 1;
            padding: 0 4px;
            cursor: pointer;
            flex-shrink: 0;
        }

        /* Panel lateral personalizado flotante (Inicia oculto a la izquierda) */
        .custom-sidebar {
            position: fixed;
            top: 0;
            left: -320px;
            width: min(300px, 85vw);
            height: 100vh;
            background-color: #0A0A0A;
            border-right: 3px solid #FFFFFF;
            z-index: 999999;
            transition: left 0.3s ease;
            box-shadow: 10px 0 30px rgba(0,0,0,0.8);
            padding: 20px;
            box-sizing: border-box;
            overflow-y: auto;
        }

        .custom-sidebar:target {
            left: 0;
        }

        .sidebar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            border-bottom: 2px solid #333333;
            padding-bottom: 10px;
        }

        .sidebar-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #FFFFFF;
            margin: 0;
        }

        /* Estilos para los textos interactivos del menú personalizado */
        .menu-item {
            background-color: #161616;
            border: 2px solid #333333;
            border-radius: 8px;
            padding: 12px 14px;
            width: 100%;
            display: block;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: left !important;
            margin-bottom: 8px;
            color: #FFFFFF !important;
            font-weight: 600;
            text-decoration: none !important;
            box-sizing: border-box;
        }

        .menu-item:hover {
            border-color: #FF0000;
            background-color: #222222;
            color: #FF0000 !important;
        }

        .menu-item.active {
            border-color: #FFFFFF;
            background-color: #222222;
            color: #FFFFFF !important;
        }

        /* Tarjeta central original restaurada (700px de ancho máximo y centrada) */
        .block-container {
            max-width: 700px !important;
            width: 100% !important;
            padding: 2rem !important;
            text-align: center;
            background-color: #0A0A0A;
            border: 3px solid #FFFFFF;
            border-radius: 16px;
            margin: 2rem auto 3rem auto !important;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
            box-sizing: border-box;
        }

        /* Tarjeta lateral para el truco/solución (mismo formato y exactamente 450px de ancho) */
        .side-trick-card {
            position: absolute;
            left: calc(50% + 380px);
            top: 180px;
            width: 450px;
            background-color: #0A0A0A;
            border: 3px solid #FFFFFF;
            border-radius: 16px;
            padding: 2rem;
            box-sizing: border-box;
            z-index: 99997;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
            text-align: center;
        }

        @media (max-width: 1300px) {
            .side-trick-card {
                position: relative !important;
                left: auto !important;
                top: auto !important;
                width: 100% !important;
                max-width: 450px !important;
                margin: 1.5rem auto 0 auto !important;
            }
        }

        h1, h2, h3, p, label, .stMarkdown, span, div {
            font-family: 'Montserrat', sans-serif !important;
            color: #FFFFFF;
            text-transform: uppercase !important;
        }

        h1, h2, h3, p, div.stTextInput, .stButton, .feedback-success, .img-borde, .test-result {
            margin-top: 0 !important;
            margin-bottom: 0.75rem !important;
        }

        h1 {
            color: #FFFFFF;
            font-weight: 700;
            letter-spacing: -0.03em;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            text-align: center !important;
        }

        .subtitle {
            font-family: 'Montserrat', sans-serif;
            color: #FFCCCC;
            font-size: 0.75rem;
            font-weight: 500;
            letter-spacing: 0.1em;
            opacity: 0.9;
            text-align: center !important;
        }

        .pregunta-counter {
            font-size: 0.8rem;
            color: #FFCCCC;
            text-align: center !important;
        }

        div.stTextInput {
            text-align: center;
            max-width: 450px !important;
            width: 100% !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        div.stTextInput > label {
            display: block;
            text-align: center !important;
            font-weight: 600;
            color: #FFFFFF;
            font-size: 0.75rem;
            margin-bottom: 2px !important;
        }

        div.stTextInput > div > div {
            background-color: #161616;
            border: 3px solid #FFFFFF;
            border-radius: 10px;
            box-sizing: border-box;
        }

        div.stTextInput input {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: #FFFFFF;
            text-align: center !important;
            font-family: 'Montserrat', sans-serif;
            text-transform: uppercase !important;
            padding: 6px;
            resize: none !important;
        }

        div.stTextInput [data-testid="stInputInstructions"],
        div.stTextInput [data-baseweb="input"] > div:nth-child(2),
        div.stTextInput [data-baseweb="input"] > div:last-child {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            height: 0 !important;
            opacity: 0 !important;
        }

        .stButton {
            display: flex !important;
            justify-content: center !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        .stButton > button {
            background-color: #FF0000;
            color: #FFFFFF;
            border: 3px solid #FFFFFF;
            border-radius: 10px;
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase !important;
            padding: 0.5rem 1.8rem;
            transition: background-color 0.2s ease;
            cursor: pointer;
            display: block;
            margin: 0 auto;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
        }

        .stButton > button:hover {
            background-color: #D90000;
            color: #FFFFFF;
        }

        .feedback-success {
            background-color: #80FF40 !important;
            color: #000000 !important;
            border: 3px solid #000000;
            border-radius: 10px;
            padding: 0.8rem 1rem;
            max-width: 450px;
            width: 100%;
            text-align: center !important;
            font-family: 'Montserrat', sans-serif;
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase !important;
            line-height: 1.5;
            box-sizing: border-box;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        .feedback-success * {
            color: #000000 !important;
        }

        .test-result {
            color: #FFFFFF;
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            font-size: 1.15rem;
            text-align: center !important;
            text-decoration: none !important;
            text-transform: uppercase !important;
        }

        .test-result.fail {
            color: #FF6666;
            text-decoration: none !important;
        }

        .img-borde {
            background-color: #161616;
            border: 3px solid #FFFFFF;
            border-radius: 10px;
            box-sizing: border-box;
            padding: 6px;
            max-width: 450px;
            width: 100%;
            display: block;
            text-align: center;
            margin: 0 auto;
        }

        button[kind="tertiary"] {
            min-width: 0 !important;
            width: auto !important;
            height: auto !important;
            padding: 0 !important;
            background: transparent !important;
            color: #FFFFFF !important;
            border: none !important;
            font-size: 2.5rem !important;
            font-weight: 300 !important;
            box-shadow: none !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin: auto !important;
        }
        button[kind="tertiary"]:hover {
            color: #FF0000 !important;
            background: transparent !important;
            border: none !important;
        }
        button[kind="tertiary"]:disabled {
            color: #444444 !important;
            opacity: 0.2 !important;
        }

        .footer-band {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #FF0000;
            color: #FFFFFF;
            text-align: center;
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
            font-size: 0.75rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            padding: 10px 0;
            z-index: 99998;
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

# Cargar la imagen del logo directamente desde la ruta local 'pp_2.png'
logo_path = Path("pp_2.png")
if logo_path.exists():
    logo_base64 = base64.b64encode(logo_path.read_bytes()).decode("utf-8")
else:
    logo_base64 = ""

# Sección seleccionada mediante query_params
query_params = st.query_params
if "grupo" in query_params:
    seccion_seleccionada = query_params["grupo"]
else:
    seccion_seleccionada = "VERTEBRADOS"

clase_vert = "menu-item active" if seccion_seleccionada == "VERTEBRADOS" else "menu-item"
clase_inv = "menu-item active" if seccion_seleccionada == "INVERTEBRADOS" else "menu-item"
clase_art = "menu-item active" if seccion_seleccionada == "ARTRÓPODOS" else "menu-item"

# 1. Logotipo estático con etiqueta <img> nativa para conservar la máxima nitidez
st.markdown(f"""
    <div class="logo-wrapper">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo">
    </div>
""", unsafe_allow_html=True)

# 2. Flecha de apertura fuera del panel. El fragmento #customSidebar abre el panel sin recargar.
st.markdown('<div class="toggle-btn-wrapper"><a href="#customSidebar" aria-label="Abrir menú">›</a></div>', unsafe_allow_html=True)

# 3. Panel lateral; la flecha de cierre está integrada en su cabecera.
sidebar_html = f"""
    <div id="customSidebar" class="custom-sidebar">
        <div class="sidebar-header">
            <h3 class="sidebar-title">MENÚ</h3>
            <a href="#" class="sidebar-close" aria-label="Cerrar menú">‹</a>
        </div>
        <p style='font-size: 0.75rem; color: #FFCCCC; margin-bottom: 8px;'>SELECCIONA GRUPO</p>
        <a href="?grupo=VERTEBRADOS" class="{clase_vert}">VERTEBRADOS</a>
        <a href="?grupo=INVERTEBRADOS" class="{clase_inv}">INVERTEBRADOS</a>
        <a href="?grupo=ARTRÓPODOS" class="{clase_art}">ARTRÓPODOS</a>
    </div>
"""
st.markdown(sidebar_html, unsafe_allow_html=True)

# Banda longitudinal inferior con las redes sociales
st.markdown("""
    <div class="footer-band">
        @PISTO.MAG [IG] &nbsp;&nbsp;|&nbsp;&nbsp; @PISTO.MAG [TIKTOK] &nbsp;&nbsp;|&nbsp;&nbsp; @PISTO_MAG [X] &nbsp;&nbsp;|&nbsp;&nbsp; @PISTOMAG [SUBSTACK]
    </div>
""", unsafe_allow_html=True)

DATOS_VERTEBRADOS = [
    {"clase": "CL. MYXINI", "orden": "O. MYXINIFORMES", "especie": "Mixin (Myxine glutinosa)", "cientifico": "Myxine_glutinosa", "truco": "Babas abundantes, carece de mandíbulas y aletas pares; pariente de lampreas pero con tentáculos bucales."},
    {"clase": "CL. HYPEROARTIA", "orden": "O. PETROMYZONTIFORMES", "especie": "Lamprea de mar (Petromyzon marinus)", "cientifico": "Petromyzon_marinus", "truco": "Disco bucal succionador con dientes córneos y 7 agujeros branquiales laterales."},
    {"clase": "CL. HYPEROARTIA", "orden": "O. PETROMYZONTIFORMES", "especie": "Lamprea de arroyo (Lampetra fluviatilis)", "cientifico": "Lampetra_fluviatilis", "truco": "Menor tamaño que la marina, aletas dorsales separadas; típica de arroyos europeos."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. CHIMAERIFORMES", "especie": "Quimera (Chimaera monstrosa)", "cientifico": "Chimaera_monstrosa", "truco": "Esqueleto cartilaginoso con opérculo membranoso, espina venenosa en primera dorsal y placas trituradoras."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. ORECTOLOBIFORMES", "especie": "Tiburón ballena (Rhincodon typus)", "cientifico": "Rhincodon_typus", "truco": "Patrón único de lunares y líneas blancas sobre fondo oscuro; filtrador gigante."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. LAMNIFORMES", "especie": "Pez zorro (Alopias vulpinus)", "cientifico": "Alopias_vulpinus", "truco": "Aleta caudal extremadamente alargada (la mitad de su longitud) usada para aturdir peces."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. LAMNIFORMES", "especie": "Tiburón blanco (Carcharodon carcharias)", "cientifico": "Carcharodon_carcharias", "truco": "Dientes triangulares serrados gigantes, hocico cónico y quilla caudal muy marcada."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. LAMNIFORMES", "especie": "Marrajo (Isurus oxyrinchus)", "cientifico": "Isurus_oxyrinchus", "truco": "Hocico muy puntiagudo, dientes en daga sin sierras y cuerpo hidrodinámico azul metálico."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. LAMNIFORMES", "especie": "Peregrino (Cetorhinus maximus)", "cientifico": "Cetorhinus_maximus", "truco": "Branquias inmensas que casi rodean la cabeza; filtrador pasivo lento y hocico cónico."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. LAMNIFORMES", "especie": "Tiburón toro (Carcharias taurus)", "cientifico": "Carcharias_taurus", "truco": "Dientes largos y curvos hacia fuera visibles con la boca cerrada; manchas pardas difusas."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. CARCHARHINIFORMES", "especie": "Pintarroja (Scyliorhinus canicula)", "cientifico": "Scyliorhinus_canicula", "truco": "Cuerpo alargado con abundantes motas marrones oscuras sobre fondo beige claro."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. CARCHARHINIFORMES", "especie": "Tintorera (Prionace glauca)", "cientifico": "Prionace_glauca", "truco": "Cuerpo muy esbelto, aletas pectorales larguísimas y color azul añil intenso en el dorso."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. CARCHARHINIFORMES", "especie": "Pez martillo (Sphyrna zygaena)", "cientifico": "Sphyrna_zygaena", "truco": "Cabeza ensanchada en martillo (cefalofolio) con ojos en los extremos."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. HEXANCHIFORMES", "especie": "Cañabota gris (Hexanchus griseus)", "cientifico": "Hexanchus_griseus", "truco": "6 hendiduras branquiales laterales y una sola aleta dorsal muy retrasada."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. SQUALIFORMES", "especie": "Mielga (Squalus acanthias)", "cientifico": "Squalus_acanthias", "truco": "Espinas venenosas delante de cada aleta dorsal y ausencia total de aleta anal."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. SQUATINIFORMES", "especie": "Angelote (Squatina squatina)", "cientifico": "Squatina_squatina", "truco": "Cuerpo aplanado tipo raya pero con aletas pectorales separadas y branquias laterales."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. RAJIFORMES", "especie": "Raya noruega (Dipturus batis)", "cientifico": "Dipturus_batis", "truco": "Gran raya de profundidad con hocico muy puntiagudo y dentículos en la cola."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. RHINOBATIFORMES", "especie": "Pez guitarra (Rhinobatos rhinobatos)", "cientifico": "Rhinobatos_rhinobatos", "truco": "Forma intermedia tiburón/raya; hocico triangular prolongado y dos aletas dorsales."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. TORPEDINIFORMES", "especie": "Tremielga (Torpedo torpedo)", "cientifico": "Torpedo_torpedo", "truco": "Órganos eléctricos a los lados de la cabeza; cuerpo discoidal liso y blando."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. MYLIOBATIFORMES", "especie": "Pastinaca (Dasyatis pastinaca)", "cientifico": "Dasyatis_pastinaca", "truco": "Cola larga en forma de látigo con aguijón aserrado venenoso; sin aleta caudal."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. MYLIOBATIFORMES", "especie": "Manta (Mobula mobular)", "cientifico": "Mobula_mobular", "truco": "Aletas cefálicas en cuernos ('diablos de mar') y boca ventral filtradora pelágica."},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. MYLIOBATIFORMES", "especie": "Águila marina (Myliobatis aquila)", "cientifico": "Myliobatis_aquila", "truco": "Cabeza elevada sobre el disco, aletas angulosas y dientes en placa trituradora."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. POLYPTERIFORMES", "especie": "Bichir (Polypterus bichir)", "cientifico": "Polypterus_bichir", "truco": "Aleta dorsal dividida en múltiples pínulas independientes y respiración pulmonar."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. ACIPENSERIFORMES", "especie": "Esturión (Acipenser sturio)", "cientifico": "Acipenser_sturio", "truco": "Hocico con barbillas ventrales, boca protráctil y 5 hileras de escudos óseos."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. ACIPENSERIFORMES", "especie": "Pez espátula (Polyodon spathula)", "cientifico": "Polyodon_spathula", "truco": "Hocico en forma de pala o remo extremadamente alargado y plano."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. LEPISOSTEIFORMES", "especie": "Pez lagarto (Lepisosteus osseus)", "cientifico": "Lepisosteus_osseus", "truco": "Hocico en pinza con dientes y escudos ganoideos romboidales muy duros."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. AMIIFORMES", "especie": "Pez del cieno (Amia calva)", "cientifico": "Amia_calva", "truco": "Placa gular ósea entre mandíbulas y larga aleta dorsal ondulante."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. OSTEOGLOSSIFORMES", "especie": "Arapaima (Arapaima gigas)", "cientifico": "Arapaima_gigas", "truco": "Escamas grandes con bordes rosados, lengua ósea dentada y gran tamaño fluvial."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. ANGUILLIFORMES", "especie": "Anguila (Anguilla anguilla)", "cientifico": "Anguilla_anguilla", "truco": "Aleta dorsal continua unida a anal y caudal; mandíbula inferior prominente."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. ANGUILLIFORMES", "especie": "Congrio (Conger conger)", "cientifico": "Conger_conger", "truco": "Mandíbula superior sobresaliente; aleta dorsal comienza a la altura pectoral."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. ANGUILLIFORMES", "especie": "Morena (Muraena helena)", "cientifico": "Muraena_helena", "truco": "Sin aletas pectorales, piel lisa con patrones marmóreos amarillos y pardos."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CLUPEIFORMES", "especie": "Boquerón (Engraulis encrasicolus)", "cientifico": "Engraulis_encrasicolus", "truco": "Hocico muy prominente que sobresale sobre la boca y banda lateral plateada."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CLUPEIFORMES", "especie": "Sardina (Sardina pilchardus)", "cientifico": "Sardina_pilchardus", "truco": "Opérculo con estrías radiadas y vientre con quilla serrada de escudos."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CYPRINIFORMES", "especie": "Barbo comiza (Luciobarbus comizo)", "cientifico": "Luciobarbus_comizo", "truco": "Cabeza muy alargada y cónica con cuatro barbillas táctiles y labios carnosos."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CYPRINIFORMES", "especie": "Carpa (Cyprinus carpio)", "cientifico": "Cyprinus_carpio", "truco": "Dos pares de barbillas y gran espina dentada en la aleta dorsal."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CYPRINIFORMES", "especie": "Carpín dorado (Carassius auratus)", "cientifico": "Carassius_auratus", "truco": "Sin barbillas bucales y borde posterior de la aleta dorsal cóncavo."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SILURIFORMES", "especie": "Siluro (Silurus glanis)", "cientifico": "Silurus_glanis", "truco": "Cabeza grande aplanada con 3 pares de barbillas largas y aleta anal muy larga."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CHARACIFORMES", "especie": "Piraña negra (Serrasalmus rhombeus)", "cientifico": "Serrasalmus_rhombeus", "truco": "Perfil cefálico cóncavo, mandíbula prognata con dientes triangulares cortantes."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CHARACIFORMES", "especie": "Tetra neón (Paracheirodon innesi)", "cientifico": "Paracheirodon_innesi", "truco": "Franja horizontal azul eléctrico brillante combinada con mancha roja posterior."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. GYMNOTIFORMES", "especie": "Anguila eléctrica (Electrophorus electricus)", "cientifico": "Electrophorus_electricus", "truco": "Cuerpo cilíndrico largo sin aletas dorsales/ventrales; genera alto voltaje."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SALMONIFORMES", "especie": "Trucha (Salmo trutta)", "cientifico": "Salmo_trutta", "truco": "Puntos negros y rojos rodeados de un halo claro y presencia de aleta adiposa."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SALMONIFORMES", "especie": "Salmón (Salmo salar)", "cientifico": "Salmo_salar", "truco": "Pedúnculo caudal estrecho y escasos puntos en forma de X o cruz."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SALMONIFORMES", "especie": "Salmón rojo (Oncorhynchus nerka)", "cientifico": "Oncorhynchus_nerka", "truco": "Cuerpo rojo vivo con cabeza verde oliva durante la época de reproducción."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. ESOCIFORMES", "especie": "Lucio (Esox lucius)", "cientifico": "Esox_lucius", "truco": "Cabeza en pico de pato con dientes hacia atrás y dorsal muy retrasada."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. LOPHIIFORMES", "especie": "Rape (Lophius piscatorius)", "cientifico": "Lophius_piscatorius", "truco": "Cabeza enorme aplanada con primer radio dorsal en antena señuelo (ilicio)."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. GADIFORMES", "especie": "Merluza (Merluccius merluccius)", "cientifico": "Merluccius_merluccius", "truco": "Boca negra por dentro, mandíbula inferior prominente y dos aletas dorsales."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. GADIFORMES", "especie": "Bacalao (Gadus morhua)", "cientifico": "Gadus_morhua", "truco": "3 aletas dorsales, 2 anales y barbilla marcada en la barbilla."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CYPRINODONTIFORMES", "especie": "Gambusia (Gambusia affinis)", "cientifico": "Gambusia_affinis", "truco": "Pez pequeño de aguas someras; hembras con mancha anal oscura."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CYPRINODONTIFORMES", "especie": "Guppy (Poecilia reticulata)", "cientifico": "Poecilia_reticulata", "truco": "Dimorfismo sexual extremo: machos muy coloridos y veliformes; hembras grises."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. GASTEROSTEIFORMES", "especie": "Espinoso (Gasterosteus aculeatus)", "cientifico": "Gasterosteus_aculeatus", "truco": "3 espinas dorsales aisladas independientes y placas óseas laterales."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SYNGNATHIFORMES", "especie": "Caballito de mar (Hippocampus zosterae)", "cientifico": "Hippocampus_zosterae", "truco": "Cabeza en ángulo recto, cuerpo anillado óseo y cola prensil sin caudal."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SCORPAENIFORMES", "especie": "Cabracho (Scorpaena scrofa)", "cientifico": "Scorpaena_scrofa", "truco": "Cabeza con espinas y tentáculos cutáneos; coloración roja y espinas venenosas."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. BLENNIIFORMES", "especie": "Fraile (Salaria fluviatilis)", "cientifico": "Salaria_fluviatilis", "truco": "Blenénido de agua dulce con cresta carnosa prominente en los machos."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CARANGIFORMES", "especie": "Jurel (Trachurus trachurus)", "cientifico": "Trachurus_trachurus", "truco": "Línea lateral curvada con escudos óseos angulares (quillas) muy desarrollados."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. PERCIFORMES", "especie": "Salmonete de fango (Mullus barbatus)", "cientifico": "Mullus_barbatus", "truco": "Dos largas barbillas táctiles bajo la barbilla y perfil de hocico casi vertical."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. PERCIFORMES", "especie": "Mero (Epinephelus marginatus)", "cientifico": "Epinephelus_marginatus", "truco": "Opérculo con tres espinas aplanadas y aleta caudal redondeada con borde blanco."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SPARIFORMES", "especie": "Besugo (Pagellus bogaraveo)", "cientifico": "Pagellus_bogaraveo", "truco": "Mancha negra característica y bien visible detrás del opérculo."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SPARIFORMES", "especie": "Dorada (Sparus aurata)", "cientifico": "Sparus_aurata", "truco": "Franja dorada transversal uniendo ambos ojos y mancha negra en agallas."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. MORONIFORMES", "especie": "Lubina (Dicentrarchus labrax)", "cientifico": "Dicentrarchus_labrax", "truco": "Cuerpo plateado, dos dorsales separadas y mancha difusa oscura en opérculo."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SCOMBRIFORMES", "especie": "Caballa (Scomber scombrus)", "cientifico": "Scomber_scombrus", "truco": "Bandas oscuras onduladas en el dorso y pínulas tras la dorsal y anal."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SCOMBRIFORMES", "especie": "Atún (Thunnus thynnus)", "cientifico": "Thunnus_thynnus", "truco": "Pínulas dorsales y anales amarillas con punta blanca; pectorales cortas."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SCOMBRIFORMES", "especie": "Bonito (Thunnus alalunga)", "cientifico": "Thunnus_alalunga", "truco": "Aletas pectorales extraordinariamente largas que superan la segunda dorsal."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. PLEURONECTIFORMES", "especie": "Rodaballo (Scophthalmus maximus)", "cientifico": "Scophthalmus_maximus", "truco": "Cuerpo romboidal ancho sin escamas pero con tubérculos óseos en lado ocular."},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. PLEURONECTIFORMES", "especie": "Lenguado (Solea solea)", "cientifico": "Solea_solea", "truco": "Hocico redondeado que sobresale sobre la boca y ojo superior adelantado."},
    {"clase": "CL. SARCOPTERYGII", "orden": "O. COELACANTHIFORMES", "especie": "Celacanto (Latimeria chalumnae)", "cientifico": "Latimeria_chalumnae", "truco": "Aletas pares lobuladas con pedúnculos carnosos y cola trilobulada central."},
    {"clase": "CL. SARCOPTERYGII", "orden": "O. CERATODONTIFORMES", "especie": "Pez de barro americano (Lepidosiren paradoxa)", "cientifico": "Lepidosiren_paradoxa", "truco": "Cuerpo anguiliforme muy alargado con aletas pectorales/pélvicas filamentosas."},
    {"clase": "CL. AMPHIBIA", "orden": "O. GYMNOPHIONA", "especie": "Cecilia de Ceilán (Ichthyophis glutinosus)", "cientifico": "Ichthyophis_glutinosus", "truco": "Anfibio ápodo vermiforme con anillos cutáneos y tentáculos sensoriales."},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Salamandra gigante de China (Andrias davidianus)", "cientifico": "Andrias_davidianus", "truco": "Anfibio más grande; cabeza aplanada ancha y piel rugosa con pliegues laterales."},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Salamandra rabilarga (Chioglossa lusitanica)", "cientifico": "Chioglossa_lusitanica", "truco": "Cola extremadamente larga (el doble que el cuerpo) y dos líneas dorsales doradas."},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Gallipato (Pleurodeles waltl)", "cientifico": "Pleurodeles_waltl", "truco": "Costillas afiladas que pueden atravesar la piel como defensa y cola aplanada."},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Salamandra común (Salamandra salamandra)", "cientifico": "Salamandra_salamandra", "truco": "Fondo negro intenso con manchas amarillas/naranjas vivas y glándulas parótideas."},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Tritón palmeado (Lissotriton helveticus)", "cientifico": "Lissotriton_helveticus", "truco": "Machos con patas posteriores palmeadas y filamento caudal terminal."},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Tritón ibérico (Lissotriton boscai)", "cientifico": "Lissotriton_boscai", "truco": "Garganta completamente impune (blanquecina sin manchas) y listas oculares."},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Tritón de los Pirineos (Calotriton asper)", "cientifico": "Calotriton_asper", "truco": "Adaptado a torrentes, piel muy rugosa con tubérculos córneos y sin cresta."},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Proteo (Proteus anguinus)", "cientifico": "Proteus_anguinus", "truco": "Cavernícola ciego, piel rosada despigmentada, branquias externas rojas."},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Ajolote (Ambystoma mexicanum)", "cientifico": "Ambystoma_mexicanum", "truco": "Neotenia permanente, grandes branquias externas plumosas rojas."},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Sapo común ibérico (Bufo spinosus)", "cientifico": "Bufo_spinosus", "truco": "Gran tamaño, verrugas cónicas y glándulas parótideas alargadas oblicuas."},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Sapo corredor (Epidalea calamita)", "cientifico": "Epidalea_calamita", "truco": "Línea vertebral amarilla fina y desplazamiento caminando por patas cortas."},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Sapo partero ibérico (Alytes cisternasii)", "cientifico": "Alytes_cisternasii", "truco": "Pupila vertical y machos portando los huevos enrollados en las patas."},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Rana verde común (Pelophylax perezi)", "cientifico": "Pelophylax_perezi", "truco": "Pliegues dorsolaterales marcados y vocalizadores externos blancos."},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Rana patilarga (Rana iberica)", "cientifico": "Rana_iberica", "truco": "Mancha oscura temporal en máscara piramidal tras el ojo y patas muy largas."},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Ranita de San Antonio ibérica (Hyla molleri)", "cientifico": "Hyla_molleri", "truco": "Discos adhesivos en dedos para trepar y banda lateral oscura curvada."},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Sapito de Darwin (Rhinoderma darwinii)", "cientifico": "Rhinoderma_darwinii", "truco": "Hocico puntiagudo carnoso; machos incuban renacuajos en el saco vocal."},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Sapo de Surinam (Pipa pipa)", "cientifico": "Pipa_pipa", "truco": "Cuerpo aplanado como hoja seca; huevos incubados en celdas en la espalda."},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Rana punta de flecha (Dendrobates tinctorius)", "cientifico": "Dendrobates_tinctorius", "truco": "Colores aposemáticos llamativos (azul/amarillo/negro) y piel muy tóxica."},
    {"clase": "CL. REPTILIA", "orden": "O. CHELONIA", "especie": "Tortuga de caparazón blando del Ganges (Nilssonia gangetica)", "cientifico": "Nilssonia_gangetica", "truco": "Caparazón flexible sin placas córneas y hocico tubular con probóscide."},
    {"clase": "CL. REPTILIA", "orden": "O. CHELONIA", "especie": "Tortuga boba (Caretta caretta)", "cientifico": "Caretta_caretta", "truco": "Cabeza muy grande y robusta, 5 pares de escudos costales en el caparazón."},
    {"clase": "CL. REPTILIA", "orden": "O. CHELONIA", "especie": "Tortuga laúd (Dermochelys coriacea)", "cientifico": "Dermochelys_coriacea", "truco": "Sin placas óseas sino piel de cuero con 7 quillas longitudinales."},
    {"clase": "CL. REPTILIA", "orden": "O. CHELONIA", "especie": "Tortuga caimán (Macrochelys temminckii)", "cientifico": "Macrochelys_temminckii", "truco": "Apéndice vermiforme en la boca para pescar y caparazón con 3 quillas serradas."},
    {"clase": "CL. REPTILIA", "orden": "O. CHELONIA", "especie": "Tortuga mora (Testudo graeca)", "cientifico": "Testudo_graeca", "truco": "Caparazón abombado con manchas oscuras y ausencia de uña en la cola."},
    {"clase": "CL. REPTILIA", "orden": "O. CHELONIA", "especie": "Galápago leproso (Mauremys leprosa)", "cientifico": "Mauremys_leprosa", "truco": "Cuello con líneas amarillas/naranjas longitudinales y plastrón plano."},
    {"clase": "CL. REPTILIA", "orden": "O. CHELONIA", "especie": "Tortuga gigante de las Galápagos (Chelonoidis niger)", "cientifico": "Chelonoidis_niger", "truco": "Enorme tamaño, cuello largo y caparazón abombado o en silla de montar."},
    {"clase": "CL. REPTILIA", "orden": "O. SPHENODONTIA", "especie": "Tuátara (Sphenodon punctatus)", "cientifico": "Sphenodon_punctatus", "truco": "Fósil con cresta de espinas dorsales blandas y tercer ojo parietal rudimentario."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Iguana común (Iguana iguana)", "cientifico": "Iguana_iguana", "truco": "Gran papada gular, cresta dorsal de espinas y escama subtimpánica redonda."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Iguana marina (Amblyrhynchus cristatus)", "cientifico": "Amblyrhynchus_cristatus", "truco": "Hocico corto chato para raspar algas y sal exudada en la cabeza."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Agama común (Agama agama)", "cientifico": "Agama_agama", "truco": "Machos con cabeza y cola naranja/rojo vivo brillante y cuerpo azul oscuro."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Camaleón común (Chamaeleo chamaeleon)", "cientifico": "Chamaeleo_chamaeleon", "truco": "Ojos con movimiento independiente, lengua protráctil y pies didáctilos en pinza."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Salamanquesa común (Tarentola mauritanica)", "cientifico": "Tarentola_mauritanica", "truco": "Gran cabeza triangular, ojos sin párpados con pupila vertical y tubérculos."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Eslizón ibérico (Chalcides bedriagai)", "cientifico": "Chalcides_bedriagai", "truco": "Cuerpo cilíndrico muy alargado y brillante con extremidades minúsculas."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Lagarto ocelado ibérico (Timon lepidus)", "cientifico": "Timon_lepidus", "truco": "Mayor lacértido europeo; verde con grandes ocelos azules en los flancos."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Lagartija roquera (Podarcis muralis)", "cientifico": "Podarcis_muralis", "truco": "Dorso reticulado con banda vertebral oscura y ventrales con borde negro."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Lagartija colilarga (Psammodromus algirus)", "cientifico": "Psammodromus_algirus", "truco": "Cola larguísima y escamas dorsales quilladas solapadas como tejas."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Lución (Anguis fragilis)", "cientifico": "Anguis_fragilis", "truco": "Lagarto sin patas con párpados móviles (falsa serpiente ápoda)."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Monstruo de Gila (Heloderma suspectum)", "cientifico": "Heloderma_suspectum", "truco": "Lagarto venenoso con piel de cuentas de abalorio y patrón rosado/negro."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Varano de Komodo (Varanus komodoensis)", "cientifico": "Varanus_komodoensis", "truco": "Lagarto más grande del mundo, lengua bífida amarilla y glándulas de veneno."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Varano del Nilo (Varanus niloticus)", "cientifico": "Varanus_niloticus", "truco": "Gran lagarto acuático con anillos amarillos en cuello y cola con quilla."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Culebrilla ciega común (Blanus cinereus)", "cientifico": "Blanus_cinereus", "truco": "Amfisbaeno subterráneo anillado sin patas y con ojos ocultos."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Anaconda (Eunectes murinus)", "cientifico": "Eunectes_murinus", "truco": "Serpiente más pesada, ojos/fosas nasales dorsales y manchas ovales negras."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Culebra bastarda (Malpolon monspessulanus)", "cientifico": "Malpolon_monspessulanus", "truco": "Grandes cejas salientes marcadas y dientes opistoglifos venenosos posteriores."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Culebra de collar mediterránea (Natrix astreptophora)", "cientifico": "Natrix_astreptophora", "truco": "Collar nucal negro muy marcado, escamas quilladas y hábitos acuáticos."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Culebra de escalera (Zamenis scalaris)", "cientifico": "Zamenis_scalaris", "truco": "Jóvenes con patrón en 'escalera' que desaparece en adultos."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Cobra (Naja naja)", "cientifico": "Naja_naja", "truco": "Capacidad de expandir capuchón con dibujo dorsal en forma de gafas."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Serpiente de mar (Laticauda colubrina)", "cientifico": "Laticauda_colubrina", "truco": "Cola en remo para nadar y franjas negras anulares en cuerpo gris-azulado."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Víbora hocicuda (Vipera latastei)", "cientifico": "Vipera_latastei", "truco": "Hocico con pequeño apéndice levantado, pupila vertical y zigzag dorsal."},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Serpiente de cascabel (Crotalus horridus)", "cientifico": "Crotalus_horridus", "truco": "Sonajero córneo en el extremo de la cola y fosas termorreceptoras."},
    {"clase": "CL. REPTILIA", "orden": "O. CROCODYLIA", "especie": "Cocodrilo del Nilo (Crocodylus niloticus)", "cientifico": "Crocodylus_niloticus", "truco": "Cuarto diente inferior visible con la boca cerrada y hocico ancho osteodermo."},
    {"clase": "CL. REPTILIA", "orden": "O. CROCODYLIA", "especie": "Aligátor americano (Alligator mississippiensis)", "cientifico": "Alligator_mississippiensis", "truco": "Hocico ancho redondeado en U; al cerrar la boca los dientes inferiores quedan ocultos."},
    {"clase": "CL. REPTILIA", "orden": "O. CROCODYLIA", "especie": "Gavial (Gavialis gangeticus)", "cientifico": "Gavialis_gangeticus", "truco": "Hocico extremadamente estrecho, largo y cilíndrico para capturar peces."},
    {"clase": "CL. AVES", "orden": "O. STRUTHIONIFORMES", "especie": "Avestruz (Struthio camelus)", "cientifico": "Struthio_camelus", "truco": "Ave más grande; 2 dedos en cada pata (adaptación única para correr) y cuello desnudo."},
    {"clase": "CL. AVES", "orden": "O. RHEIFORMES", "especie": "Nandú (Rhea americana)", "cientifico": "Rhea_americana", "truco": "Ave corredora sudamericana con 3 dedos en cada pata y sin plumas caudales."},
    {"clase": "CL. AVES", "orden": "O. TINAMIFORMES", "especie": "Tinamú común (Nothura maculosa)", "cientifico": "Nothura_maculosa", "truco": "Aspecto de perdiz pero vuela torpemente; huevos brillantes tipo porcelana."},
    {"clase": "CL. AVES", "orden": "O. CASUARIIFORMES", "especie": "Casuario (Casuarius casuarius)", "cientifico": "Casuarius_casuarius", "truco": "Casco óseo en la cabeza, barbillones azules/rojos y uña interior en daga."},
    {"clase": "CL. AVES", "orden": "O. APTERYGIFORMES", "especie": "Kiwi sureño (Apteryx australis)", "cientifico": "Apteryx_australis", "truco": "Fosas nasales en la punta del pico largo, plumas filamentosas y alas vestigiales."},
    {"clase": "CL. AVES", "orden": "O. GALLIFORMES", "especie": "Urogallo común (Tetrao urogallus)", "cientifico": "Tetrao_urogallus", "truco": "Gran gallináceo forestal con cejas rojas, barba negra y abanico caudal."},
    {"clase": "CL. AVES", "orden": "O. GALLIFORMES", "especie": "Perdiz roja (Alectoris rufa)", "cientifico": "Alectoris_rufa", "truco": "Garganta blanca con collar negro, listas superciliares y patas/pico rojo coral."},
    {"clase": "CL. AVES", "orden": "O. GALLIFORMES", "especie": "Perdiz pardilla (Perdix perdix)", "cientifico": "Perdix_perdix", "truco": "Mancha pectoral en herradura castaña roja y flancos barrados de gris."},
    {"clase": "CL. AVES", "orden": "O. ANSERIFORMES", "especie": "Ánsar común (Anser anser)", "cientifico": "Anser_anser", "truco": "Pico anaranjado robusto y plumaje gris pardusco uniforme."},
    {"clase": "CL. AVES", "orden": "O. ANSERIFORMES", "especie": "Ánade azulón (Anas platyrhynchos)", "cientifico": "Anas_platyrhynchos", "truco": "Macho con cabeza verde iridiscente brillante, collar blanco y espejo azul."},
    {"clase": "CL. AVES", "orden": "O. ANSERIFORMES", "especie": "Porrón europeo (Aythya ferina)", "cientifico": "Aythya_ferina", "truco": "Cabeza redondeada castaño rojiza cobriza y ojos rojos intensos."},
    {"clase": "CL. AVES", "orden": "O. CAPRIMULGIFORMES", "especie": "Chotacabras europeo (Caprimulgus europaeus)", "cientifico": "Caprimulgus_europaeus", "truco": "Plumaje críptico a corteza de árbol, boca enorme con bigoteras nocturnas."},
    {"clase": "CL. AVES", "orden": "O. CAPRIMULGIFORMES", "especie": "Vencejo común (Apus apus)", "cientifico": "Apus_apus", "truco": "Alas larguísimas en hoz, patas muy cortas y plumaje pardo oscuro."},
    {"clase": "CL. AVES", "orden": "O. CAPRIMULGIFORMES", "especie": "Colibrí zunzuncito (Mellisuga helenae)", "cientifico": "Mellisuga_helenae", "truco": "Ave más pequeña del mundo (Cuba), iridiscencia rosada y tamaño de abejorro."},
    {"clase": "CL. AVES", "orden": "O. CAPRIMULGIFORMES", "especie": "Guácharo (Steatornis caripensis)", "cientifico": "Steatornis_caripensis", "truco": "Ave nocturna de cueva que usa ecolocalización mediante chasquidos audibles."},
    {"clase": "CL. AVES", "orden": "O. COLUMBIFORMES", "especie": "Paloma torcaz (Columba palumbus)", "cientifico": "Columba_palumbus", "truco": "Manchas blancas muy llamativas a ambos lados del cuello."},
    {"clase": "CL. AVES", "orden": "O. COLUMBIFORMES", "especie": "Tórtola europea (Streptopelia turtur)", "cientifico": "Streptopelia_turtur", "truco": "Collar rayado negro y blanco en el cuello y dorso escamado canela."},
    {"clase": "CL. AVES", "orden": "O. CUCULIFORMES", "especie": "Cuco (Cuculus canorus)", "cientifico": "Cuculus_canorus", "truco": "Parásito de puesta, aspecto de pequeño halcón gris con listas ventrales."},
    {"clase": "CL. AVES", "orden": "O. OTIDIFORMES", "especie": "Avutarda euroasiática (Otis tarda)", "cientifico": "Otis_tarda", "truco": "Machos gigantes con 'bigotes' de plumas blancas basales y gran dimorfismo."},
    {"clase": "CL. AVES", "orden": "O. GRUIFORMES", "especie": "Grulla común (Grus grus)", "cientifico": "Grus_grus", "truco": "Ave zancuda gris con penacho rojo en la coronilla y gritos trompeteros."},
    {"clase": "CL. AVES", "orden": "O. GRUIFORMES", "especie": "Focha común (Fulica atra)", "cientifico": "Fulica_atra", "truco": "Plumaje negro tizón uniforme con escudo frontal y pico blancos puros."},
    {"clase": "CL. AVES", "orden": "O. PHOENICOPTERIFORMES", "especie": "Flamenco común (Phoenicopterus roseus)", "cientifico": "Phoenicopterus_roseus", "truco": "Pico curvado filtrador, patas rosadas larguísimas y color por carotenoides."},
    {"clase": "CL. AVES", "orden": "O. CHARADRIIFORMES", "especie": "Avefría europea (Vanellus vanellus)", "cientifico": "Vanellus_vanellus", "truco": "Larga cresta plumosa trasera y alas anchas con verde metálico."},
    {"clase": "CL. AVES", "orden": "O. CHARADRIIFORMES", "especie": "Avoceta común (Recurvirostra avosetta)", "cientifico": "Recurvirostra_avosetta", "truco": "Pico fino elegantemente curvado hacia arriba y plumaje blanco y negro."},
    {"clase": "CL. AVES", "orden": "O. CHARADRIIFORMES", "especie": "Gaviota reidora (Chroicocephalus ridibundus)", "cientifico": "Chroicocephalus_ridibundus", "truco": "Capucha marrón chocolate oscura en época nupcial y punta alar blanca."},
    {"clase": "CL. AVES", "orden": "O. CHARADRIIFORMES", "especie": "Gaviota sombría (Larus fuscus)", "cientifico": "Larus_fuscus", "truco": "Manto y alas gris oscuro antracita/negro, patas amarillas brillantes."},
    {"clase": "CL. AVES", "orden": "O. CHARADRIIFORMES", "especie": "Frailecillo atlántico (Fratercula arctica)", "cientifico": "Fratercula_arctica", "truco": "Pico alto comprimido colorido en franjas naranjas y antifaz triangular."},
    {"clase": "CL. AVES", "orden": "O. PODICIPEDIFORMES", "especie": "Somormujo lavanco (Podiceps cristatus)", "cientifico": "Podiceps_cristatus", "truco": "Doble penacho auricular negro y collar rufo rojizo desplegable en celo."},
    {"clase": "CL. AVES", "orden": "O. SPHENISCIFORMES", "especie": "Pingüino emperador (Aptenodytes forsteri)", "cientifico": "Aptenodytes_forsteri", "truco": "Manchas amarillas/naranjas en la zona auricular y vientre blanco puro."},
    {"clase": "CL. AVES", "orden": "O. PELECANIFORMES", "especie": "Pelícano común (Pelecanus onocrotalus)", "cientifico": "Pelecanus_onocrotalus", "truco": "Bolsa gular inferior enorme amarilla/rosada y plumaje blanco rosáceo."},
    {"clase": "CL. AVES", "orden": "O. PELECANIFORMES", "especie": "Garza real (Ardea cinerea)", "cientifico": "Ardea_cinerea", "truco": "Pico amarillo en daga, penacho negro y cuello en S en vuelo."},
    {"clase": "CL. AVES", "orden": "O. PELECANIFORMES", "especie": "Garceta común (Egretta garzetta)", "cientifico": "Egretta_garzetta", "truco": "Plumaje enteramente blanco puro, pico y patas negras con dedos amarillos."},
    {"clase": "CL. AVES", "orden": "O. PELECANIFORMES", "especie": "Espátula común (Platalea leucorodia)", "cientifico": "Platalea_leucorodia", "truco": "Pico negro aplanado y ancho en la punta en forma de espátula."},
    {"clase": "CL. AVES", "orden": "O. SULIFORMES", "especie": "Cormorán grande (Phalacrocorax carbo)", "cientifico": "Phalacrocorax_carbo", "truco": "Plumaje negro verdoso con mancha gular blanca; seca las alas abiertas."},
    {"clase": "CL. AVES", "orden": "O. CICONIIFORMES", "especie": "Cigüeña blanca (Ciconia ciconia)", "cientifico": "Ciconia_ciconia", "truco": "Plumaje blanco y negro en alas, pico y patas largas rojo vivo."},
    {"clase": "CL. AVES", "orden": "O. CICONIIFORMES", "especie": "Cigüeña negra (Ciconia nigra)", "cientifico": "Ciconia_nigra", "truco": "Plumaje totalmente negro con brillos verdes/púrpuras y vientre blanco."},
    {"clase": "CL. AVES", "orden": "O. OPISTHOCOMIFORMES", "especie": "Hoacín (Opisthocomus hoazin)", "cientifico": "Opisthocomus_hoazin", "truco": "Gran cresta desordenada; crías con garras funcionales en las alas."},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Buitre leonado (Gyps fulvus)", "cientifico": "Gyps_fulvus", "truco": "Cabeza y cuello con plumón blanco, collar de plumas lanceoladas y alas anchas."},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Buitre negro (Aegypius monachus)", "cientifico": "Aegypius_monachus", "truco": "Mayor buitre europeo, plumaje negruzco, cabeza con plumón gris."},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Quebrantahuesos (Gypaetus barbatus)", "cientifico": "Gypaetus_barbatus", "truco": "Barba negra bajo el pico, ojos con anillo rojo y rompe huesos en altura."},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Alimoche común (Neophron percnopterus)", "cientifico": "Neophron_percnopterus", "truco": "Cara y pico amarillos desprovistos de plumas, plumaje blanco con cuñas negras."},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Águila imperial ibérica (Aquila adalberti)", "cientifico": "Aquila_adalberti", "truco": "Hombros blancos muy llamativos en adultos, nuca dorada y alas rectilíneas."},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Águila real (Aquila chrysaetos)", "cientifico": "Aquila_chrysaetos", "truco": "Nuca dorada brillante contrastada y patas emplumadas hasta los dedos."},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Busardo ratonero (Buteo buteo)", "cientifico": "Buteo_buteo", "truco": "Silueta compacta de cola corta redondeada y banda pectoral clara."},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Milano real (Milvus milvus)", "cientifico": "Milvus_milvus", "truco": "Cola ahorquillada muy profunda rojiza y manchas blancas bajo las alas."},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Milano negro (Milvus migrans)", "cientifico": "Milvus_migrans", "truco": "Cola ahorquillada menos marcada y plumaje marrón oscuro uniforme."},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Gavilán común (Accipiter nisus)", "cientifico": "Accipiter_nisus", "truco": "Alas cortas redondeadas y larga cola para maniobrar en bosques."},
    {"clase": "CL. AVES", "orden": "O. STRIGIFORMES", "especie": "Lechuza común (Tyto alba)", "cientifico": "Tyto_alba", "truco": "Disco facial en forma de corazón blanco, ojos negros y dorso dorado."},
    {"clase": "CL. AVES", "orden": "O. STRIGIFORMES", "especie": "Búho real (Bubo bubo)", "cientifico": "Bubo_bubo", "truco": "Mayor búho, grandes penachos orejudos erectos y ojos naranja brillante."},
    {"clase": "CL. AVES", "orden": "O. STRIGIFORMES", "especie": "Mochuelo europeo (Athene noctua)", "cientifico": "Athene_noctua", "truco": "Pequeño tamaño, cejas blancas aplanadas y hábitos diurnos/crepusculares."},
    {"clase": "CL. AVES", "orden": "O. STRIGIFORMES", "especie": "Cárabo común (Strix aluco)", "cientifico": "Strix_aluco", "truco": "Sin penachos, ojos negros grandes y disco facial con listas concéntricas."},
    {"clase": "CL. AVES", "orden": "O. BUCEROTIFORMES", "especie": "Abubilla común (Upupa epops)", "cientifico": "Upupa_epops", "truco": "Larga cresta replegable de plumas canelas con puntas negras y pico largo."},
    {"clase": "CL. AVES", "orden": "O. CORACIIFORMES", "especie": "Abejaruco europeo (Merops apiaster)", "cientifico": "Merops_apiaster", "truco": "Colores brillantes tropicales y pico largo ligeramente curvado."},
    {"clase": "CL. AVES", "orden": "O. CORACIIFORMES", "especie": "Martín pescador común (Alcedo atthis)", "cientifico": "Alcedo_atthis", "truco": "Dorso azul cobrizo eléctrico, vientre naranja y pico de estilete negro."},
    {"clase": "CL. AVES", "orden": "O. PICIFORMES", "especie": "Pico picapinos (Dendrocopos major)", "cientifico": "Dendrocopos_major", "truco": "Blanco y negro con mancha roja en nuca y obispillo rojo vivo."},
    {"clase": "CL. AVES", "orden": "O. PICIFORMES", "especie": "Pito real ibérico (Picus sharpei)", "cientifico": "Picus_sharpei", "truco": "Dorso verde oliva, píleo rojo brillante y bigotera negra con centro rojo."},
    {"clase": "CL. AVES", "orden": "O. FALCONIFORMES", "especie": "Cernícalo (Falco tinnunculus)", "cientifico": "Falco_tinnunculus", "truco": "Hábito de cernirse estático en el aire y dorso rojizo con lunares negros."},
    {"clase": "CL. AVES", "orden": "O. FALCONIFORMES", "especie": "Halcón peregrino (Falco peregrinus)", "cientifico": "Falco_peregrinus", "truco": "Bigotera negra ancha ('casco') y ave más rápida en vuelo en picado."},
    {"clase": "CL. AVES", "orden": "O. PSITTACIFORMES", "especie": "Cotorra argentina (Myiopsitta monachus)", "cientifico": "Myiopsitta_monachus", "truco": "Verde brillante con frente/pecho gris pálido; nidos comunales gigantes."},
    {"clase": "CL. AVES", "orden": "O. PSITTACIFORMES", "especie": "Cotorra de Kramer (Psittacula krameri)", "cientifico": "Psittacula_krameri", "truco": "Verde vivo, cola muy larga fina y collar rosado/negro en machos."},
    {"clase": "CL. AVES", "orden": "O. PSITTACIFORMES", "especie": "Loro gris (Psittacus erithacus)", "cientifico": "Psittacus_erithacus", "truco": "Gris ceniza uniforme y cola corta de color rojo escarlata vivo."},
    {"clase": "CL. AVES", "orden": "O. PSITTACIFORMES", "especie": "Guacamayo rojo (Ara macao)", "cientifico": "Ara_macao", "truco": "Colores primarios vivos (rojo, amarillo, azul) y rostro blanco desnudo."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Alondra común (Alauda arvensis)", "cientifico": "Alauda_arvensis", "truco": "Pequeña cresta en la nuca y canto continuo ascendiendo en vertical."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Lavandera blanca (Motacilla alba)", "cientifico": "Motacilla_alba", "truco": "Blanco, negro y gris con larga cola que mueve constantemente arriba y abajo."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Alcaudón real (Lanius meridionalis)", "cientifico": "Lanius_meridionalis", "truco": "Antifaz negro sobre los ojos y pico de rapaz en miniatura ganchudo."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Curruca capirotada (Sylvia atricapilla)", "cientifico": "Sylvia_atricapilla", "truco": "Capirote negro azabache en machos (marrón en hembras) sobre dorso gris."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Mosquitero común (Phylloscopus collybita)", "cientifico": "Phylloscopus_collybita", "truco": "Pequeño verde oliváceo con patas oscuras y ceja pálida poco marcada."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Tarabilla europea (Saxicola rubicola)", "cientifico": "Saxicola_rubicola", "truco": "Macho con cabeza negra, collar blanco y pecho naranja rojizo intenso."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Collalba rubia (Oenanthe hispanica)", "cientifico": "Oenanthe_hispanica", "truco": "Obispillo blanco brillante y antifaz negro contrastado en machos."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Petirrojo europeo (Erithacus rubecula)", "cientifico": "Erithacus_rubecula", "truco": "Babero y frente naranja anaranjado intenso rodeado de gris azulado."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Mirlo común (Turdus merula)", "cientifico": "Turdus_merula", "truco": "Machos negro azabache con pico amarillo anaranjado; hembras marrones."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Carbonero común (Parus major)", "cientifico": "Parus_major", "truco": "Franja negra central ('corbata') sobre fondo amarillo vivo y mejillas blancas."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Chochín paleártico (Troglodytes troglodytes)", "cientifico": "Troglodytes_troglodytes", "truco": "Tamaño diminuto, cola corta levantada verticalmente y canto potente."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Pinzón vulgar (Fringilla coelebs)", "cientifico": "Fringilla_coelebs", "truco": "Doble barra alar blanca brillante y tonos rosados en el pecho."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Jilguero europeo (Carduelis carduelis)", "cientifico": "Carduelis_carduelis", "truco": "Máscara facial roja brillante, lista alar amarilla y pico cónico para cardos."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Estornino negro (Sturnus unicolor)", "cientifico": "Sturnus_unicolor", "truco": "Negro con brillos metálicos púrpuras y pico amarillo brillante en cría."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Gorrión común (Passer domesticus)", "cientifico": "Passer_domesticus", "truco": "Babero negro en machos, píleo gris y dorso marrón estriado."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Urraca común (Pica pica)", "cientifico": "Pica_pica", "truco": "Larga cola metálica azul/verde, hombros y vientre blanco puro."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Cuervo grande (Corvus corax)", "cientifico": "Corvus_corax", "truco": "Mayor córvido, negro brillante con plumas de garganta lanceoladas y cola en cuña."},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Rabilargo ibérico (Cyanopica cooki)", "cientifico": "Cyanopica_cooki", "truco": "Píleo negro, cuerpo gris beis y larga cola azul con punta blanca."},
    {"clase": "CL. MAMMALIA", "orden": "O. MONOTREMATA", "especie": "Ornitorrinco (Ornithorhynchus anatinus)", "cientifico": "Ornithorhynchus_anatinus", "truco": "Hocico en pico de pato flexible, espolones venenosos y ponedor de huevos."},
    {"clase": "CL. MAMMALIA", "orden": "O. MONOTREMATA", "especie": "Equidna de hocico corto (Tachyglossus aculeatus)", "cientifico": "Tachyglossus_aculeatus", "truco": "Cuerpo cubierto de fuertes púas defensivas y hocico tubular sin dientes."},
    {"clase": "CL. MAMMALIA", "orden": "O. DIDELPHIMORPHIA", "especie": "Zarigüeya (Didelphis marsupialis)", "cientifico": "Didelphis_marsupialis", "truco": "Marsupial americano con cola prensil desnuda y pulgar oponible."},
    {"clase": "CL. MAMMALIA", "orden": "O. MICROBIOTHERIA", "especie": "Monito de monte (Dromiciops gliroides)", "cientifico": "Dromiciops_gliroides", "truco": "Pequeño marsupial arborícola nocturno sudamericano con cola parcialmente prensil."},
    {"clase": "CL. MAMMALIA", "orden": "O. DASYUROMORPHIA", "especie": "Lobo marsupial (Thylacinus cynocephalus)", "cientifico": "Thylacinus_cynocephalus", "truco": "Rayas oscuras transversales en el lomo tipo tigre; extinto."},
    {"clase": "CL. MAMMALIA", "orden": "O. DASYUROMORPHIA", "especie": "Diablo de Tasmania (Sarcophilus harrisii)", "cientifico": "Sarcophilus_harrisii", "truco": "Negro con mancha pectoral blanca y mandíbulas capaces de triturar huesos."},
    {"clase": "CL. MAMMALIA", "orden": "O. DIPROTODONTIA", "especie": "Koala (Phascolarctos cinereus)", "cientifico": "Phascolarctos_cinereus", "truco": "Orejas grandes redondas peludas y extremidades con dos dedos opuestos."},
    {"clase": "CL. MAMMALIA", "orden": "O. DIPROTODONTIA", "especie": "Petauro (Petaurus breviceps)", "cientifico": "Petaurus_breviceps", "truco": "Membrana deslizante (patagio) entre muñecas y tobillos para planear."},
    {"clase": "CL. MAMMALIA", "orden": "O. DIPROTODONTIA", "especie": "Canguro Rojo (Macropus rufus)", "cientifico": "Macropus_rufus", "truco": "Grandes patas traseras saltadoras y potente cola de equilibrio."},
    {"clase": "CL. MAMMALIA", "orden": "O. MACROSCELIDEA", "especie": "Musaraña elefante (Elephantulus rufescens)", "cientifico": "Elephantulus_rufescens", "truco": "Hocico móvil muy alargado en trompa corta y patas traseras para saltar."},
    {"clase": "CL. MAMMALIA", "orden": "O. TUBULIDENTATA", "especie": "Cerdo hormiguero (Orycteropus afer)", "cientifico": "Orycteropus_afer", "truco": "Orejas de conejo, hocico tubular y garras excavadoras para termitas."},
    {"clase": "CL. MAMMALIA", "orden": "O. HYRACOIDEA", "especie": "Damán (Procavia capensis)", "cientifico": "Procavia_capensis", "truco": "Aspecto de cobaya grande emparentado con elefantes; pezuñas en vez de garras."},
    {"clase": "CL. MAMMALIA", "orden": "O. PROBOSCIDEA", "especie": "Elefante africano (Loxodonta africana)", "cientifico": "Loxodonta_africana", "truco": "Grandes orejas como mapa de África y dos dedos prensiles en la trompa."},
    {"clase": "CL. MAMMALIA", "orden": "O. PROBOSCIDEA", "especie": "Elefante indio (Elephas maximus)", "cientifico": "Elephas_maximus", "truco": "Orejas pequeñas rectangulares y un solo dedo prensil en la trompa."},
    {"clase": "CL. MAMMALIA", "orden": "O. SIRENIA", "especie": "Manatí (Trichechus manatus)", "cientifico": "Trichechus_manatus", "truco": "Aleta caudal redondeada en pala horizontal y hocico superior dividido móvil."},
    {"clase": "CL. MAMMALIA", "orden": "O. CINGULATA", "especie": "Armadillo (Dasypus novemcinctus)", "cientifico": "Dasypus_novemcinctus", "truco": "Placas óseas dérmicas articuladas en bandas transversales y hocico puntiagudo."},
    {"clase": "CL. MAMMALIA", "orden": "O. PILOSA", "especie": "Perezoso (Bradypus tridactylus)", "cientifico": "Bradypus_tridactylus", "truco": "3 dedos con garras en gancho, pelo verdoso por algas y metabolismo lento."},
    {"clase": "CL. MAMMALIA", "orden": "O. PILOSA", "especie": "Oso hormiguero (Myrmecophaga tridactyla)", "cientifico": "Myrmecophaga_tridactyla", "truco": "Morro tubular sin dientes, lengua larguísima y cola con penacho largo."},
    {"clase": "CL. MAMMALIA", "orden": "O. DERMOPTERA", "especie": "Colugo (Cynocephalus volans)", "cientifico": "Cynocephalus_volans", "truco": "Patagio completo que abarca espacios interdigitales y cola para planear."},
    {"clase": "CL. MAMMALIA", "orden": "O. SCANDENTIA", "especie": "Tupaya (Tupaia tana)", "cientifico": "Tupaia_tana", "truco": "Aspecto de musaraña con afinidades primate; gran cerebro y hocico puntiagudo."},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Lémur de cola anillada (Lemur catta)", "cientifico": "Lemur_catta", "truco": "Larga cola con anillos blancos y negros alternos y ojos grandes."},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Aye-aye (Daubentonia madagascariensis)", "cientifico": "Daubentonia_madagascariensis", "truco": "Dedo medio de la mano extraordinariamente alargado y fino para extraer larvas."},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Gálago (Galago senegalensis)", "cientifico": "Galago_senegalensis", "truco": "Grandes ojos nocturnos y orejas membranosas que se pliegan."},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Loris (Loris lydekkerianus)", "cientifico": "Loris_lydekkerianus", "truco": "Hábitos nocturnos arborícolas lentos, sin cola aparente y grandes ojos fijos."},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Tarsero (Tarsius tarsier)", "cientifico": "Tarsius_tarsier", "truco": "Enormes ojos fijos y huesos del tarso alargados para saltar."},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Mono capuchino (Cebus capucinus)", "cientifico": "Cebus_capucinus", "truco": "Frente blanca y píleo negro distintivo ('monje'); uso de herramientas."},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Mono aullador (Alouatta palliata)", "cientifico": "Alouatta_palliata", "truco": "Mandíbula con hueso hioides hipertrofiado para emitir fuertes aullidos."},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Macaco de Berbería (Macaca sylvanus)", "cientifico": "Macaca_sylvanus", "truco": "Único primate silvestre en Europa, cola vestigial y pelaje marrón beis."},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Papión negro (Papio ursinus)", "cientifico": "Papio_ursinus", "truco": "Hocico alargado tipo perro con caninos potentes y callosidades isquiáticas."},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Mono patas (Erythrocebus patas)", "cientifico": "Erythrocebus_patas", "truco": "Patas muy largas para carrera veloz en sabanas abiertas; pelaje rojizo."},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Colobo (Colobus guereza)", "cientifico": "Colobus_guereza", "truco": "Pelaje negro con capa de pelo blanco largo colgante en flancos; sin pulgar."},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Gibón (Hylobates lar)", "cientifico": "Hylobates_lar", "truco": "Brazos larguísimos para braquiación y marcas blancas en manos/pies."},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Orangután de Sumatra (Pongo abelii)", "cientifico": "Pongo_abelii", "truco": "Pelaje rojo anaranjado, arborícola solitario y grandes mofletes en machos."},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Gorila de montaña (Gorilla beringei)", "cientifico": "Gorilla_beringei", "truco": "Mayor primate, cresta sagital en machos, pecho ancho sin pelo."},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Chimpancé (Pan troglodytes)", "cientifico": "Pan_troglodytes", "truco": "Orejas grandes prominentes y alta inteligencia social con herramientas."},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Rata parda (Rattus norvegicus)", "cientifico": "Rattus_norvegicus", "truco": "Cola más corta que cabeza y cuerpo combinados; robusta y excavadora."},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Ratón de campo (Apodemus sylvaticus)", "cientifico": "Apodemus_sylvaticus", "truco": "Mancha amarillita en el pecho entre las patas delanteras."},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Topillo campesino (Microtus arvalis)", "cientifico": "Microtus_arvalis", "truco": "Cuerpo rechoncho, cola corta y orejas ocultas en el pelaje denso."},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Lirón careto (Eliomys quercinus)", "cientifico": "Eliomys_quercinus", "truco": "Antifaz negro alrededor de los ojos y cola con pincel de pelos blanco/negro."},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Ardilla roja (Sciurus vulgaris)", "cientifico": "Sciurus_vulgaris", "truco": "Pinceles de pelos largos en las puntas de las orejas en invierno."},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Castor europeo (Castor fiber)", "cientifico": "Castor_fiber", "truco": "Cola aplanada escamosa en pala e incisivos naranjas para talar árboles."},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Marmota alpina (Marmota marmota)", "cientifico": "Marmota_marmota", "truco": "Roedor social de alta montaña con silbidos estridentes de alarma."},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Capibara (Hydrochoerus hydrochaeris)", "cientifico": "Hydrochoerus_hydrochaeris", "truco": "Roedor más grande del mundo, cuerpo semicuadriculado adaptado al agua."},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Mara (Dolichotis patagonum)", "cientifico": "Dolichotis_patagonum", "truco": "Aspecto de liebre de patas largas con pezuñas en vez de garras."},
    {"clase": "CL. MAMMALIA", "orden": "O. LAGOMORPHA", "especie": "Pica (Ochotona princeps)", "cientifico": "Ochotona_princeps", "truco": "Sin cola aparente, orejas redondeadas y almacena 'heno' para el invierno."},
    {"clase": "CL. MAMMALIA", "orden": "O. LAGOMORPHA", "especie": "Conejo (Oryctolagus cuniculus)", "cientifico": "Oryctolagus_cuniculus", "truco": "Orejas más cortas que la cabeza y crías altrices nacidas sin pelo."},
    {"clase": "CL. MAMMALIA", "orden": "O. LAGOMORPHA", "especie": "Liebre ibérica (Lepus granatensis)", "cientifico": "Lepus_granatensis", "truco": "Orejas muy largas con las puntas negras muy marcadas."},
    {"clase": "CL. MAMMALIA", "orden": "O. EULIPOTYPHLA", "especie": "Erizo europeo (Erinaceus europaeus)", "cientifico": "Erinaceus_europaeus", "truco": "Dorso cubierto de fuertes púas y capacidad de enrollarse en bola."},
    {"clase": "CL. MAMMALIA", "orden": "O. EULIPOTYPHLA", "especie": "Musaraña gris (Crocidura russula)", "cientifico": "Crocidura_russula", "truco": "Dientes completamente blancos sin pigmentación roja y olor almizclado."},
    {"clase": "CL. MAMMALIA", "orden": "O. EULIPOTYPHLA", "especie": "Desmán ibérico (Galemys pyrenaicus)", "cientifico": "Galemys_pyrenaicus", "truco": "Trompa móvil en probóscide y cola con quilla para natación fluvial."},
    {"clase": "CL. MAMMALIA", "orden": "O. EULIPOTYPHLA", "especie": "Topo europeo (Talpa europaea)", "cientifico": "Talpa_europaea", "truco": "Extremidades delanteras palmeadas en pala con grandes uñas hacia fuera."},
    {"clase": "CL. MAMMALIA", "orden": "O. CHIROPTERA", "especie": "Zorro volador (Pteropus conspicillatus)", "cientifico": "Pteropus_conspicillatus", "truco": "Gran murciélago frugívoro con anillos amarillos alrededor de los ojos."},
    {"clase": "CL. MAMMALIA", "orden": "O. CHIROPTERA", "especie": "Murciélago enano (Pipistrellus pipistrellus)", "cientifico": "Pipistrellus_pipistrellus", "truco": "Muy pequeño, hocico corto y vuelo rápido e irregular en ciudades."},
    {"clase": "CL. MAMMALIA", "orden": "O. CHIROPTERA", "especie": "Murciélago grande de herradura (Rhinolophus ferrumequinum)", "cientifico": "Rhinolophus_ferrumequinum", "truco": "Hoja nasal compleja en forma de herradura para ecolocalización."},
    {"clase": "CL. MAMMALIA", "orden": "O. PHOLIDOTA", "especie": "Pangolín (Manis crassicaudata)", "cientifico": "Manis_crassicaudata", "truco": "Grandes escamas superpuestas de queratina y lengua larguísima."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Lince ibérico (Lynx pardinus)", "cientifico": "Lynx_pardinus", "truco": "Pinceles de pelos negros en las orejas, patillas faciales y capa moteada."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Gato montés (Felis silvestris)", "cientifico": "Felis_silvestris", "truco": "Cola gruesa embotada con anillos negros y raya dorsal que no llega a la punta."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "León (Panthera leo)", "cientifico": "Panthera_leo", "truco": "Melena en machos, coloración arena uniforme y vida social en manadas."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Leopardo (Panthera pardus)", "cientifico": "Panthera_pardus", "truco": "Rosetas oscuras en el pelaje sin punto central y gran habilidad trepadora."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Jaguar (Panthera onca)", "cientifico": "Panthera_onca", "truco": "Rosetas grandes en el pelaje que contienen motas negras en su interior."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Puma (Puma concolor)", "cientifico": "Puma_concolor", "truco": "Pelaje leonado uniforme sin manchas en adultos y gran salto vertical."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Guepardo (Acinonyx jubatus)", "cientifico": "Acinonyx_jubatus", "truco": "Líneas lacrimales negras ('lágrimas') desde los ojos y uñas no retráctiles."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Gineta (Genetta genetta)", "cientifico": "Genetta_genetta", "truco": "Cuerpo alargado, anillos negros en la cola y filas de manchas oscuras."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Hiena manchada (Crocuta crocuta)", "cientifico": "Crocuta_crocuta", "truco": "Patas delanteras más largas que las traseras y mandíbulas trituradoras."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Meloncillo (Herpestes ichneumon)", "cientifico": "Herpestes_ichneumon", "truco": "Grisáceo agutí con cola en pincel oscuro; inmune a veneno de serpiente."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Lobo (Canis lupus)", "cientifico": "Canis_lupus", "truco": "Hocico ancho, orejas erguidas y ojos con iris amarillento; huellas alineadas."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Zorro (Vulpes vulpes)", "cientifico": "Vulpes_vulpes", "truco": "Punta de la cola blanca brillante, antifaz rojizo y pupilas ovaladas."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Lobo de crin (Chrysocyon brachyurus)", "cientifico": "Chrysocyon_brachyurus", "truco": "Extremidades extraordinariamente largas (parece zanco) y melena dorsal negra."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Licaón (Lycaon pictus)", "cientifico": "Lycaon_pictus", "truco": "Orejas redondeadas tipo murciélago y manchas tricolores irregulares."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Oso pardo (Ursus arctos)", "cientifico": "Ursus_arctos", "truco": "Joroba muscular prominente en los hombros y garras delanteras curvas."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Oso panda (Ailuropoda melanoleuca)", "cientifico": "Ailuropoda_melanoleuca", "truco": "Manchas negras distintivas en ojos y cuerpo; falso pulgar para bambú."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Foca común (Phoca vitulina)", "cientifico": "Phoca_vitulina", "truco": "Cabeza redondeada tipo perro y orificios nasales en V invertida."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Lobo marino (Otaria flavescens)", "cientifico": "Otaria_flavescens", "truco": "Hocico corto levantado, melena rudimentaria en machos y orejas externas."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Mapache (Procyon lotor)", "cientifico": "Procyon_lotor", "truco": "Antifaz negro de bandido sobre los ojos y cola con anillos blancos y negros."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Comadreja (Mustela nivalis)", "cientifico": "Mustela_nivalis", "truco": "Carnívoro más pequeño, cuerpo vermiforme alargado y cola sin punta negra."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Garduña (Martes foina)", "cientifico": "Martes_foina", "truco": "Mancha pectoral blanca bifurcada hacia las patas y nariz rosada."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Nutria paleártica (Lutra lutra)", "cientifico": "Lutra_lutra", "truco": "Membranas interdigitales, cabeza aplanada con bigotes largos e hidrófuga."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Tejón (Meles meles)", "cientifico": "Meles_meles", "truco": "Bandas longitudinales blancas y negras muy marcadas en la cabeza."},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Glotón (Gulo gulo)", "cientifico": "Gulo_gulo", "truco": "Mayor mustélido terrestre, aspecto de oso robusto con bandas claras en flanco."},
    {"clase": "CL. MAMMALIA", "orden": "O. PERISSODACTYLA", "especie": "Onagro (Equus hemionus)", "cientifico": "Equus_hemionus", "truco": "Coloración arena uniforme, raya dorsal estrecha y sin rayas en extremidades."},
    {"clase": "CL. MAMMALIA", "orden": "O. PERISSODACTYLA", "especie": "Cebra común (Equus quagga)", "cientifico": "Equus_quagga", "truco": "Rayas anchas negras y blancas hasta el vientre con bandas 'sombra' marrones."},
    {"clase": "CL. MAMMALIA", "orden": "O. PERISSODACTYLA", "especie": "Tapir de montaña (Tapirus pinchaque)", "cientifico": "Tapirus_pinchaque", "truco": "Larga probóscide móvil y pelo lanoso espeso oscuro con labios blancos."},
    {"clase": "CL. MAMMALIA", "orden": "O. PERISSODACTYLA", "especie": "Rinoceronte indio (Rhinoceros unicornis)", "cientifico": "Rhinoceros_unicornis", "truco": "Un solo cuerno nasal y piel con pliegues profundos tipo armadura."},
    {"clase": "CL. MAMMALIA", "orden": "O. PERISSODACTYLA", "especie": "Rinoceronte negro (Diceros bicornis)", "cientifico": "Diceros_bicornis", "truco": "Labio superior prehensil en punta para ramonear y dos cuernos."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Guanaco (Lama guanicoe)", "cientifico": "Lama_guanicoe", "truco": "Pelaje marrón canela en lomo y blanco en vientre; cara grisácea."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Camello (Camelus ferus)", "cientifico": "Camelus_ferus", "truco": "Dos jorobas dorsales de grasa, pelo lanoso largo y pestañas dobles."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Jabalí (Sus scrofa)", "cientifico": "Sus_scrofa", "truco": "Cerdas oscuras, morro en disco cartilaginoso y colmillos salientes."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Hipopótamo (Hippopotamus amphibius)", "cientifico": "Hippopotamus_amphibius", "truco": "Cuerpo masivo sin pelo, piel secretando sudor rojo y boca de gran apertura."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Ciervo (Cervus elaphus)", "cientifico": "Cervus_elaphus", "truco": "Gran cuerna ramificada en machos con roseta y mancha blanca en obispillo."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Gamo (Dama dama)", "cientifico": "Dama_dama", "truco": "Cuernas aplanadas en palma y pelaje rojizo con llamativos lunares blancos."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Corzo (Capreolus capreolus)", "cientifico": "Capreolus_capreolus", "truco": "Mancha blanca pura en el trasero (espejo anal) y cuernas cortas perladas."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Reno (Rangifer tarandus)", "cientifico": "Rangifer_tarandus", "truco": "Cuernas en ambos sexos, pezuñas anchas para nieve y hocico peludo."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Alce euroasiático (Alces alces)", "cientifico": "Alces_alces", "truco": "Hocico abultado colgante, papada carnosa y cuernas masivas palmeadas."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Rebeco (Rupicapra pyrenaica)", "cientifico": "Rupicapra_pyrenaica", "truco": "Cuernos cortos verticales con ganchos en anzuelo y listas faciales oscuras."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Cabra montés (Capra pyrenaica)", "cientifico": "Capra_pyrenaica", "truco": "Cuernos grandes estriados curvados hacia atrás en arco en machos."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Muflón (Ovis gmelini)", "cientifico": "Ovis_gmelini", "truco": "Machos con grandes cuernos curvados en espiral y mancha clara en silla."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Bisonte europeo (Bison bonasus)", "cientifico": "Bison_bonasus", "truco": "Melena delantera frondosa, joroba menos marcada y cola peluda."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Gacela común (Gazella dorcas)", "cientifico": "Gazella_dorcas", "truco": "Pequeña gacela desértica con cuernos en lira y franja oscura en flanco."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Saiga (Saiga tatarica)", "cientifico": "Saiga_tatarica", "truco": "Hocico bulboso flexible en trompa corta y cuernos céros transparentes."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Chirú (Pantholops hodgsonii)", "cientifico": "Pantholops_hodgsonii", "truco": "Antílope tibetano con cuernos rectos verticales finos y hocico abultado."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Búfalo africano (Syncerus caffer)", "cientifico": "Syncerus_caffer", "truco": "Bases de cuernos fusionadas en la frente formando un escudo óseo continuo."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Nu azul (Connochaetes taurinus)", "cientifico": "Connochaetes_taurinus", "truco": "Cabeza robusta con barba, cuernos en paréntesis y lomo inclinado."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Berrendo (Antilocapra americana)", "cientifico": "Antilocapra_americana", "truco": "Cuernos bifurcados con estuche córneo que se muda anualmente."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Jirafa (Giraffa camelopardalis)", "cientifico": "Giraffa_camelopardalis", "truco": "Cuello y extremidades muy alargadas, osicones con piel y manchas poligonales."},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Okapi (Okapia johnstoni)", "cientifico": "Okapia_johnstoni", "truco": "Rayas blancas horizontales en patas estilo cebra y lengua azul larga."},
    {"clase": "CL. MAMMALIA", "orden": "O. INFRAORDEN CETACEA", "especie": "Delfín listado (Stenella coeruleoalba)", "cientifico": "Stenella_coeruleoalba", "truco": "Franja oscura azulada desde el ojo hasta el ano y flancos blanquecinos."},
    {"clase": "CL. MAMMALIA", "orden": "O. INFRAORDEN CETACEA", "especie": "Orca (Orcinus orca)", "cientifico": "Orcinus_orca", "truco": "Mancha blanca ovalada detrás del ojo, aleta dorsal gigante y contraste negro/blanco."},
    {"clase": "CL. MAMMALIA", "orden": "O. INFRAORDEN CETACEA", "especie": "Cachalote (Physeter macrocephalus)", "cientifico": "Physeter_macrocephalus", "truco": "Cabeza cuadrada gigantesca, espiráculo a la izquierda y piel arrugada."},
    {"clase": "CL. MAMMALIA", "orden": "O. INFRAORDEN CETACEA", "especie": "Yubarta (Megaptera novaeangliae)", "cientifico": "Megaptera_novaeangliae", "truco": "Aletas pectorales extraordinariamente largas con bordes serrados nudosos."},
    {"clase": "CL. MAMMALIA", "orden": "O. INFRAORDEN CETACEA", "especie": "Ballena franca (Eubalaena glacialis)", "cientifico": "Eubalaena_glacialis", "truco": "Ausencia de aleta dorsal y callosidades córneas blanquecinas en la cabeza."}
]

# Cabecera dinámica estrictamente centrada según la sección seleccionada
if seccion_seleccionada == "VERTEBRADOS":
    st.markdown("<h1>VISU VERTEBRADOS</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>identificación de especies</div>", unsafe_allow_html=True)
elif seccion_seleccionada == "INVERTEBRADOS":
    st.markdown("<h1>VISU INVERTEBRADOS</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>no artrópodos</div>", unsafe_allow_html=True)
else:
    st.markdown("<h1>VISU ARTRÓPODOS</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>insectos, arácnidos y crustáceos</div>", unsafe_allow_html=True)

def normalizar_texto(texto):
    """Elimina tildes, convierte a minúsculas y limpia espacios."""
    if not texto:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', texto)
    sin_tildes = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    return sin_tildes.strip().lower()

def obtener_fotos(nombre_especie, max_fotos=2):
    carpeta_base = Path("IMAGENES") / nombre_especie
    fotos = []
    
    if carpeta_base.exists() and carpeta_base.is_dir():
        extensiones = ("*.jpg", "*.jpeg", "*.webp")
        archivos_locales = []
        for ext in extensiones:
            archivos_locales.extend(list(carpeta_base.glob(ext)))
            
        archivos_locales = sorted(archivos_locales)[:max_fotos]
        
        for archivo in archivos_locales:
            try:
                with open(archivo, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")
                    data_url = f"data:image/jpeg;base64,{encoded}"
                
                fotos.append({
                    "url": data_url,
                    "fuente": "Carpeta Local",
                    "licencia": "Uso personal",
                    "autor": "Propio"
                })
            except Exception:
                continue
                
    return fotos

# Lógica condicional para mostrar el contenido según la opción del menú
if seccion_seleccionada == "VERTEBRADOS":
    if 'sesion_vert' not in st.session_state:
        cantidad_preguntas = min(10, len(DATOS_VERTEBRADOS))
        st.session_state.sesion_vert = random.sample(DATOS_VERTEBRADOS, cantidad_preguntas)
        st.session_state.idx_vert = 0
        st.session_state.aciertos_vert = 0
        st.session_state.fallos_vert = 0
        st.session_state.estado_respuesta_vert = None
        st.session_state.temp_c = ""
        st.session_state.temp_o = ""
        st.session_state.temp_e = ""

    if st.session_state.idx_vert < len(st.session_state.sesion_vert):
        actual = st.session_state.sesion_vert[st.session_state.idx_vert]

        if st.session_state.get("imagen_especie_actual") != actual["especie"]:
            st.session_state.imagen_especie_actual = actual["especie"]
            st.session_state.indice_imagen = 0

        fotos_pregunta = obtener_fotos(actual["especie"], max_fotos=2)

        st.markdown(
            f"<p class='pregunta-counter'>"
            f"Pregunta {st.session_state.idx_vert + 1} de {len(st.session_state.sesion_vert)}</p>",
            unsafe_allow_html=True
        )

        if fotos_pregunta:
            st.session_state.indice_imagen = min(
                st.session_state.indice_imagen, len(fotos_pregunta) - 1
            )
            
            col_izq, col_img, col_der = st.columns([0.6, 12, 0.6], vertical_alignment="center")
            
            with col_izq:
                if st.button("‹", key=f"foto_anterior_{st.session_state.idx_vert}", type="tertiary",
                             disabled=len(fotos_pregunta) < 2, help="Fotografía anterior"):
                    st.session_state.indice_imagen = (
                        st.session_state.indice_imagen - 1
                    ) % len(fotos_pregunta)
                    st.rerun()

            with col_img:
                foto_actual = fotos_pregunta[st.session_state.indice_imagen]
                st.markdown(
                    f"""<div class="img-borde">
                        <img src="{foto_actual["url"]}" style="max-width: 100%; max-height: 400px; width: auto; height: auto; border-radius: 6px; display: block; margin: 0 auto;">
                    </div>""",
                    unsafe_allow_html=True
                )

            with col_der:
                if st.button("›", key=f"foto_siguiente_{st.session_state.idx_vert}", type="tertiary",
                             disabled=len(fotos_pregunta) < 2, help="Fotografía siguiente"):
                    st.session_state.indice_imagen = (
                        st.session_state.indice_imagen + 1
                    ) % len(fotos_pregunta)
                    st.rerun()

            st.markdown(
                f"<p class='pregunta-counter'>"
                f"{st.session_state.indice_imagen + 1} / {len(fotos_pregunta)}</p>",
                unsafe_allow_html=True
            )
        else:
            st.warning("No se han encontrado fotografías locales para esta especie en su carpeta.")

        if st.session_state.estado_respuesta_vert is not None:
            val_c = actual["clase"]
            val_o = actual["orden"]
            val_e = actual["especie"]
        else:
            val_c = st.session_state.temp_c
            val_o = st.session_state.temp_o
            val_e = st.session_state.temp_e

        c_ing = st.text_input("CLASE", value=val_c, key="input_c")
        o_ing = st.text_input("ORDEN", value=val_o, key="input_o")
        e_ing = st.text_input("ESPECIE", value=val_e, key="input_e")

        # Recuadro separado a la derecha del panel central en caso de fallo
        if st.session_state.estado_respuesta_vert == 'fallo':
            st.markdown(
                f"""<div class="side-trick-card">
                    <p style="color: #FF6666; font-weight: 700; font-size: 0.85rem; margin-bottom: 0.75rem;">¡OOPS! RESPUESTA INCORRECTA</p>
                    <p style="font-size: 0.75rem; color: #FFFFFF; margin-bottom: 0.75rem; line-height: 1.4;">
                        <b>SOLUCIÓN:</b><br>{actual['clase']} | {actual['orden']} | {actual['especie']}
                    </p>
                    <hr style="border: 0; border-top: 1px solid #333333; margin: 0.75rem 0;">
                    <p style="font-size: 0.75rem; color: #FFCCCC; font-weight: 600; line-height: 1.4;">
                        <b>TRUCO VISU:</b><br>{actual['truco']}
                    </p>
                </div>""",
                unsafe_allow_html=True
            )
        elif st.session_state.estado_respuesta_vert == 'acierto':
            st.markdown(
                f"<div class='feedback-success'>¡RESPUESTA CORRECTA!<br>HAS IDENTIFICADO LA ESPECIE CORRECTAMENTE.</div>",
                unsafe_allow_html=True
            )

        if st.session_state.estado_respuesta_vert is not None:
            _, centro_siguiente, _ = st.columns([1, 2, 1])
            with centro_siguiente:
                siguiente = st.button("Siguiente pregunta", use_container_width=True)
            if siguiente:
                st.session_state.estado_respuesta_vert = None
                st.session_state.temp_c = ""
                st.session_state.temp_o = ""
                st.session_state.temp_e = ""
                st.session_state.idx_vert += 1
                st.rerun()
        else:
            _, centro_comprobar, _ = st.columns([1, 2, 1])
            with centro_comprobar:
                comprobar = st.button("Comprobar respuesta", type="primary", use_container_width=True)
            if comprobar:
                clase_ok = normalizar_texto(c_ing) == normalizar_texto(actual["clase"])
                orden_ok = normalizar_texto(o_ing) == normalizar_texto(actual["orden"])
                especie_ok = normalizar_texto(e_ing) == normalizar_texto(actual["especie"])

                if clase_ok and orden_ok and especie_ok:
                    st.session_state.aciertos_vert += 1
                    st.session_state.estado_respuesta_vert = 'acierto'
                else:
                    st.session_state.fallos_vert += 1
                    st.session_state.estado_respuesta_vert = 'fallo'
                st.rerun()
    else:
        total_preguntas = len(st.session_state.sesion_vert)
        aciertos = st.session_state.aciertos_vert
        fallos = st.session_state.fallos_vert

        nota = round((aciertos / total_preguntas) * 10, 1) if total_preguntas > 0 else 0

        st.markdown("<h3 style='text-align: center;'>Resultados del Test Visu</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Aciertos totales: {aciertos}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Fallos totales: {fallos}</p>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>Puntuación Final: {nota} / 10</h3>", unsafe_allow_html=True)

        if nota >= 5.0:
            st.balloons()
            st.markdown("<div class='test-result'>TEST SUPERADO CON ÉXITO</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='test-result fail'>TEST NO SUPERADO</div>", unsafe_allow_html=True)
            st.markdown("<p class='subtitle'>Se recomienda repasar las especies.</p>", unsafe_allow_html=True)

        _, centro_reiniciar, _ = st.columns([1, 2, 1])
        with centro_reiniciar:
            reiniciar = st.button("Reiniciar test", use_container_width=True)
        
        if reiniciar:
            for key in ['sesion_vert', 'idx_vert', 'aciertos_vert', 'fallos_vert', 'estado_respuesta_vert']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

elif seccion_seleccionada == "INVERTEBRADOS":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>MÓDULO EN DESARROLLO</h3>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle' style='text-align: center;'>Próximamente disponible el test de invertebrados no artrópodos.</p>", unsafe_allow_html=True)

else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>MÓDULO EN DESARROLLO</h3>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle' style='text-align: center;'>Próximamente disponible el test de artrópodos.</p>", unsafe_allow_html=True)