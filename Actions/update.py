from OpenGL.GLUT import *
from Actions import state, camera
from Actions import gestor_audio
from Actions.colisiones import CollisionObject
import math
import random

def enforce_scene_bounds(player):
    # CORREGIDO: Se cambia scene_bounds por scenario_bounds y se indexa con el escenario actual
    bounds = state.scenario_bounds.get(state.scenario, {"x": (-40.0, 40.0), "z": (-40.0, 40.0)})
    x_min, x_max = bounds["x"]
    z_min, z_max = bounds["z"]
    player.x = max(x_min, min(x_max, player.x))
    player.z = max(z_min, min(z_max, player.z))

def enforce_camera_bounds(player):
    """Evita que la cámara salga de los límites del escenario"""
    # CORREGIDO: Igual que el anterior, indexado dinámicamente
    bounds = state.scenario_bounds.get(state.scenario, {"x": (-40.0, 40.0), "z": (-40.0, 40.0)})
    x_min, x_max = bounds["x"]
    z_min, z_max = bounds["z"]
    # Nota: Se valida la posición base del jugador para evitar desajustes de cámara
    player.x = max(x_min, min(x_max, player.x))
    player.z = max(z_min, min(z_max, player.z))

def get_collision_objects_for_scenario(scenario_id):
    """Retorna los objetos de colisión según el escenario"""
    if scenario_id == 4:
        if state.level1_enabled and state.level1_phase >= state.LEVEL1_ACTIVE:
            return state.objetos_salon_level1_active
        return state.objetos_salon
    elif scenario_id == 5:
        return state.objetos_cancha
    elif scenario_id == 6:
        return state.objetos_auditorio
    elif scenario_id in [1, 2, 3, 7]:
        return state.objetos_escenas
    else:
        return []

def is_player_on_platform(player, platform):
    x, z, width, depth = platform
    return abs(player.x - x) <= width / 2 and abs(player.z - z) <= depth / 2

def are_players_on_start_platforms():
    if not state.level1_enabled or state.scenario != 4 or state.level1_phase != state.LEVEL1_WAITING:
        return False
    platforms = state.level1_platforms
    p1_on = [is_player_on_platform(state.p1, plat) for plat in platforms]
    p2_on = [is_player_on_platform(state.p2, plat) for plat in platforms]
    if sum(p1_on) != 1 or sum(p2_on) != 1:
        return False
    return p1_on != p2_on

def start_level1_sequence():
    state.level1_phase = state.LEVEL1_TRANSITION
    state.level1_transition_alpha = 0.0
    state.level1_message = "COMIENZA EL JUEGO"
    state.level1_feedback = ""
    state.level1_feedback_timer = 0

def begin_level1_play():
    state.level1_phase = state.LEVEL1_ACTIVE
    state.level1_hazards = []
    state.level1_hazard_timer = 0
    state.level1_play_timer = 0
    state.p1.x, state.p1.z = state.level1_active_positions[0]
    state.p2.x, state.p2.z = state.level1_active_positions[1]
    state.p1.direction_angle = 180.0
    state.p2.direction_angle = 180.0
    state.level1_message = ""

def spawn_level1_hazard():
    x = random.uniform(-26.0, 26.0)
    z = -37.0
    tipos = ["cube", "barrier"]
    if state.level1_play_timer > 900:  # ~15 segundos a 60 fps
        tipos.append("sphere")
        tipos.append("sphere")     
    tipo = random.choice(tipos)
    if tipo == "barrier":
        speed = random.uniform(0.12, 0.20)
        new_hazard = CollisionObject(0.0, z, size=1.0, color=(0.8, 0.2, 0.2), 
                                  label="Barrera", width=70.0, depth=1.5, shape="cube")
        new_hazard.speed = speed
    elif tipo == "sphere":
        speed = random.uniform(0.35, 0.55)
        new_hazard = CollisionObject(x, z, size=2.0, color=(0.2, 0.8, 0.8), 
                                   label="Esfera", width=2.0, depth=2.0, shape="sphere")
        new_hazard.speed = speed
    else:
        speed = random.uniform(0.12, 0.26)
        new_hazard = CollisionObject(x, z, size=2.0, color=(1.0, 0.45, 0.1), 
                                        label="PiezaPizarron", width=2.4, depth=2.4, shape="cube")
        new_hazard.speed = speed      
    state.level1_hazards.append(new_hazard)

