import abc

from ..component.base_rpc import BaseRpc


class ApplicationsRpc(BaseRpc, metaclass=abc.ABCMeta):
    CHANNEL_APPLICATION_LISTING = "com.apple.instruments.server.services.device.applictionListing"  # 获取应用数据

    # _selector
    # - installedApplicationsMatching: registerUpdateToken:
    # - unregisterUpdateToken:

    def call_application_listing(self, *args):
        return self.get_call_result(self.CHANNEL_APPLICATION_LISTING, *args)

    def get_apps(self, bundle_id: str = None):
        apps = self.call_application_listing("installedApplicationsMatching:registerUpdateToken:", {}, '')
        if bundle_id:
            return [x for x in apps if x.get('CFBundleIdentifier') == bundle_id]
        return apps



