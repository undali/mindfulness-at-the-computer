import enum
import os
import logging
from PyQt5 import QtCore
from PyQt5 import QtGui

#############################################
# This file contains
# * global application state which is not stored in the database (on disk)
# * global functions relating to file names/paths
# * global font functions
# * potentially other global functions
#############################################

APPLICATION_TITLE_STR = "Mindfulness at the Computer"
APPLICATION_VERSION_STR = "1.0.0-alpha.4"
NO_PHRASE_SELECTED_INT = -1
NO_REST_ACTION_SELECTED_INT = -1
NOTHING_SELECTED_INT = -1
# -TODO: merge these three above into one

APPLICATION_ICON_NAME_STR = "icon.png"
DATABASE_FILE_STR = "mindfulness-at-the-computer.db"
README_FILE_STR = "README.md"

USER_FILES_DIR_STR = "user_files"
IMAGES_DIR_STR = "images"
ICONS_DIR_STR = "icons"
AUDIO_DIR_STR = "audio"

active_rest_action_id_it = NO_REST_ACTION_SELECTED_INT
active_phrase_id_it = NO_PHRASE_SELECTED_INT
testing_bool = False
rest_reminder_minutes_passed_int = 0
# active_rest_image_full_path_str = "user_files/tea.png"
db_file_exists_at_application_startup_bl = False
display_inline_help_texts_bool = True  # -TODO


class BreathingState(enum.Enum):
    inactive = 0
    breathing_in = 1
    breathing_out = 2


breathing_state = BreathingState.inactive


class BreathingVisType(enum.Enum):
    mainwindow_widget = 0
    popup_dialog = 1


def get_base_dir():
    base_dir_str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return base_dir_str


def get_database_filename():
    if testing_bool:
        return ":memory:"
    else:
        ret_path_str = os.path.join(get_base_dir(), USER_FILES_DIR_STR, DATABASE_FILE_STR)
        return ret_path_str


def get_user_images_path(i_file_name: str=""):
    if i_file_name:
        user_images_path_str = os.path.join(get_base_dir(), USER_FILES_DIR_STR, IMAGES_DIR_STR, i_file_name)
    else:
        user_images_path_str = os.path.join(get_base_dir(), USER_FILES_DIR_STR, IMAGES_DIR_STR)
    return user_images_path_str
    # user_dir_path_str = QtCore.QDir.currentPath() + "/user_files/images/"
    # return QtCore.QDir.toNativeSeparators(user_dir_path_str)


def get_icon_path(i_file_name: str):
    ret_icon_path_str = os.path.join(get_base_dir(), ICONS_DIR_STR, i_file_name)
    return ret_icon_path_str


def get_app_icon_path():
    icon_file_name_str = "icon.png"
    ret_icon_path_str = os.path.join(get_base_dir(), ICONS_DIR_STR, icon_file_name_str)
    return ret_icon_path_str


def get_user_files_path(i_file_name: str):
    return os.path.join(get_base_dir(), USER_FILES_DIR_STR, i_file_name)

"""
def does_database_exist_started() -> bool:
    if os.path.isfile(DATABASE_FILE_NAME):
        return True
    else:
        return False
"""

# Standard font size is (on almost all systems) 12


def get_font_medium(i_italics: bool=False, i_bold: bool=False):
    font = QtGui.QFont()
    font.setItalic(i_italics)
    font.setBold(i_bold)
    return font


def get_font_large(i_underscore: bool=False, i_italics: bool=False):
    font = QtGui.QFont()
    font.setPointSize(13)
    font.setUnderline(i_underscore)
    font.setItalic(i_italics)
    return font


def get_font_xlarge(i_underscore: bool=False, i_italics: bool=False, i_bold: bool=False):
    font = QtGui.QFont()
    font.setPointSize(16)
    font.setUnderline(i_underscore)
    font.setItalic(i_italics)
    font.setBold(i_bold)
    return font


def get_font_xxlarge():
    font = QtGui.QFont()
    font.setPointSize(24)
    return font


class EventSource(enum.Enum):
    undefined = 0
    rest_action_changed = 11
    rest_list_selection_changed = 12
    breathing_list_phrase_updated = 21
    breathing_list_selection_changed = 22
    rest_settings_changed = 31
    rest_slider_value_changed = 34
    breathing_settings_changed = 4
    rest_opened = 5
    rest_closed = 6



