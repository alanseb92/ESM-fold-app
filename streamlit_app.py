import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio
import biotite.structure.io.pdb as pdb
import tempfile

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

            # Use a temporary file to save the PDB content
            with tempfile.NamedTemporaryFile(suffix=".pdb", delete=False) as temp_pdb:
                temp_pdb.write(pdb_string.encode())
                temp_pdb.flush()  # Ensure the content is written

                # Load the structure using Biotite
                struct = pdb.PDBFile.read(temp_pdb.name).get_structure()

            # Calculate the mean b-factor (plDDT)
            b_factors = struct.b_factor
            if b_factors is not None:
                b_value = round(b_factors.mean(), 4)
            else:
                b_value = 'N/A'

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
    except ValueError as e:
        st.error(f'File format error: {e}')
    except AttributeError as e:
        st.error(f'Attribute error: {e}')

# Prediction button
if st.sidebar.button('Predict'):
    update(txt)
else:
    st.warning('👈📑🧪 Enter protein sequence data to make a prediction')
