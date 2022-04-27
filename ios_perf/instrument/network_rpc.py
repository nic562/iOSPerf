import abc

from ..component.base_rpc import BaseRpc
from ..util.log import default as log


class NetworkingRpc(BaseRpc, metaclass=abc.ABCMeta):
    CHANNEL_NETWORKING = 'com.apple.instruments.server.services.networking'  # 全局网络数据
    # _selector
    # - replayLastRecordedSession
    # - stopMonitoring
    # - setTargetPID:
    # - startMonitoring

    CHANNEL_NETWORK_STATISTICS = 'com.apple.xcode.debug-gauge-data-providers.NetworkStatistics'  # 获取单进程网络数据

    def call_networking(self, *args):
        return self.get_call_result(self.CHANNEL_NETWORKING, *args)

    def call_network_statistics(self, *args):
        return self.get_call_result(self.CHANNEL_NETWORK_STATISTICS, *args)

    def start_network_statistics(self, pid: int):
        return self.call_network_statistics("startSamplingForPIDs:", {str(pid)})

    def stop_network_statistics(self, pid: int):
        return self.call_network_statistics("stopSamplingForPIDs:", {str(pid)})

    def get_network_statistics(self, pid: int, attrs: dict = None):
        return self.call_network_statistics("sampleAttributes:forPIDs:", attrs or {}, {str(pid)})

    def start_networking_sampling(self, callback: callable):
        self.register_channel_callback(self.CHANNEL_NETWORKING, callback)
        log.info('networking replayLastRecordedSession:', self.call_networking("replayLastRecordedSession"))
        return self.call_networking("startMonitoring")

    def stop_networking_sampling(self):
        return self.call_networking("stopMonitoring")
