from App import WebSite
from config import *


if __name__ == '__main__':
    site = WebSite(__name__)
    site.run(host=host, port=port, debug=debug)
