"""
NAPI helper functions for access_manager.views.search
"""
from concurrent import futures

from wgen.logger.stats import timed
from napiclient import NapiClient
from wgen.httpconn import HttpConnectionFactory

NAPI_TIMEOUT = 7


def napi_args(settings):
    """Napi args"""
    return [settings[key] for key in ('napi.url', 'napi.port', 'napi.user', 'napi.password')]


def napiclient_from_auth_token(auth_token, settings):
    """Return napi client"""
    url, port, user, password = napi_args(settings)
    factory = HttpConnectionFactory(url, port, user, password)
    http_conn = factory.get_connection(auth_token)
    return NapiClient(http_conn)


def napi_main(auth_token, settings, tracekey, staff_uid):
    """Napi call"""
    with timed(metric_name='edx-platform.common.djangoapps.third_party_auth.lib.search_napi.napi_main',
               tracekey=tracekey):
        napiclient = napiclient_from_auth_token(auth_token, settings)

        with futures.ThreadPoolExecutor(max_workers=3) as executor:
            webcalls = {
                "details": executor.submit(napiclient.staff_view, staff_uids=[staff_uid], tracekey=tracekey),
            }
            _, notdone = futures.wait(webcalls.values(), timeout=NAPI_TIMEOUT)
            if notdone:
                # http://docs.python.org/dev/library/concurrent.futures.html#concurrent.futures.wait
                raise Exception("napi")
            else:
                details = (fut.result() for _, fut in sorted(webcalls.items()))

        return list(details)
