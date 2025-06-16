from groq import Groq
import streamlit as st

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=True
    )

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

st.set_page_config(page_title="Tarea Nro 6", page_icon="6", layout="centered")

st.title("esto lo tengo que modificar")
nombre = st.text_input("¿Cuál es tu nombre?")

if st.button("saludar"):
    st.write(f"Hola, {nombre}. Gracias por venir a Telnto Tech")

def configurar_pagina():
    st.title("Y esto también")
    st.sidebar.title("Configuración de la IA")
    elegirModelo = st.sidebar.selectbox("Elegí un modelo", options=MODELOS, index=0)
    return elegirModelo

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

clienteUsuario = crear_usuario_groq()
inicializar_estado()


def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar":avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])


def area_chat():
    contenderoDelChat = st.container(height=400, border=True)
    with contenderoDelChat:
        mostrar_historial()


def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for parte in chat_completo:
        if hasattr(parte.choices[0].delta, "content") and parte.choices[0].delta.content:
            texto = parte.choices[0].delta.content
            respuesta_completa += texto
            yield texto



def main():
    # Primero configuramos la página y obtenemos el modelo
    modelo = configurar_pagina()
    
    clienteUsuario = crear_usuario_groq()
    
    inicializar_estado()
    area_chat()
    # Tomamos el mensaje del usuario por input
    mensaje = st.chat_input("Escribí tu mensaje:")
    
    
    if mensaje:
        actualizar_historial("user", mensaje,"😒")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)


        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa,"🤖")
                
            st.rerun()
    

if __name__ == "__main__":
    main()