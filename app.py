import streamlit as st
from PIL import Image
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.firecrawl import FirecrawlTools
import google.generativeai as genai
from google.generativeai import upload_file,get_file
import io
import base64

import time
from pathlib import Path
import tempfile

from dotenv import load_dotenv
load_dotenv()

import os

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Page Configuration

st.set_page_config(
    page_title="AI Shopping Partner",
    page_icon="🤖🛍️",
    layout="centered"
)

st.title("AI Shopping Partner")
st.header("Powered by Agno and Google Gemini")
#st.cache_resource

def get_gemini_response(api_key,prompt,image):   
    model=genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
    response= model.generate_content([prompt,image])
    return response.text

def initialize_agent():
    return Agent(

        name="Shopping Partner",
        model=Gemini(id="gemini-2.0-flash-exp"),  
        instructions=[
            "You are a product recommender agent specializing in finding products that match user preferences.",
            "Prioritize finding products that satisfy as many user requirements as possible, but ensure a minimum match of 50%.",
            "Search for products only from authentic and trusted e-commerce websites such as Google Shopping, Amazon, Flipkart, Myntra, Meesho, Nike, and other reputable platforms.",
            "Verify that each product recommendation is in stock and available for purchase.",
            "Avoid suggesting counterfeit or unverified products.",
            "Clearly mention the key attributes of each product (e.g., price, brand, features) in the response.",
            "Format the recommendations neatly and ensure clarity for ease of user understanding.",
        ],
        tools=[FirecrawlTools()],
        markdown=True
        )

#Initialize the Agent
multimodal_Agent = initialize_agent()

# Define acceptable file types and MIME types
accepted_mime_types = ["image/jpeg", "image/png"]

#File Uploader
image_file = st.file_uploader("Upload a image File to Analyse and provide relevant shopping links",type=["jpg","jpeg","png"],help="Upload max 200mb image for AI Analysis")
image= None

#Prompt
prompt= "What is in this photo?"



if image_file is not None:
    # Convert the uploaded file into a BytesIO stream
    #image_stream = io.BytesIO(image_file.read())
    image = Image.open(image_file)
    
    try:
        # Open the image using PIL
        #image = Image.open(image_stream)  

        # Display the image in Streamlit
        st.image(image, caption="Uploaded Image", use_container_width=False,width=400)
        with st.spinner("AI is processing this image and gathering insights..."):
            response= get_gemini_response(API_KEY,prompt,image)
            st.write(f"Product Identified using AI: {response}")

    except Exception as e:
        st.error(f"Error: Unable to open image. {e}")

    # Specify the mime_type if Streamlit cannot auto-detect
    #mime_type = image_file.type

    #if mime_type:
        #st.write(f"File MIME type detected: {mime_type}")
        # Proceed with file processing
    #else:
        #st.error("Could not determine MIME type for the uploaded file. Please upload a valid file.")

    #if mime_type in accepted_mime_types:
        #st.write(f"File uploaded: {image_file.name}")
        # Process the file as needed
    #else:
        #st.error(f"Unsupported file type: {mime_type}")



    #prompt= st.text_input("Input prompt(e.g., 'What is in this photo?'):",key="input")
    promptColor= st.text_input("'What Color you are looking for?'",key="inputcolor")
    promptPurpose= st.text_input("'For what purpose you are looking for this product?'",key="inputpurpose")
    promptBudget= st.text_input("'What is your budget?'",key="inputbudget")
    
    

    user_query= st.text_area("What specific insights are you looking for from the image?",                 
                 placeholder="Ask any questions related to the image content. The AI agent will analyze and gather more context if necessary",
                 help="Share the specific questions or details you want to explore from the image."
                 )
    
    if st.button("Search this Product",key="analyse_image_button"):
        if not user_query:
            st.warning("Please enter a query to analyse this image")
        else:
            try:
                with st.spinner("AI is Processing this image and gathering insights..."):

                    #Upload and process the video file
                    #processed_image = upload_file(image_path)                                      
                    #st.write(f"processed_image: {processed_image}")

                    response= get_gemini_response(API_KEY,prompt,image)
                    #st.write(f"Product Identified: {response}")

                    

                    #Prompt generation for Analysis
                    analysis_prompt =(
                        f"""
                        I am looking for 
                        {response}
                        with the below preferences: 
                        {promptColor} 
                        {promptPurpose}
                        {promptBudget}
                        Can you provide recommendations. Always make sure that you provide hyperlinks to the product.
                        {user_query}
                        """
                )

                    #AI Agent Processing
                    response = multimodal_Agent.run(analysis_prompt,image=image)

                    # multimodal_Agent.print_response(
                    # "I am looking for running shoes with the following preferences: Color: Black Purpose: Comfortable for long-distance running Budget: Under Rs. 10,000. Can you provide recommendations. Also provide links to the product. Search in Myntra"
                    # )

                #Display the result
                st.subheader("Relevant search links for the product")
                st.markdown(response.content)
                #st.write(response)

            except Exception as error:
                st.error(f"An error occured during analysis:{error}")
            finally:
                #Clean up temporary video file
                # Path(image_path).unlink(missing_ok=True)
                st.info("Clean up temporary image file")
    #else:
        #st.info("Upload a image file to start the Analysis")
    
        #Customize text area height
    st.markdown(
        """
        <style>
        .stTextArea textarea{
            height:100px;   
        }
        </style>
        """,
        unsafe_allow_html=True

    )