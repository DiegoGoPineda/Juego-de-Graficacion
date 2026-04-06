import pygame
import os
from Actions import state

pygame.mixer.init()
SOUND_PATH = os.path.join("Utils", "Sonidos")

sounds = {
    "neutral": pygame.mixer.Sound(os.path.join(SOUND_PATH, "mi-bombo-duolingo_1.wav")),
    "happy": pygame.mixer.Sound(os.path.join(SOUND_PATH, "that-one-josh.wav")),
    "sad": pygame.mixer.Sound(os.path.join(SOUND_PATH, "gah-dayum.wav")),
    "angry": pygame.mixer.Sound(os.path.join(SOUND_PATH, "lightsaber_3.wav")),
    "surprised": pygame.mixer.Sound(os.path.join(SOUND_PATH, "hamburger-sound.wav")),
    "fear": pygame.mixer.Sound(os.path.join(SOUND_PATH, "oh-my-god-meme.wav")),
    "interest": pygame.mixer.Sound(os.path.join(SOUND_PATH, "bad-to-the-bone.wav"))
}

# lista escenarios
lista_musica = {
    1: "one-more-time-daft-punk.wav",
    2: "rat-dance-music.wav",
    3: "pirates-mp3cut_xxOvJfH.wav",
    4: "never-gonna.wav",
    5: "social-credit-music.wav",
    6: "money_2_UgUMA51.wav",
    7: "what-bottom.wav"
}

def play_action_sound(action_name):
    if state.sonido_activo and action_name in sounds:
        sounds[action_name].play()

def play_background_music(scenario_id):
    #Carga y reproduce la música del escenario seleccionado
    if not state.sonido_activo:
        return
    
    try:
        # Detener la música actual antes de cargar la siguiente
        pygame.mixer.music.stop()
        
        file_name = lista_musica.get(scenario_id, "one-more-time-daft-punk.wav")
        path = os.path.join(SOUND_PATH, file_name)
        
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1) # Loop infinito
    except Exception as e:
        print(f"Error al cambiar música: {e}")