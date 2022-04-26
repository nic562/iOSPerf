import abc

from ..component.base_rpc import BaseRpc


class MobileNotifyRpc(BaseRpc, metaclass=abc.ABCMeta):
    CHANNEL_MOBILE_NOTIFICATIONS = 'com.apple.instruments.server.services.mobilenotifications'  # 监控应用状态

    # _selector
    # - setApplicationStateNotificationsEnabled:
    # - setMemoryNotificationsEnabled:

    def call_mobile_notify(self, *args):
        return self.get_call_result(self.CHANNEL_MOBILE_NOTIFICATIONS, *args)

    def enable_app_status_notification(self, callback: callable):
        self.register_channel_callback(self.CHANNEL_MOBILE_NOTIFICATIONS, callback)
        self.call_mobile_notify('setApplicationStateNotificationsEnabled:', str(True))

    def disable_app_status_notification(self):
        self.call_mobile_notify('setApplicationStateNotificationsEnabled:', str(False))
