import sys
import math
import time
import random
import ctypes
from PyQt6.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import (
    QPainter, QRadialGradient, QColor, QPainterPath,
    QCursor, QPen, QBrush, QIcon, QPixmap, QActionGroup
)

# Farb-Presets für verschiedene Zelda-Feen (R, G, B)
FAIRY_THEMES = {
    "Navi (Blau)": {
        "mid": (180, 245, 255),
        "outer": (40, 195, 255),
        "deep": (0, 130, 255),
        "wing": (170, 235, 255),
        "sparkle": (110, 225, 255),
    },
    "Ciela (Gold)": {
        "mid": (255, 250, 190),
        "outer": (255, 210, 40),
        "deep": (255, 160, 0),
        "wing": (255, 240, 170),
        "sparkle": (255, 225, 90),
    },
    "Taya (Pink/Lila)": {
        "mid": (255, 205, 250),
        "outer": (235, 95, 220),
        "deep": (185, 30, 190),
        "wing": (250, 190, 245),
        "sparkle": (245, 140, 235),
    },
    "Tael (Violett)": {
        "mid": (215, 195, 255),
        "outer": (135, 80, 255),
        "deep": (85, 25, 220),
        "wing": (200, 180, 255),
        "sparkle": (165, 120, 255),
    },
    "Heilfee (Smaragd)": {
        "mid": (195, 255, 215),
        "outer": (50, 225, 120),
        "deep": (0, 170, 75),
        "wing": (180, 250, 205),
        "sparkle": (110, 245, 160),
    }
}


class NaviOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.win_size = 240
        self.theme_names = list(FAIRY_THEMES.keys())
        self.current_theme_name = self.theme_names[0]
        self.theme = FAIRY_THEMES[self.current_theme_name]

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(self.win_size, self.win_size)

        cursor = QCursor.pos()
        self.curr_x = float(cursor.x() - 28)
        self.curr_y = float(cursor.y() - 28)
        self.prev_x = self.curr_x
        self.prev_y = self.curr_y

        self.particles = []
        self.start_time = time.time()

        self._setup_tray()
        self.show()
        self._make_clickthrough()
        self.z_order_counter = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_state)
        self.timer.start(16)

    def _create_tray_icon(self, theme):
        """Zeichnet ein kleines leuchtendes Feen-Icon für die Taskleiste."""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        p = QPainter(pixmap)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Leuchtender Schein
        grad = QRadialGradient(32, 32, 30)
        grad.setColorAt(0.0, QColor(255, 255, 255, 255))
        grad.setColorAt(0.35, QColor(*theme["mid"], 240))
        grad.setColorAt(0.7, QColor(*theme["outer"], 160))
        grad.setColorAt(1.0, QColor(*theme["deep"], 0))
        p.setBrush(QBrush(grad))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(2, 2, 60, 60)

        # Weißer Kern
        p.setBrush(QColor(255, 255, 255, 255))
        p.drawEllipse(22, 22, 20, 20)
        p.end()
        return QIcon(pixmap)

    def _setup_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self._create_tray_icon(self.theme))
        self.tray.setToolTip(f"Fee: {self.current_theme_name}\n(Linksklick: Farbe wechseln | Rechtsklick: Menü)")

        menu = QMenu()
        color_menu = menu.addMenu("Farbe wählen")
        self.action_group = QActionGroup(self)
        self.action_group.setExclusive(True)
        self.theme_actions = {}

        for name in self.theme_names:
            action = color_menu.addAction(name)
            action.setCheckable(True)
            if name == self.current_theme_name:
                action.setChecked(True)
            action.triggered.connect(lambda checked, n=name: self.set_theme(n))
            self.action_group.addAction(action)
            self.theme_actions[name] = action

        menu.addSeparator()
        quit_action = menu.addAction("Beenden")
        quit_action.triggered.connect(QApplication.instance().quit)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

    def _on_tray_activated(self, reason):
        # Einfacher Linksklick schaltet direkt zur nächsten Farbe
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            idx = (self.theme_names.index(self.current_theme_name) + 1) % len(self.theme_names)
            self.set_theme(self.theme_names[idx])

    def set_theme(self, name):
        self.current_theme_name = name
        self.theme = FAIRY_THEMES[name]
        self.theme_actions[name].setChecked(True)
        self.tray.setIcon(self._create_tray_icon(self.theme))
        self.tray.setToolTip(f"Fee: {name}\n(Linksklick: Farbe wechseln | Rechtsklick: Menü)")

    def _make_clickthrough(self):
        hwnd = int(self.winId())
        GWL_EXSTYLE = -20
        WS_EX_LAYERED = 0x80000
        WS_EX_TRANSPARENT = 0x20
        WS_EX_TOOLWINDOW = 0x80
        WS_EX_NOACTIVATE = 0x08000000

        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(
            hwnd,
            GWL_EXSTYLE,
            style | WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE
        )
        self._force_topmost()

    def _force_topmost(self):
        #Schiebt das Fenster über die Windows-Taskleiste und UI-Elemente.
        hwnd = int(self.winId())
        HWND_TOPMOST = -1
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001
        SWP_NOACTIVATE = 0x0010
        SWP_SHOWWINDOW = 0x0040
        ctypes.windll.user32.SetWindowPos(
            hwnd, HWND_TOPMOST, 0, 0, 0, 0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW
        )

    def update_state(self):
        # Alle ~30 Frames (ca. 0,5 Sek.) sicherstellen, dass Navi über der Taskleiste bleibt
        self.z_order_counter += 1
        if self.z_order_counter >= 30:
            self.z_order_counter = 0
            self._force_topmost()
        cursor = QCursor.pos()
        target_x = cursor.x() - 28
        target_y = cursor.y() - 28

        self.curr_x += (target_x - self.curr_x) * 0.11
        self.curr_y += (target_y - self.curr_y) * 0.11

        dx = self.curr_x - self.prev_x
        dy = self.curr_y - self.prev_y
        speed = math.hypot(dx, dy)
        self.prev_x, self.prev_y = self.curr_x, self.curr_y

        half = self.win_size // 2
        self.move(int(self.curr_x - half), int(self.curr_y - half))

        if speed > 3.5:
            spawn_count = min(int(speed / 4), 4)
            for _ in range(spawn_count):
                self.particles.append({
                    "x": self.curr_x + random.uniform(-6, 6),
                    "y": self.curr_y + random.uniform(-6, 6),
                    "vx": random.uniform(-0.6, 0.6) - dx * 0.08,
                    "vy": random.uniform(-0.3, 0.9) - dy * 0.08,
                    "life": 1.0,
                    "decay": random.uniform(0.025, 0.05),
                    "size": random.uniform(1.5, 3.8),
                    "is_sparkle": random.random() > 0.45
                })

        alive_particles = []
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= p["decay"]
            if p["life"] > 0:
                alive_particles.append(p)
        self.particles = alive_particles

        self.update()

    def draw_wing(self, painter, cx, cy, angle_deg, length, width, alpha):
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(angle_deg)

        path = QPainterPath()
        path.moveTo(0, 0)
        path.cubicTo(length * 0.35, -width, length * 0.95, -width * 0.7, length, 0)
        path.cubicTo(length * 0.95, width * 0.7, length * 0.35, width, 0, 0)

        w_rgb = self.theme["wing"]
        o_rgb = self.theme["outer"]

        grad = QRadialGradient(length * 0.4, 0, length * 0.8)
        grad.setColorAt(0.0, QColor(250, 253, 255, int(alpha * 220)))
        grad.setColorAt(0.6, QColor(*w_rgb, int(alpha * 145)))
        grad.setColorAt(1.0, QColor(*o_rgb, int(alpha * 45)))

        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(QColor(*w_rgb, int(alpha * 165)), 0.8))
        painter.drawPath(path)
        painter.restore()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        t = time.time() - self.start_time
        hover_y = math.sin(t * 4.2) * 4.5
        half = self.win_size // 2
        cx = float(half)
        cy = float(half) + hover_y

        sp_rgb = self.theme["sparkle"]
        dp_rgb = self.theme["deep"]

        # 1. Glitzerstaub
        for p in self.particles:
            px = half + (p["x"] - self.curr_x)
            py = half + (p["y"] - self.curr_y)
            alpha = int(max(0, min(255, p["life"] * 255)))
            s = p["size"]

            glow = QRadialGradient(px, py, s * 2.2)
            glow.setColorAt(0.0, QColor(255, 255, 255, alpha))
            glow.setColorAt(0.5, QColor(*sp_rgb, int(alpha * 0.75)))
            glow.setColorAt(1.0, QColor(*dp_rgb, 0))
            painter.setBrush(QBrush(glow))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPointF(px, py), s * 2.2, s * 2.2)

            if p["is_sparkle"] and p["life"] > 0.35:
                painter.setPen(QPen(QColor(255, 255, 255, alpha), 1.0))
                spark = s * 1.6
                painter.drawLine(QPointF(px - spark, py), QPointF(px + spark, py))
                painter.drawLine(QPointF(px, py - spark), QPointF(px, py + spark))

        # 2. Flügel
        flap = math.sin(t * 22) * 14
        self.draw_wing(painter, cx - 2, cy - 2, -138 + flap, length=24, width=6.5, alpha=0.85)
        self.draw_wing(painter, cx + 2, cy - 2, -42 - flap, length=24, width=6.5, alpha=0.85)
        self.draw_wing(painter, cx - 2, cy + 1, 148 - flap * 0.6, length=15, width=4.2, alpha=0.75)
        self.draw_wing(painter, cx + 2, cy + 1, 32 + flap * 0.6, length=15, width=4.2, alpha=0.75)

        # 3. Äußerer Glow
        aura_radius = 24 + math.sin(t * 6) * 1.5
        aura = QRadialGradient(cx, cy, aura_radius)
        aura.setColorAt(0.0, QColor(255, 255, 255, 255))
        aura.setColorAt(0.22, QColor(*self.theme["mid"], 235))
        aura.setColorAt(0.45, QColor(*self.theme["outer"], 135))
        aura.setColorAt(0.75, QColor(*dp_rgb, 45))
        aura.setColorAt(1.0, QColor(*dp_rgb, 0))
        painter.setBrush(QBrush(aura))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(cx, cy), aura_radius, aura_radius)

        # 4. Kern
        core = QRadialGradient(cx, cy, 6.5)
        core.setColorAt(0.0, QColor(255, 255, 255, 255))
        core.setColorAt(0.7, QColor(*self.theme["mid"], 240))
        core.setColorAt(1.0, QColor(*self.theme["outer"], 0))
        painter.setBrush(QBrush(core))
        painter.drawEllipse(QPointF(cx, cy), 6.5, 6.5)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Verhindert, dass sich die App schließt, wenn nur ein Kontextmenü zugeht
    app.setQuitOnLastWindowClosed(False)
    navi = NaviOverlay()
    sys.exit(app.exec())