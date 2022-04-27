import time
import sys

from ios_perf.instrument_server import InstrumentServer


class IosDevice(InstrumentServer):
    pass


def _test(dv: IosDevice, bundle_id: str):
    print('current device::::', dv.get_system_info())
    print('get match time:', dv.get_match_time_info())

    pid = dv.launch_app(bundle_id)
    print('launch app ::: ', pid)
    time.sleep(1)
    print('execute path:', dv.get_process_execute_name(pid))
    print('start network statistics:::', dv.start_network_statistics(pid))
    print('network statistics:', dv.get_network_statistics(pid))
    dv.start_sys_mon_tap_simple(callback=lambda x: print('tap::', x), pid_list=[pid])
    dv.start_gpu_fps(callback=lambda x: print('fps:::', x))

    print('waiting...')
    time.sleep(6)
    dv.stop_sys_mon_tap()
    dv.kill_app(pid)
    print('kill app::::', pid)


def test(bundle_id: str):
    dv = IosDevice().init()
    try:
        _test(dv, bundle_id)
    finally:
        dv.stop()


if __name__ == '__main__':
    test(sys.argv[1])
