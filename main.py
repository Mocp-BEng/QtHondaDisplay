import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPixmap, QConicalGradient
from PyQt5.QtCore import Qt, QTimer, QRect, QSize
from math import sin, cos, radians

# Constants
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
OUTER_MAX_DEGREE = 70
CIRCULAR_BAR_THICKNESS = 80
LABEL_DISTANCE = 135
ICON_SIZE = 80
ICON_SPACING = 60

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle('Electric Motorcycle Dashboard')

        self.left_value = 0
        self.right_value = 0
        self.center_value = 0
        self.icon1_visible = False
        self.icon2_visible = True
        self.icon3_visible = False
        self.blinker_left = False
        self.blinker_right = False
        self.driving_state = True  # 1: Driving, 0: Reverse
        self.warning_state = False
        self.motor_temp = 0
        self.battery_temp = 0
        self.is_charging = False  # Logic bit to switch between first and second page

        # Load icons
        self.icon1_pixmap = QPixmap("Blinker_left.png")
        self.icon2_warning_pixmap = QPixmap("Warning_icon.png")
        self.icon2_driving_pixmap = QPixmap("driving_icon.png")
        self.icon2_reverse_pixmap = QPixmap("reverse_icon.png")
        self.icon3_pixmap = QPixmap("Blinker_right.png")

        # Create a QTimer to update the values every second
        self.timer_one_sec = QTimer(self)
        self.timer_one_sec.timeout.connect(self.set_left_icon_visibility)
        self.timer_one_sec.timeout.connect(self.set_right_icon_visibility)
        self.timer_one_sec.start(1000)  # Blink every 1000 milliseconds (1 second)

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw black background
        painter.setBrush(QColor(30, 30, 30))  # Darker background
        painter.drawRect(0, 0, self.width(), self.height())

        if not self.is_charging:
            self.draw_first_page(painter)
        else:
            self.draw_charging_page(painter)

    def draw_first_page(self, painter):
        outer_radius = min(self.width(), self.height()) / 2
        outer_circle_radius = int(self.height() / 2)
        outer_thickness = 1

        # Draw outer circle
        painter.setPen(QPen(QColor(200, 200, 200), outer_thickness, Qt.SolidLine))
        painter.drawEllipse(int(self.width() / 2 - outer_circle_radius),
                            int(self.height() / 2 - outer_circle_radius),
                            int(outer_circle_radius * 2),
                            int(outer_circle_radius * 2))

        self.draw_left_circular_bar(painter, outer_radius)
        self.draw_right_circular_bar(painter, outer_radius)
        self.draw_center_value(painter)
        self.draw_additional_text(painter)
        self.draw_temp_values(painter)
        self.draw_icons(painter)

    def draw_left_circular_bar(self, painter, outer_radius):
        left_bar_radius = outer_radius - CIRCULAR_BAR_THICKNESS / 2
        left_bar_background_angle = 180 * OUTER_MAX_DEGREE / 100
        painter.setPen(QPen(QColor(100, 100, 100), CIRCULAR_BAR_THICKNESS, Qt.SolidLine, cap=Qt.RoundCap))
        painter.drawArc(int(self.width() / 2 - left_bar_radius),
                        int(self.height() / 2 - left_bar_radius),
                        int(left_bar_radius * 2), int(left_bar_radius * 2),
                        int(250 * 16),
                        int(-left_bar_background_angle * 16))

        left_bar_angle = 180 * self.left_value / 100
        gradient = QConicalGradient(self.width() / 2, self.height() / 2, 0)
        gradient.setColorAt(1, QColor(0, 122, 204))  # Blue color
        gradient.setColorAt(0, Qt.transparent)
        painter.setPen(QPen(gradient, CIRCULAR_BAR_THICKNESS, Qt.SolidLine, cap=Qt.RoundCap))
        painter.drawArc(int(self.width() / 2 - left_bar_radius),
                        int(self.height() / 2 - left_bar_radius),
                        int(left_bar_radius * 2),
                        int(left_bar_radius * 2),
                        int(250 * 16),
                        int(-left_bar_angle * 16))

        self.draw_left_lines(painter, outer_radius)
        self.draw_left_value(painter)

    def draw_left_lines(self, painter, outer_radius):
        line_length = CIRCULAR_BAR_THICKNESS * 0.25
        line_angle = 180 * OUTER_MAX_DEGREE / 100
        painter.setPen(QPen(QColor(30, 30, 30), 5, Qt.SolidLine))  # Darker lines
        for i in range(6):
            angle = line_angle / 6 * i + 130
            x1 = int(self.width() / 2 + (outer_radius - line_length) * cos(radians(angle)))
            y1 = int(self.height() / 2 - (outer_radius - line_length) * sin(radians(angle)))
            x2 = int(self.width() / 2 + outer_radius * cos(radians(angle)))
            y2 = int(self.height() / 2 - outer_radius * sin(radians(angle)))
            painter.drawLine(x1, y1, x2, y2)

    def draw_left_value(self, painter):
        painter.setPen(QPen(QColor(200, 200, 200), 2, Qt.SolidLine))
        left_text = "[A]"
        left_font = QFont('Arial', 30, QFont.Bold)
        painter.setFont(left_font)
        left_text_width = painter.fontMetrics().width(left_text)
        left_text_height = painter.fontMetrics().height()
        painter.drawText(int(LABEL_DISTANCE - left_text_width / 2),
                         int(self.height() / 2 + left_text_height / 4),
                         left_text)

    def draw_right_circular_bar(self, painter, outer_radius):
        right_bar_radius = outer_radius - CIRCULAR_BAR_THICKNESS / 2
        right_bar_background_angle = 180 * OUTER_MAX_DEGREE / 100
        painter.setPen(QPen(QColor(100, 100, 100), CIRCULAR_BAR_THICKNESS, Qt.SolidLine, cap=Qt.RoundCap))
        painter.drawArc(int(self.width() / 2 - right_bar_radius),
                        int(self.height() / 2 - right_bar_radius),
                        int(right_bar_radius * 2),
                        int(right_bar_radius * 2),
                        int(-70 * 16),
                        int(right_bar_background_angle * 16))

        right_bar_angle = 180 * self.right_value / 100
        gradient = QConicalGradient(self.width() / 2, self.height() / 2, -120)
        gradient.setColorAt(0, QColor(204, 0, 0))  # Red color
        gradient.setColorAt(1, Qt.transparent)
        painter.setPen(QPen(gradient, CIRCULAR_BAR_THICKNESS, Qt.SolidLine, cap=Qt.RoundCap))
        painter.drawArc(int(self.width() / 2 - right_bar_radius),
                        int(self.height() / 2 - right_bar_radius),
                        int(right_bar_radius * 2),
                        int(right_bar_radius * 2),
                        int(-70 * 16),
                        int(right_bar_angle * 16))

        self.draw_right_lines(painter, outer_radius)
        self.draw_right_value(painter)

    def draw_right_lines(self, painter, outer_radius):
        line_length = CIRCULAR_BAR_THICKNESS * 0.25
        line_angle = 180 * OUTER_MAX_DEGREE / 100
        painter.setPen(QPen(QColor(30, 30, 30), 5, Qt.SolidLine))  # Darker lines
        for i in range(6):
            angle = line_angle / 6 * i - 60
            x1 = int(self.width() / 2 + (outer_radius - line_length) * cos(radians(angle)))
            y1 = int(self.height() / 2 - (outer_radius - line_length) * sin(radians(angle)))
            x2 = int(self.width() / 2 + outer_radius * cos(radians(angle)))
            y2 = int(self.height() / 2 - outer_radius * sin(radians(angle)))
            painter.drawLine(x1, y1, x2, y2)

    def draw_right_value(self, painter):
        painter.setPen(QPen(QColor(200, 200, 200), 2, Qt.SolidLine))
        right_text = "[rpm]"
        right_font = QFont('Arial', 30, QFont.Bold)
        painter.setFont(right_font)
        right_text_width = painter.fontMetrics().width(right_text)
        right_text_height = painter.fontMetrics().height()
        painter.drawText(int(self.width() - LABEL_DISTANCE - right_text_width / 2),
                         int(self.height() / 2 + right_text_height / 4),
                         right_text)

    def draw_center_value(self, painter):
        painter.setPen(QPen(QColor(200, 200, 200), 2, Qt.SolidLine))
        center_text = str(self.center_value)
        center_font = QFont('Arial', 150, QFont.Bold)
        painter.setFont(center_font)
        center_text_width = painter.fontMetrics().width(center_text)
        center_text_height = painter.fontMetrics().height()
        painter.drawText(int(self.width() / 2 - center_text_width / 2),
                         int(self.height() / 2 + center_text_height / 4),
                         center_text)

        percent_font = QFont('Arial', 40)
        painter.setFont(percent_font)
        painter.drawText(int(self.width() / 2 + center_text_width / 2 + 5),
                         int(self.height() / 2 + center_text_height / 4),
                         "%")

    def draw_additional_text(self, painter):
        additional_text = "MZ 200e"
        additional_font = QFont('Tahoma', 40, QFont.Bold)
        painter.setFont(additional_font)
        additional_text_width = painter.fontMetrics().width(additional_text)
        painter.drawText(int(self.width() / 2 - additional_text_width / 2),
                         int(self.height() / 2 - 150),
                         additional_text)

    def draw_temp_values(self, painter):
        motor_text = "Motor"
        additional_font = QFont('Arial', 30, QFont.Bold)
        painter.setFont(additional_font)
        motor_text_width = painter.fontMetrics().width(motor_text)
        motor_text_height = painter.fontMetrics().height()
        painter.drawText(int(self.width() / 2 - motor_text_width / 2 - 100),
                         int(self.height() / 2 + motor_text_height + 150),
                         motor_text)

        motor_temp = str(self.motor_temp) + " °C"
        motor_temp_width = painter.fontMetrics().width(motor_temp)
        motor_temp_height = painter.fontMetrics().height()
        painter.drawText(int(self.width() / 2 - motor_temp_width / 2 + 100),
                         int(self.height() / 2 + motor_text_height + 150),
                         motor_temp)

        battery_text = "Battery"
        battery_text_width = painter.fontMetrics().width(battery_text)
        battery_text_height = painter.fontMetrics().height()
        painter.drawText(int(self.width() / 2 - motor_text_width / 2 - 100),
                         int(self.height() / 2 + motor_text_height * 2 + 150),
                         battery_text)

        battery_temp = str(self.battery_temp) + " °C"
        battery_temp_width = painter.fontMetrics().width(battery_temp)
        battery_temp_height = painter.fontMetrics().height()
        painter.drawText(int(self.width() / 2 - battery_temp_width / 2 + 100),
                         int(self.height() / 2 + motor_text_height * 2 + 150),
                         battery_temp)

    def draw_icons(self, painter):
        icon_x = int(self.width() / 2 - (ICON_SIZE * 3 + ICON_SPACING * 2) / 2)
        icon_y = int(self.height() / 2 + 150)

        icon_x1 = icon_x + ICON_SIZE + ICON_SPACING
        icon_x2 = icon_x1 + ICON_SIZE + ICON_SPACING

        if self.icon1_visible:
            painter.drawPixmap(icon_x, icon_y, ICON_SIZE, ICON_SIZE, self.icon1_pixmap)

        if self.icon2_visible:
            if self.warning_state:
                painter.drawPixmap(icon_x1, icon_y, ICON_SIZE, ICON_SIZE, self.icon2_warning_pixmap)
            elif self.driving_state:
                painter.drawPixmap(icon_x1, icon_y, ICON_SIZE, ICON_SIZE, self.icon2_driving_pixmap)
            else:
                painter.drawPixmap(icon_x1, icon_y, ICON_SIZE, ICON_SIZE, self.icon2_reverse_pixmap)

        if self.icon3_visible:
            painter.drawPixmap(icon_x2, icon_y, ICON_SIZE, ICON_SIZE, self.icon3_pixmap)

    def draw_charging_page(self, painter):
        outer_radius = min(self.width(), self.height()) / 2
        right_bar_radius = outer_radius - CIRCULAR_BAR_THICKNESS / 2

        self.draw_center_value(painter)

        additional_text = "Charging"
        additional_font = QFont('Arial', 40, QFont.Bold)
        painter.setFont(additional_font)
        additional_text_width = painter.fontMetrics().width(additional_text)
        painter.drawText(int(self.width() / 2 - additional_text_width / 2),
                         int(self.height() / 2 - 150),
                         additional_text)

        painter.setPen(QPen(QColor(100, 100, 100), CIRCULAR_BAR_THICKNESS, Qt.SolidLine, cap=Qt.RoundCap))
        painter.drawArc(int(self.width() / 2 - right_bar_radius),
                        int(self.height() / 2 - right_bar_radius),
                        int(right_bar_radius * 2),
                        int(right_bar_radius * 2),
                        int(-70 * 16),
                        int(360 * 16))

        right_bar_angle = -360 * self.center_value / 100
        painter.setPen(QPen(QColor(200, 200, 200), CIRCULAR_BAR_THICKNESS, Qt.SolidLine, cap=Qt.RoundCap))
        painter.drawArc(int(self.width() / 2 - right_bar_radius),
                        int(self.height() / 2 - right_bar_radius),
                        int(right_bar_radius * 2),
                        int(right_bar_radius * 2),
                        int(90 * 16),
                        int(right_bar_angle * 16))

    def set_temp_value(self, value_motor, value_battery):
        self.motor_temp = value_motor
        self.battery_temp = value_battery
        self.update()

    def set_left_value(self, value):
        self.left_value = value
        self.update()

    def set_right_value(self, value):
        self.right_value = value
        self.update()

    def set_center_value(self, value):
        self.center_value = value
        self.update()

    def set_left_icon_visibility(self):
        if self.blinker_left:
            self.icon1_visible = not self.icon1_visible
        else:
            self.icon1_visible = False
        self.update()

    def set_middle_icon_visibility(self, visible):
        self.icon2_visible = visible
        self.update()

    def set_right_icon_visibility(self):
        if self.blinker_right:
            self.icon3_visible = not self.icon3_visible
        else:
            self.icon3_visible = False
        self.update()

    def set_charging_state(self, is_charging):
        self.is_charging = is_charging
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.set_left_value(80)  # Example left value
    dashboard.set_right_value(80)  # Example right value
    dashboard.set_center_value(60)  # Example center value
    dashboard.blinker_left = True  # Example icon visibility
    dashboard.blinker_right = True  # Example icon visibility
    dashboard.show()

    def update_values():
        # Increment the center value by 1
        dashboard.set_center_value(dashboard.center_value + 1)
        dashboard.set_left_value(dashboard.left_value + 1)
        dashboard.set_right_value(dashboard.right_value + 1)
        dashboard.set_temp_value(dashboard.motor_temp + 1, dashboard.battery_temp + 1)

        if dashboard.center_value > 100:
            dashboard.set_center_value(0)  # Reset to 0 if it exceeds 100
            dashboard.set_temp_value(0, 0)  # Reset to 0 if it exceeds 100

        if dashboard.left_value > 70:
            dashboard.set_left_value(0)
            dashboard.set_right_value(0)

    def toggle_charging_state():
        dashboard.set_charging_state(not dashboard.is_charging)

    # Create a QTimer to update the values every second
    timer = QTimer()
    timer.timeout.connect(update_values)
    timer.start(100)  # Update every 100 milliseconds (0.1 second)

    # Create a QTimer to toggle the charging state every 5 seconds
    charging_timer = QTimer()
    charging_timer.timeout.connect(toggle_charging_state)
    charging_timer.start(10000)  # Toggle every 5000 milliseconds (5 seconds)

    sys.exit(app.exec_())