def update_level1_hazards():
    for hazard in list(state.level1_hazards):
        hazard.z += hazard.speed

        bounds = state.scenario_bounds.get(state.scenario, {1: {"z": (-40.0, 40.0)}})
        if hazard.z > bounds['z'][1] + 5:
            state.level1_hazards.remove(hazard)

def check_level1_hazard_collisions():
    if state.level1_phase != state.LEVEL1_ACTIVE:
        return
    for hazard in list(state.level1_hazards):
        if hazard.check_collision(state.p1.x, state.p1.z, threshold=1.2, gato_y=state.p1.jump_offset):
            state.level1_hazards.remove(hazard)
            state.level1_phase = state.LEVEL1_TRIVIA
            state.level1_current_question = random.choice(state.level1_trivia_questions)
            state.level1_question_target = 'p1'
            state.level1_selected_option = 0
            state.level1_trivia_answered = False
            state.level1_show_feedback_msg = False
            state.level1_feedback_msg = ""
            state.level1_feedback_msg_timer = 0
            return
        if hazard.check_collision(state.p2.x, state.p2.z, threshold=1.2, gato_y=state.p2.jump_offset):
            state.level1_hazards.remove(hazard)
            state.level1_phase = state.LEVEL1_TRIVIA
            state.level1_current_question = random.choice(state.level1_trivia_questions)
            state.level1_question_target = 'p2'
            state.level1_selected_option = 0
            state.level1_trivia_answered = False
            state.level1_show_feedback_msg = False
            state.level1_feedback_msg = ""
            state.level1_feedback_msg_timer = 0
            return

def process_level1_trivia_answer(is_correct):
    target = state.level1_question_target
    player = state.p1 if target == 'p1' else state.p2
    if is_correct:
        state.level1_feedback_msg = "RESPUESTA CORRECTA"
        state.level1_feedback_msg_timer = 120
    else:
        player.lives -= 1
        state.level1_feedback_msg = f"RESPUESTA INCORRECTA - Vidas: {player.lives}"
        state.level1_feedback_msg_timer = 120
        if player.lives <= 0:
            state.level1_game_over = True
            state.level1_winner = 'p2' if target == 'p1' else 'p1'
            state.level1_loser = target
    state.level1_show_feedback_msg = True
    state.level1_trivia_answered = True

def update_level1_state():
    if not state.level1_enabled or state.scenario != 4:
        return
    if state.level1_phase == state.LEVEL1_WAITING:
        if are_players_on_start_platforms():
            start_level1_sequence()
    elif state.level1_phase == state.LEVEL1_TRANSITION:
        state.level1_transition_alpha = min(1.0, state.level1_transition_alpha + 0.03)
        if state.level1_transition_alpha >= 1.0:
            state.level1_phase = state.LEVEL1_COUNTDOWN
            state.level1_countdown = 3
            state.level1_countdown_timer = 0
            state.level1_hazard_timer = 0
            state.level1_message = ""
    elif state.level1_phase == state.LEVEL1_COUNTDOWN:
        state.level1_countdown_timer += 1
        if state.level1_countdown_timer >= 60:
            state.level1_countdown_timer = 0
            state.level1_countdown -= 1
            if state.level1_countdown <= 0:
                begin_level1_play()
    elif state.level1_phase == state.LEVEL1_TRIVIA:
        if state.level1_show_feedback_msg:
            state.level1_feedback_msg_timer -= 1
            if state.level1_feedback_msg_timer <= 0:
                state.level1_show_feedback_msg = False
                if state.level1_game_over:
                    state.level1_phase = state.LEVEL1_FINISHED
                else:
                    state.level1_phase = state.LEVEL1_ACTIVE
                    state.level1_hazards = []
                    state.level1_hazard_timer = 0
    elif state.level1_phase == state.LEVEL1_ACTIVE:
        state.level1_play_timer += 1
        if state.level1_game_over:
            state.level1_phase = state.LEVEL1_FINISHED
            return
        state.level1_hazard_timer += 1
        if state.level1_hazard_timer >= 55:
            spawn_level1_hazard()
            state.level1_hazard_timer = 0
        update_level1_hazards()
        check_level1_hazard_collisions()


