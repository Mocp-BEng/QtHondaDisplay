import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPixmap, QConicalGradient
from PyQt5.QtCore import Qt, QTimer, QRect, QSize
from math import sin, cos, radians
from config import *

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

        # Draw background using config
        painter.setBrush(BACKGROUND_COLOR)
        painter.drawRect(0, 0, self.width(), self.height())

        if not self.is_charging:
            self.draw_first_page(painter)
        else:
            self.draw_charging_page(painter)

    def draw_first_page(self, painter):
        outer_radius = min(self.width(), self.height()) / 2
        outer_circle_radius = int(self.height() / 2)
        outer_thickness = 1

        # Draw outer circle using config
        painter.setPen(QPen(CIRCLE_COLOR, outer_thickness, Qt.SolidLine))
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
        painter.setPen(QPen(BAR_BG_COLOR, CIRCULAR_BAR_THICKNESS, Qt.SolidLine, cap=Qt.RoundCap))
        painter.drawArc(int(self.width() / 2 - left_bar_radius),
                        int(self.height() / 2 - left_bar_radius),
                        int(left_bar_radius * 2), int(left_bar_radius * 2),
                        int(250 * 16),
                        int(-left_bar_background_angle * 16))

        left_bar_angle = 180 * self.left_value / 100
        gradient = QConicalGradient(self.width() / 2, self.height() / 2, 0)
        gradient.setColorAt(1, LEFT_BAR_COLOR)
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
        small_line_length = CIRCULAR_BAR_THICKNESS * 0.13  # Minor marks
        tiny_line_length = CIRCULAR_BAR_THICKNESS * 0.08   # Even smaller marks
        line_angle = 180 * OUTER_MAX_DEGREE / 100
        painter.setFont(MARK_FONT)
        start_angle = 250
        sweep_angle = -line_angle  # Negative for counter-clockwise

        # 5 intervals = 6 big marks, 4 small steps between = 21 positions
        for i in range(21):
            angle = start_angle + (sweep_angle / 20) * i
            if i % 4 == 0:
                # Big mark
                painter.setPen(QPen(LINE_COLOR, 5, Qt.SolidLine))
                l_length = line_length
            elif i % 2 == 0:
                # Medium mark
                painter.setPen(QPen(LINE_COLOR, 2, Qt.SolidLine))
                l_length = small_line_length
            else:
                # Tiny mark
                painter.setPen(QPen(LINE_COLOR, 1, Qt.SolidLine))
                l_length = tiny_line_length

            x1 = int(self.width() / 2 + (outer_radius - l_length) * cos(radians(angle)))
            y1 = int(self.height() / 2 - (outer_radius - l_length) * sin(radians(angle)))
            x2 = int(self.width() / 2 + outer_radius * cos(radians(angle)))
            y2 = int(self.height() / 2 - outer_radius * sin(radians(angle)))
            painter.drawLine(x1, y1, x2, y2)

            # Draw numbers just inside the arc for big marks only
            if i % 4 == 0:
                value = int((i // 4) * (OUTER_MAX_DEGREE / 5))
                num_radius = outer_radius - CIRCULAR_BAR_THICKNESS / 1.5
                num_x = int(self.width() / 2 + num_radius * cos(radians(angle)))
                num_y = int(self.height() / 2 - num_radius * sin(radians(angle)))
                painter.setPen(QPen(LINE_COLOR))
                painter.drawText(num_x - 12, num_y + 10, f"{value}")

    def draw_right_circular_bar(self, painter, outer_radius):
        right_bar_radius = outer_radius - CIRCULAR_BAR_THICKNESS / 2
        right_bar_background_angle = 180 * OUTER_MAX_DEGREE / 100
        painter.setPen(QPen(BAR_BG_COLOR, CIRCULAR_BAR_THICKNESS, Qt.SolidLine, cap=Qt.RoundCap))
        painter.drawArc(int(self.width() / 2 - right_bar_radius),
                        int(self.height() / 2 - right_bar_radius),
                        int(right_bar_radius * 2),
                        int(right_bar_radius * 2),
                        int(-70 * 16),
                        int(right_bar_background_angle * 16))

        right_bar_angle = 180 * self.right_value / 100
        gradient = QConicalGradient(self.width() / 2, self.height() / 2, -120)
        gradient.setColorAt(0, RIGHT_BAR_COLOR)
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
        small_line_length = CIRCULAR_BAR_THICKNESS * 0.13  # Minor marks
        tiny_line_length = CIRCULAR_BAR_THICKNESS * 0.08   # Even smaller marks
        line_angle = 180 * OUTER_MAX_DEGREE / 100
        painter.setFont(MARK_FONT)
        start_angle = -70
        sweep_angle = line_angle  # Positive for clockwise

        # 5 intervals = 6 big marks, 4 small steps between = 21 positions
        for i in range(21):
            angle = start_angle + (sweep_angle / 20) * i
            if i % 4 == 0:
                # Big mark
                painter.setPen(QPen(LINE_COLOR, 5, Qt.SolidLine))
                l_length = line_length
            elif i % 2 == 0:
                # Medium mark
                painter.setPen(QPen(LINE_COLOR, 2, Qt.SolidLine))
                l_length = small_line_length
            else:
                # Tiny mark
                painter.setPen(QPen(LINE_COLOR, 1, Qt.SolidLine))
                l_length = tiny_line_length

            x1 = int(self.width() / 2 + (outer_radius - l_length) * cos(radians(angle)))
            y1 = int(self.height() / 2 - (outer_radius - l_length) * sin(radians(angle)))
            x2 = int(self.width() / 2 + outer_radius * cos(radians(angle)))
            y2 = int(self.height() / 2 - outer_radius * sin(radians(angle)))
            painter.drawLine(x1, y1, x2, y2)

            # Draw numbers just inside the arc for big marks only
            if i % 4 == 0:
                value = int((i // 4) * (OUTER_MAX_DEGREE / 5))
                num_radius = outer_radius - CIRCULAR_BAR_THICKNESS / 1.5
                num_x = int(self.width() / 2 + num_radius * cos(radians(angle)))
                num_y = int(self.height() / 2 - num_radius * sin(radians(angle)))
                painter.setPen(QPen(LINE_COLOR))
                painter.drawText(num_x - 12, num_y + 10, f"{value}")

    def draw_center_value(self, painter):
        painter.setPen(QPen(TEXT_COLOR, 2, Qt.SolidLine))
        center_text = str(self.center_value)
        painter.setFont(CENTER_FONT)
        center_text_width = painter.fontMetrics().width(center_text)
        center_text_height = painter.fontMetrics().height()
        painter.drawText(int(self.width() / 2 - center_text_width / 2),
                         int(self.height() / 2 + center_text_height / 4),
                         center_text)

        painter.setFont(PERCENT_FONT)
        painter.drawText(int(self.width() / 2 + center_text_width / 2 + 5),
                         int(self.height() / 2 + center_text_height / 4),
                         "%")

    def draw_additional_text(self, painter):
        additional_text = "MZ 200e"
        painter.setFont(ADDITIONAL_FONT)
        additional_text_width = painter.fontMetrics().width(additional_text)
        painter.drawText(int(self.width() / 2 - additional_text_width / 2),
                         int(self.height() / 2 - 150),
                         additional_text)

    def draw_temp_values(self, painter):
        # Use TEMP_X_OFFSET and TEMP_Y_OFFSET for positioning
        motor_text = "Motor"
        painter.setFont(TEMP_FONT)
        motor_text_width = painter.fontMetrics().width(motor_text)
        motor_text_height = painter.fontMetrics().height()
        painter.drawText(int(self.width() / 2 - TEMP_X_OFFSET - motor_text_width / 2),
                         int(self.height() / 2 + TEMP_Y_OFFSET),
                         motor_text)

        motor_temp = str(self.motor_temp) + " °C"
        motor_temp_width = painter.fontMetrics().width(motor_temp)
        painter.drawText(int(self.width() / 2 - TEMP_X_OFFSET - motor_temp_width / 2 + TEMP_X_OFFSET * 2),
                         int(self.height() / 2 + TEMP_Y_OFFSET),
                         motor_temp)

        battery_text = "Battery"
        battery_text_width = painter.fontMetrics().width(battery_text)
        painter.drawText(int(self.width() / 2 - TEMP_X_OFFSET - battery_text_width / 2),
                         int(self.height() / 2 + TEMP_Y_OFFSET + motor_text_height),
                         battery_text)

        battery_temp = str(self.battery_temp) + " °C"
        battery_temp_width = painter.fontMetrics().width(battery_temp)
        painter.drawText(int(self.width() / 2 - TEMP_X_OFFSET - battery_temp_width / 2 + TEMP_X_OFFSET * 2),
                         int(self.height() / 2 + TEMP_Y_OFFSET + motor_text_height),
                         battery_temp)

    def draw_icons(self, painter):
        # Centered horizontally, offset vertically by ICONS_Y_OFFSET
        icon_y = int(self.height() / 2 + ICONS_Y_OFFSET)
        icon_x = int(self.width() / 2 - (ICON_SIZE * 3 + ICON_SPACING * 2) / 2 + ICONS_X_OFFSET)
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
        painter.setFont(CHARGING_FONT)
        additional_text_width = painter.fontMetrics().width(additional_text)
        painter.drawText(int(self.width() / 2 - additional_text_width / 2),
                         int(self.height() / 2 - 150),
                         additional_text)

        painter.setPen(QPen(BAR_BG_COLOR, CIRCULAR_BAR_THICKNESS, Qt.SolidLine, cap=Qt.RoundCap))
        painter.drawArc(int(self.width() / 2 - right_bar_radius),
                        int(self.height() / 2 - right_bar_radius),
                        int(right_bar_radius * 2),
                        int(right_bar_radius * 2),
                        int(-70 * 16),
                        int(360 * 16))

        right_bar_angle = -360 * self.center_value / 100
        painter.setPen(QPen(CIRCLE_COLOR, CIRCULAR_BAR_THICKNESS, Qt.SolidLine, cap=Qt.RoundCap))
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

    def draw_left_value(self, painter):
        painter.setPen(QPen(TEXT_COLOR, 2, Qt.SolidLine))
        left_text = "[A]"
        painter.setFont(LEFT_FONT)
        left_text_width = painter.fontMetrics().width(left_text)
        left_text_height = painter.fontMetrics().height()
        painter.drawText(int(LABEL_DISTANCE - left_text_width / 2),
                         int(self.height() / 2 + left_text_height / 4),
                         left_text)

    def draw_right_value(self, painter):
        painter.setPen(QPen(TEXT_COLOR, 2, Qt.SolidLine))
        right_text = "[rpm]"
        painter.setFont(RIGHT_FONT)
        right_text_width = painter.fontMetrics().width(right_text)
        right_text_height = painter.fontMetrics().height()
        painter.drawText(int(self.width() - LABEL_DISTANCE - right_text_width / 2),
                         int(self.height() / 2 + right_text_height / 4),
                         right_text)

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