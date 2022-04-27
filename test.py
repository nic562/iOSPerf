import time
import threading

from ios_perf.instrument_server import InstrumentServer


class IosDevice(InstrumentServer):
    thread_event = threading.Event()


def _test(dv: IosDevice):
    print('current device::::', dv.get_system_info())

    app = 'com.midea.msmart.appstore'
    pid = dv.launch_app(app)
    print('launch app ::: ', pid)
    time.sleep(1)
    try:
        print('start network statistics:::', dv.start_network_statistics(pid))
        print('network statistics:', dv.get_network_statistics(pid))
        dv.start_sys_mon_tap_simple(callback=lambda x: print('tap::', x), pid_list=[pid])
    except KeyboardInterrupt:
        dv.thread_event.clear()

    print('waiting...')
    time.sleep(6)
    dv.stop_sys_mon_tap()
    dv.kill_app(pid)
    print('kill app::::', pid)


def test():
    dv = IosDevice().init()
    try:
        _test(dv)
    finally:
        dv.stop()


if __name__ == '__main__':
    test()
