import abc

from ..component.base_rpc import BaseRpc


class ProcessControlRpc(BaseRpc, metaclass=abc.ABCMeta):
    CHANNEL_PROCESS_CONTROL = "com.apple.instruments.server.services.processcontrol"  # 控制应用进程

    # _selector
    # - stopObservingPid:
    # - launchSuspendedProcessWithDevicePath:bundleIdentifier:environment:arguments:options:
    # - sendSignal:toPid:
    # - startObservingPid:
    # - suspendPid:
    # - resumePid:
    # - killPid:
    # - sendProcessControlEvent:toPid:

    def call_process_ctl(self, *args):
        return self.get_call_result(self.CHANNEL_PROCESS_CONTROL, *args)

    def launch_app(self, bundle_id: str, app_path: str = '', args: list = None, env: dict = None, options: dict = None,
                   kill_exists: bool = True,
                   callback: callable = None):
        if args is None:
            args = []
        if env is None:
            env = {}
        if options is None:
            options = {
                "StartSuspendedKey": 0,
                "KillExisting": kill_exists,
            }
        if callback:
            self.register_channel_callback(self.CHANNEL_PROCESS_CONTROL, callback)
        return self.call_process_ctl(
            "launchSuspendedProcessWithDevicePath:bundleIdentifier:environment:arguments:options:",
            app_path, bundle_id, env, args, options)

    def kill_app(self, pid: int):
        return self.call_process_ctl("killPid:", str(pid))
