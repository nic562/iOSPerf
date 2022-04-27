import abc

from ..component.base_rpc import BaseRpc


class OthersRpc(BaseRpc, metaclass=abc.ABCMeta):
    CHANNEL_SCREEN_SHOT = 'com.apple.instruments.server.services.screenshot'  # 获取画面
    # _selector
    # - takeScreenshot

    CHANNEL_POWER = 'com.apple.instruments.server.services.power'

    CHANNEL_ENERGY = 'com.apple.xcode.debug-gauge-data-providers.Energy'

    CHANNEL_CONDITION_INDUCER = "com.apple.instruments.server.services.ConditionInducer"  # 控制手机，比如网络，手机状态

    # - availableConditionInducers
    # - disableActiveCondition
    # - disableConditionWithIdentifier:
    # - enableConditionWithIdentifier: profileIdentifier:

    def call_power(self, *args):
        return self.get_call_result(self.CHANNEL_POWER, *args)

    def call_energy(self, *args):
        return self.get_call_result(self.CHANNEL_ENERGY, *args)

    def call_condition(self, *args):
        return self.get_call_result(self.CHANNEL_CONDITION_INDUCER, *args)

    def get_screenshot(self):
        return self.get_call_result(self.CHANNEL_SCREEN_SHOT, "takeScreenshot")

    def start_power_stream_transfer(self, callback: callable):
        self.register_channel_callback(self.CHANNEL_POWER, callback)
        stream_num = float(self.call_power("openStreamForPath:", "live/level.dat"))
        return self.call_power("startStreamTransfer:", stream_num), stream_num

    def stop_power_stream_transfer(self, stream_num: float):
        self.call_power('endStreamTransfer:', stream_num)

    def start_energy_sampling(self, pid: int):
        return self.call_energy("startSamplingForPIDs:", {str(pid)})

    def get_energy_sampling(self, pid: int):
        return self.call_energy("sampleAttributes:forPIDs:", {}, {str(pid)})

    def get_condition_inducer(self):
        """获取网络配置参数"""
        return self.call_condition("availableConditionInducers")

    def set_condition_inducer(self,
                              condition_identifier,
                              profile_identifier):
        """设置手机状态，模拟网络，手机压力数据等
        :param condition_identifier:
        :param profile_identifier:
        :return:
        """
        return self.call_condition('enableConditionWithIdentifier:profileIdentifier:',
                                   condition_identifier, profile_identifier)

    def disable_condition_inducer(self):
        """ 关闭手机状态，模拟网络，手机压力数据等
        """
        return self.call_condition('disableActiveCondition')
