import abc
import typing

from .dtx_msg import DTXMessage


class BaseRpc(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def call(self, channel: str, selector: str, *args) -> DTXMessage:
        raise NotImplementedError

    def register_channel_callback(self, channel: str, callback: typing.Callable):
        raise NotImplementedError

    def register_undefined_callback(self, callback: typing.Callable):
        raise NotImplementedError

    def get_call_result(self, channel: str, selector: str, *args):
        rs = self.call(channel, selector, *args).selector
        if isinstance(rs, dict):
            if rs.get('$class') == 'NSError':
                raise ValueError(rs)
        return rs

