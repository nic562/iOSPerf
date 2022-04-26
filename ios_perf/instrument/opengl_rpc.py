import abc

from ..util.log import default as log
from ..util.gpu_decode import JSEvn, TraceData
from ..component.base_rpc import BaseRpc
from ..component.dtx_msg import RawInt64sl, RawInt32sl


class OpenGLRpc(BaseRpc, metaclass=abc.ABCMeta):
    CHANNEL_OPENGL = "com.apple.instruments.server.services.graphics.opengl"  # 获取 FPS

    # _selector
    # - startSamplingAtTimeInterval:processIdentifier:
    # - startSamplingAtTimeInterval:
    # - availableStatistics
    # - driverNames
    # - valueForSwitch:
    # - setValue: forSwitchName:
    # - setSamplingRate:
    # - stopSampling
    # - cleanup

    CHANNEL_GPU = 'com.apple.instruments.server.services.gpu'

    def call_opengl(self, *args):
        return self.get_call_result(self.CHANNEL_OPENGL, *args)

    def call_gpu(self, *args):
        return self.get_call_result(self.CHANNEL_GPU, *args)

    def start_opengl_sampling(self, callback: callable, interval_ms: int = 1000):
        self.register_channel_callback(self.CHANNEL_OPENGL, callback)
        log.info('openGL availableStatistics: %s', self.call_opengl("availableStatistics"))
        log.info('openGL driverNames: %s', self.call_opengl("driverNames"))
        self.call_opengl("setSamplingRate:", interval_ms / 100.0)
        return self.call_opengl("startSamplingAtTimeInterval:", 0.0)

    def stop_opengl_sampling(self):
        self.call_opengl("stopSampling")

    def start_gpu_counter(self, callback: callable):
        self.register_undefined_callback(callback)
        info = self.call_gpu('requestDeviceGPUInfo')[0]
        interval = info.get('min-collection-interval')
        self.call_gpu("configureCounters:counterProfile:interval:windowLimit:tracingPID:",
                      RawInt64sl(interval, 3, 1, 0), RawInt32sl(-1))
        self.call_gpu('startCollectingCounters')

    def stop_gpu_counter(self, js_env: JSEvn = None):
        self.call_gpu('stopCollectingCounters')
        data = self.call_gpu('flushRemainingData')
        if js_env:
            return js_env.dump_trace(TraceData(*(data[0])))
        return data

    def start_gpu_fps(self, callback: callable):
        self.register_channel_callback(self.CHANNEL_OPENGL, callback)
        self.call_opengl("startSamplingAtTimeInterval:", 0.0)

    def stop_gpu_fps(self):
        self.call_opengl("stopSampling")
