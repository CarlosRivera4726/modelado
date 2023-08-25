import cv2
import numpy as np

class Mallado:
    image_path = None
    image, gray_image, gradient_magnitude = None, None, None
    light_source = np.array([100, 100])
    def __init__(self, image_path):
        self.image_path = image_path

    def cargar_imagen(self):
        self.image = cv2.imread(self.image_path)

    def imagen_BW(self):
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gradient_x = cv2.Sobel(self.gray_image, cv2.CV_64F, 1, 0, ksize=3)
        gradient_y = cv2.Sobel(self.gray_image, cv2.CV_64F, 0, 1, ksize=3)
        self.gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
        return gradient_x, gradient_y

    def direccion_normal(self, gradient_x, gradient_y):
        # Calcular la dirección de la normal en cada punto (simulación de superficie)
        normals = np.stack((-gradient_x, gradient_y), axis=-1)
        normals_magnitude = np.linalg.norm(normals, axis=-1)
        normals /= np.maximum(normals_magnitude, 1e-6)[:, :, np.newaxis]
        return normals
    def producto_escalar(self, normals):
        # Calcular el producto escalar entre las normales y la dirección de la luz
        shading = np.sum(normals * self.light_source, axis=-1)
        shading = np.clip(shading, 0, 255).astype(np.uint8)

        return shading
