import threading, http.server, os, time
from playwright.sync_api import sync_playwright

os.chdir(r'c:/Users/Paul/Coding/havenshine-Gambia.solar')

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

httpd = http.server.HTTPServer(('localhost', 8746), Handler)
t = threading.Thread(target=httpd.serve_forever)
t.daemon = True
t.start()
time.sleep(0.5)

with sync_playwright() as p:
    browser = p.chromium.launch()

    # Desktop
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    page.goto('http://localhost:8746/', wait_until='networkidle', timeout=15000)
    page.screenshot(path=r'.claude/screenshot_desktop.png')
    page.close()

    # Mobile - closed
    page2 = browser.new_page(viewport={'width': 390, 'height': 844})
    page2.goto('http://localhost:8746/', wait_until='networkidle', timeout=15000)
    page2.screenshot(path=r'.claude/screenshot_mobile_closed.png')

    # Mobile - sidebar open
    page2.click('#nav-dots-btn')
    page2.wait_for_timeout(500)
    page2.screenshot(path=r'.claude/screenshot_mobile_open.png')

    browser.close()

httpd.shutdown()
print('done')
