import streamlit as st
from groq import Groq
from PIL import Image
st.set_page_config(page_title="Habla con Solid Snake", page_icon="🐍")
st.title("Este es un chat para hablar con Solid Snake de Metal Gear Solid")

nombre = st.text_input("Cual es tu nombre?")
if st.button("Saludar!"):
    if nombre== "Solid Snake":
        st.write("NO THAT IS NOT SOLID SNAKE")
    else:
        st.write(f"Hola {nombre}! ¿Que quieres saber acerca de Shadow Mowses?")
    if "Ulises" or "Jan" in nombre:
        st.write(f"prosigamos con la conversacion {nombre}")
        
    else:
        st.write("Are you the master?")

MODELOS = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile', 'deepseek-r1-distill-llama-70b']

def configurar_pagina():
    st.title("148.45")
    st.sidebar.title("Configuracion de la IA")

    elegirModelo = st.sidebar.selectbox(
        "Elegi un modelo",
        options = MODELOS,
        index = 0
    )

    return elegirModelo

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user", "content": mensajeDeEntrada}],
        stream = True
)

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) : st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border= True)
    with contenedorDelChat: mostrar_historial()

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) : st.markdown(mensaje["content"])

def generar_respuestas(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        print(frase.choices[0].delta.content)
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    modelo = configurar_pagina()
    area_chat() #Nuevo 
    mensaje = st.chat_input("Escribi tu mensaje:")
    if mensaje:
        actualizar_historial("user", mensaje, "😉")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
                with st.chat_message("assistant"):
                    respuesta_completa = st.write_stream(generar_respuestas(chat_completo))
                    actualizar_historial("assistant", respuesta_completa, "🐍")
                    st.rerun()


if __name__ == "__main__":
    main()
