import pygame
import os
from Actions import state

try:
    pygame.mixer.init()
    audio_enabled = True
except Exception as e:
    print(f"Error inicializando audio: {e}. Audio deshabilitado.")
    audio_enabled = False

# Rutas de archivos
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOUND_PATH = os.path.join(SCRIPT_DIR, "Utils", "Sonidos")

# diccionarios para sonidos de acciones y personajes
sounds = {}
sounds_personajes = {}

if audio_enabled:
    try:
        # Sonidos de interfaz y acciones generales
        sounds = {
            "neutral": pygame.mixer.Sound(os.path.join(SOUND_PATH, "mi-bombo-duolingo_1.wav")),
            "happy": pygame.mixer.Sound(os.path.join(SOUND_PATH, "that-one-josh.wav")),
            "sad": pygame.mixer.Sound(os.path.join(SOUND_PATH, "gah-dayum.wav")),
            "angry": pygame.mixer.Sound(os.path.join(SOUND_PATH, "lightsaber_3.wav")),
            "surprised": pygame.mixer.Sound(os.path.join(SOUND_PATH, "hamburger-sound.wav")),
            "fear": pygame.mixer.Sound(os.path.join(SOUND_PATH, "oh-my-god-meme.wav")),
            "interest": pygame.mixer.Sound(os.path.join(SOUND_PATH, "bad-to-the-bone.wav"))
        }

        # Sonidos específicos de personajes
        sounds_personajes = {
            "gato": pygame.mixer.Sound(os.path.join(SOUND_PATH, "money_2_UgUMA51.wav")),
            "lola": pygame.mixer.Sound(os.path.join(SOUND_PATH, "what-bottom.wav")),
            "mosca": pygame.mixer.Sound(os.path.join(SOUND_PATH, "never-gonna.wav")),
            "KingLi": pygame.mixer.Sound(os.path.join(SOUND_PATH, "hamburger-sound.wav")),
            "amongus": pygame.mixer.Sound(os.path.join(SOUND_PATH, "gah-dayum.wav")),
            "meteoro": pygame.mixer.Sound(os.path.join(SOUND_PATH, "oh-my-god-meme.wav"))
        }
    except Exception as e:
        print(f"Error cargando archivos de sonido: {e}. Audio parcialmente deshabilitado.")

#canales
if audio_enabled:
    canal_voces = pygame.mixer.Channel(1)

# Lista de música de escenarios
lista_musica = {
    1: "one-more-time-daft-punk.wav",
    2: "rat-dance-music.wav",
    3: "pirates-mp3cut_xxOvJfH.wav",
    4: "never-gonna.wav",
    5: "social-credit-music.wav",
    6: "money_2_UgUMA51.wav",
    7: "what-bottom.wav"
}
# control
def play_action_sound(action_name):
    if audio_enabled and state.sonido_activo and action_name in sounds:
        try:
            sounds[action_name].play()
        except Exception as e:
            print(f"Error reproduciendo sonido {action_name}: {e}")

def play_character_selection_sound(tipo_personaje):
    if audio_enabled and state.sonido_activo and tipo_personaje in sounds_personajes:
        try:
            canal_voces.play(sounds_personajes[tipo_personaje])
        except Exception as e:
            print(f"Error en canal de voz para {tipo_personaje}: {e}")

def stop_voices():
    if audio_enabled:
        canal_voces.stop()

def play_background_music(scenario_id):
    if not audio_enabled or not state.sonido_activo:
        return
    try:
        pygame.mixer.music.stop() # Detener la anterior   
        file_name = lista_musica.get(scenario_id, "one-more-time-daft-punk.wav")
        path = os.path.join(SOUND_PATH, file_name)   
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1) # Loop infinito
        else:
            print(f"Archivo de música no encontrado: {path}")
    except Exception as e:
        print(f"Error al cambiar música: {e}")

def toggle_audio():
    if not audio_enabled:
        return       
    if not state.sonido_activo:
        pygame.mixer.music.pause()
        stop_voices()
    else:
        pygame.mixer.music.unpause()