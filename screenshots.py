import os
import time
import threading
import pyautogui
import glob
import argparse  # Para gestionar los parámetros de la línea de comandos
import keyboard  # Para detectar las teclas presionadas

# Screenshot thread to capture game frames
class ScreenshotThread:
    """
    Thread to continuously capture screenshots and save them to a folder.
    Automatically removes old screenshots to prevent excessive storage usage.
    """

    def __init__(self, folder="screenshots", interval=1/60):
        """
        Initialize the screenshot thread.
        Args:
            folder (str): Directory to save screenshots.
            interval (float): Time interval between screenshots in seconds. By default, 60 FPS.
        """
        self.folder = folder
        self.interval = interval
        self.stop_event = threading.Event()
        self.counter = 1054  # Counter for sequential image names

        # Ensure the screenshot folder exists
        if not os.path.exists(folder):
            os.makedirs(folder)

    def start(self):
        """Start the screenshot capturing thread."""
        self.thread = threading.Thread(target=self._capture_screenshots)
        self.thread.daemon = True  # Daemon thread to automatically exit with the main program
        self.thread.start()

    def stop(self):
        """Stop the screenshot capturing thread."""
        self.stop_event.set()
        self.thread.join()

    def _capture_screenshots(self):
        """Continuously capture screenshots and save them to the folder."""
        while not self.stop_event.is_set():
            # Create screenshot name using the counter
            screenshot_name = f"{self.counter}.png"
            screenshot_path = os.path.join(self.folder, screenshot_name)
            pyautogui.screenshot(screenshot_path)

            # Increment the counter for the next screenshot
            self.counter += 1

            # Remove old screenshots (older than 1 second)
            #self._remove_old_screenshots()

            # Wait for the specified interval
            self.stop_event.wait(self.interval)

    def _remove_old_screenshots(self):
        """Remove screenshots older than 1 second."""
        current_time = time.time()
        for screenshot in glob.glob(os.path.join(self.folder, "*.png")):
            creation_time = os.path.getmtime(screenshot)
            if current_time - creation_time > 1:
                os.remove(screenshot)

def main():
    # Configurar los argumentos de la línea de comandos
    parser = argparse.ArgumentParser(description="Captura de pantallas en un videojuego.")
    parser.add_argument(
        "--fps",
        type=float,
        default=3,
        help="Número de imágenes por segundo (FPS) a capturar. Por defecto es 3 FPS.",
    )
    parser.add_argument(
        "--folder",
        type=str,
        default="screenshots",
        help="Carpeta donde guardar las capturas de pantalla.",
    )
    
    # Parsear los argumentos
    args = parser.parse_args()

    # Crear una instancia de ScreenshotThread con el intervalo correspondiente
    interval = 1 / args.fps  # Calcula el intervalo en función de los FPS
    screenshot_thread = ScreenshotThread(folder=args.folder, interval=interval)

    # Iniciar la captura de pantallas
    screenshot_thread.start()

    # Mantener el script en ejecución hasta que se presione la tecla "q"
    print("Presiona 'q' para detener la captura.")
    try:
        while not keyboard.is_pressed('q'):  # Mientras no se presione la tecla 'q'
            time.sleep(0.1)  # Pequeña espera para evitar el uso excesivo de CPU
        print("Deteniendo la captura...")
        screenshot_thread.stop()  # Detener el hilo de captura
    except KeyboardInterrupt:
        # Detener el hilo cuando se interrumpe el script (Ctrl+C)
        screenshot_thread.stop()
        print("Captura de pantallas detenida.")

if __name__ == "__main__":
    main()