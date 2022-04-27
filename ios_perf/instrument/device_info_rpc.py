import abc
import plistlib

from ..component.base_rpc import BaseRpc


class DeviceInfoRpc(BaseRpc, metaclass=abc.ABCMeta):
    CHANNEL_DEVICE_INFO = 'com.apple.instruments.server.services.deviceinfo'  # 获取设备信息

    # _selector
    # - machTimeInfo
    # - runningProcesses
    # - nameForGID:
    # - execnameForPid:
    # - isRunningPid:
    # - machKernelName
    # - symbolicatorSignatureForPid: trackingSelector:
    # - unregisterSignatureTrackingForPid:
    # - enableExpiredPidTracking:
    # - symbolicatorSignaturesForExpiredPids
    # - directoryListingForPath:
    # - iconDescriptionFileForAppPath:
    # - hardwareInformation
    # - traceCodesFile
    # - kpepDatabase
    # - sysmonProcessAttributes
    # - sysmonSystemAttributes
    # - sysmonCoalitionAttributes
    # - systemInformation
    # - networkInformation
    # - nameForUID:

    def call_device_info(self, *args):
        return self.get_call_result(self.CHANNEL_DEVICE_INFO, *args)

    def get_processes(self):
        return self.call_device_info("runningProcesses")

    def get_process_execute_name(self, pid: int):
        # 获取应用路径
        return self.call_device_info('execnameForPid:', str(pid))

    def is_process_running(self, pid: int):
        return self.call_device_info("isRunningPid:", str(pid))

    def get_uid_name(self, uid: str):
        return self.call_device_info("nameForUID:", uid)

    def get_match_time_info(self):
        # 获取时间校准信息
        return self.call_device_info('machTimeInfo')

    def get_trace_codes(self):
        # 获取 traceCodes 堆栈 code 码
        parsed = self.call_device_info("traceCodesFile")
        return {int(k, 16): v for k, v in map(lambda l: l.split(), parsed.splitlines())}

    def get_network_info(self):
        # 当前网络信息
        return self.call_device_info("networkInformation")

    def get_system_info(self):
        # 设备基本信息
        return self.call_device_info("systemInformation")

    def get_hardware_info(self):
        # 硬件信息
        return self.call_device_info("hardwareInformation")

    def get_mon_process_attributes(self) -> list:
        # 获取应用性能数据所需的参数
        return list(self.call_device_info("sysmonProcessAttributes"))

    def get_mon_system_attributes(self) -> list:
        # 获取系统性能数据所需的参数
        return list(self.call_device_info("sysmonSystemAttributes"))

    def get_symbolicator_signatures(self):
        return self.call_device_info("symbolicatorSignaturesForExpiredPids")

    def get_directory_listing(self, path: str):
        # 监听文件夹路径
        return self.call_device_info("directoryListingForPath:", path)

    def get_app_icon(self, path: str):
        # 获取应用 icon 数据
        return self.call_device_info("iconDescriptionFileForAppPath:", path)

    def get_kpep_database(self):
        rs = self.call_device_info("kpepDatabase")
        return plistlib.loads(rs)

    def get_mach_kernel_name(self):
        return self.call_device_info("machKernelName")
