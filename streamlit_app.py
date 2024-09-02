
import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio

# Set full-width layout
st.set_page_config(layout='wide')

# Sidebar title and description
st.sidebar.title('🧪 🧫🧑‍🔬 ESMFold')
st.sidebar.write('[*ESMFold*](https://esmatlas.com/about) is an end-to-end single sequence protein structure predictor based on the ESM-2 language model. For more information, read the [research article](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v2) and the [news article](https://www.nature.com/articles/d41586-022-03539-1) published in *Nature*.')

# Function to render the protein structure
def render_mol(pdb):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb, 'pdb')
    pdbview.setStyle({'cartoon': {'color': 'spectrum'}})
    pdbview.setBackgroundColor('white')
    pdbview.zoomTo()
    pdbview.zoom(2, 800)
    pdbview.spin(True)
    showmol(pdbview, height=500, width=800)

# Protein sequence input
DEFAULT_SEQ = "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTARQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGSLISAANNPSLKAAAPQAPWDSSTNFSSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCANSGNSNQALIGKKGVAWMKRFMDNDTRYSTFACENPNSTRVSDFRTANCSLEDPAANKARKEAELAAATAEQ"
txt = st.sidebar.text_area('Protein sequence', DEFAULT_SEQ, height=275)

# ESMFold update function
def update(sequence):
    try:
        with st.spinner('🔄 Processing prediction, please wait...'):
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence, verify=False)
            response.raise_for_status()  # To handle HTTP errors
            pdb_string = response.content.decode('utf-8')

            struct = bsio.load_structure(pdb_string, extra_fields=["b_factor"])
            b_value = round(struct.b_factor.mean(), 4)

            # Display the predicted structure
            st.subheader('Visualization of predicted protein structure')
            render_mol(pdb_string)

            # Display plDDT value
            st.subheader('plDDT')
            st.write('plDDT is a per-residue estimate of the confidence in prediction on a scale from 0 to 100.')
            st.info(f'plDDT: {b_value}')

            # Button to download the PDB file
            st.download_button(
                label="Download PDB",
                data=pdb_string,
                file_name='predicted.pdb',
                mime='text/plain',
            )
    except requests.exceptions.RequestException as e:
        st.error(f'Prediction error: {e}')

# Prediction button
if st.sidebar.button('Predict'):
    update(txt)
else:
    st.warning('📚📑🧪 Enter protein sequence data to make a prediction')


