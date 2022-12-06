# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 09:42:03 2022

@author: shahmohammadim
"""
conda install -c conda-forge faiss-cpu

#import pandas as pd
from scipy.spatial.distance import cdist
#import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
#import streamlit as st

st.title('Occupation Similarity Check')

######## Part 1: Kwaliteit ######
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    
#SBB_Data = pd.read_csv(r'C:/Users/shahmohammadim/OneDrive - TNO/Healthy Living/SBB Similarity/SBB.csv', decimal=",", encoding = "ANSI")
    SBB_Data = pd.read_csv(uploaded_file,decimal=",", encoding = "ANSI")
    
    SBB_Data.Kwalificatiecode = SBB_Data.Kwalificatiecode.astype(str)
    #SBB_Data.dtypes
    
    SBB_Data_Quality = SBB_Data[(SBB_Data["Soort skill"] == 'Kwaliteit')]
    
    
    
    
    #Profession = "25559"
        
    SBB_Data_Quality_Selected = SBB_Data_Quality[['ISCO1',
     'ISCO2',
     'ISCO3',
     'ISCO4',
     'ISCO5',
     'Kwalificatiecode',
     'Kwalificatienaam',
     'skill',
     'Soort skill',
     'Skillscode (type en oorsprong)',
     'Percentage kwaliteit']].reset_index(drop=True)
    
    
    SBB_Data_Quality_Wide = pd.pivot_table(SBB_Data_Quality_Selected,index=['Kwalificatiecode','Kwalificatienaam'], columns='skill', values='Percentage kwaliteit').reset_index() ### make data wide format
    
    SBB_Data_Quality_Wide= SBB_Data_Quality_Wide.replace(np.nan,0)  ### Replace NAs with 0s
     
    SBB_Data4Cosine = SBB_Data_Quality_Wide.iloc[:,2:]
    
    #########
    ## %% Cosine Distance ####### 
    #########
    
    Distance_Cosine = cdist(SBB_Data4Cosine,SBB_Data4Cosine, 'cos')
    Distance_Cosine_df = pd.DataFrame(Distance_Cosine).reset_index()
    
    Distance_Cosine_df.insert(1, "Code", SBB_Data_Quality_Wide.reset_index()["Kwalificatiecode"])
    #Distance_Cosine_df.insert(1, "Name", SBB_Data_Quality_Wide.reset_index()["Kwalificatienaam"])
    
    Distance_Cosine_df = Distance_Cosine_df.drop(columns = "index")
    
    Title = pd.Series(["Title"])
    
    Coln = Title.append(SBB_Data_Quality_Wide["Kwalificatiecode"])
    
    Distance_Cosine_df.columns = Coln
    Distance_Cosine_df.insert(1, "Name", SBB_Data_Quality_Wide.reset_index()["Kwalificatienaam"])
    
    ### Choose an occupation
    Profession = st.sidebar.selectbox(
        'Select a Profession',
         Distance_Cosine_df['Title'])
    
    'You selected: ', Profession
    
    
    
    Distance_Cosine_df_sorted = Distance_Cosine_df.sort_values(by=Profession)
    
    
    ######## Part 2: Beroepsvaardigheid
    # Similarity using tasks : Faiss model
    #########
    
    Beroepsvaardigheid = SBB_Data[(SBB_Data["Soort skill"] == 'Beroepsvaardigheid')]
    
    
    Task_statements_grouped= Beroepsvaardigheid.groupby(['Kwalificatiecode','Kwalificatienaam'])['ESCO Naam laag 3'].apply(','.join).reset_index()
    
    Task_statements_grouped['Kwalificatiecode'] = Task_statements_grouped['Kwalificatiecode'].astype(str)
    
    #sentences = Task_statements_grouped['skill'].tolist()
    sentences = Task_statements_grouped['ESCO Naam laag 3'].tolist()
    
    
    # initialize sentence transformer model
    
    #### check all pre-trained models here: https://www.sbert.net/docs/pretrained_models.html
    
    model = SentenceTransformer('distiluse-base-multilingual-cased-v1')  #### This model works for Dutch
     
    # create sentence embeddings
    sentence_embeddings = model.encode(sentences)
    sentence_embeddings.shape
    
    #### Vector Dimension
    d = sentence_embeddings.shape[1]
    
    
    index = faiss.IndexFlatL2(d)
    #index.is_trained
    
    faiss.normalize_L2(sentence_embeddings)
    
    
    index.add(sentence_embeddings)
    
    
    
    
    ESCO_Index = Task_statements_grouped[Task_statements_grouped['Kwalificatiecode'] == Profession].index[0]
    
    Tasks = sentences[ESCO_Index]
    
    ##### Select the number of similar jobs
    k = len(sentences)
    
    ### Query
    xq = model.encode(Tasks)[np.newaxis]
    faiss.normalize_L2(xq)
    
    D, I = index.search(xq, k)  # search
    
    Similar_professions_index = I.tolist()
    
    sentences_df = pd.DataFrame(sentences)
    
    Similar_Professions_Tasks= sentences_df[0].iloc[Similar_professions_index[0]]
    
    Similar_Professions = Task_statements_grouped.iloc[Similar_professions_index[0]].rename({'Title': 'Task_Based'}, axis=1)
    
    
    
    Compare_all = pd.concat([Distance_Cosine_df_sorted.iloc[:,1].reset_index(drop=True), Similar_Professions.iloc[:,1].reset_index(drop=True)], sort=False, axis=1)
    Compare_all.columns = ["Kwaliteit","Beroepsvaardigheid"]
    
    st.subheader('List of Occupations')
    st.dataframe(Task_statements_grouped)
        
    st.subheader('Comparing Similarities using "Kwaliteit" and "Beroepsvaardigheid"')
    st.table(Compare_all)
    
        
