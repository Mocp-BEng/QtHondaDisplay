import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPixmap, QConicalGradient, QMovie
from PyQt5.QtCore import Qt, QTimer, QRect
import random


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 800)
        self.setWindowTitle('Electric Motorcycle Dashboard')

        self.left_value = 0
        self.right_value = 0
        self.outer_max_degree = 70
        self.center_value = 0
        self.icon1_visible = False
        self.icon2_visible = False
        self.icon3_visible = False
        self.driving_state = 0  # 1: Driving, 0: Reverse
        self.warning_state = 0

        self.is_charging = False  # Logic bit to switch between first and second page

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw black background
        painter.setBrush(Qt.black)
        painter.drawRect(0, 0, self.width(), self.height())

        if not self.is_charging:
            # Draw first page
            # Draw outer circle
            outer_radius = min(self.width(), self.height()) / 2
            outer_circle_radius = 400
            outer_thickness = 1
            painter.setPen(QPen(Qt.white, outer_thickness, Qt.SolidLine))
            painter.drawEllipse(self.width() / 2 - outer_circle_radius, self.height() / 2 - outer_circle_radius,
                                outer_circle_radius * 2, outer_circle_radius * 2)

            circular_bar_thickness = 80

            # Draw left circular bar background
            left_bar_radius = outer_radius - circular_bar_thickness / 2
            left_bar_background_angle = 180 * self.outer_max_degree / 100
            painter.setPen(QPen(Qt.darkGray, circular_bar_thickness, Qt.SolidLine))
            painter.drawArc(self.width() / 2 - left_bar_radius, self.height() / 2 - left_bar_radius,
                            left_bar_radius * 2, left_bar_radius * 2, 250 * 16, -left_bar_background_angle * 16)

            # Draw left circular bar
            left_bar_radius = outer_radius - circular_bar_thickness / 2
            left_bar_angle = 180 * self.left_value / 100
            gradient = QConicalGradient(self.width() / 2, self.height() / 2, 0)
            gradient.setColorAt(1, Qt.blue)
            gradient.setColorAt(0, Qt.transparent)
            painter.setPen(QPen(gradient, circular_bar_thickness, Qt.SolidLine))
            painter.drawArc(self.width() / 2 - left_bar_radius, self.height() / 2 - left_bar_radius,
                            left_bar_radius * 2, left_bar_radius * 2, 250 * 16, -left_bar_angle * 16)

            # # Draw left value
            # painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))
            # left_text = str(self.left_value)
            # left_font = QFont('Arial', 20, QFont.Bold)
            # painter.setFont(left_font)
            # left_text_width = painter.fontMetrics().width(left_text)
            # left_text_height = painter.fontMetrics().height()
            # painter.drawText(120 - left_text_width / 2,
            #                  self.height() / 2 + left_text_height / 4, left_text)

            # Draw right circular bar background
            right_bar_radius = outer_radius - circular_bar_thickness / 2
            right_bar_background_angle = 180 * self.outer_max_degree / 100
            painter.setPen(QPen(Qt.darkGray, circular_bar_thickness, Qt.SolidLine))
            painter.drawArc(self.width() / 2 - right_bar_radius, self.height() / 2 - right_bar_radius,
                            right_bar_radius * 2, right_bar_radius * 2, -70 * 16, right_bar_background_angle * 16)

            # Draw right circular bar
            right_bar_radius = outer_radius - circular_bar_thickness / 2
            right_bar_angle = 180 * self.right_value / 100
            gradient = QConicalGradient(self.width() / 2, self.height() / 2, -120)
            gradient.setColorAt(0, Qt.red)
            gradient.setColorAt(1, Qt.transparent)
            painter.setPen(QPen(gradient, circular_bar_thickness, Qt.SolidLine))
            painter.drawArc(self.width() / 2 - right_bar_radius, self.height() / 2 - right_bar_radius,
                            right_bar_radius * 2, right_bar_radius * 2, -70 * 16, right_bar_angle * 16)


            # Draw center value
            painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))
            center_text = str(self.center_value)
            center_font = QFont('Arial', 60, QFont.Bold)
            painter.setFont(center_font)
            center_text_width = painter.fontMetrics().width(center_text)
            center_text_height = painter.fontMetrics().height()
            painter.drawText(self.width() / 2 - center_text_width / 2,
                             self.height() / 2 + center_text_height / 4, center_text)

            # Draw additional text above center value
            additional_text = "MZ 200e"
            additional_font = QFont('Arial', 20, QFont.Bold)
            painter.setFont(additional_font)
            additional_text_width = painter.fontMetrics().width(additional_text)
            painter.drawText(self.width() / 2 - additional_text_width / 2,
                             self.height() / 2 - center_text_height, additional_text)

            # Draw "%"
            percent_font = QFont('Arial', 20)
            painter.setFont(percent_font)
            painter.drawText(self.width() / 2 + center_text_width / 2 + 5,
                             self.height() / 2 + center_text_height / 4, "%")


            # Draw icons
            icon_size = 100
            icon_spacing = 20
            icon_x = self.width() / 2 - (icon_size * 3 + icon_spacing * 2) / 2
            icon_y = self.height() / 2 + center_text_height / 2 + 20

            icon_x1 = icon_x + icon_size + icon_spacing
            icon_x2 = icon_x1 + icon_size + icon_spacing

            if self.icon1_visible:
                # Draw the first icon
                icon1_pixmap = QPixmap("Blinker_left.png")  # Replace "icon1.png" with the file path of your first icon
                painter.drawPixmap(icon_x, icon_y, icon_size, icon_size, icon1_pixmap)


            if self.icon2_visible:
                # Draw the state icon
                if self.warning_state:  # Show warning icon
                    icon2_pixmap = QPixmap("Warning_icon.png")  # Replace "icon2.png" with the file path of your second icon
                    painter.drawPixmap(icon_x1, icon_y, icon_size, icon_size, icon2_pixmap)
                elif self.driving_state:  # Show drive icon
                    icon2_pixmap = QPixmap("driving_icon.png")  # Replace "icon2.png" with the file path of your second icon
                    painter.drawPixmap(icon_x1, icon_y, icon_size, icon_size, icon2_pixmap)
                else:  # Show reverse icon
                    icon2_pixmap = QPixmap("reverse_icon.png")  # Replace "icon2.png" with the file path of your second icon
                    painter.drawPixmap(icon_x1, icon_y, icon_size, icon_size, icon2_pixmap)

            if self.icon3_visible:
                # Draw the third icon
                icon3_pixmap = QPixmap("Blinker_right.png")  # Replace "icon3.png" with the file path of your third icon
                painter.drawPixmap(icon_x2, icon_y, icon_size, icon_size, icon3_pixmap)
        else:

            height_offset = 55
            # Draw center value
            painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))
            center_text = str(self.center_value)
            center_font = QFont('Arial', 60, QFont.Bold)
            painter.setFont(center_font)
            center_text_width = painter.fontMetrics().width(center_text)
            center_text_height = painter.fontMetrics().height()
            painter.drawText(self.width() / 2 - center_text_width / 2,
                             self.height() / 2 + center_text_height / 4 - height_offset, center_text)

            # Draw "%"
            percent_font = QFont('Arial', 20)
            painter.setFont(percent_font)
            painter.drawText(self.width() / 2 + center_text_width / 2 + 5,
                             self.height() / 2 + center_text_height / 4 - height_offset, "%")

    def set_left_value(self, value):
        self.left_value = value
        self.update()

    def set_right_value(self, value):
        self.right_value = value
        self.update()

    def set_center_value(self, value):
        self.center_value = value
        self.update()

    def set_icon_visibility(self, icon_index, visible):
        if icon_index == 1:
            self.icon1_visible = visible
        elif icon_index == 2:
            self.icon2_visible = visible
        elif icon_index == 3:
            self.icon3_visible = visible
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
    dashboard.set_icon_visibility(1, False)  # Example icon visibility
    dashboard.set_icon_visibility(2, True)  # Example icon visibility
    dashboard.set_icon_visibility(3, True)  # Example icon visibility

    def update_values():
        # Increment the center value by 1
        dashboard.set_center_value(dashboard.center_value + 1)
        dashboard.set_left_value(dashboard.left_value + 1)
        dashboard.set_right_value(dashboard.right_value + 1)

        if dashboard.center_value > 100:
            dashboard.set_center_value(0)  # Reset to 0 if it exceeds 100

        if dashboard.left_value > 70:
            dashboard.set_left_value(0)
            dashboard.set_right_value(0)

    def toggle_charging_state():
        dashboard.set_charging_state(not dashboard.is_charging)

    # Create a QTimer to update the values every second
    timer = QTimer()
    timer.timeout.connect(update_values)
    timer.start(100)  # Update every 1000 milliseconds (1 second)

    # Create a QTimer to toggle the charging state every 5 seconds
    charging_timer = QTimer()
    charging_timer.timeout.connect(toggle_charging_state)
    charging_timer.start(5000)  # Toggle every 5000 milliseconds (5 seconds)

    sys.exit(app.exec_())