def start_level2_sequence():
    state.level2_phase = state.LEVEL2_TRANSITION
    state.level2_transition_alpha = 0.0
    state.level2_message = "CARGANDO NIVEL 2..."
    state.level2_countdown = 3
    state.level2_countdown_timer = 0


def begin_level2_play():
    state.level2_phase = state.LEVEL2_ACTIVE
    state.level_balones_enabled = True
    if hasattr(state, 'level_balones_jugador'):
        state.level_balones_jugador.clear()
    state.level_balones_spawn_timer = 0
    state.p1.x, state.p1.z = state.level2_active_positions[0]
    state.p2.x, state.p2.z = state.level2_active_positions[1]


def are_players_on_level2_wait_positions():
    dx1 = state.p1.x - state.level2_wait_positions[0][0]
    dz1 = state.p1.z - state.level2_wait_positions[0][1]
    dx2 = state.p2.x - state.level2_wait_positions[1][0]
    dz2 = state.p2.z - state.level2_wait_positions[1][1]
    return abs(dx1) < 1.5 and abs(dz1) < 1.5 and abs(dx2) < 1.5 and abs(dz2) < 1.5


def update_level2_state():
    if state.scenario != 5 or state.level2_phase in (state.LEVEL2_NONE, state.LEVEL2_FINISHED):
        return
    if state.level2_phase == state.LEVEL2_WAITING:
        if are_players_on_level2_wait_positions():
            start_level2_sequence()
    elif state.level2_phase == state.LEVEL2_TRANSITION:
        state.level2_transition_alpha = min(1.0, state.level2_transition_alpha + 0.03)
        if state.level2_transition_alpha >= 1.0:
            state.level2_phase = state.LEVEL2_COUNTDOWN
            state.level2_countdown = 3
            state.level2_countdown_timer = 0
    elif state.level2_phase == state.LEVEL2_COUNTDOWN:
        state.level2_countdown_timer += 1
        if state.level2_countdown_timer >= 60:
            state.level2_countdown_timer = 0
            state.level2_countdown -= 1
            if state.level2_countdown <= 0:
                begin_level2_play()


def check_collision_with_obstacles(player, collision_objects, push_distance=1.0):
    """Detecta colisión con obstáculos y empuja al jugador si colisiona"""
    player_radius = 1.0
    for obj in collision_objects:
        dx = player.x - obj.x
        dz = player.z - obj.z
        overlap_x = player_radius + obj.width / 2 - abs(dx)
        overlap_z = player_radius + obj.depth / 2 - abs(dz)

        if overlap_x > 0 and overlap_z > 0:
            if overlap_x < overlap_z:
                correction = overlap_x + 0.01
                player.x += correction if dx >= 0 else -correction
            else:
                correction = overlap_z + 0.01
                player.z += correction if dz >= 0 else -correction

def check_collision_between_players(p1, p2, push_distance=0.5):
    """Detecta colisión entre jugadores y los empuja"""
    player_radius = 1.0
    dx = p1.x - p2.x
    dz = p1.z - p2.z
    distance = (dx**2 + dz**2) ** 0.5
    min_distance = player_radius * 2
    
    if distance < min_distance and distance > 0:
        push_ratio = (min_distance - distance) / (distance * 2)
        p1.x += dx * push_ratio * push_distance
        p1.z += dz * push_ratio * push_distance
        p2.x -= dx * push_ratio * push_distance
        p2.z -= dz * push_ratio * push_distance

