import os
import urllib.parse
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

__QUICKTS_INIT = "https://tlmisi2.adp.com/adptlmqts/quickTS.aspx"
__QUICKTS_ACTION = "https://bgateway.adp.com/siteminderagent/forms/login.fcc"
__SMAGENTNAME = "tlmisi2-prod-dc2prisivag0013-1"


class _CustomSSLContextHTTPAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        ctx = requests.urllib3.util.create_urllib3_context()
        ctx.set_ciphers("ECDHE-RSA-AES256-SHA:ECDHE-RSA-AES128-GCM-SHA256")
        self.ssl_context = ctx
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = requests.urllib3.poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context,
        )


def quick_timestamp():
    return
    username = os.environ.get("ISTO_USERNAME")
    password = os.environ.get("ISTO_PASSWORD")
    if not username or not password:
        return

    tz = ZoneInfo("America/Chicago")
    now = datetime.now(tz=tz)

    # The offset expected by the form is minutes from UTC. And weirdly,
    # it expects POSITIVE numbers for timezones behind UTC and NEGATIVE
    # numbers for timezones ahead of UTC. Bass-ackwards, as they say.
    tzoffset = -(tz.utcoffset(now).total_seconds() / 60)
    timestamp = urllib.parse.quote_plus(now.strftime("%-m/%-d/%Y %-I:%M:%S %p"))
    retUrl = f"https://tlmisi2.adp.com/adptlmqts/Private/quickTSprivate.aspx?TimeZoneOffset={tzoffset}&TimeStamp={timestamp}&BrowserTime={timestamp}"

    session = requests.session()
    session.adapters.pop("https://", None)
    session.mount("https://", _CustomSSLContextHTTPAdapter())
    response = session.get(__QUICKTS_INIT)

    dom = BeautifulSoup(response.text, features="html.parser")

    retUrl = (
        dom.find(id="retURL").attrs.get("value")
        + f"TimeZoneOffset={tzoffset}"
        + f"&Timestamp={timestamp}&BrowserTime={timestamp}"
    )

    inputs = {
        node.attrs.get("name", ""): node.attrs.get("value", "")
        for node in dom.css.select('form[id="aspnetForm"] input')
    }

    inputs["ctl00$ContentPlaceHolderMain$TextboxUsername"] = username
    inputs["ctl00$ContentPlaceHolderMain$TextboxPassword"] = password
    inputs["USER"] = username
    inputs["PASSWORD"] = password
    inputs["smagentname"] = __SMAGENTNAME
    inputs["retURL"] = retUrl
    inputs["TARGET"] = retUrl

    r = session.post(
        __QUICKTS_ACTION,
        cookies=response.cookies,
        data=inputs,
        allow_redirects=False,
    )

    rr = session.get(
        retUrl,
        cookies=r.cookies,
    )

    # url = f"https://tlmisi2.adp.com/adptlmqts/Private/quickTSprivate.aspx?TimeZoneOffset={tzoffset}&TimeStamp={timestamp}&BrowserTime={timestamp}&USER={username}&PASSWORD={password}&smagentname={smagentname}"
