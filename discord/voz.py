import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from deep_translator import GoogleTranslator
import random

words_by_level = {
    "facil": ["gato", "perro", "manzana", "leche", "sol", "luna", "agua", "mesa", "silla", "libro"],
    "medio": ["banano", "escuela", "amigo", "ventana", "amarillo", "computadora", "trabajo", "familia", "ciudad", "jardin"],
    "dificil": ["tecnologia", "universidad", "informacion", "pronunciacion", "imaginacion", "responsabilidad", "comunicacion", "conocimiento", "oportunidad", "pensamiento"]
}

print("--- BIENVENIDO A HABLA CORRECTO ---")
print("Niveles: facil, medio, dificil")
nivel = input("Elige tu nivel: ").lower()

if nivel not in words_by_level:
    nivel = "facil"

points = 0
errores = 0

print("\nALERTA: ¡Si cometes 3 errores, el juego termina!\n")

while errores < 3:
    palabra = random.choice(words_by_level[nivel])
    print(f"\n> Palabra a traducir: {palabra.upper()}")
    print("...Grabando audio (5 segundos)...")
    
    recording = sd.rec(int(5 * 44100), samplerate=44100, channels=1, dtype="int16")
    sd.wait()
    wav.write("output.wav", 44100, recording)

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="en")
        result = GoogleTranslator(source='es', target='en').translate(palabra)
        
        print(f"Dijiste: {text} | Correcto era: {result}")
        
        if text.lower() == result.lower():
            print("CORRECTO! +10 puntos.")
            points += 10
        else:
            errores += 1
            print(f"INCORRECTO. Llevas {errores} de 3 errores.")
            
    except sr.UnknownValueError:
        print("No se escuchó bien.")
            
    if errores < 3:
        if input("¿Seguir practicando? (s/n): ").lower() != "s":
            break

print(f"\nJUEGO TERMINADO. Puntos finales: {points}")




