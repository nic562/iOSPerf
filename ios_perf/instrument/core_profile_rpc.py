import abc
import uuid

from ..component.base_rpc import BaseRpc


class CoreProfileRpc(BaseRpc, metaclass=abc.ABCMeta):
    CHANNEL_CORE_PROFILE_SESSION_TAP = "com.apple.instruments.server.services.coreprofilesessiontap"  # 获取内核数据

    # _selector
    # - fetchDataNow
    # - pause
    # - stop
    # - start
    # - unpause
    # - setConfig:

    def call_core_profile(self, *args):
        return self.get_call_result(self.CHANNEL_CORE_PROFILE_SESSION_TAP, *args)

    def start_core_profile_session_tap(self, callback: callable):
        self.register_channel_callback(self.CHANNEL_CORE_PROFILE_SESSION_TAP, callback)
        self.call_core_profile("setConfig:", {
            'rp': 10,
            'tc': [{'kdf2': {630784000, 833617920, 830472456},
                    'tk': 3,
                    'uuid': str(uuid.uuid4()).upper()}],
            'ur': 500
        })
        self.call_core_profile("start")

    def stop_core_profile_session_tap(self):
        self.call_core_profile("stop")
