import pygame
import os
from Actions import state

try:
    pygame.mixer.init()
    audio_enabled = True
except Exception as e:
    print(f"Error inicializando audio: {e}. Audio deshabilitado.")
    audio_enabled = False

# Obtener la ruta correcta del directorio del script
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOUND_PATH = os.path.join(SCRIPT_DIR, "Utils", "Sonidos")

sounds = {}
if audio_enabled:
    try:
        sounds = {
            "neutral": pygame.mixer.Sound(os.path.join(SOUND_PATH, "mi-bombo-duolingo_1.wav")),
            "happy": pygame.mixer.Sound(os.path.join(SOUND_PATH, "that-one-josh.wav")),
            "sad": pygame.mixer.Sound(os.path.join(SOUND_PATH, "gah-dayum.wav")),
            "angry": pygame.mixer.Sound(os.path.join(SOUND_PATH, "lightsaber_3.wav")),
            "surprised": pygame.mixer.Sound(os.path.join(SOUND_PATH, "hamburger-sound.wav")),
            "fear": pygame.mixer.Sound(os.path.join(SOUND_PATH, "oh-my-god-meme.wav")),
            "interest": pygame.mixer.Sound(os.path.join(SOUND_PATH, "bad-to-the-bone.wav"))
        }
    except Exception as e:
        print(f"Error cargando sonidos: {e}. Audio deshabilitado.")
        audio_enabled = False
        sounds = {}

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
    if audio_enabled and state.sonido_activo and action_name in sounds:
        try:
            sounds[action_name].play()
        except Exception as e:
            print(f"Error reproduciendo sonido {action_name}: {e}")

def play_background_music(scenario_id):
    #Carga y reproduce la música del escenario seleccionado
    if not audio_enabled or not state.sonido_activo:
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