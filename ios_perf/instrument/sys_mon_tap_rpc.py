import abc
import dataclasses

from ..component.base_rpc import BaseRpc
from ..component.dtx_msg import DTXMessage


class SysMonTapRpc(BaseRpc, metaclass=abc.ABCMeta):
    CHANNEL_SYS_MON_TAP = "com.apple.instruments.server.services.sysmontap"  # 获取应用性能数据

    # _selector
    # - setConfig: {'ur,'bm','procAttrs','sysAttrs','cpuUsage','sampleInterval'}
    # - fetchDataNow
    # - pause
    # - stop
    # - start
    # - unpause

    @property
    def sys_mon_process_attrs(self) -> list:
        """进程信息全量字段，以下枚举(内容不全)按需使用， 输出字段顺序与自定义相同
        ['memVirtualSize', 'cpuUsage', 'procStatus', 'appSleep', 'uid', 'vmPageIns', 'memRShrd',
          'ctxSwitch', 'memCompressed', 'intWakeups', 'cpuTotalSystem', 'responsiblePID', 'physFootprint',
          'cpuTotalUser', 'sysCallsUnix', 'memResidentSize', 'sysCallsMach', 'memPurgeable',
          'diskBytesRead', 'machPortCount', '__suddenTerm', '__arch', 'memRPrvt', 'msgSent', 'ppid',
          'threadCount', 'memAnon', 'diskBytesWritten', 'pgid', 'faults', 'msgRecv', '__restricted', 'pid',
          '__sandbox']"""
        raise NotImplementedError

    @property
    def sys_mon_system_attrs(self) -> list:
        """系统信息全量字段，以下枚举(内容不全)按需使用， 输出字段顺序与自定义相同
        ['diskWriteOps', 'diskBytesRead', 'diskBytesWritten', 'threadCount', 'vmCompressorPageCount',
         'vmExtPageCount', 'vmFreeCount', 'vmIntPageCount', 'vmPurgeableCount', 'netPacketsIn',
         'vmWireCount', 'netBytesIn', 'netPacketsOut', 'diskReadOps', 'vmUsedCount', '__vmSwapUsage',
         'netBytesOut']"""
        raise NotImplementedError

    def call_sys_mon_tap(self, *args):
        return self.get_call_result(self.CHANNEL_SYS_MON_TAP, *args)

    def start_sys_mon_tap(self, callback: callable, interval_ms: int = 1000,
                          pid_list: list[int] = None,
                          process_attrs: list = None, system_attrs: list = None):
        hd = TapDataHandler(callback, pid_list,
                            process_attrs or self.sys_mon_process_attrs,
                            system_attrs or self.sys_mon_system_attrs)
        self.call_sys_mon_tap("setConfig:", {
            'ur': interval_ms,  # 输出频率 ms
            'bm': 0,
            'procAttrs': hd.process_attrs,  # 输出的进程信息字段
            'sysAttrs': hd.system_attrs,  # 输出的系统信息字段
            'cpuUsage': True,
            'sampleInterval': 1000000000  # 1e9 ns == 1s
        })
        self.register_channel_callback(self.CHANNEL_SYS_MON_TAP, hd.data_handler)
        return self.call_sys_mon_tap("start")

    def stop_sys_mon_tap(self):
        self.call_sys_mon_tap("stop")

    def start_sys_mon_tap_simple(self, callback: callable, interval_ms: int = 1000, pid_list: list[int] = None):
        # physFootprint 物理内存
        # memResidentSize rss 常驻内存
        # memVirtualSize vss  虚拟内存
        # memAnon 匿名内存?
        return self.start_sys_mon_tap(
            callback, interval_ms, pid_list,
            ["memVirtualSize", "cpuUsage", "ctxSwitch", "intWakeups", "physFootprint", "memResidentSize",
             "memAnon", 'pid'],  # 如需进程名可加 'name'
            ["vmExtPageCount", "vmFreeCount", "vmPurgeableCount", "vmSpeculativeCount", "physMemSize"])


class TapDataHandler:
    def __init__(self, callback: callable, pid_list: list[int] = None,
                 process_attrs: set = None, system_attrs: set = None):
        self.callback = callback
        self.pid_list = pid_list
        self.process_attrs = process_attrs
        self.system_attrs = system_attrs

    def data_handler(self, result: DTXMessage):
        data = result.selector
        if not isinstance(data, list):
            # 如果不是列表数据，则表示不是目标数据，直接抛弃
            return
        # 正常来说，这个列表有2个字段，第一个为系统性能数据，第二个为进程性能数据
        process_data = {}
        sys_data = None
        for d in data:
            assert isinstance(d, dict)
            if 'System' in d:
                sys_attrs = dataclasses.make_dataclass(
                    'SystemAttributes',
                    self.system_attrs
                )
                sys_data = sys_attrs(*d['System']).__dict__
                sys_data['StartMachAbsTime'] = d['StartMachAbsTime']
                sys_data['EndMachAbsTime'] = d['EndMachAbsTime']
                sys_data['CPU_TotalLoad'] = d['SystemCPUUsage']['CPU_TotalLoad']
                sys_data['CPUCount'] = d['CPUCount']

            if 'Processes' in d:
                for pid, v in d['Processes'].items():
                    if self.pid_list and pid not in self.pid_list:
                        continue
                    process_attrs = dataclasses.make_dataclass(
                        'ProcessAttributes',
                        self.process_attrs
                    )
                    attrs = process_attrs(*v)
                    process_data[attrs.pid] = attrs.__dict__
                    data_dict = process_data[attrs.pid]
                    data_dict['StartMachAbsTime'] = d['StartMachAbsTime']
                    data_dict['EndMachAbsTime'] = d['EndMachAbsTime']
        self.callback({'sys': sys_data, 'process': process_data})





