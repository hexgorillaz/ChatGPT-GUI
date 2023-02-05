import openai
import os
from PyQt5.QtWidgets import QApplication, QTextEdit, QLineEdit, QVBoxLayout, QLabel, QSlider, QPushButton, QDial, QWidget, QHBoxLayout, QDialog
from PyQt5.QtCore import QTimer, Qt
import re
import requests
from io import BytesIO
from PyQt5.QtGui import QPixmap

openai.api_key = os.environ['OPENAI_API_KEY']
model = "text-davinci-002"

# GUI:
app = QApplication([])
text_area = QTextEdit()
text_area.setFocusPolicy(Qt.NoFocus)
text_area.setStyleSheet("background-color: #FFF; font-size: 16px;")
message = QLineEdit()
message.setStyleSheet("font-size: 16px;")
layout = QVBoxLayout()
layout.addWidget(text_area)
layout.addWidget(message)

# Add temperature slider
temperature_label = QLabel("Temperature:")
temperature_label.setStyleSheet("font-size: 14px;")
temperature_slider = QSlider(Qt.Horizontal)
temperature_slider.setMinimum(0)
temperature_slider.setMaximum(20)
temperature_slider.setValue(int(0.5 * 10))
temperature_slider.setTickInterval(1)
temperature_slider.setTickPosition(QSlider.TicksBelow)

# Add top_p slider
top_p_label = QLabel("Top P:")
top_p_slider = QSlider(Qt.Horizontal)
top_p_slider.setMinimum(0)
top_p_slider.setMaximum(1)
top_p_slider.setValue(int(0.9 * 100))
top_p_slider.setTickInterval(int(0.1 * 100))
top_p_slider.setTickPosition(QSlider.TicksBelow)

# Add widgets to layout
layout.addWidget(temperature_label)
layout.addWidget(temperature_slider)
layout.addWidget(top_p_label)
layout.addWidget(top_p_slider)

# Add buttons layout
button_layout = QHBoxLayout()
button_layout.addStretch(1)

# Add display image button
display_image_button = QPushButton("Display Image")
display_image_button.setStyleSheet("background-color: #ccc; font-size: 14px;")
display_image_button.clicked.connect(lambda: display_image(text_area.toPlainText()))

# Add clear button
clear_button = QPushButton("Clear")
clear_button.setStyleSheet("background-color: #ccc; font-size: 14px;")
clear_button.clicked.connect(lambda: text_area.setPlainText(""))

def clear_text(self):
        self.text_area.setPlainText("")

# Add save button
save_button = QPushButton("Save")
save_button.setStyleSheet("background-color: #ccc; font-size: 14px;")

def save_text():
    question = message.text().strip()
    filename = re.sub(r'[^\w\s]', '_', question) + ".txt"
    with open(filename, "w") as f:
        f.write(text_area.toPlainText())

save_button.clicked.connect(save_text)

# Add buttons to the horizontal layout
button_layout = QHBoxLayout()
button_layout.addWidget(clear_button)
button_layout.addWidget(save_button)
button_layout.addWidget(display_image_button)

# Set the spacing between buttons in the horizontal layout
button_layout.setSpacing(10)

# Add the horizontal layout to the main layout
layout.addLayout(button_layout)

window = QWidget()
window.setLayout(layout)
window.show()

# Event handlers:
def display_new_message():
    temperature = temperature_slider.value() / 10
    top_p = top_p_slider.value() / 100

    response = openai.Completion.create(
        engine=model,
        prompt=f"{text_area.toPlainText()}\n{message.text()}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=temperature,
        top_p=top_p
    )

    text_area.append(f"\n{response.choices[0].text}")

def display_image(prompt):
    response = requests.post(
    "https://api.openai.com/v1/images/generations",
headers={
"Content-Type": "application/json",
"Authorization": f"Bearer {openai.api_key}"
},
json={
"model": "image-alpha-001",
"prompt": prompt,
"num_images": 1,
"size": "256x256"
}
)
    image_url = response.json()["data"][0]["url"]
    image = QPixmap()
    image.loadFromData(requests.get(image_url).content)
   
    dialog = QDialog()
    label = QLabel(dialog)
    label.setPixmap(image)
    dialog.exec_()

message.returnPressed.connect(display_new_message)

app.exec()
