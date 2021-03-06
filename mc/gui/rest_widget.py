import os

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from mc import model, mc_global

IMAGE_GOAL_WIDTH_INT = 240
IMAGE_GOAL_HEIGHT_INT = IMAGE_GOAL_WIDTH_INT
CLOSED_RESULT_INT = -1
CLOSED_WITH_BREATHING_RESULT_INT = -2


class RestComposite(QtWidgets.QWidget):
    result_signal = QtCore.pyqtSignal(int)
    # -used both for wait and for closing

    def __init__(self):
        super().__init__()
        self.show()

        self.updating_gui_bool = False

        self.rest_actions_qbg = QtWidgets.QButtonGroup()

        # self.setWindowTitle("Please take care of yourself")
        # self.setWindowIcon(QtGui.QIcon(mc.mc_global.get_app_icon_path()))
        # self.setMinimumWidth(IMAGE_GOAL_WIDTH_INT * 2)
        # self.setMinimumHeight(IMAGE_GOAL_WIDTH_INT)
        # self.setSizePolicy(asdf)

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        # Help text
        self.help_text_qll = QtWidgets.QLabel("Please select a rest action from the list to the left")
        vbox_l2.addWidget(self.help_text_qll)
        self.help_text_qll.setFont(mc_global.get_font_xlarge(i_italics=True))

        # Main area

        self.title_qll = QtWidgets.QLabel()
        vbox_l2.addWidget(self.title_qll)

        # Image (or text if image is missing)
        self.image_qll = QtWidgets.QLabel()
        vbox_l2.addWidget(self.image_qll)
        self.image_qll.setScaledContents(True)
        self.image_qll.setMinimumWidth(IMAGE_GOAL_WIDTH_INT)
        self.image_qll.setMinimumHeight(IMAGE_GOAL_HEIGHT_INT)

        # TODO: Quote here?

        # self.image_qll.setPixmap(QtGui.QPixmap(mc_global.active_rest_image_full_path_str))
        # self.resize_image()

        """
        self.qpb = QtWidgets.QProgressBar()
        vbox_l2.addWidget(self.qpb)
        self.qpb.setMinimum(0)
        self.qpb.setMaximum(0)
        """

        vbox_l2.addStretch(1)
        self.title_qll = QtWidgets.QLabel("Please take good care of yourself")
        self.title_qll.setFont(mc_global.get_font_xlarge())
        vbox_l2.addWidget(self.title_qll)
        vbox_l2.addStretch(1)

        # TODO: Wait interface here to indicate that the user should take a break
        # For example we could use a progressbar "without end" (it's possible to set this)


        # Line of buttons (and widgets) at the bottom of the widget
        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)

        # TODO: Reset timer and .. close / breathe

        close_qgb = QtWidgets.QGroupBox()
        hbox_l3.addWidget(close_qgb)
        hbox_l4 = QtWidgets.QHBoxLayout()
        close_qgb.setLayout(hbox_l4)

        self.close_and_breathe_qpb = QtWidgets.QPushButton("Breathe")
        hbox_l4.addWidget(self.close_and_breathe_qpb)
        self.close_and_breathe_qpb.clicked.connect(self.on_close_and_breathe_button_clicked)
        self.close_and_breathe_qpb.setFont(mc_global.get_font_xlarge(i_bold=True))

        hbox_l4.addStretch(1)

        self.wait_qpb = QtWidgets.QPushButton("Wait")
        hbox_l4.addWidget(self.wait_qpb)
        self.wait_qpb.clicked.connect(self.on_wait_clicked)
        self.wait_qpb.setFont(mc_global.get_font_xlarge())
        hbox_l4.addWidget(QtWidgets.QLabel("for"))
        self.wait_qsb = QtWidgets.QSpinBox()
        self.wait_qsb.setMinimum(1)
        self.wait_qsb.setFont(mc_global.get_font_xlarge())
        hbox_l4.addWidget(self.wait_qsb)
        hbox_l4.addWidget(QtWidgets.QLabel("minutes"))

        hbox_l4.addStretch(1)

        self.close_qpb = QtWidgets.QPushButton("Close")
        hbox_l4.addWidget(self.close_qpb)
        self.close_qpb.clicked.connect(self.on_close_button_clicked)
        self.close_qpb.setFont(mc_global.get_font_xlarge())

    def on_wait_clicked(self):
        # minutes_int = self.wait_qsb.value()
        # self.dialog_outcome_int = minutes_int
        # self.accept()
        self.result_signal.emit(self.wait_qsb.value())

    def on_close_and_breathe_button_clicked(self):
        self.result_signal.emit(CLOSED_WITH_BREATHING_RESULT_INT)

    def on_close_button_clicked(self):
        self.result_signal.emit(CLOSED_RESULT_INT)

    def resize_image(self):
        if self.image_qll.pixmap() is None:
            return
        old_width_int = self.image_qll.pixmap().width()
        old_height_int = self.image_qll.pixmap().height()
        if old_width_int == 0:
            return
        width_relation_float = old_width_int / IMAGE_GOAL_WIDTH_INT
        height_relation_float = old_height_int / IMAGE_GOAL_HEIGHT_INT

        if width_relation_float > height_relation_float:
            scaled_width_int = IMAGE_GOAL_WIDTH_INT
            scaled_height_int = (scaled_width_int / old_width_int) * old_height_int
        else:
            scaled_height_int = IMAGE_GOAL_HEIGHT_INT
            scaled_width_int = (scaled_height_int / old_height_int) * old_width_int

        self.image_qll.setFixedWidth(scaled_width_int)
        self.image_qll.setFixedHeight(scaled_height_int)

    def update_gui(self):
        self.updating_gui_bool = True
        if mc_global.active_rest_action_id_it == mc_global.NO_REST_ACTION_SELECTED_INT:
            self.help_text_qll.show()
        else:
            self.help_text_qll.hide()

            rest_action = model.RestActionsM.get(mc_global.active_rest_action_id_it)
            if rest_action.image_path_str and os.path.isfile(rest_action.image_path_str):
                self.image_qll.show()
                self.image_qll.setPixmap(
                    QtGui.QPixmap(
                        rest_action.image_path_str
                    )
                )
                self.resize_image()
            else:
                self.image_qll.hide()
                self.image_qll.clear()

            self.title_qll.setText(rest_action.title_str)
            self.title_qll.setFont(mc_global.get_font_xlarge())
            self.title_qll.setWordWrap(True)

            self.updating_gui_bool = False

