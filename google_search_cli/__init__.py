import os
import sys
import socket
from cmd import Cmd
import json

try:
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
    from html.parser import HTMLParser
    from urllib.error import URLError
except:
    from urllib2 import Request, urlopen, URLError
    from urllib import urlencode
    from HTMLParser import HTMLParser


from .socks import PROXY_TYPE_SOCKS5, PROXY_TYPE_HTTP


def get(url, params=None):
    if params:
        url += '?' + urlencode(params)
    request = Request(url)
    request.add_header('Cache-Control', 'no-cache')
    try:
        response = urlopen(request)
    except URLError:
        sys.exit(1)
    result = response.read()
    if type(result) is not str:
        return result.decode()
    return result


def search(keywords, offset, limit):
    params = dict(v='1.0', start=offset, rsz=limit, q=keywords)
    url = 'http://ajax.googleapis.com/ajax/services/search/web'
    response = json.loads(get(url, params))
    if response['responseStatus'] != 200:
        print(error.format(response['responseDetails']))
        sys.exit(1)
    else:
        print_result(response['responseData']['results'])
        if 'resultCount' in response['responseData']['cursor']:
            print_pager(response['responseData']['cursor']['resultCount'],
                        offset, limit)
        else:
            print_not_found()


class Format:
    end = '\033[0m'

    def __init__(self, fg, bg=None, style=0):
        self.fg = fg
        self.bg = bg
        self.style = style

    def bold(self):
        self.style = 1
        return self

    def normal(self):
        self.style = 0
        return self

    def __str__(self):
        return self.color()

    def format(self, content):
        return self.color() + content + self.end

    def color(self):
        if self.bg:
            return "\033[%s;%s;%sm" % (self.style, self.fg, self.bg)
        else:
            return "\033[%s;%sm" % (self.style, self.fg)


title = Format(34)
url = Format(32)
content = Format(0)
error = Format(31)
pager = Format(33)

parser = HTMLParser()


def b2bold(line, color):
    line = line.replace('<b>', Format.end + color.bold().color())
    line = line.replace('</b>', Format.end + color.normal().color())
    return parser.unescape(line)


def print_result(results):
    for entry in results:
        print("\n" + title.format(b2bold(entry['title'], title)) + "\n")
        print(url.format(entry['unescapedUrl']))
        print(content.format(b2bold(entry['content'], content)))


def print_pager(total, offset, limit):
    print(pager.format("\nShowing %d to %d of %s Press RET for more\n" %
                       (offset + 1, offset + limit, total)))


def print_not_found():
    print(pager.format("\nNothing Found\n"))


def get_proxy_setting():
    proxy = os.getenv('SOCKS_SERVER', os.getenv('socks_server'))
    if proxy:
        return (PROXY_TYPE_SOCKS5, proxy)
    proxy = os.getenv('http_proxy', os.getenv('HTTP_PROXY'))
    if proxy:
        return (PROXY_TYPE_HTTP, proxy)


def setup_proxy(proxy_type, host, port):
    from .socks import setdefaultproxy, socksocket
    setdefaultproxy(proxy_type, host, port)
    socket.socket = socksocket


def setup_proxy_from_env():
    proxy = get_proxy_setting()
    if proxy:
        proxy_type, url = proxy
        host, port = url.split(':')
        setup_proxy(proxy_type, host, int(port))


class App(Cmd):
    limit = 4

    def default(self, arg):
        if arg == 'EOF':
            print('')
            sys.exit(0)
        search(arg, 0, self.limit)
        self.offset = self.limit

    def preloop(self):
        # print(pager.format('\nPowered by Google'))
        if len(sys.argv) > 1:
            keywords = ' '.join(sys.argv[1:])
            self.default(keywords)
            self.lastcmd = keywords

    def emptyline(self):
        if self.lastcmd:
            search(self.lastcmd, self.offset, self.limit)
            self.offset += self.limit

    def do_whoami(self, arg):
        "print your ip"
        if len(arg) == 0:
            print(get('http://ifconfig.me/ip'))


def run():
    setup_proxy_from_env()
    app = App()
    app.prompt = pager.format('> ')
    try:
        app.cmdloop()
    except KeyboardInterrupt:
        sys.exit(1)
