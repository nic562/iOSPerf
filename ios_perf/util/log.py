from logging import getLogger, StreamHandler, INFO, Formatter


default_stream_handler = StreamHandler()
default_stream_handler.setLevel(INFO)
default_stream_handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))


def get_log(name: str = ''):
    lg = getLogger(f'iOsPerf{name and f":{name}" or ""}')
    lg.addHandler(default_stream_handler)
    return lg


default = get_log()
