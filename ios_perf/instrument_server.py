from distutils.version import LooseVersion

from .component.dtx import DTXServer
from .component.lockdown import LockdownClient
from .instrument.applications_rpc import ApplicationsRpc
from .instrument.core_profile_rpc import CoreProfileRpc
from .instrument.device_info_rpc import DeviceInfoRpc
from .instrument.mobile_notify_rpc import MobileNotifyRpc
from .instrument.network_rpc import NetworkingRpc
from .instrument.opengl_rpc import OpenGLRpc
from .instrument.process_ctl_rpc import ProcessControlRpc
from .instrument.sys_mon_tap_rpc import SysMonTapRpc
from .instrument.others_rpc import OthersRpc
from .util.exceptions import StartServiceError


class InstrumentServer(DTXServer,
                       ApplicationsRpc,
                       CoreProfileRpc,
                       DeviceInfoRpc,
                       MobileNotifyRpc,
                       NetworkingRpc,
                       OpenGLRpc,
                       ProcessControlRpc,
                       SysMonTapRpc,
                       OthersRpc):
    _sys_mon_process_attrs = None
    _sys_mon_system_attrs = None

    def __init__(self, udid=None, network=None):
        super().__init__()
        self.lockdown = LockdownClient(udid=udid, network=network)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    @property
    def sys_mon_process_attrs(self) -> list:
        if not self._sys_mon_process_attrs:
            self._sys_mon_process_attrs = self.get_mon_process_attributes()
        return self._sys_mon_process_attrs

    @property
    def sys_mon_system_attrs(self) -> list:
        if not self._sys_mon_system_attrs:
            self._sys_mon_system_attrs = self.get_mon_system_attributes()
        return self._sys_mon_system_attrs

    def init(self, _cli=None):
        if not _cli:
            try:
                if self.lockdown.ios_version >= LooseVersion('14.0'):
                    self._cli = self.lockdown.start_service("com.apple.instruments.remoteserver.DVTSecureSocketProxy")
                else:
                    self._cli = self.lockdown.start_service("com.apple.instruments.remoteserver")
                    if hasattr(self._cli.sock, '_sslobj'):
                        self._cli.sock._sslobj = None  # remote server 协议配对成功之后，需要关闭 ssl 协议通道，使用明文传输
            except StartServiceError as E:
                raise E
        else:
            self._cli = _cli
        self._start()
        if self._cli is None:
            return False
        return self
