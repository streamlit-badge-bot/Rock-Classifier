from fastai.vision import open_image, load_learner, image, torch
import streamlit as st
import numpy as np
import matplotlib.image as mpimg
import os
import time
import PIL.Image
import requests
from io import BytesIO


#App title
st.title("Rock Classifier")


#loads model and makes prediction
def predict(img, display_img):

    # Display the test image
    st.image(display_img, use_column_width=True)

    # Temporarily displays a message while executing 
    with st.spinner('Wait for it...'):
        time.sleep(3)

    # Load model and make prediction
    model  = load_learner('/home/cate/Cate/DSI/Rock-Classifier/model/', 'stage-1.pkl')
    pred_class = model.predict(img)[0] # get the predicted class
    pred_prob = round(torch.max(model.predict(img)[2]).item()*100) # get the max probability
    
    # Display the prediction
    if str(pred_class) == 'chip':
        st.success("This is in class chip with the probability of " + str(pred_prob) + '%.')
    elif str(pred_class) == 'fines':
        st.success("This is in class fines with the probability of " + str(pred_prob) + '%.')
    elif str(pred_class) == 'lump':
        st.success("This is in class lump with the probability of " + str(pred_prob) + '%.')
    elif str(pred_class) == 'mixed':
        st.success("This is in class mixed with the probability of " + str(pred_prob) + '%.')
    else:
        st.success("This is in class pellets with the probability of " + str(pred_prob) + '%.')

option = st.radio('', ['Choose a test image', 'Choose your own image'])

if option == 'Choose a test image':
            
    # Test image selection
    test_images = os.listdir('/home/cate/Cate/DSI/Rock-Classifier/samp/')
    test_image = st.selectbox(
        'Please select a test image:', test_images)
    
    # Read the image
    file_path = '/home/cate/Cate/DSI/Rock-Classifier/samp/' + test_image
    img = open_image(file_path)
    
    # Get the image to display
    display_img = mpimg.imread(file_path)
    
    # Predict and display the image
    predict(img, display_img)

else:
    url = st.text_input("Please input a url:")
    if url != "":
        try:
            # Read image from the url
            response = requests.get(url)
            pil_img = PIL.Image.open(BytesIO(response.content))
            display_img = np.asarray(pil_img) # Image to display
        
            # Transform the image to feed into the model
            img = pil_img.convert('RGB')
            img = image.pil2tensor(img, np.float32).div_(255)
            img = image.Image(img)
        
            # Predict and display the image
            predict(img, display_img)
        
        except:
            st.text("Invalid url!")
