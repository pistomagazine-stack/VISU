import streamlit as st
import random
from pathlib import Path
import base64
import unicodedata

# Configuración de la página
st.set_page_config(
    page_title="Visu Zoología - UCM",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS con flechas limpias sin bordes ni botones y campos de texto ajustados al ancho de la imagen
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
        }

        /* Logotipo flotante */
        .logo-container {
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 99999;
            width: 75px;
            height: 75px;
            border-radius: 14px;
            overflow: hidden;
            border: none;
            background: transparent;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .logo-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 14px;
        }

        /* Ocultar el header superior nativo de Streamlit */
        header[data-testid="stHeader"] {
            background: transparent !important;
            visibility: hidden;
        }

        /* Tarjeta central estabilizada y centrada siempre */
        .block-container {
            max-width: 700px !important;
            width: 100% !important;
            padding: 2rem !important;
            text-align: center;
            background-color: #0A0A0A;
            border: 3px solid #FFFFFF;
            border-radius: 16px;
            margin: 2rem auto !important;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
            box-sizing: border-box;
        }

        h1, h2, h3, p, label, .stMarkdown, span, div {
            font-family: 'Montserrat', sans-serif !important;
            text-align: center !important;
            color: #FFFFFF;
            text-transform: uppercase !important;
        }

        /* Ritmo vertical */
        h1, h2, h3, p, div.stTextInput, .stButton, .feedback-error, .feedback-success, .img-borde, .test-result {
            margin-top: 0 !important;
            margin-bottom: 0.75rem !important;
        }

        h1 {
            color: #FFFFFF;
            font-weight: 700;
            letter-spacing: -0.03em;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }

        .subtitle {
            font-family: 'Montserrat', sans-serif;
            color: #FFCCCC;
            font-size: 0.75rem;
            font-weight: 500;
            letter-spacing: 0.1em;
            opacity: 0.9;
        }

        .pregunta-counter {
            font-size: 0.8rem;
            color: #FFCCCC;
        }

        /* Inputs ajustados exactamente al ancho de la imagen (450px) */
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

        ::-webkit-resizer {
            display: none !important;
        }

        div.stTextInput > div > div:focus-within {
            border-color: #FF0000;
        }

        /* Botones principales de acción */
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

        /* Bloques de feedback */
        .feedback-error {
            background-color: #FF0000 !important;
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
        .feedback-error * {
            color: #000000 !important;
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

        /* Contenedor de la imagen */
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

        /* Flechas sin apariencia de botón, sin fondo ni borde */
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
    </style>
""", unsafe_allow_html=True)

# Logotipo flotante
st.markdown("""
    <div class="logo-container">
        <img src="data:image/png;base64,""" + __import__("base64").b64encode(open("pp_2.png", "rb").read()).decode("utf-8") + """" alt="Logo">
    </div>
""", unsafe_allow_html=True)

DATOS_ESPECIES = [
    {"clase": "CL. MYXINI", "orden": "O. MYXINIFORMES", "especie": "Mixin (Myxine glutinosa)", "cientifico": "Myxine_glutinosa"},
    {"clase": "CL. HYPEROARTIA", "orden": "O. PETROMYZONTIFORMES", "especie": "Lamprea de mar (Petromyzon marinus)", "cientifico": "Petromyzon_marinus"},
    {"clase": "CL. HYPEROARTIA", "orden": "O. PETROMYZONTIFORMES", "especie": "Lamprea de arroyo (Lampetra fluviatilis)", "cientifico": "Lampetra_fluviatilis"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. CHIMAERIFORMES", "especie": "Quimera (Chimaera monstrosa)", "cientifico": "Chimaera_monstrosa"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. ORECTOLOBIFORMES", "especie": "Tiburón ballena (Rhincodon typus)", "cientifico": "Rhincodon_typus"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. LAMNIFORMES", "especie": "Pez zorro (Alopias vulpinus)", "cientifico": "Alopias_vulpinus"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. LAMNIFORMES", "especie": "Tiburón blanco (Carcharodon carcharias)", "cientifico": "Carcharodon_carcharias"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. LAMNIFORMES", "especie": "Marrajo (Isurus oxyrinchus)", "cientifico": "Isurus_oxyrinchus"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. LAMNIFORMES", "especie": "Peregrino (Cetorhinus maximus)", "cientifico": "Cetorhinus_maximus"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. LAMNIFORMES", "especie": "Tiburón toro (Carcharias taurus)", "cientifico": "Carcharias_taurus"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. CARCHARHINIFORMES", "especie": "Pintarroja (Scyliorhinus canicula)", "cientifico": "Scyliorhinus_canicula"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. CARCHARHINIFORMES", "especie": "Tintorera (Prionace glauca)", "cientifico": "Prionace_glauca"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. CARCHARHINIFORMES", "especie": "Pez martillo (Sphyrna zygaena)", "cientifico": "Sphyrna_zygaena"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. HEXANCHIFORMES", "especie": "Cañabota gris (Hexanchus griseus)", "cientifico": "Hexanchus_griseus"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. SQUALIFORMES", "especie": "Mielga (Squalus acanthias)", "cientifico": "Squalus_acanthias"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. SQUATINIFORMES", "especie": "Angelote (Squatina squatina)", "cientifico": "Squatina_squatina"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. RAJIFORMES", "especie": "Raya noruega (Dipturus batis)", "cientifico": "Dipturus_batis"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. RHINOBATIFORMES", "especie": "Pez guitarra (Rhinobatos rhinobatos)", "cientifico": "Rhinobatos_rhinobatos"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. TORPEDINIFORMES", "especie": "Tremielga (Torpedo torpedo)", "cientifico": "Torpedo_torpedo"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. MYLIOBATIFORMES", "especie": "Pastinaca (Dasyatis pastinaca)", "cientifico": "Dasyatis_pastinaca"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. MYLIOBATIFORMES", "especie": "Manta (Mobula mobular)", "cientifico": "Mobula_mobular"},
    {"clase": "CL. CHONDRICHTHYES", "orden": "O. MYLIOBATIFORMES", "especie": "Águila marina (Myliobatis aquila)", "cientifico": "Myliobatis_aquila"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. POLYPTERIFORMES", "especie": "Bichir (Polypterus bichir)", "cientifico": "Polypterus_bichir"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. ACIPENSERIFORMES", "especie": "Esturión (Acipenser sturio)", "cientifico": "Acipenser_sturio"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. ACIPENSERIFORMES", "especie": "Pez espátula (Polyodon spathula)", "cientifico": "Polyodon_spathula"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. LEPISOSTEIFORMES", "especie": "Pez lagarto (Lepisosteus osseus)", "cientifico": "Lepisosteus_osseus"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. AMIIFORMES", "especie": "Pez del cieno (Amia calva)", "cientifico": "Amia_calva"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. OSTEOGLOSSIFORMES", "especie": "Arapaima (Arapaima gigas)", "cientifico": "Arapaima_gigas"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. ANGUILLIFORMES", "especie": "Anguila (Anguilla anguilla)", "cientifico": "Anguilla_anguilla"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. ANGUILLIFORMES", "especie": "Congrio (Conger conger)", "cientifico": "Conger_conger"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. ANGUILLIFORMES", "especie": "Morena (Muraena helena)", "cientifico": "Muraena_helena"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CLUPEIFORMES", "especie": "Boquerón (Engraulis encrasicolus)", "cientifico": "Engraulis_encrasicolus"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CLUPEIFORMES", "especie": "Sardina (Sardina pilchardus)", "cientifico": "Sardina_pilchardus"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CYPRINIFORMES", "especie": "Barbo comiza (Luciobarbus comizo)", "cientifico": "Luciobarbus_comizo"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CYPRINIFORMES", "especie": "Carpa (Cyprinus carpio)", "cientifico": "Cyprinus_carpio"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CYPRINIFORMES", "especie": "Carpín dorado (Carassius auratus)", "cientifico": "Carassius_auratus"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SILURIFORMES", "especie": "Siluro (Silurus glanis)", "cientifico": "Silurus_glanis"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CHARACIFORMES", "especie": "Piraña negra (Serrasalmus rhombeus)", "cientifico": "Serrasalmus_rhombeus"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CHARACIFORMES", "especie": "Tetra neón (Paracheirodon innesi)", "cientifico": "Paracheirodon_innesi"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. GYMNOTIFORMES", "especie": "Anguila eléctrica (Electrophorus electricus)", "cientifico": "Electrophorus_electricus"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SALMONIFORMES", "especie": "Trucha (Salmo trutta)", "cientifico": "Salmo_trutta"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SALMONIFORMES", "especie": "Salmón (Salmo salar)", "cientifico": "Salmo_salar"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SALMONIFORMES", "especie": "Salmón rojo (Oncorhynchus nerka)", "cientifico": "Oncorhynchus_nerka"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. ESOCIFORMES", "especie": "Lucio (Esox lucius)", "cientifico": "Esox_lucius"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. LOPHIIFORMES", "especie": "Rape (Lophius piscatorius)", "cientifico": "Lophius_piscatorius"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. GADIFORMES", "especie": "Merluza (Merluccius merluccius)", "cientifico": "Merluccius_merluccius"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. GADIFORMES", "especie": "Bacalao (Gadus morhua)", "cientifico": "Gadus_morhua"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CYPRINODONTIFORMES", "especie": "Gambusia (Gambusia affinis)", "cientifico": "Gambusia_affinis"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CYPRINODONTIFORMES", "especie": "Guppy (Poecilia reticulata)", "cientifico": "Poecilia_reticulata"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. GASTEROSTEIFORMES", "especie": "Espinoso (Gasterosteus aculeatus)", "cientifico": "Gasterosteus_aculeatus"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SYNGNATHIFORMES", "especie": "Caballito de mar (Hippocampus zosterae)", "cientifico": "Hippocampus_zosterae"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SCORPAENIFORMES", "especie": "Cabracho (Scorpaena scrofa)", "cientifico": "Scorpaena_scrofa"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. BLENNIIFORMES", "especie": "Fraile (Salaria fluviatilis)", "cientifico": "Salaria_fluviatilis"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. CARANGIFORMES", "especie": "Jurel (Trachurus trachurus)", "cientifico": "Trachurus_trachurus"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. PERCIFORMES", "especie": "Salmonete de fango (Mullus barbatus)", "cientifico": "Mullus_barbatus"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. PERCIFORMES", "especie": "Mero (Epinephelus marginatus)", "cientifico": "Epinephelus_marginatus"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SPARIFORMES", "especie": "Besugo (Pagellus bogaraveo)", "cientifico": "Pagellus_bogaraveo"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SPARIFORMES", "especie": "Dorada (Sparus aurata)", "cientifico": "Sparus_aurata"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. MORONIFORMES", "especie": "Lubina (Dicentrarchus labrax)", "cientifico": "Dicentrarchus_labrax"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SCOMBRIFORMES", "especie": "Caballa (Scomber scombrus)", "cientifico": "Scomber_scombrus"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SCOMBRIFORMES", "especie": "Atún (Thunnus thynnus)", "cientifico": "Thunnus_thynnus"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. SCOMBRIFORMES", "especie": "Bonito (Thunnus alalunga)", "cientifico": "Thunnus_alalunga"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. PLEURONECTIFORMES", "especie": "Rodaballo (Scophthalmus maximus)", "cientifico": "Scophthalmus_maximus"},
    {"clase": "CL. ACTINOPTERYGII", "orden": "O. PLEURONECTIFORMES", "especie": "Lenguado (Solea solea)", "cientifico": "Solea_solea"},
    {"clase": "CL. SARCOPTERYGII", "orden": "O. COELACANTHIFORMES", "especie": "Celacanto (Latimeria chalumnae)", "cientifico": "Latimeria_chalumnae"},
    {"clase": "CL. SARCOPTERYGII", "orden": "O. CERATODONTIFORMES", "especie": "Pez de barro americano (Lepidosiren paradoxa)", "cientifico": "Lepidosiren_paradoxa"},
    {"clase": "CL. AMPHIBIA", "orden": "O. GYMNOPHIONA", "especie": "Cecilia de Ceilán (Ichthyophis glutinosus)", "cientifico": "Ichthyophis_glutinosus"},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Salamandra gigante de China (Andrias davidianus)", "cientifico": "Andrias_davidianus"},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Salamandra rabilarga (Chioglossa lusitanica)", "cientifico": "Chioglossa_lusitanica"},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Gallipato (Pleurodeles waltl)", "cientifico": "Pleurodeles_waltl"},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Salamandra común (Salamandra salamandra)", "cientifico": "Salamandra_salamandra"},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Tritón palmeado (Lissotriton helveticus)", "cientifico": "Lissotriton_helveticus"},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Tritón ibérico (Lissotriton boscai)", "cientifico": "Lissotriton_boscai"},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Tritón de los Pirineos (Calotriton asper)", "cientifico": "Calotriton_asper"},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Proteo (Proteus anguinus)", "cientifico": "Proteus_anguinus"},
    {"clase": "CL. AMPHIBIA", "orden": "O. CAUDATA", "especie": "Ajolote (Ambystoma mexicanum)", "cientifico": "Ambystoma_mexicanum"},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Sapo común ibérico (Bufo spinosus)", "cientifico": "Bufo_spinosus"},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Sapo corredor (Epidalea calamita)", "cientifico": "Epidalea_calamita"},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Sapo partero ibérico (Alytes cisternasii)", "cientifico": "Alytes_cisternasii"},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Rana verde común (Pelophylax perezi)", "cientifico": "Pelophylax_perezi"},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Rana patilarga (Rana iberica)", "cientifico": "Rana_iberica"},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Ranita de San Antonio ibérica (Hyla molleri)", "cientifico": "Hyla_molleri"},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Sapito de Darwin (Rhinoderma darwinii)", "cientifico": "Rhinoderma_darwinii"},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Sapo de Surinam (Pipa pipa)", "cientifico": "Pipa_pipa"},
    {"clase": "CL. AMPHIBIA", "orden": "O. SALIENTIA", "especie": "Rana punta de flecha (Dendrobates tinctorius)", "cientifico": "Dendrobates_tinctorius"},
    {"clase": "CL. REPTILIA", "orden": "O. CHELONIA", "especie": "Tortuga de caparazón blando del Ganges (Nilssonia gangetica)", "cientifico": "Nilssonia_gangetica"},
    {"clase": "CL. REPTILIA", "orden": "O. CHELONIA", "especie": "Tortuga boba (Caretta caretta)", "cientifico": "Caretta_caretta"},
    {"clase": "CL. REPTILIA", "orden": "O. CHELONIA", "especie": "Tortuga laúd (Dermochelys coriacea)", "cientifico": "Dermochelys_coriacea"},
    {"clase": "CL. REPTILIA", "orden": "O. CHELONIA", "especie": "Tortuga caimán (Macrochelys temminckii)", "cientifico": "Macrochelys_temminckii"},
    {"clase": "CL. REPTILIA", "orden": "O. CHELONIA", "especie": "Tortuga mora (Testudo graeca)", "cientifico": "Testudo_graeca"},
    {"clase": "CL. REPTILIA", "orden": "O. CHELONIA", "especie": "Galápago leproso (Mauremys leprosa)", "cientifico": "Mauremys_leprosa"},
    {"clase": "CL. REPTILIA", "orden": "O. CHELONIA", "especie": "Tortuga gigante de las Galápagos (Chelonoidis niger)", "cientifico": "Chelonoidis_niger"},
    {"clase": "CL. REPTILIA", "orden": "O. SPHENODONTIA", "especie": "Tuátara (Sphenodon punctatus)", "cientifico": "Sphenodon_punctatus"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Iguana común (Iguana iguana)", "cientifico": "Iguana_iguana"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Iguana marina (Amblyrhynchus cristatus)", "cientifico": "Amblyrhynchus_cristatus"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Agama común (Agama agama)", "cientifico": "Agama_agama"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Camaleón común (Chamaeleo chamaeleon)", "cientifico": "Chamaeleo_chamaeleon"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Salamanquesa común (Tarentola mauritanica)", "cientifico": "Tarentola_mauritanica"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Eslizón ibérico (Chalcides bedriagai)", "cientifico": "Chalcides_bedriagai"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Lagarto ocelado ibérico (Timon lepidus)", "cientifico": "Timon_lepidus"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Lagartija roquera (Podarcis muralis)", "cientifico": "Podarcis_muralis"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Lagartija colilarga (Psammodromus algirus)", "cientifico": "Psammodromus_algirus"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Lución (Anguis fragilis)", "cientifico": "Anguis_fragilis"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Monstruo de Gila (Heloderma suspectum)", "cientifico": "Heloderma_suspectum"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Varano de Komodo (Varanus komodoensis)", "cientifico": "Varanus_komodoensis"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Varano del Nilo (Varanus niloticus)", "cientifico": "Varanus_niloticus"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Culebrilla ciega común (Blanus cinereus)", "cientifico": "Blanus_cinereus"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Anaconda (Eunectes murinus)", "cientifico": "Eunectes_murinus"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Culebra bastarda (Malpolon monspessulanus)", "cientifico": "Malpolon_monspessulanus"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Culebra de collar mediterránea (Natrix astreptophora)", "cientifico": "Natrix_astreptophora"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Culebra de escalera (Zamenis scalaris)", "cientifico": "Zamenis_scalaris"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Cobra (Naja naja)", "cientifico": "Naja_naja"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Serpiente de mar (Laticauda colubrina)", "cientifico": "Laticauda_colubrina"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Víbora hocicuda (Vipera latastei)", "cientifico": "Vipera_latastei"},
    {"clase": "CL. REPTILIA", "orden": "O. SQUAMATA", "especie": "Serpiente de cascabel (Crotalus horridus)", "cientifico": "Crotalus_horridus"},
    {"clase": "CL. REPTILIA", "orden": "O. CROCODYLIA", "especie": "Cocodrilo del Nilo (Crocodylus niloticus)", "cientifico": "Crocodylus_niloticus"},
    {"clase": "CL. REPTILIA", "orden": "O. CROCODYLIA", "especie": "Aligátor americano (Alligator mississippiensis)", "cientifico": "Alligator_mississippiensis"},
    {"clase": "CL. REPTILIA", "orden": "O. CROCODYLIA", "especie": "Gavial (Gavialis gangeticus)", "cientifico": "Gavialis_gangeticus"},
    {"clase": "CL. AVES", "orden": "O. STRUTHIONIFORMES", "especie": "Avestruz (Struthio camelus)", "cientifico": "Struthio_camelus"},
    {"clase": "CL. AVES", "orden": "O. RHEIFORMES", "especie": "Nandú (Rhea americana)", "cientifico": "Rhea_americana"},
    {"clase": "CL. AVES", "orden": "O. TINAMIFORMES", "especie": "Tinamú común (Nothura maculosa)", "cientifico": "Nothura_maculosa"},
    {"clase": "CL. AVES", "orden": "O. CASUARIIFORMES", "especie": "Casuario (Casuarius casuarius)", "cientifico": "Casuarius_casuarius"},
    {"clase": "CL. AVES", "orden": "O. APTERYGIFORMES", "especie": "Kiwi sureño (Apteryx australis)", "cientifico": "Apteryx_australis"},
    {"clase": "CL. AVES", "orden": "O. GALLIFORMES", "especie": "Urogallo común (Tetrao urogallus)", "cientifico": "Tetrao_urogallus"},
    {"clase": "CL. AVES", "orden": "O. GALLIFORMES", "especie": "Perdiz roja (Alectoris rufa)", "cientifico": "Alectoris_rufa"},
    {"clase": "CL. AVES", "orden": "O. GALLIFORMES", "especie": "Perdiz pardilla (Perdix perdix)", "cientifico": "Perdix_perdix"},
    {"clase": "CL. AVES", "orden": "O. ANSERIFORMES", "especie": "Ánsar común (Anser anser)", "cientifico": "Anser_anser"},
    {"clase": "CL. AVES", "orden": "O. ANSERIFORMES", "especie": "Ánade azulón (Anas platyrhynchos)", "cientifico": "Anas_platyrhynchos"},
    {"clase": "CL. AVES", "orden": "O. ANSERIFORMES", "especie": "Porrón europeo (Aythya ferina)", "cientifico": "Aythya_ferina"},
    {"clase": "CL. AVES", "orden": "O. CAPRIMULGIFORMES", "especie": "Chotacabras europeo (Caprimulgus europaeus)", "cientifico": "Caprimulgus_europaeus"},
    {"clase": "CL. AVES", "orden": "O. CAPRIMULGIFORMES", "especie": "Vencejo común (Apus apus)", "cientifico": "Apus_apus"},
    {"clase": "CL. AVES", "orden": "O. CAPRIMULGIFORMES", "especie": "Colibrí zunzuncito (Mellisuga helenae)", "cientifico": "Mellisuga_helenae"},
    {"clase": "CL. AVES", "orden": "O. CAPRIMULGIFORMES", "especie": "Guácharo (Steatornis caripensis)", "cientifico": "Steatornis_caripensis"},
    {"clase": "CL. AVES", "orden": "O. COLUMBIFORMES", "especie": "Paloma torcaz (Columba palumbus)", "cientifico": "Columba_palumbus"},
    {"clase": "CL. AVES", "orden": "O. COLUMBIFORMES", "especie": "Tórtola europea (Streptopelia turtur)", "cientifico": "Streptopelia_turtur"},
    {"clase": "CL. AVES", "orden": "O. CUCULIFORMES", "especie": "Cuco (Cuculus canorus)", "cientifico": "Cuculus_canorus"},
    {"clase": "CL. AVES", "orden": "O. OTIDIFORMES", "especie": "Avutarda euroasiática (Otis tarda)", "cientifico": "Otis_tarda"},
    {"clase": "CL. AVES", "orden": "O. GRUIFORMES", "especie": "Grulla común (Grus grus)", "cientifico": "Grus_grus"},
    {"clase": "CL. AVES", "orden": "O. GRUIFORMES", "especie": "Focha común (Fulica atra)", "cientifico": "Fulica_atra"},
    {"clase": "CL. AVES", "orden": "O. PHOENICOPTERIFORMES", "especie": "Flamenco común (Phoenicopterus roseus)", "cientifico": "Phoenicopterus_roseus"},
    {"clase": "CL. AVES", "orden": "O. CHARADRIIFORMES", "especie": "Avefría europea (Vanellus vanellus)", "cientifico": "Vanellus_vanellus"},
    {"clase": "CL. AVES", "orden": "O. CHARADRIIFORMES", "especie": "Avoceta común (Recurvirostra avosetta)", "cientifico": "Recurvirostra_avosetta"},
    {"clase": "CL. AVES", "orden": "O. CHARADRIIFORMES", "especie": "Gaviota reidora (Chroicocephalus ridibundus)", "cientifico": "Chroicocephalus_ridibundus"},
    {"clase": "CL. AVES", "orden": "O. CHARADRIIFORMES", "especie": "Gaviota sombría (Larus fuscus)", "cientifico": "Larus_fuscus"},
    {"clase": "CL. AVES", "orden": "O. CHARADRIIFORMES", "especie": "Frailecillo atlántico (Fratercula arctica)", "cientifico": "Fratercula_arctica"},
    {"clase": "CL. AVES", "orden": "O. PODICIPEDIFORMES", "especie": "Somormujo lavanco (Podiceps cristatus)", "cientifico": "Podiceps_cristatus"},
    {"clase": "CL. AVES", "orden": "O. SPHENISCIFORMES", "especie": "Pingüino emperador (Aptenodytes forsteri)", "cientifico": "Aptenodytes_forsteri"},
    {"clase": "CL. AVES", "orden": "O. PELECANIFORMES", "especie": "Pelícano común (Pelecanus onocrotalus)", "cientifico": "Pelecanus_onocrotalus"},
    {"clase": "CL. AVES", "orden": "O. PELECANIFORMES", "especie": "Garza real (Ardea cinerea)", "cientifico": "Ardea_cinerea"},
    {"clase": "CL. AVES", "orden": "O. PELECANIFORMES", "especie": "Garceta común (Egretta garzetta)", "cientifico": "Egretta_garzetta"},
    {"clase": "CL. AVES", "orden": "O. PELECANIFORMES", "especie": "Espátula común (Platalea leucorodia)", "cientifico": "Platalea_leucorodia"},
    {"clase": "CL. AVES", "orden": "O. SULIFORMES", "especie": "Cormorán grande (Phalacrocorax carbo)", "cientifico": "Phalacrocorax_carbo"},
    {"clase": "CL. AVES", "orden": "O. CICONIIFORMES", "especie": "Cigüeña blanca (Ciconia ciconia)", "cientifico": "Ciconia_ciconia"},
    {"clase": "CL. AVES", "orden": "O. CICONIIFORMES", "especie": "Cigüeña negra (Ciconia nigra)", "cientifico": "Ciconia_nigra"},
    {"clase": "CL. AVES", "orden": "O. OPISTHOCOMIFORMES", "especie": "Hoacín (Opisthocomus hoazin)", "cientifico": "Opisthocomus_hoazin"},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Buitre leonado (Gyps fulvus)", "cientifico": "Gyps_fulvus"},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Buitre negro (Aegypius monachus)", "cientifico": "Aegypius_monachus"},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Quebrantahuesos (Gypaetus barbatus)", "cientifico": "Gypaetus_barbatus"},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Alimoche común (Neophron percnopterus)", "cientifico": "Neophron_percnopterus"},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Águila imperial ibérica (Aquila adalberti)", "cientifico": "Aquila_adalberti"},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Águila real (Aquila chrysaetos)", "cientifico": "Aquila_chrysaetos"},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Busardo ratonero (Buteo buteo)", "cientifico": "Buteo_buteo"},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Milano real (Milvus milvus)", "cientifico": "Milvus_milvus"},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Milano negro (Milvus migrans)", "cientifico": "Milvus_migrans"},
    {"clase": "CL. AVES", "orden": "O. ACCIPITRIFORMES", "especie": "Gavilán común (Accipiter nisus)", "cientifico": "Accipiter_nisus"},
    {"clase": "CL. AVES", "orden": "O. STRIGIFORMES", "especie": "Lechuza común (Tyto alba)", "cientifico": "Tyto_alba"},
    {"clase": "CL. AVES", "orden": "O. STRIGIFORMES", "especie": "Búho real (Bubo bubo)", "cientifico": "Bubo_bubo"},
    {"clase": "CL. AVES", "orden": "O. STRIGIFORMES", "especie": "Mochuelo europeo (Athene noctua)", "cientifico": "Athene_noctua"},
    {"clase": "CL. AVES", "orden": "O. STRIGIFORMES", "especie": "Cárabo común (Strix aluco)", "cientifico": "Strix_aluco"},
    {"clase": "CL. AVES", "orden": "O. BUCEROTIFORMES", "especie": "Abubilla común (Upupa epops)", "cientifico": "Upupa_epops"},
    {"clase": "CL. AVES", "orden": "O. CORACIIFORMES", "especie": "Abejaruco europeo (Merops apiaster)", "cientifico": "Merops_apiaster"},
    {"clase": "CL. AVES", "orden": "O. CORACIIFORMES", "especie": "Martín pescador común (Alcedo atthis)", "cientifico": "Alcedo_atthis"},
    {"clase": "CL. AVES", "orden": "O. PICIFORMES", "especie": "Pico picapinos (Dendrocopos major)", "cientifico": "Dendrocopos_major"},
    {"clase": "CL. AVES", "orden": "O. PICIFORMES", "especie": "Pito real ibérico (Picus sharpei)", "cientifico": "Picus_sharpei"},
    {"clase": "CL. AVES", "orden": "O. FALCONIFORMES", "especie": "Cernícalo (Falco tinnunculus)", "cientifico": "Falco_tinnunculus"},
    {"clase": "CL. AVES", "orden": "O. FALCONIFORMES", "especie": "Halcón peregrino (Falco peregrinus)", "cientifico": "Falco_peregrinus"},
    {"clase": "CL. AVES", "orden": "O. PSITTACIFORMES", "especie": "Cotorra argentina (Myiopsitta monachus)", "cientifico": "Myiopsitta_monachus"},
    {"clase": "CL. AVES", "orden": "O. PSITTACIFORMES", "especie": "Cotorra de Kramer (Psittacula krameri)", "cientifico": "Psittacula_krameri"},
    {"clase": "CL. AVES", "orden": "O. PSITTACIFORMES", "especie": "Loro gris (Psittacus erithacus)", "cientifico": "Psittacus_erithacus"},
    {"clase": "CL. AVES", "orden": "O. PSITTACIFORMES", "especie": "Guacamayo rojo (Ara macao)", "cientifico": "Ara_macao"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Alondra común (Alauda arvensis)", "cientifico": "Alauda_arvensis"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Lavandera blanca (Motacilla alba)", "cientifico": "Motacilla_alba"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Alcaudón real (Lanius meridionalis)", "cientifico": "Lanius_meridionalis"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Curruca capirotada (Sylvia atricapilla)", "cientifico": "Sylvia_atricapilla"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Mosquitero común (Phylloscopus collybita)", "cientifico": "Phylloscopus_collybita"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Tarabilla europea (Saxicola rubicola)", "cientifico": "Saxicola_rubicola"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Collalba rubia (Oenanthe hispanica)", "cientifico": "Oenanthe_hispanica"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Petirrojo europeo (Erithacus rubecula)", "cientifico": "Erithacus_rubecula"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Mirlo común (Turdus merula)", "cientifico": "Turdus_merula"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Carbonero común (Parus major)", "cientifico": "Parus_major"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Chochín paleártico (Troglodytes troglodytes)", "cientifico": "Troglodytes_troglodytes"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Pinzón vulgar (Fringilla coelebs)", "cientifico": "Fringilla_coelebs"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Jilguero europeo (Carduelis carduelis)", "cientifico": "Carduelis_carduelis"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Estornino negro (Sturnus unicolor)", "cientifico": "Sturnus_unicolor"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Gorrión común (Passer domesticus)", "cientifico": "Passer_domesticus"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Urraca común (Pica pica)", "cientifico": "Pica_pica"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Cuervo grande (Corvus corax)", "cientifico": "Corvus_corax"},
    {"clase": "CL. AVES", "orden": "O. PASSERIFORMES", "especie": "Rabilargo ibérico (Cyanopica cooki)", "cientifico": "Cyanopica_cooki"},
    {"clase": "CL. MAMMALIA", "orden": "O. MONOTREMATA", "especie": "Ornitorrinco (Ornithorhynchus anatinus)", "cientifico": "Ornithorhynchus_anatinus"},
    {"clase": "CL. MAMMALIA", "orden": "O. MONOTREMATA", "especie": "Equidna de hocico corto (Tachyglossus aculeatus)", "cientifico": "Tachyglossus_aculeatus"},
    {"clase": "CL. MAMMALIA", "orden": "O. DIDELPHIMORPHIA", "especie": "Zarigüeya (Didelphis marsupialis)", "cientifico": "Didelphis_marsupialis"},
    {"clase": "CL. MAMMALIA", "orden": "O. MICROBIOTHERIA", "especie": "Monito de monte (Dromiciops gliroides)", "cientifico": "Dromiciops_gliroides"},
    {"clase": "CL. MAMMALIA", "orden": "O. DASYUROMORPHIA", "especie": "Lobo marsupial (Thylacinus cynocephalus)", "cientifico": "Thylacinus_cynocephalus"},
    {"clase": "CL. MAMMALIA", "orden": "O. DASYUROMORPHIA", "especie": "Diablo de Tasmania (Sarcophilus harrisii)", "cientifico": "Sarcophilus_harrisii"},
    {"clase": "CL. MAMMALIA", "orden": "O. DIPROTODONTIA", "especie": "Koala (Phascolarctos cinereus)", "cientifico": "Phascolarctos_cinereus"},
    {"clase": "CL. MAMMALIA", "orden": "O. DIPROTODONTIA", "especie": "Petauro (Petaurus breviceps)", "cientifico": "Petaurus_breviceps"},
    {"clase": "CL. MAMMALIA", "orden": "O. DIPROTODONTIA", "especie": "Canguro Rojo (Macropus rufus)", "cientifico": "Macropus_rufus"},
    {"clase": "CL. MAMMALIA", "orden": "O. MACROSCELIDEA", "especie": "Musaraña elefante (Elephantulus rufescens)", "cientifico": "Elephantulus_rufescens"},
    {"clase": "CL. MAMMALIA", "orden": "O. TUBULIDENTATA", "especie": "Cerdo hormiguero (Orycteropus afer)", "cientifico": "Orycteropus_afer"},
    {"clase": "CL. MAMMALIA", "orden": "O. HYRACOIDEA", "especie": "Damán (Procavia capensis)", "cientifico": "Procavia_capensis"},
    {"clase": "CL. MAMMALIA", "orden": "O. PROBOSCIDEA", "especie": "Elefante africano (Loxodonta africana)", "cientifico": "Loxodonta_africana"},
    {"clase": "CL. MAMMALIA", "orden": "O. PROBOSCIDEA", "especie": "Elefante indio (Elephas maximus)", "cientifico": "Elephas_maximus"},
    {"clase": "CL. MAMMALIA", "orden": "O. SIRENIA", "especie": "Manatí (Trichechus manatus)", "cientifico": "Trichechus_manatus"},
    {"clase": "CL. MAMMALIA", "orden": "O. CINGULATA", "especie": "Armadillo (Dasypus novemcinctus)", "cientifico": "Dasypus_novemcinctus"},
    {"clase": "CL. MAMMALIA", "orden": "O. PILOSA", "especie": "Perezoso (Bradypus tridactylus)", "cientifico": "Bradypus_tridactylus"},
    {"clase": "CL. MAMMALIA", "orden": "O. PILOSA", "especie": "Oso hormiguero (Myrmecophaga tridactyla)", "cientifico": "Myrmecophaga_tridactyla"},
    {"clase": "CL. MAMMALIA", "orden": "O. DERMOPTERA", "especie": "Colugo (Cynocephalus volans)", "cientifico": "Cynocephalus_volans"},
    {"clase": "CL. MAMMALIA", "orden": "O. SCANDENTIA", "especie": "Tupaya (Tupaia tana)", "cientifico": "Tupaia_tana"},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Lémur de cola anillada (Lemur catta)", "cientifico": "Lemur_catta"},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Aye-aye (Daubentonia madagascariensis)", "cientifico": "Daubentonia_madagascariensis"},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Gálago (Galago senegalensis)", "cientifico": "Galago_senegalensis"},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Loris (Loris lydekkerianus)", "cientifico": "Loris_lydekkerianus"},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Tarsero (Tarsius tarsier)", "cientifico": "Tarsius_tarsier"},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Mono capuchino (Cebus capucinus)", "cientifico": "Cebus_capucinus"},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Mono aullador (Alouatta palliata)", "cientifico": "Alouatta_palliata"},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Macaco de Berbería (Macaca sylvanus)", "cientifico": "Macaca_sylvanus"},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Papión negro (Papio ursinus)", "cientifico": "Papio_ursinus"},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Mono patas (Erythrocebus patas)", "cientifico": "Erythrocebus_patas"},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Colobo (Colobus guereza)", "cientifico": "Colobus_guereza"},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Gibón (Hylobates lar)", "cientifico": "Hylobates_lar"},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Orangután de Sumatra (Pongo abelii)", "cientifico": "Pongo_abelii"},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Gorila de montaña (Gorilla beringei)", "cientifico": "Gorilla_beringei"},
    {"clase": "CL. MAMMALIA", "orden": "O. PRIMATES", "especie": "Chimpancé (Pan troglodytes)", "cientifico": "Pan_troglodytes"},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Rata parda (Rattus norvegicus)", "cientifico": "Rattus_norvegicus"},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Ratón de campo (Apodemus sylvaticus)", "cientifico": "Apodemus_sylvaticus"},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Topillo campesino (Microtus arvalis)", "cientifico": "Microtus_arvalis"},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Lirón careto (Eliomys quercinus)", "cientifico": "Eliomys_quercinus"},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Ardilla roja (Sciurus vulgaris)", "cientifico": "Sciurus_vulgaris"},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Castor europeo (Castor fiber)", "cientifico": "Castor_fiber"},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Marmota alpina (Marmota marmota)", "cientifico": "Marmota_marmota"},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Capibara (Hydrochoerus hydrochaeris)", "cientifico": "Hydrochoerus_hydrochaeris"},
    {"clase": "CL. MAMMALIA", "orden": "O. RODENTIA", "especie": "Mara (Dolichotis patagonum)", "cientifico": "Dolichotis_patagonum"},
    {"clase": "CL. MAMMALIA", "orden": "O. LAGOMORPHA", "especie": "Pica (Ochotona princeps)", "cientifico": "Ochotona_princeps"},
    {"clase": "CL. MAMMALIA", "orden": "O. LAGOMORPHA", "especie": "Conejo (Oryctolagus cuniculus)", "cientifico": "Oryctolagus_cuniculus"},
    {"clase": "CL. MAMMALIA", "orden": "O. LAGOMORPHA", "especie": "Liebre ibérica (Lepus granatensis)", "cientifico": "Lepus_granatensis"},
    {"clase": "CL. MAMMALIA", "orden": "O. EULIPOTYPHLA", "especie": "Erizo europeo (Erinaceus europaeus)", "cientifico": "Erinaceus_europaeus"},
    {"clase": "CL. MAMMALIA", "orden": "O. EULIPOTYPHLA", "especie": "Musaraña gris (Crocidura russula)", "cientifico": "Crocidura_russula"},
    {"clase": "CL. MAMMALIA", "orden": "O. EULIPOTYPHLA", "especie": "Desmán ibérico (Galemys pyrenaicus)", "cientifico": "Galemys_pyrenaicus"},
    {"clase": "CL. MAMMALIA", "orden": "O. EULIPOTYPHLA", "especie": "Topo europeo (Talpa europaea)", "cientifico": "Talpa_europaea"},
    {"clase": "CL. MAMMALIA", "orden": "O. CHIROPTERA", "especie": "Zorro volador (Pteropus conspicillatus)", "cientifico": "Pteropus_conspicillatus"},
    {"clase": "CL. MAMMALIA", "orden": "O. CHIROPTERA", "especie": "Murciélago enano (Pipistrellus pipistrellus)", "cientifico": "Pipistrellus_pipistrellus"},
    {"clase": "CL. MAMMALIA", "orden": "O. CHIROPTERA", "especie": "Murciélago grande de herradura (Rhinolophus ferrumequinum)", "cientifico": "Rhinolophus_ferrumequinum"},
    {"clase": "CL. MAMMALIA", "orden": "O. PHOLIDOTA", "especie": "Pangolín (Manis crassicaudata)", "cientifico": "Manis_crassicaudata"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Lince ibérico (Lynx pardinus)", "cientifico": "Lynx_pardinus"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Gato montés (Felis silvestris)", "cientifico": "Felis_silvestris"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "León (Panthera leo)", "cientifico": "Panthera_leo"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Leopardo (Panthera pardus)", "cientifico": "Panthera_pardus"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Jaguar (Panthera onca)", "cientifico": "Panthera_onca"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Puma (Puma concolor)", "cientifico": "Puma_concolor"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Guepardo (Acinonyx jubatus)", "cientifico": "Acinonyx_jubatus"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Gineta (Genetta genetta)", "cientifico": "Genetta_genetta"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Hiena manchada (Crocuta crocuta)", "cientifico": "Crocuta_crocuta"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Meloncillo (Herpestes ichneumon)", "cientifico": "Herpestes_ichneumon"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Lobo (Canis lupus)", "cientifico": "Canis_lupus"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Zorro (Vulpes vulpes)", "cientifico": "Vulpes_vulpes"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Lobo de crin (Chrysocyon brachyurus)", "cientifico": "Chrysocyon_brachyurus"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Licaón (Lycaon pictus)", "cientifico": "Lycaon_pictus"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Oso pardo (Ursus arctos)", "cientifico": "Ursus_arctos"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Oso panda (Ailuropoda melanoleuca)", "cientifico": "Ailuropoda_melanoleuca"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Foca común (Phoca vitulina)", "cientifico": "Phoca_vitulina"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Lobo marino (Otaria flavescens)", "cientifico": "Otaria_flavescens"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Mapache (Procyon lotor)", "cientifico": "Procyon_lotor"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Comadreja (Mustela nivalis)", "cientifico": "Mustela_nivalis"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Garduña (Martes foina)", "cientifico": "Martes_foina"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Nutria paleártica (Lutra lutra)", "cientifico": "Lutra_lutra"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Tejón (Meles meles)", "cientifico": "Meles_meles"},
    {"clase": "CL. MAMMALIA", "orden": "O. CARNIVORA", "especie": "Glotón (Gulo gulo)", "cientifico": "Gulo_gulo"},
    {"clase": "CL. MAMMALIA", "orden": "O. PERISSODACTYLA", "especie": "Onagro (Equus hemionus)", "cientifico": "Equus_hemionus"},
    {"clase": "CL. MAMMALIA", "orden": "O. PERISSODACTYLA", "especie": "Cebra común (Equus quagga)", "cientifico": "Equus_quagga"},
    {"clase": "CL. MAMMALIA", "orden": "O. PERISSODACTYLA", "especie": "Tapir de montaña (Tapirus pinchaque)", "cientifico": "Tapirus_pinchaque"},
    {"clase": "CL. MAMMALIA", "orden": "O. PERISSODACTYLA", "especie": "Rinoceronte indio (Rhinoceros unicornis)", "cientifico": "Rhinoceros_unicornis"},
    {"clase": "CL. MAMMALIA", "orden": "O. PERISSODACTYLA", "especie": "Rinoceronte negro (Diceros bicornis)", "cientifico": "Diceros_bicornis"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Guanaco (Lama guanicoe)", "cientifico": "Lama_guanicoe"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Camello (Camelus ferus)", "cientifico": "Camelus_ferus"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Jabalí (Sus scrofa)", "cientifico": "Sus_scrofa"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Hipopótamo (Hippopotamus amphibius)", "cientifico": "Hippopotamus_amphibius"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Ciervo (Cervus elaphus)", "cientifico": "Cervus_elaphus"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Gamo (Dama dama)", "cientifico": "Dama_dama"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Corzo (Capreolus capreolus)", "cientifico": "Capreolus_capreolus"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Reno (Rangifer tarandus)", "cientifico": "Rangifer_tarandus"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Alce euroasiático (Alces alces)", "cientifico": "Alces_alces"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Rebeco (Rupicapra pyrenaica)", "cientifico": "Rupicapra_pyrenaica"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Cabra montés (Capra pyrenaica)", "cientifico": "Capra_pyrenaica"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Muflón (Ovis gmelini)", "cientifico": "Ovis_gmelini"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Bisonte europeo (Bison bonasus)", "cientifico": "Bison_bonasus"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Gacela común (Gazella dorcas)", "cientifico": "Gazella_dorcas"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Saiga (Saiga tatarica)", "cientifico": "Saiga_tatarica"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Chirú (Pantholops hodgsonii)", "cientifico": "Pantholops_hodgsonii"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Búfalo africano (Syncerus caffer)", "cientifico": "Syncerus_caffer"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Nu azul (Connochaetes taurinus)", "cientifico": "Connochaetes_taurinus"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Berrendo (Antilocapra americana)", "cientifico": "Antilocapra_americana"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Jirafa (Giraffa camelopardalis)", "cientifico": "Giraffa_camelopardalis"},
    {"clase": "CL. MAMMALIA", "orden": "O. CETARTIODACTYLA", "especie": "Okapi (Okapia johnstoni)", "cientifico": "Okapia_johnstoni"},
    {"clase": "CL. MAMMALIA", "orden": "INFRAORDEN CETACEA", "especie": "Delfín listado (Stenella coeruleoalba)", "cientifico": "Stenella_coeruleoalba"},
    {"clase": "CL. MAMMALIA", "orden": "INFRAORDEN CETACEA", "especie": "Orca (Orcinus orca)", "cientifico": "Orcinus_orca"},
    {"clase": "CL. MAMMALIA", "orden": "INFRAORDEN CETACEA", "especie": "Cachalote (Physeter macrocephalus)", "cientifico": "Physeter_macrocephalus"},
    {"clase": "CL. MAMMALIA", "orden": "INFRAORDEN CETACEA", "especie": "Yubarta (Megaptera novaeangliae)", "cientifico": "Megaptera_novaeangliae"},
    {"clase": "CL. MAMMALIA", "orden": "INFRAORDEN CETACEA", "especie": "Ballena franca (Eubalaena glacialis)", "cientifico": "Eubalaena_glacialis"}
]

