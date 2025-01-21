import gym
from gym import spaces
import numpy as np
import cv2
import pyautogui
from time import sleep
from WindowCapture import WindowCapture#, ImageProcessor

class HollowKnightEnv(gym.Env):
    def __init__(self, window_name):
        super(HollowKnightEnv, self).__init__()

        # Current 
        self.wincap = WindowCapture(window_name)
        
        # self.improc = ImageProcessor(self.wincap.get_window_size(), cfg_file, weights_file)

        # Espacio de acciones: Por ejemplo, 6 acciones (izquierda, derecha, saltar, atacar, usar hechizo, no hacer nada)
        self.action_space = spaces.MultiBinary(11)  # Para 11 acciones posibles

        # Espacio de observaciones: Imágenes redimensionadas (RGB)
        self.observation_space = spaces.Box(low=0, high=255, shape=(84, 84, 3), dtype=np.uint8)

        # Estado inicial
        self.state = None
        self.prev_health = 100  # Salud inicial del jugador
        self.done = False

    def reset(self):
        """ Reinicia el entorno y devuelve el estado inicial. """
        sleep(2)  # Pausa para asegurar reinicio correcto
        self.state = self.get_state()
        self.done = False
        self.prev_health = 100
        return self.state

    def step(self, action):
        """ Ejecuta una acción, devuelve estado, recompensa, si terminó y más información. """
        self.perform_action(action)
        sleep(0.1)  # Pausa para dejar que el juego procese la acción

        # Obtener nuevo estado y calcular recompensa
        self.state = self.get_state()
        reward = self.calculate_reward()
        self.done = self.check_done()

        return self.state, reward, self.done, {}

    def perform_action(self, action):
        """
        Perform the given action(s) in the game by simulating keypresses.
        Args:
            action (list or array): A binary array of length 11 indicating actions.
                                    Each element is 1 (perform the action) or 0 (do nothing).
        """
        # Define the key mapping for each action
        keys = ['w', 's', 'a', 'd', 'space', 'j', 'k', 'e', 'r', 'f', 'q']

        # Press keys for active actions (where action[i] == 1)
        for i, key in enumerate(keys):
            if action[i] == 1:
                pyautogui.keyDown(key)  # Simulate pressing the key
            else:
                pyautogui.keyUp(key)   # Ensure the key is released if not active


    def get_state(self):
        """ Captura y procesa la pantalla como observación. """
        screenshot = self.wincap.get_screenshot()
        resized_img = cv2.resize(screenshot, (84, 84))  # Redimensionar a 84x84
        return cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

    def calculate_reward(self):
        """ Calcula la recompensa basada en eventos observados. """
        reward = 0

        # Penalización por daño recibido
        health = self.get_player_health()
        if health < self.prev_health:
            reward -= (self.prev_health - health) * 10  # Penalización proporcional al daño

        # Recompensa por derrotar enemigos
        enemies_defeated = self.get_enemies_defeated()
        reward += enemies_defeated * 50  # Recompensa fija por enemigo derrotado

        # Recompensa por progreso en el mapa
        progress = self.get_player_progress()
        reward += progress * 5  # Escala de recompensa por avanzar

        # Penalización por inacción
        if np.sum(self.last_action) == 0:
            reward -= 1  # Penalización leve por no hacer nada

        self.prev_health = health
        return reward


    def get_player_health(self):
        """ Detecta la salud del jugador analizando la barra de vida en la pantalla. """
        screenshot = self.wincap.get_screenshot()
        #x_min=84, y_min=58, x_max=583, y_max=193 # Con img_1.png incluyendo bordes
        x_min=89, y_min=49, x_max=383, y_max=143  # Con img_2.png sin bordes
        health_bar_region = screenshot[y_min:y_max, x_min:x_max]
        hsv = cv2.cvtColor(health_bar_region, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))  # Rango de color rojo
        health_ratio = np.sum(mask > 0) / mask.size  # Porcentaje de píxeles rojos
        return int(health_ratio * 100)  # Devuelve la salud como porcentaje

    
    def get_enemies_defeated(self):
        """ Detecta si un enemigo ha desaparecido de una región fija de la pantalla. """
        screenshot = self.wincap.get_screenshot()
        enemy_region = screenshot[200:400, 300:500]  # Región donde suelen estar enemigos
        enemy_template = cv2.imread('enemy_template.png', 0)  # Plantilla del enemigo
        res = cv2.matchTemplate(screenshot, enemy_template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        if np.max(res) < threshold:
            return 1  # Un enemigo derrotado
        return 0  # Ningún enemigo detectado

    
    def get_player_progress(self):
        """ Detecta el progreso analizando el desplazamiento del fondo. """
        screenshot = self.wincap.get_screenshot()
        background_region = screenshot[150:300, 100:400]  # Región del fondo
        movement_metric = np.mean(background_region)  # Promedio de valores de píxeles
        return movement_metric  # Devuelve un proxy del progreso


    def check_done(self):
        """ Verifica si el episodio ha terminado (e.g., muerte del jugador). """
        return self.get_player_health() <= 0

    def close(self):
        """ Cierra cualquier recurso abierto, si aplica. """
        cv2.destroyAllWindows()
