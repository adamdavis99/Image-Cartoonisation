import cv2
import numpy as np
import streamlit as st
from PIL import Image

def pencilsketch(img):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    value=st.sidebar.slider('Tune Brightness of your sketch',0.0,300.0,250.0)
    kernel=st.sidebar.slider('Tune boldness of edges of image',1,99,25,step=2)
    gray_blur=cv2.GaussianBlur(gray,(kernel,kernel),0)
    cartoon=cv2.divide(gray,gray_blur,scale=value)
    return cartoon

def penciledge(img):
    kernel=st.sidebar.slider('Sharpness of sketch',1,99,25,step=2)
    laplacian_filter=st.sidebar.slider('Edge detection power',3,9,3,step=2)
    noise_reduction=st.sidebar.slider('Noise effects',10,255,150)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray=cv2.medianBlur(gray,kernel)
    edges=cv2.Laplacian(gray,-1,ksize=laplacian_filter)
    edges_inv=255-edges
    dummy,cartoon=cv2.threshold(edges_inv,noise_reduction,255,cv2.THRESH_BINARY)
    return cartoon


def detailenhance(img):
    smooth=st.sidebar.slider('Smoothness',3,99,5,step=2)
    kernel=st.sidebar.slider('Sharpness',1,40,3,step=2)
    edge_preserve=st.sidebar.slider('Tune Color Averaging effects',0.0,1.0,0.05)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray=cv2.medianBlur(gray,kernel)
    edges=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)
    color=cv2.detailEnhance(img,sigma_s=smooth,sigma_r=edge_preserve)
    cartoon=cv2.bitwise_and(color,color,mask=edges)
    return color

def bilateral(img):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    smooth=st.sidebar.slider('Smoothness',3,99,5,step=2)
    kernel=st.sidebar.slider('Sharpness',1,21,3,step=2)
    edge_preserve=st.sidebar.slider('Tune Color Averaging effects',1,100,50)
    gray=cv2.medianBlur(gray,kernel)
    edges=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)
    color=cv2.bilateralFilter(img,smooth,edge_preserve,smooth)
    cartoon=cv2.bitwise_and(color,color,mask=edges)
    return color


st.title("Basic Image Editor")
#st.write(""" # Cartoonize Your Image! """)
file=st.sidebar.file_uploader("Upload an Image file",type=["jpg","png"])
if(file is None):
    st.write("Oops! You haven't uploaded any image file")
else:
    img=Image.open(file)
    img=np.array(img)
    option=st.sidebar.selectbox('Select the filters you wish to apply',('Pencil sketch','Pencil edge','Detail Enhance','Bilateral Filter'))
    st.text("Your Original Image")
    st.image(img,use_column_width=True)
    if(option=='Pencil sketch'):
        st.text("Your pencil sketch")
        cartoon=pencilsketch(img)
        st.image(cartoon,use_column_width=True)
    elif(option=='Pencil edge'):
        st.text('Your sketch')
        cartoon=penciledge(img)
        st.image(cartoon,use_column_width=True)
    elif(option=='Detail Enhance'):
        st.text('Your sketch')
        cartoon=detailenhance(img)
        st.image(cartoon,use_column_width=True)
    elif(option=='Bilateral Filter'):
        st.text('Your sketch')
        cartoon=bilateral(img)
        st.image(cartoon,use_column_width=True)

        

    