st.title("VISU ZOOLOGIA")
st.markdown("<div class='subtitle'>identificación de especies</div>", unsafe_allow_html=True)

def normalizar_texto(texto):
    """Elimina tildes, convierte a minúsculas y limpia espacios."""
    if not texto:
        return ""
    # Descompone los caracteres acentuados en carácter base + tilde y filtra la tilde (categoría Mn)
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

if 'sesion' not in st.session_state:
    cantidad_preguntas = min(10, len(DATOS_ESPECIES))
    st.session_state.sesion = random.sample(DATOS_ESPECIES, cantidad_preguntas)
    st.session_state.idx = 0
    st.session_state.aciertos = 0
    st.session_state.fallos = 0
    st.session_state.estado_respuesta = None
    st.session_state.temp_c = ""
    st.session_state.temp_o = ""
    st.session_state.temp_e = ""

if st.session_state.idx < len(st.session_state.sesion):
    actual = st.session_state.sesion[st.session_state.idx]

    if st.session_state.get("imagen_especie_actual") != actual["especie"]:
        st.session_state.imagen_especie_actual = actual["especie"]
        st.session_state.indice_imagen = 0

    fotos_pregunta = obtener_fotos(actual["especie"], max_fotos=2)

    st.markdown(
        f"<p class='pregunta-counter'>"
        f"Pregunta {st.session_state.idx + 1} de {len(st.session_state.sesion)}</p>",
        unsafe_allow_html=True
    )

    if fotos_pregunta:
        st.session_state.indice_imagen = min(
            st.session_state.indice_imagen, len(fotos_pregunta) - 1
        )
        
        col_izq, col_img, col_der = st.columns([0.6, 12, 0.6], vertical_alignment="center")
        
        with col_izq:
            if st.button("‹", key=f"foto_anterior_{st.session_state.idx}", type="tertiary",
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
            if st.button("›", key=f"foto_siguiente_{st.session_state.idx}", type="tertiary",
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

    if st.session_state.estado_respuesta is not None:
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

    if st.session_state.estado_respuesta == 'fallo':
        st.markdown(
            f"<div class='feedback-error'>¡OOPS! RESPUESTA INCORRECTA.<br>"
            f"solución: {actual['clase']} | {actual['orden']} | {actual['especie']}</div>",
            unsafe_allow_html=True
        )
    elif st.session_state.estado_respuesta == 'acierto':
        st.markdown(
            f"<div class='feedback-success'>¡RESPUESTA CORRECTA!<br>HAS IDENTIFICADO LA ESPECIE CORRECTAMENTE.</div>",
            unsafe_allow_html=True
        )

    if st.session_state.estado_respuesta is not None:
        _, centro_siguiente, _ = st.columns([1, 2, 1])
        with centro_siguiente:
            siguiente = st.button("Siguiente pregunta", use_container_width=True)
        if siguiente:
            st.session_state.estado_respuesta = None
            st.session_state.temp_c = ""
            st.session_state.temp_o = ""
            st.session_state.temp_e = ""
            st.session_state.idx += 1
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
                st.session_state.aciertos += 1
                st.session_state.estado_respuesta = 'acierto'
            else:
                st.session_state.fallos += 1
                st.session_state.estado_respuesta = 'fallo'
            st.rerun()
else:
    total_preguntas = len(st.session_state.sesion)
    aciertos = st.session_state.aciertos
    fallos = st.session_state.fallos

    nota = round((aciertos / total_preguntas) * 10, 1) if total_preguntas > 0 else 0

    st.subheader("Resultados del Test Visu")
    st.write(f"Aciertos totales: {aciertos}")
    st.write(f"Fallos totales: {fallos}")
    st.markdown(f"### Puntuación Final: {nota} / 10")

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
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()