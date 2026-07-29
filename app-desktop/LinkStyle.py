#!/usr/bin/env python3
import sys
import unicodedata
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QLineEdit, QPushButton, QCheckBox, QGridLayout,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl

# --- FUNCIONES DE TRANSFORMACIÓN UNICODE SEGURAS ---

def normalize_text(text: str) -> str:
    """ Quita acentos y convierte 'ñ/Ñ' en 'n/N' """
    text = text.replace('ñ', 'n').replace('Ñ', 'N')
    nfkd_form = unicodedata.normalize('NFD', text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def to_unicode_math(text: str, start_upper: int, start_lower: int, start_digit: int = None) -> str:
    res = []
    for char in text:
        code = ord(char)
        if 65 <= code <= 90:  # A-Z
            res.append(chr(start_upper + (code - 65)))
        elif 97 <= code <= 122:  # a-z
            res.append(chr(start_lower + (code - 97)))
        elif 48 <= code <= 57 and start_digit:  # 0-9
            res.append(chr(start_digit + (code - 48)))
        else:
            res.append(char)
    return "".join(res)

def style_bold(text: str) -> str:
    return to_unicode_math(text, 0x1D400, 0x1D41A, 0x1D7CE)

def style_italic(text: str) -> str:
    res = []
    for c in text:
        if c == 'h':
            res.append(chr(0x210E))
        elif 'a' <= c <= 'z':
            res.append(chr(0x1D44E + (ord(c) - ord('a'))))
        elif 'A' <= c <= 'Z':
            res.append(chr(0x1D434 + (ord(c) - ord('A'))))
        else:
            res.append(c)
    return "".join(res)

def style_bold_italic(text: str) -> str:
    return to_unicode_math(text, 0x1D468, 0x1D482)

def style_monospace(text: str) -> str:
    return to_unicode_math(text, 0x1D670, 0x1D68A, 0x1D7F6)

def style_underline(text: str) -> str:
    return "".join(c + '\u0332' if c != ' ' and c != '\n' else c for c in text)

def style_bold_underline(text: str) -> str:
    bold = style_bold(text)
    return "".join(c + '\u0332' if c != ' ' and c != '\n' else c for c in bold)

def style_strikethrough(text: str) -> str:
    return "".join(c + '\u0336' if c != ' ' and c != '\n' else c for c in text)

def style_inverted(text: str) -> str:
    # 1. Caracteres originales (62 caracteres: a-z, A-Z, 0-9)
    normal =  "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    # 2. Caracteres volcados/invertidos en el MISMO ORDEN (a->z, A->Z, 0->9)
    flipped = "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz∀qƆpƎℲפHIſʞ˥WNOԀΌᴚS┴∩ΛWX⅄Z0ƖᄅƐㄣϛ9L86"
    
    trans = str.maketrans(normal, flipped)
    # Traducimos los caracteres y luego invertimos la cadena completa
    return text.translate(trans)[::-1]


# --- APLICACIÓN PRINCIPAL ---

class LinkStyleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LinkStyle - Formatos Unicode para LinkedIn")
        self.resize(950, 820)
        self.setMinimumSize(850, 700)
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #FAFAFA;
                font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            }
            QScrollArea {
                border: none;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 30, 40, 30)
        container_layout.setSpacing(15)
        scroll_area.setWidget(container)

        # 1. ENCABEZADO
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_title = QLabel('LinkStyle')
        logo_title.setStyleSheet("font-size: 32px; font-weight: bold; color: #0284c7;")
        logo_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(logo_title)

        subtitle = QLabel("Dale estilo a tus publicaciones de forma profesional y segura.")
        subtitle.setStyleSheet("font-size: 14px; color: #64748b;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle)

        container_layout.addLayout(header_layout)

        # 2. TÍTULOS DE SECCIÓN
        section_title = QLabel("LinkStyle: Formatos Unicode optimizados para LinkedIn")
        section_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #0369a1; margin-top: 15px;")
        section_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(section_title)

        section_desc = QLabel("Edita tus textos para LinkedIn\nDesde aquí puedes dar distintos tipos de estilos a tus textos y destacar tu contenido.")
        section_desc.setStyleSheet("font-size: 13px; color: #475569;")
        container_layout.addWidget(section_desc)

        # 3. TEXTO ENTRADA
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Escribe tu texto...")
        self.text_input.setMaximumHeight(100)
        self.text_input.setStyleSheet("""
            QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #0284c7;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #1e293b;
            }
            QTextEdit:focus {
                border: 2px solid #0284c7;
            }
        """)
        self.text_input.textChanged.connect(self.update_styles)
        container_layout.addWidget(self.text_input)

        # Contador
        info_layout = QHBoxLayout()
        warning_lbl = QLabel("Los caracteres con tildes o la 'ñ' no tienen sustituto en UNICODE. Usa 'Normalizar texto'.")
        warning_lbl.setStyleSheet("font-size: 11px; color: #64748b;")
        info_layout.addWidget(warning_lbl, stretch=1)

        self.counter_lbl = QLabel("0 / 150")
        self.counter_lbl.setStyleSheet("""
            background-color: #0284c7; color: white; font-size: 11px;
            font-weight: bold; padding: 3px 8px; border-radius: 10px;
        """)
        info_layout.addWidget(self.counter_lbl)
        container_layout.addLayout(info_layout)

        # Checkbox
        self.chk_normalize = QCheckBox("Normalizar texto (quitar acentos y convertir ñ en n)")
        self.chk_normalize.setChecked(True)
        self.chk_normalize.setStyleSheet("font-size: 13px; color: #334155;")
        self.chk_normalize.stateChanged.connect(self.update_styles)
        container_layout.addWidget(self.chk_normalize)

        container_layout.addSpacing(10)

        # 4. GRID DE RESULTADOS EN 2 COLUMNAS
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(25)
        grid_layout.setVerticalSpacing(15)

        self.fields = {}

        styles_col_left = [
            ("Texto negrita", "bold", style_bold),
            ("Texto negrita y cursiva", "bold_italic", style_bold_italic),
            ("Texto subrayado", "underline", style_underline),
            ("Texto Monospaciado", "monospace", style_monospace),
        ]

        styles_col_right = [
            ("Texto en cursiva", "italic", style_italic),
            ("Texto subrayado y negrita", "bold_underline", style_bold_underline),
            ("Texto tachado", "strikethrough", style_strikethrough),
            ("Texto invertido", "inverted", style_inverted),
        ]

        for row, (label_text, key, func) in enumerate(styles_col_left):
            grid_layout.addWidget(self.create_output_widget(label_text, key, func), row, 0)

        for row, (label_text, key, func) in enumerate(styles_col_right):
            grid_layout.addWidget(self.create_output_widget(label_text, key, func), row, 1)

        container_layout.addLayout(grid_layout)

        container_layout.addSpacing(20)

        # 5. PIE DE PÁGINA / CRÉDITOS
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("background-color: #E2E8F0; border: none; min-height: 1px;")
        container_layout.addWidget(divider)

        footer_lbl = QLabel('Aplicación basada en LinkStyle de <b>JagMolar</b> (<a href="https://jagmolar.github.io/LinkStyle/" style="color: #0284c7; text-decoration: none;">https://jagmolar.github.io/LinkStyle/</a>)')
        footer_lbl.setStyleSheet("font-size: 12px; color: #64748b; margin-top: 5px;")
        footer_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_lbl.setOpenExternalLinks(True)  # Permite abrir la URL en el navegador predeterminado al pulsar
        container_layout.addWidget(footer_lbl)

    def create_output_widget(self, label_text: str, key: str, func) -> QWidget:
        wrapper = QWidget()
        vbox = QVBoxLayout(wrapper)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(4)

        lbl = QLabel(label_text)
        lbl.setStyleSheet("font-weight: bold; font-size: 13px; color: #1e293b;")
        vbox.addWidget(lbl)

        hbox = QHBoxLayout()
        hbox.setSpacing(0)

        entry = QLineEdit()
        entry.setReadOnly(True)
        entry.setStyleSheet("""
            QLineEdit {
                background-color: #F1F5F9;
                border: 1px solid #CBD5E1;
                border-top-left-radius: 6px;
                border-bottom-left-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                color: #334155;
            }
        """)
        hbox.addWidget(entry, stretch=1)

        btn_copy = QPushButton("Copy")
        btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_copy.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF; color: #0284c7; border: 1px solid #0284c7;
                border-top-right-radius: 6px; border-bottom-right-radius: 6px;
                padding: 8px 16px; font-size: 12px; font-weight: bold;
            }
            QPushButton:hover { background-color: #E0F2FE; }
            QPushButton:pressed { background-color: #BAE6FD; }
        """)
        
        btn_copy.clicked.connect(lambda _, e=entry, b=btn_copy: self.copy_to_clipboard(e.text(), b))
        hbox.addWidget(btn_copy)

        vbox.addLayout(hbox)

        self.fields[key] = {
            'entry': entry,
            'func': func
        }

        return wrapper

    def update_styles(self):
        raw_text = self.text_input.toPlainText()
        
        char_count = len(raw_text)
        self.counter_lbl.setText(f"{char_count} / 150")
        if char_count > 150:
            self.counter_lbl.setStyleSheet("background-color: #EF4444; color: white; font-size: 11px; font-weight: bold; padding: 3px 8px; border-radius: 10px;")
        else:
            self.counter_lbl.setStyleSheet("background-color: #0284c7; color: white; font-size: 11px; font-weight: bold; padding: 3px 8px; border-radius: 10px;")

        text = normalize_text(raw_text) if self.chk_normalize.isChecked() else raw_text

        for item in self.fields.values():
            try:
                styled_text = item['func'](text) if text else ""
                item['entry'].setText(styled_text)
            except Exception:
                item['entry'].setText(text)

    def copy_to_clipboard(self, text: str, button: QPushButton):
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            
            button.setText("¡Copiado!")
            button.setStyleSheet("""
                QPushButton {
                    background-color: #22C55E; color: white; border: 1px solid #22C55E;
                    border-top-right-radius: 6px; border-bottom-right-radius: 6px;
                    padding: 8px 16px; font-size: 12px; font-weight: bold;
                }
            """)
            
            QTimer.singleShot(1500, lambda: self.reset_button(button))

    def reset_button(self, button: QPushButton):
        button.setText("Copy")
        button.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF; color: #0284c7; border: 1px solid #0284c7;
                border-top-right-radius: 6px; border-bottom-right-radius: 6px;
                padding: 8px 16px; font-size: 12px; font-weight: bold;
            }
            QPushButton:hover { background-color: #E0F2FE; }
            QPushButton:pressed { background-color: #BAE6FD; }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LinkStyleApp()
    window.show()
    sys.exit(app.exec())
