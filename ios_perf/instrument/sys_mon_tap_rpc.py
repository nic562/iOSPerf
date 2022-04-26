import abc

from ..component.base_rpc import BaseRpc


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
    def sys_mon_process_attrs(self):
        raise NotImplementedError

    @property
    def sys_mon_system_attrs(self):
        raise NotImplementedError

    def call_sys_mon_tap(self, *args):
        return self.get_call_result(self.CHANNEL_SYS_MON_TAP, *args)

    def start_sys_mon_tap(self, callback: callable, interval_ms: int = 1000):
        process_attrs = self.sys_mon_process_attrs
        system_attrs = self.sys_mon_system_attrs
        self.call_sys_mon_tap("setConfig:", {
            'ur': interval_ms,  # 输出频率 ms
            'bm': 0,
            'procAttrs': process_attrs,  # 输出所有进程信息字段，字段顺序与自定义相同（全量自字段，按需使用）
            'sysAttrs': system_attrs,  # 系统信息字段
            'cpuUsage': True,
            'sampleInterval': 1000000000})
        self.register_channel_callback(self.CHANNEL_SYS_MON_TAP, callback)
        self.call_sys_mon_tap("start")

    def stop_sys_mon_tap(self):
        self.call_sys_mon_tap("stop")