def apply_movement_from_keys(player, is_p1=False):
    """Aplica movimiento al jugador basado en las teclas presionadas"""
    paso = 0.5
    if state.estado_actual != state.EN_JUEGO:
        return
    if state.level1_enabled and state.level1_phase in [state.LEVEL1_TRANSITION, state.LEVEL1_COUNTDOWN, state.LEVEL1_FINISHED]:
        return
    if state.level1_enabled and state.level1_phase == state.LEVEL1_TRIVIA:
        if (is_p1 and state.level1_question_target == 'p1') or (not is_p1 and state.level1_question_target == 'p2'):
            return
    
    if is_p1:
        # Jugador 1: WASD
        if state.keys_pressed.get(b'w', False):
            forward, right = camera.get_forward_right_vectors()
            player.x += forward[0] * paso
            player.z += forward[2] * paso
            player.walking = True
            player.direction_angle = camera.direction_angle_from_vector(forward[0], forward[2])
        if state.keys_pressed.get(b's', False):
            forward, right = camera.get_forward_right_vectors()
            player.x -= forward[0] * paso
            player.z -= forward[2] * paso
            player.walking = True
            player.direction_angle = camera.direction_angle_from_vector(-forward[0], -forward[2])
        if state.keys_pressed.get(b'a', False):
            forward, right = camera.get_forward_right_vectors()
            player.x -= right[0] * paso
            player.z -= right[2] * paso
            player.walking = True
            player.direction_angle = camera.direction_angle_from_vector(-right[0], -right[2])
        if state.keys_pressed.get(b'd', False):
            forward, right = camera.get_forward_right_vectors()
            player.x += right[0] * paso
            player.z += right[2] * paso
            player.walking = True
            player.direction_angle = camera.direction_angle_from_vector(right[0], right[2])
        
        if not (state.keys_pressed.get(b'w', False) or state.keys_pressed.get(b'a', False) or 
                state.keys_pressed.get(b's', False) or state.keys_pressed.get(b'd', False)):
            player.walking = False
    else:
        # Jugador 2: Flechas de dirección
        if state.keys_pressed.get('up', False):
            forward, right = camera.get_forward_right_vectors()
            player.x += forward[0] * paso
            player.z += forward[2] * paso
            player.walking = True
            player.direction_angle = camera.direction_angle_from_vector(forward[0], forward[2])
        if state.keys_pressed.get('down', False):
            forward, right = camera.get_forward_right_vectors()
            player.x -= forward[0] * paso
            player.z -= forward[2] * paso
            player.walking = True
            player.direction_angle = camera.direction_angle_from_vector(-forward[0], -forward[2])
        if state.keys_pressed.get('left', False):
            forward, right = camera.get_forward_right_vectors()
            player.x -= right[0] * paso
            player.z -= right[2] * paso
            player.walking = True
            player.direction_angle = camera.direction_angle_from_vector(-right[0], -right[2])
        if state.keys_pressed.get('right', False):
            forward, right = camera.get_forward_right_vectors()
            player.x += right[0] * paso
            player.z += right[2] * paso
            player.walking = True
            player.direction_angle = camera.direction_angle_from_vector(right[0], right[2])
        
        if not (state.keys_pressed.get('up', False) or state.keys_pressed.get('left', False) or 
                state.keys_pressed.get('down', False) or state.keys_pressed.get('right', False)):
            player.walking = False

