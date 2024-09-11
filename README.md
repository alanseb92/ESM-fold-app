# **ESMFold Protein Structure Prediction App**

 **DEMO APP** https://esm-fold-app.streamlit.app/

This project is a **Streamlit-based web application** that predicts the 3D structure of proteins using the **ESMFold model**, which is built on top of the **ESM-2 language model** developed by Meta AI. The app allows users to input a protein sequence and retrieve a predicted 3D structure in PDB format, along with the plDDT confidence score.

## **Table of Contents**
1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Features](#features)
5. [License](#license)
6. [Acknowledgements](#acknowledgements)
7. [References](#references)

---

## **Overview**
The **ESMFold Protein Structure Prediction App** provides an accessible interface for single-sequence protein structure prediction. Users can input protein sequences, visualize the predicted 3D structure interactively, and download the results in **PDB format**. Additionally, the app computes the **plDDT** confidence score, which represents the per-residue confidence in the predicted structure.

**ESMFold** is an end-to-end deep learning model for protein structure prediction that leverages large-scale language models trained on protein sequences. This application serves as an interface to access ESMFold predictions via API.

### **Key Features:**
- **Protein sequence input**: Accepts amino acid sequences in standard one-letter code.
- **3D Visualization**: Provides an interactive 3D visualization of the predicted protein structure using `py3Dmol`.
- **plDDT Confidence Score**: Displays the confidence score of the predicted structure based on the ESMFold output.
- **Downloadable PDB**: Allows users to download the predicted structure as a PDB file.

## **Installation**

### **Prerequisites**
- Python 3.8 or higher
- Required Python packages:
  - `streamlit`
  - `stmol`
  - `py3Dmol`
  - `requests`
  - `biotite`

To install the required dependencies, run:
```bash
pip install streamlit stmol py3Dmol requests biotite
```

### **Running the App**
To run the application locally:
```bash
streamlit run streamlit_app.py
```

This will start a local web server where you can access the app through your web browser at `http://localhost:8501`.

## **Usage**

1. **Input Sequence**: Enter a valid protein sequence in one-letter amino acid code (e.g., "MGSSHHHHHHSSGLVPRGSH...") into the text area in the app's sidebar.
2. **Predict**: Click on the "Predict" button to generate the protein structure prediction.
3. **Visualization**: The predicted protein structure will be displayed in a 3D interactive viewer. The visualization is based on the predicted PDB structure.
4. **plDDT Score**: The app will calculate and display the plDDT confidence score, which ranges from 0 to 100, indicating the reliability of the prediction.
5. **Download PDB**: The predicted protein structure can be downloaded in PDB format by clicking the "Download PDB" button.

## **Features**

### **1. 3D Protein Structure Visualization**
The app uses **py3Dmol** to render the 3D structure of the predicted protein in real-time. The structure is shown with a cartoon representation and a color spectrum to indicate different regions of the protein.

### **2. plDDT Score**
The **plDDT score** is a confidence measure for the predicted protein structure. It is displayed on a scale of 0 to 100, where higher values indicate more confident predictions.

### **3. PDB Download**
The predicted structure is available for download in the **PDB (Protein Data Bank)** format, enabling users to further analyze the structure or use it in other molecular modeling applications.

## **License**
This project is distributed under the MIT License. See the `LICENSE` file for more details.

## **Acknowledgements**
This application leverages the **ESMFold** model developed by Meta AI, and the **py3Dmol** library for molecular visualization. We also acknowledge the use of **Streamlit** for the rapid development of this web-based interface.

## **References**

1. Meta AI, **ESMFold**: End-to-End Protein Structure Prediction Using ESM-2. [Website](https://esmatlas.com/about).
2. Lin, Z., Akin, H., Rao, R., et al. **Evolutionary-scale prediction of atomic-level protein structure with a language model**. *bioRxiv* (2022). [Link](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v2).
3. Nature Article on ESMFold: [Link](https://www.nature.com/articles/d41586-022-03539-1).
