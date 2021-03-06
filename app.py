import pickle
import json
import numpy as np
from tensorflow import keras
import streamlit as st


with open("intents.json") as file:
    data = json.load(file)


def chat(msg):
    # load trained model
    model = keras.models.load_model('chat_model')

    # load tokenizer object
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
    max_len = 20

    while True:
        print("User: ", end="")
        if msg.lower() == "quit":
            break
        if(msg is not None):
            result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([msg]),
                                                                              truncating='post', maxlen=max_len))
            tag = lbl_encoder.inverse_transform([np.argmax(result)])

        for i in data['intents']:
            if i['tag'] == tag:
                return np.random.choice(i['responses'])


def main():

    st.title("ChatBot Created Using RNN and NLP")
    html_temp = """
    <div style = "background-colo:tomato;padding:10px">
    <h2 style = "color:white;text-align:center;">
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    
    msg = st.text_input("Start messaging with the bot (type quit to stop)!")
    ans = chat(msg)
    if st.button("Send"):
        st.success("ChatBot: {}".format(ans))


if __name__ == '__main__':
    main()