def update_jugador_logica(player, is_p1=False):
    apply_movement_from_keys(player, is_p1)
    enforce_scene_bounds(player)
    enforce_camera_bounds(player)
    
    collision_objects = get_collision_objects_for_scenario(state.scenario)
    check_collision_with_obstacles(player, collision_objects, push_distance=1.2)
    
    if is_p1:
        check_collision_between_players(player, state.p2, push_distance=0.6)
    else:
        check_collision_between_players(player, state.p1, push_distance=0.6)
    
    enforce_scene_bounds(player)
    
    actualmente_colisionando = False
    objeto_tocado = None
    if state.estado_actual == state.EN_JUEGO:
        if state.scenario not in [4, 5, 6]:
            for obj in state.objetos_escenas:
                if obj.check_collision(player.x, player.z, 1.5):
                    actualmente_colisionando = True
                    objeto_tocado = obj
                    break 
            if actualmente_colisionando and not player.hay_choque:
                player.expression = objeto_tocado.expresion
                player.reaction_type = objeto_tocado.animacion
                player.reaction_timer = 0
                player.color_colision_actual = objeto_tocado.color
                gestor_audio.play_action_sound(objeto_tocado.expresion)
    else:
        actualmente_colisionando = False
    player.hay_choque = actualmente_colisionando
    
    # Física de salto
    gravity = 0.08
    if player.is_jumping:
        player.jump_offset += player.jump_velocity
        player.jump_velocity -= gravity
        if player.jump_offset <= 0:
            player.jump_offset = 0
            player.is_jumping = False
            player.jump_velocity = 0.0
    
    player.animation_angle += 0.15
    if player.blinking:
        player.blink_timer += 0.1
    if player.moving_tail:
        player.tail_angle += 0.1
    if player.walking:
        player.animation_angle += 0.15
        player.leg_swing = math.sin(player.animation_angle) * 25
        player.walk_bob = math.sin(player.animation_angle * 2.0) * 0.2
        player.arm_left_angle = math.sin(player.animation_angle) * 20
        player.arm_right_angle = math.sin(player.animation_angle + math.pi) * 20
    else:
        player.leg_swing = 0
        player.walk_bob = 0
        player.arm_left_angle = 0
        player.arm_right_angle = 0
    if player.reaction_type:
        player.reaction_timer += 1
        if player.reaction_timer >= player.reaction_duration:
            player.reaction_type = None
            player.reaction_timer = 0
            player.color_colision_actual = (1.0, 1.0, 1.0)
    t_blink = player.blink_timer
    if player.arm_waving:
        player.arm_wave_angle = math.sin(t_blink * 8) * 35 
    else:
        player.arm_wave_angle = 0
    if player.ears_twitching:   
        player.ears_twitch_angle = math.sin(t_blink * 15) * 20
    else:
        player.ears_twitch_angle = 0
    player.front_paws_up_angle = 70 if player.front_paws_up_active else 0

def update(value):
    update_jugador_logica(state.p1, is_p1=True)
    update_jugador_logica(state.p2, is_p1=False)
    
    update_level1_state()
    update_level2_state()
    actualizar_nivel_balones()
    
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

