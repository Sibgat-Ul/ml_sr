import streamlit as sr

sr.title("This is a streamlit short tutorial")
sr.write("Welcome to the Streamlit tutorial!")

sr.header("This is a header")

sr.subheader("This is a sub header")

sr.text("This is a text")

text_input = sr.text_input("This is how you take text input", "This is a default text")
text_select = sr.selectbox("This is how you take a selection", ["Option 1", "Option 2", "Option 3"])
text_radio = sr.radio("This is how you take a radio selection", ["Option 1", "Option 2", "Option 3"])

print(text_input, text_select, text_radio)

this_is_a_button = sr.button("This is a button")

if this_is_a_button:
    sr.write("Button clicked!")
    sr.write("Text Input: " + text_input)
    sr.write("Select Box: " + text_select)
    sr.write("Radio Button: " + text_radio)
