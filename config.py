from PyQt5.QtGui import QColor, QFont

# Window
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900

# Circular Bar
OUTER_MAX_DEGREE = 70
CIRCULAR_BAR_THICKNESS = 80

# Labels & Icons
LABEL_DISTANCE = 135
ICON_SIZE = 80
ICON_SPACING = 60

# Colors
BACKGROUND_COLOR = QColor(32, 58, 88)  # Changed to dark blue
CIRCLE_COLOR = QColor(200, 200, 200)
LEFT_BAR_COLOR = QColor(59, 90, 32)
RIGHT_BAR_COLOR = QColor(204, 0, 0)
BAR_BG_COLOR = QColor(100, 100, 100)
LINE_COLOR = QColor(255, 255, 255)  # Marks in the bar are now white
TEXT_COLOR = QColor(200, 200, 200)
MARK_FONT = QFont('Arial', 14, QFont.Bold)  # Font for numbers on the marks, made smaller

# Fonts
LEFT_FONT = QFont('Arial', 30, QFont.Bold)
RIGHT_FONT = QFont('Arial', 30, QFont.Bold)
CENTER_FONT = QFont('Arial', 150, QFont.Bold)
PERCENT_FONT = QFont('Arial', 40)
ADDITIONAL_FONT = QFont('Tahoma', 40, QFont.Bold)
TEMP_FONT = QFont('Arial', 30, QFont.Bold)
CHARGING_FONT = QFont('Arial', 40, QFont.Bold)

# Icon and temperature positions (offsets from center)
ICONS_Y_OFFSET = 120  # vertical offset for icons row
ICONS_X_OFFSET = 0    # horizontal offset for icons row (0 = centered)
TEMP_Y_OFFSET = 250   # vertical offset for temperature row
TEMP_X_OFFSET = 120   # horizontal offset for temperature columns