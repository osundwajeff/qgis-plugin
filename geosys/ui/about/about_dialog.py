# coding=utf-8
"""About Dialog."""

# This import is to enable SIP API V2
# noinspection PyUnresolvedReferences
import qgis  # NOQA pylint: disable=unused-import
from qgis.PyQt import QtGui, QtWidgets, QtCore

from geosys.utilities.about import get_about_html
from geosys.utilities.resources import get_ui_class, resources_path

FORM_CLASS = get_ui_class('about_dialog_base.ui')

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = '$Format:%H$'


class AboutDialog(QtWidgets.QDialog, FORM_CLASS):
    """About dialog for the GEOSYS plugin."""

    def __init__(self, parent=None, message=None):
        """Constructor for the dialog.

        :param message: An optional message object to display in the dialog.
        :type message: Message.Message

        :param parent: Parent widget of this dialog
        :type parent: QWidget
        """

        QtWidgets.QDialog.__init__(
            self, parent)
        self.setupUi(self)
        self.parent = parent
        icon = resources_path('img', 'icons', 'icon.png')
        self.setWindowIcon(QtGui.QIcon(icon))

        # Make the html links open on the default browser instead
        # of opening the current about dialog.
        self.about_text_browser = QtWidgets.QTextBrowser(self)
        self.about_text_browser.setOpenExternalLinks(False)  # Prevent navigation
        self.about_text_browser.setOpenLinks(False)  # Fully block QTextBrowser's link navigation
        self.layout().addWidget(self.about_text_browser)

        # Load the HTML content
        self.about_text_browser.setHtml(get_about_html(message))

        # Add close button
        close_button = QtWidgets.QPushButton("Close", self)
        close_button.setFixedSize(80, 25)  # Width: 80px, Height: 25px
        close_button.clicked.connect(self.close)
        # Wrap button in an alignment widget
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)  # No margins in the alignment widget
        button_layout.setAlignment(QtCore.Qt.AlignRight)  # Align button to the right
        button_layout.addWidget(close_button)

        # Add button container to the layout
        self.layout().addWidget(button_container)
        
        # Connect link handling to the slot
        self.about_text_browser.anchorClicked.connect(self.link_clicked)


    def link_clicked(self, url):
        QtGui.QDesktopServices.openUrl(url)