# ==================== MECÁNICAS NIVEL 2 ====================
def actualizar_nivel_balones():
    # 1. VALIDACIONES INICIALES DE FLUJO CORREGIDAS
    # Si cambiamos de escenario y ya NO estamos en la cancha (5), limpiamos y salimos.
    if state.scenario != 5:
        if hasattr(state, 'level_balones_jugador'):
            state.level_balones_jugador.clear()
        state.level_balones_enabled = False
        return

    # 2. Si estamos en la cancha, solo ejecutamos la lógica de balones cuando el nivel ya está activo.
    if getattr(state, 'level2_phase', 0) != getattr(state, 'LEVEL2_ACTIVE', 4) or getattr(state, 'level2_game_over', False):
        return

    state.level_balones_enabled = True

    # Reducir ráfaga/cooldowns si los ocupas
    if getattr(state, 'level2_cooldown_p1', 0) > 0: state.level2_cooldown_p1 -= 1
    if getattr(state, 'level2_cooldown_p2', 0) > 0: state.level2_cooldown_p2 -= 1

    # Obtener límites dinámicos de la Cancha
    bounds = state.scenario_bounds.get(state.scenario, {"x": (-35.0, 35.0), "z": (-35.0, 35.0)})
    x_bounds = bounds["x"]
    z_bounds = bounds["z"]

    # 2. SPAWN DE BALONES OBSTÁCULO (Caen desde arriba en Z y los jugadores deben esquivarlos)
    state.level_balones_spawn_timer += 1
    if state.level_balones_spawn_timer % state.level2_spawn_rate == 0:
        # Aparecen arriba en la cancha (z_bounds[0]) distribuidos por todo el ancho X
        spawn_x = random.uniform(x_bounds[0] + 2.0, x_bounds[1] - 2.0)
        spawn_z = z_bounds[0] + 2.0 
        
        balon_sistema = {
            "x": spawn_x,
            "y": 0.5, 
            "z": spawn_z,
            "vx": random.uniform(-0.04, 0.04) * state.level2_ball_speed_multiplier,
            "vy": 0.0,
            "vz": random.uniform(0.18, 0.32) * state.level2_ball_speed_multiplier, # Avanzan de frente hacia el fondo
            "size": 1.2,
            "color": (0.9, 0.1, 0.2), # Color de alerta
            "owner": "sistema"
        }
        state.level_balones_jugador.append(balon_sistema)

    # 3. ACTUALIZAR Y PROCESAR COLISIONES (ESQUIVAR)
    for bola in state.level_balones_jugador[:]:
        bola['x'] += bola['vx']
        bola['z'] += bola['vz']
        
        # Si el balón supera el límite inferior (pasó de largo), se elimina limpiamente sumando puntos por esquivar con éxito
        if bola['z'] >= z_bounds[1] - 1.0:
            if bola in state.level_balones_jugador:
                state.level_balones_jugador.remove(bola)
            continue

        # Eliminar balones perdidos en los laterales
        if not (x_bounds[0] - 2.0 <= bola['x'] <= x_bounds[1] + 2.0):
            if bola in state.level_balones_jugador:
                state.level_balones_jugador.remove(bola)
            continue

        # --- DETECCIÓN DE IMPACTO CON LOS JUGADORES (FRACASO AL ESQUIVAR) ---
        radio_colision = (bola['size'] / 2) + 1.0 

        # Colisión con Jugador 1
        dist_p1 = math.sqrt((bola['x'] - state.p1.x)**2 + (bola['z'] - state.p1.z)**2)
        if dist_p1 < radio_colision and state.p1.jump_offset <= 1.0:
            state.p1.lives -= 1 # Pierde vida al ser golpeado
            
            state.p1.expression = "angry"
            state.p1.reaction_type = "shake"
            state.p1.reaction_timer = 0
            gestor_audio.play_action_sound("angry")
            
            if bola in state.level_balones_jugador: state.level_balones_jugador.remove(bola)
            check_level2_victory_conditions()
            continue

        # Colisión con Jugador 2
        dist_p2 = math.sqrt((bola['x'] - state.p2.x)**2 + (bola['z'] - state.p2.z)**2)
        if dist_p2 < radio_colision and state.p2.jump_offset <= 1.0:
            state.p2.lives -= 1 # Pierde vida al ser golpeado
            
            state.p2.expression = "angry"
            state.p2.reaction_type = "shake"
            state.p2.reaction_timer = 0
            gestor_audio.play_action_sound("angry")
            
            if bola in state.level_balones_jugador: state.level_balones_jugador.remove(bola)
            check_level2_victory_conditions()
            continue

def check_level2_victory_conditions():
    """Evalúa si algún jugador se quedó sin vidas para declarar al ganador"""
    if state.p2.lives <= 0:
        state.level2_phase = getattr(state, 'LEVEL2_FINISHED', 3)
        state.level2_game_over = True
        state.level2_winner = 'p1' # Gana P1 porque P2 se quedó sin vidas primero
        
    elif state.p1.lives <= 0:
        state.level2_phase = getattr(state, 'LEVEL2_FINISHED', 3)
        state.level2_game_over = True
        state.level2_winner = 'p2' # Gana P2