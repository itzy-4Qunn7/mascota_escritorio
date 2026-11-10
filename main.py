import sys
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QWidget


CARPETA = Path(__file__).parent / "sprites"
ESCALA = 4
DURACION_FOTOGRAMA_MS = 400

ANIMACIONES = {
    "idle": [
             "elefante_para_sofi1.png",
             "elefante_para_sofi2.png",
             ],
     "kiss": [
             "elefante_para_sofi_kiss Copy1.png",
             "elefante_para_sofi_kiss Copy2.png",
             "elefante_para_sofi_kiss Copy3.png",
             ],
    "sleep": [
             "elefante_para_sofi_sleep1.png",
             "elefante_para_sofi_sleep2.png",
             "elefante_para_sofi_sleep3.png",
    ],
}

class Mascota(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("mascotita para my creampuff")
        self.setWindowFlags (
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            |Qt.WindowType.Tool
        )

        self.setAttribute(Qt.WidgetAttribute.WA_translucentBackground)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.image = QLabel(self)
        self.image.setStyleSheet("background: transparent;")

        self.fotogramas = {}
        for nombre, archivos in ANIMACIONES.items():
            self.fotogramas[nombre] = [ ]
            for archivo in archivos:
                ruta = CARPETA / archivo
                image = QPixmap(str(ruta))
                if image.isNull():
                    raise FileNotFoundError(f"No encuentro este PNG: {ruta}")
                primero = self.fotogramas["idle"][0]
                self.resize(primero.width() * ESCALA, primero.height() * ESCALA)

                self.estado = "idle"
                self.indice = 0
                self.besito_una_vez = False
                self.posicion_arrastre = None

                self.mostrar_fotograma()

                self.reloj = QTimer(self)
                self.reloj.timeout.connect(self.siguiente_fotograma)
                self.reloj.start(DURACION_FOTOGRAMA_MS)

                def mostrar_fotograma(self):
                    original = self.fotogramas[self.estado][self.indice]
                    ampliada = original.scaled(
                        self.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.FastTransformation,
                    )
                    self.image.setPixmap(ampliada)
                    self.image.resize(self.size())

                    def siguiente_fotograma(self):
                        self.indice += 1

                        if self.indice >= len(self.fotogramas[self.estado]):
                            if self.besito_una_vez:
                                self.estado = "idle"
                                self.besito_una_vez = False
                            self.indice = 0

                        self.mostrar_fotograma()

                    def mousePressEvent(self, evento):
                        if evento.button( ) == Qt.MouseButton.LeftButton:
                            self.posicion_arrastre = evento.globalPosition().toPoint() -self.pos() 
                            self.posicion_clic = evento.globalPosition().toPoint()

                    def mouseReleaseEvent(self, evento):
                        if evento.button() == Qt.MouseButton.LeftButton:
                            actual = evento.globalPosition().toPoint()
                            distancia = (actual -self.position_clic).manhattanLength()

                            if distancia < 6:
                                self.estado = "kiss"
                                self.indice = 0
                                self.besito_una_vez = True
                                self.mostrar_fotograma()

                            self.posicion_arrastre = None

                    def KeyPressEvent(self, evento):
                        if evento.key() == Qt.Key.Key_Escape:
                            self.close()
                        elif evento.key() == Qt.Key.Key_S:
                            self.estado = "sleep" if self.estado != "sleep" else "idle"
                            self.indice = 0
                            self.besito_una_vez = False
                            self.mostrar_fotograma()


app = QApplication(sys.argv)
mascota = Mascota()
mascota.show()
sys.exit(app.exec())



                    
    