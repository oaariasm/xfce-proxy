import sys
import re, shutil, os

from PyQt5 import QtWidgets
from GUI.GUI import Ui_MainWindow
from GUI.about import Ui_About_Dialog

class About(QtWidgets.QDialog, Ui_About_Dialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.about = About()
        self.auth_widget.hide()
        
        # Eventos de menú de archivo
        self.actionAcerca_de_SetProxy.triggered.connect(self.show_about)

        # Eventos de Botones
        self.auth_checkBox.clicked.connect(self.on_auth)
        self.apply_button.clicked.connect(self.set_proxy)
        self.reset_button.clicked.connect(self.reset_proxy)

    def on_auth(self):
        if self.auth_checkBox.isChecked():
            self.auth_widget.show()
        else:
            self.auth_widget.hide()

    def show_about(self):
        self.about.show()

    def read_current_proxy(self):
        try:
            env = open("/etc/environment", "r")
            for line in env:
                if "http_proxy" in line:
                    proxy = re.findall('/([\w.]+)', line)
                    proxy = proxy[0]
                    self.proxy_lineEdit.setText(proxy)

                    puerto = re.findall(
                        ':([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])', line)
                    puerto = puerto[0]
                    self.puerto_lineEdit.setText(puerto)
                elif "no_proxy" in line:
                    no_proxy = line[line.index("=") + 1:]
                    self.noproxy_lineEdit.setText(no_proxy)
            env.close()
        except FileNotFoundError:
            error_message.showMessage("No se pudo leer la configuración del proxy, no se encontró /etc/environment")


    def set_proxy(self):

        def check_backup_environment():
            if not os.path.isfile('/etc/environment.backup'):

                shutil.copy('/etc/environment', '/etc/environment.backup')

            else:

                shutil.copy('/etc/environment.backup', '/etc/environment')

        if self.puerto_lineEdit.text() == "":

            self.puerto_lineEdit.setText("3128")

        if self.proxy_lineEdit.text() == "":

            error_message.showMessage("Proxy no puede estar en blanco")

        else:

            try:

                if not self.auth_checkBox.isChecked():  # Sin autenticación

                    if self.actionUsar_para_apt.isChecked():

                        # Proxy apt
                        if os.path.isdir('/etc/apt/apt.conf.d/'):
                            aptconf = open("/etc/apt/apt.conf.d/proxy.conf", "w")
                            aptconf.write(
                                'Acquire::http::Proxy "http://' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/";\n')
                            aptconf.write(
                                'Acquire::https::Proxy "http://' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/";\n')
                            aptconf.write(
                                'Acquire::ftp::Proxy "http://' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/";\n')
                            aptconf.close()
                        else:
                             error_message.showMessage("asdd")

                    # Proxy del sistema

                    check_backup_environment()

                    envconf = open("/etc/environment", "a")
                    envconf.write('\n#Configuración generada por xfce-proxy\n')
                    envconf.write(
                        'http_proxy="http://' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/"\n')
                    envconf.write(
                        'HTTP_PROXY="http://' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/"\n')
                    envconf.write(
                        'https_proxy="http://' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/"\n')
                    envconf.write(
                        'HTTPS_PROXY="http://' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/"\n')
                    envconf.write(
                        'ftp_proxy="http://' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/"\n')
                    envconf.write(
                        'FTP_PROXY="http://' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/"\n')

                    if self.noproxy_lineEdit.text() == "":

                        envconf.close()

                    else:

                        envconf.write('no_proxy=' + self.noproxy_lineEdit.text() + '\n')
                        envconf.write('NO_PROXY=' + self.noproxy_lineEdit.text() + '\n')
                        envconf.close()

                else:  # Con autenticación
                    
                    if self.user_lineEdit.text() == "":

                        error_message.showMessage("Usuario no puede estar en blanco")

                    elif self.pass_lineEdit.text() == "":

                        error_message.showMessage("Contraseña no puede estar en blanco")

                    else:

                        if self.actionUsar_para_apt.isChecked():

                            aptconf = open("/etc/apt/apt.conf.d/proxy.conf", "w")
                            aptconf.write(
                                'Acquire::http::Proxy "http://' + self.user_lineEdit.text() + ':' + self.pass_lineEdit.text() + '@' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/";\n')
                            aptconf.write(
                                'Acquire::https::Proxy "http://' + self.user_lineEdit.text() + ':' + self.pass_lineEdit.text() + '@' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/";\n')
                            aptconf.write(
                                'Acquire::ftp::Proxy "http://' + self.user_lineEdit.text() + ':' + self.pass_lineEdit.text() + '@' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/";\n')
                            aptconf.close()

                        check_backup_environment()

                        envconf = open("/etc/environment", "a")
                        envconf.write('\n#Configuración generada por xfce-proxy\n')
                        envconf.write(
                            'http_proxy="http://' + self.user_lineEdit.text() + ':' + self.pass_lineEdit.text() + '@' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/"\n')
                        envconf.write(
                            'HTTP_PROXY="http://' + self.user_lineEdit.text() + ':' + self.pass_lineEdit.text() + '@' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/"\n')
                        envconf.write(
                            'https_proxy="http://' + self.user_lineEdit.text() + ':' + self.pass_lineEdit.text() + '@' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/"\n')
                        envconf.write(
                            'HTTPS_PROXY="http://' + self.user_lineEdit.text() + ':' + self.pass_lineEdit.text() + '@' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/"\n')
                        envconf.write(
                            'ftp_proxy="http://' + self.user_lineEdit.text() + ':' + self.pass_lineEdit.text() + '@' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/"\n')
                        envconf.write(
                            'FTP_PROXY="http://' + self.user_lineEdit.text() + ':' + self.pass_lineEdit.text() + '@' + self.proxy_lineEdit.text() + ':' + self.puerto_lineEdit.text() + '/"\n')

                        if self.noproxy_lineEdit.text() == "":

                            envconf.close()

                        else:

                            envconf.write('no_proxy=' + self.noproxy_lineEdit.text() + '\n')
                            envconf.write('NO_PROXY=' + self.noproxy_lineEdit.text() + '\n')
                            envconf.close()

            except PermissionError:
                error_message.showMessage("No se pudo modificar. Permiso denegado")

    def reset_proxy(self):
        # Reestablecer sistema
        if os.path.isfile('/etc/environment.backup'):
            shutil.copy('/etc/environment.backup', '/etc/environment')
        else:
             error_message.showMessage("environment.backup no encontrado")
        # Reestablecer apt (debian base)
        if os.path.isdir('/etc/apt/apt.conf.d'):
            os.remove('/etc/apt/apt.conf.d/proxy.conf')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MainWindow()
    error_message = QtWidgets.QErrorMessage()
    widget.read_current_proxy()
    widget.show()
    sys.exit(app.exec_())
