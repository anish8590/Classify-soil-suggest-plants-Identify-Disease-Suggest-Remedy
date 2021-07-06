import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from PIL import Image
import base64
import sys

classes = {0:"Alluvial",1:"Black",2:"Clay",3:"Red"}

suggestions = {"Alluvial": "Tomatoes, Sage, Roses, Butterfly bush, Ferns, Daffodils, Lavender", "Black" : "Citrus fruits, Sunflower, Legumes, Microgreens, Peppers",
"Clay" : "Kale, Lettuce, Broccoli, Cabbage, Aster, Daylily, Magnolia, Juniper, Pine, Geranium, Ivy", "Red" : "Peanuts, Grams, Potatoes, Sweet potato, Banana, Papaya"}

sys.setrecursionlimit(10000)

healthType=['Scab',
 'Rot',
 'Rust',
 'Healthy',
 'Healthy',
 'Powdery mildew',
 'Healthy',
 'Leaf spot',
 'Common_rust',
 'Northern Leaf Blight',
 'Healthy',
 'Black rot',
 'Black Measles',
 'Leaf blight',
 'Healthy',
 'Citrus greening',
 'Bacterial spot',
 'Healthy',
 'Bacterial spot',
 'Healthy',
 'Early blight',
 'Late blight',
 'Healthy',
 'Healthy',
 'Healthy',
 'Powdery mildew',
 'Leaf_scorch',
 'healthy',
 'Bacterial spot',
 'Early blight',
 'Late blight',
 'Leaf Mold',
 'Leaf spot',
 'Spider mite',
 'Target Spot',
 'Yellow Leaf',
 'Mosaic virus',
 'Healthy']
recomendations= {
"Scab":"Regularly applying a warm chamomile compress can help to make a scab go away faster by keeping it moist.",
 "Rot":"Start to treat root rot by removing the plant from the soil and washing the roots under running water. ",
 "Rust":"use products like copper sprays.",
 "Powdery mildew":"mix 1 tablespoon of baking soda, 1/2 teaspoon of liquid dish soap, and 1 gallon of water. Spray the mixture on your plants.",
 "Common_rust":"Water in the early morning hours — avoiding overhead sprinklers — to give plants time to dry out during the day.",
 "Northern Leaf Blight":"Mix a 50:50 milk to water solution in a spray bottle and apply to leaves of plants.",
 "Black rot":"Weed regularly to improve air circulation and light access around all plants affected by black rot.",
 "Black Measles":"Water the ground near the roots instead of soaking the bush with a spray from above.",
 "Leaf blight":" Neem oil is an excellent treatment, but increasing air circulation around your plant by pruning can be equally effective.",
 "Citrus greening":"Bactericides are a topical treatment aimed at slowing the bacteria that cause citrus greening.",
 "Powdery mildew":"The acetic acid in apple cider vinegar is very effective in killing powdery mildew.",
 "Leaf_scorch":"provide an injection containing oxytetracyclen, an antibiotic used in treating leaf scorch.",
 "Bacterial spot":"Remove affected parts of the plant and toss them.",
 "Early blight":"Baking soda has fungicidal properties that can stop or reduce the spread of early blight.",
 "Late blight":"Baking soda has fungicidal properties that can stop or reduce the spread of late blight.",
 "Leaf Mold":"Mix one to one and a half tablespoons of apple cider vinegar with 1/2 a gallon (2 l) of water and Spray it.",
 "Leaf spot":"Water in the early morning so the sun has time to dry plants before night.",
 "Spider mite":"Neem oil is an effective way to get rid of spider mites on plants.",
 "Target Spot":"Remove old plant debris at the end of the growing season",
 "Yellow Leaf":"Use a liquid plant fertilizer enriched with micronutrients , such as iron and magnesium, every two weeks until the yellowing disappears, and then fertilize every month.",
 "Mosaic virus":"There is no known cure for the hemp mosaic virus or other tobamoviruses. Once a plant has become infected with the virus the host will never be free from infection.",}



datapath = "snapshot/"


def main():

    page = st.sidebar.selectbox("App Selections", ["Homepage", "About", "Identify", "Plant_Health"])
    if page == "Identify":
        st.title("Soil Identifier")
        identify()
    elif page == "Homepage":
        homepage()
    elif page == "About":
        about()
    elif page == "Plant_Health":
        health()



def health():
    st.title("Check the health of your plant")
    set_png_as_page_bg(datapath+'identify3.jpg')
    leaf_model = load_model('models/leaf-model.h5')
    st.set_option('deprecation.showfileUploaderEncoding', True)
    st.subheader("Choose an image of a leaf that you want to check, please take photograph of only single leaf")
    uploaded_file = st.file_uploader("Upload an image", type = "jpg")
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True)
        st.write("")
        name = "temp1.jpg"

        image.save(datapath+name)

        result = model_predict(datapath+name, leaf_model)
        pred = healthType[result]
        st.header("The state of your leaf is - "+ pred )
        st.subheader("The remedy for "+ pred + " is: "+ recomendations[pred])


def homepage():
    html_temp = """
    <html>
    <head>
    <style>
    body {
      background-color: #fe2631;
    }
    </style>
    </head>
    <body>
    </body>
    """
    st.markdown(html_temp, unsafe_allow_html = True)
    image = Image.open(datapath+'home6.png')
    st.image(image, use_column_width = True)


def about():
    set_png_as_page_bg(datapath+'mud4.jpg')
    st.title("A fistful of soil")
    st.header("“And somewhere there are engineers"
    " Helping others fly faster than sound."
    " But, where are the engineers"
    " helping those who must live on the ground?“")
    st.header("      "+ "                   - A Young Oxfam Poster")

    st.subheader("This is a preliminary work to classify soils based on the images that are uploaded by the user. A Convolutional Neural Network has been trained on sample images to identify"
     " the types of soil. Such work can find application in remote sensing and automatic classification of the land areas based on soil type.")
    st.subheader("Presently, the soils are classified into 4 categories viz. Alluvial, Black, Red, or Clay. Based on the classification of the soil, suggestions are made on the type of crops"
    " that can be grown there. ")

    st.subheader("This is version 1 of the product, there will be further improvements.")

#@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: 2200px;
    background-repeat: no-repeat;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)


def identify():
    set_png_as_page_bg(datapath+'identify2.jpg')
    soil_model = load_model('models/soil_model2.h5')
    st.set_option('deprecation.showfileUploaderEncoding', False)
    st.subheader("Choose a soil image file that you extracted from the work site or field")
    uploaded_file = st.file_uploader("Upload an image", type = "jpg")
    #temp_file = NamedTemporaryFile(delete = False)
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True)
        st.write("")
        name = "temp.jpg"

        image.save(datapath+name)

        result = model_predict(datapath+name ,soil_model)
        pred = classes[result]
        st.header("The soil is of "+ pred + " type")
        st.subheader("The types of crops suggested for "+ pred + " soil are: "+ suggestions[pred])



def model_predict(image_path,model):

    image = load_img(image_path,target_size=(224,224))
    image = img_to_array(image)
    image = image/255
    image = np.expand_dims(image,axis=0)

    result = np.argmax(model.predict(image))
    return result


if __name__ == '__main__':
    main()