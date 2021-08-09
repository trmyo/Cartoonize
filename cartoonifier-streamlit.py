import numpy as np
import streamlit as st
from cv2 import *
from PIL import Image

#Fxn....to convert filename to BytesIO in streamlit to display
@st.cache
def load_image(image_file):
	img = Image.open(image_file)
	return img

# main Function
def main():
    st.subheader("Upload Image File to get Cartoon image")
    # to upload the image file...Streamlit funtion
    image_file = st.file_uploader("Upload Image",type=['png','jpeg','jpg'])
    # if no file uploaded yet...it will show this message
    if image_file is None:
        st.write("Please upload the image")
    # if image is uploaded
    else:
        st.write("Picture uploaded successfully")
        # to convert to streamlit BytesIO type using previuous defined load_image function
        img=load_image(image_file)
        # to cartoonize the photo using cartoonify function whicu is defined below
        cartoon=cartoonify(image_file)
        # to display both original image and cartoon image
        col1,col2=st.beta_columns(2)
        col1.image(img,caption=["Original Photo"])
        col2.image(cartoon,caption=["Cartoon Photo"])

# Cartoonify function
def cartoonify(image_file):
    if image_file is None:
        st.write("Please upload the image")
    else:

        # read the image to convert to nparray....img_array will be in array format
        originalimage = Image.open(image_file)
        img_array = np.array(originalimage)

        originalimage = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        # resize the image
        ReSized1 = cv2.resize(originalimage, (600, 600))
        #converting an image to grayscale
        grayScaleImage= cv2.cvtColor(originalimage, cv2.COLOR_BGR2GRAY)
        ReSized2 = cv2.resize(grayScaleImage, (600, 600))
        #applying median blur to smoothen an image
        smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
        ReSized3 = cv2.resize(smoothGrayScale, (600, 600))
        #retrieving the edges for cartoon effect
        #by using thresholding technique
        getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 9, 9)
        ReSized4 = cv2.resize(getEdge, (600, 600))
        #applying bilateral filter to remove noise and keep edge sharp as required
        colorImage = cv2.bilateralFilter(originalimage, 9, 300, 300)
        ReSized5 = cv2.resize(colorImage, (600, 600))
        #masking edged image with our "BEAUTIFY" image
        cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
        ReSized6 = cv2.resize(cartoonImage, (600, 600))
        # converting from nparray to BYTESIO for streamlit as streamlit accespts only BYTESIO
        bytes = Image.fromarray(ReSized4)
        # plotting the whole transition
        #images=[ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]
        return bytes


if __name__ == '__main__':
	main()
