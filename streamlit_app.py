
import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio

# Configurar el ancho completo de la página
st.set_page_config(layout='wide')

# Título y descripción en la barra lateral
st.sidebar.title('🧪 🧫🧑‍🔬 ESMFold')
st.sidebar.write('[*ESMFold*](https://esmatlas.com/about) es un predictor de estructuras proteicas basado en la secuencia única usando el modelo de lenguaje ESM-2. Para más información, lee el [artículo de investigación](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v2) y el [artículo de noticias](https://www.nature.com/articles/d41586-022-03539-1) publicado en *Nature*.')

# Función para renderizar la estructura proteica
def render_mol(pdb):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb, 'pdb')
    pdbview.setStyle({'cartoon': {'color': 'spectrum'}})
    pdbview.setBackgroundColor('white')
    pdbview.zoomTo()
    pdbview.zoom(2, 800)
    pdbview.spin(True)
    showmol(pdbview, height=500, width=800)

# Entrada de la secuencia proteica
DEFAULT_SEQ = "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTARQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGSLISAANNPSLKAAAPQAPWDSSTNFSSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCANSGNSNQALIGKKGVAWMKRFMDNDTRYSTFACENPNSTRVSDFRTANCSLEDPAANKARKEAELAAATAEQ"
txt = st.sidebar.text_area('Secuencia proteica', DEFAULT_SEQ, height=275)

# Función de actualización (ESMFold)
def update(sequence):
    try:
        with st.spinner('🔄 Procesando predicción, por favor espera...'):
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence, verify=False)
            response.raise_for_status()  # Para manejar errores HTTP
            pdb_string = response.content.decode('utf-8')

            struct = bsio.load_structure(pdb_string, extra_fields=["b_factor"])
            b_value = round(struct.b_factor.mean(), 4)

            # Mostrar la estructura predicha
            st.subheader('Visualización de la estructura proteica predicha')
            render_mol(pdb_string)

            # Mostrar el valor de plDDT
            st.subheader('plDDT')
            st.write('plDDT es una estimación por residuo de la confianza en la predicción en una escala de 0 a 100.')
            st.info(f'plDDT: {b_value}')

            # Botón para descargar el archivo PDB
            st.download_button(
                label="Descargar PDB",
                data=pdb_string,
                file_name='predicted.pdb',
                mime='text/plain',
            )
    except requests.exceptions.RequestException as e:
        st.error(f'Error en la predicción: {e}')

# Botón de predicción
if st.sidebar.button('Predecir'):
    update(txt)
else:
    st.warning('📚📑🧪 Ingresa una secuencia proteica para realizar la predicción')


