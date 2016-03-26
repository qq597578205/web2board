from wshubsapi.Hub import Hub

from libs.Config import Config
from libs.MainApp import getMainApp
from libs.Updaters.BitbloqLibsUpdater import getBitbloqLibsUpdater
from libs.Updaters.Updater import VersionInfo
from libs.Updaters.Web2boardUpdater import getWeb2boardUpdater


class VersionsHandlerHubException(Exception):
    pass


class VersionsHandlerHub(Hub):
    def getVersion(self):
        # todo: check in bitbloq if this is what we want
        return Config.version

    def setLibVersion(self, version):
        libUpdater = getBitbloqLibsUpdater()
        versionInfo = VersionInfo(version, Config.bitbloqLibsDownloadUrlTemplate.format(version=version))
        if libUpdater.isNecessaryToUpdate(versionToCompare=versionInfo):
            libUpdater.update(versionInfo)
        return True  # if return None, client is not informed that the request is done

    def setWeb2boardVersion(self, version):
        w2bUpdater = getWeb2boardUpdater()
        try:
            gui = getMainApp().w2bGui
            gui.startDownload(version)
            w2bUpdater.downloadVersion(version, gui.refreshProgressBar, gui.downloadEnded).get()
        except:
            self._getClientsHolder().getSubscribedClients().downloadEnded(False)
            raise
        w2bUpdater.makeAnAuxiliaryCopy()
        w2bUpdater.runAuxiliaryCopy(version)

    def __downloadProgress(self, current, total, percentage):
        getMainApp().w2bGui.refreshProgressBar(current, total, percentage)
        self._getClientsHolder().getSubscribedClients().downloadProgress(current, total, percentage)


    def __downloadEnded(self, task):
        getMainApp().w2bGui.downloadEnded()
        self._getClientsHolder().getSubscribedClients().downloadEnded(True)