from playwright.sync_api import sync_playwright
import os
import re


class BrowserTools:

    def __init__(self):

        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

        self.started = False

        self.browser_type = "brave"

        self.brave_path = self.find_brave()

        self.chrome_path = self.find_chrome()

    def find_brave(self):

        paths = [

            r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",

            r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe"

        ]

        for path in paths:

            if os.path.exists(path):

                return path

        return None

    def find_chrome(self):

        paths = [

            r"C:\Program Files\Google\Chrome\Application\chrome.exe",

            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

        ]

        for path in paths:

            if os.path.exists(path):

                return path

        return None

    def start_browser(self, browser="brave", headless=False):

        if self.started:

            return True, "Browser already running."

        executable = None

        if browser.lower() == "brave":

            executable = self.brave_path

        elif browser.lower() == "chrome":

            executable = self.chrome_path

        if executable is None:

            return False, f"{browser} not installed."

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(

            executable_path=executable,

            headless=headless

        )

        self.context = self.browser.new_context(

            viewport={

                "width": 1400,

                "height": 900

            }

        )

        self.page = self.context.new_page()

        self.started = True

        self.browser_type = browser.lower()

        return True, f"{browser.title()} launched."

    def ensure_browser(self):

        if self.started:

            return True

        ok, _ = self.start_browser(self.browser_type)

        return ok

    def goto(self, url):

        if not self.ensure_browser():

            return False, "Browser not running."

        try:

            if not url.startswith("http"):

                url = "https://" + url

            self.page.goto(

                url,

                wait_until="networkidle"

            )

            self.page.wait_for_timeout(1000)

            return True, f"Opened {url}"

        except Exception as e:

            return False, str(e)

    def google_search(self, query):

        url = "https://www.google.com/search?q=" + query.replace(" ", "+")

        return self.goto(url)

    def youtube_search(self, query):

        url = "https://www.youtube.com/results?search_query=" + query.replace(" ", "+")

        return self.goto(url)

    def back(self):

        try:

            self.page.go_back()

            return True, "Went back."

        except Exception as e:

            return False, str(e)

    def forward(self):

        try:

            self.page.go_forward()

            return True, "Went forward."

        except Exception as e:

            return False, str(e)

    def refresh(self):

        try:

            self.page.reload(

                wait_until="domcontentloaded"

            )

            return True, "Page refreshed."

        except Exception as e:

            return False, str(e)

    def new_tab(self):

        try:

            self.page = self.context.new_page()

            return True, "New tab opened."

        except Exception as e:

            return False, str(e)

    def close_tab(self):

        try:

            self.page.close()

            pages = self.context.pages

            if pages:

                self.page = pages[-1]

            return True, "Tab closed."

        except Exception as e:

            return False, str(e)

    def current_url(self):

        try:

            return True, self.page.url

        except Exception as e:

            return False, str(e)

    def page_title(self):

        try:

            return True, self.page.title()

        except Exception as e:

            return False, str(e)

    def click(self, selector, timeout=10000):

        try:

            self.page.wait_for_selector(

                selector,

                timeout=timeout

            )

            self.page.click(selector)

            return True, f"Clicked {selector}"

        except Exception as e:

            return False, str(e)

    def click_text(self, text):

        try:

            self.page.get_by_text(

                text,

                exact=False

            ).first.click(

                timeout=5000

            )

            return True, f"Clicked '{text}'"

        except Exception as e:

            return False, str(e)

    def click_link(self, text):

        try:

            self.page.get_by_role(

                "link",

                name=text

            ).first.click()

            return True, f"Clicked link '{text}'"

        except Exception as e:

            return False, str(e)

    def click_button(self, text):

        try:

            self.page.get_by_role(

                "button",

                name=text

            ).first.click()

            return True, f"Clicked button '{text}'"

        except Exception as e:

            return False, str(e)

    def click_first(self, selector):

        try:

            self.page.locator(selector).first.click()

            return True, "Clicked first element."

        except Exception as e:

            return False, str(e)

    def click_last(self, selector):

        try:

            self.page.locator(selector).last.click()

            return True, "Clicked last element."

        except Exception as e:

            return False, str(e)

    def click_index(self, selector, index):

        try:

            self.page.locator(selector).nth(index).click()

            return True, f"Clicked element {index}"

        except Exception as e:

            return False, str(e)

    def fill(self, selector, value):

        try:

            self.page.locator(

                selector

            ).fill(value)

            return True, "Text entered."

        except Exception as e:

            return False, str(e)

    def type_text(self, selector, value):

        try:

            self.page.locator(

                selector

            ).type(value)

            return True, "Typed."

        except Exception as e:

            return False, str(e)

    def fill_best_input(self, keyword, value):

        if not self.ensure_browser():

            return False, "Browser not running."

        try:

            keyword = keyword.lower()

            inputs = self.page.locator("input").all()

            for inp in inputs:

                try:

                    name = (inp.get_attribute("name") or "").lower()

                    placeholder = (inp.get_attribute("placeholder") or "").lower()

                    aria = (inp.get_attribute("aria-label") or "").lower()

                    if keyword in name or keyword in placeholder or keyword in aria:

                        inp.fill(value)

                        return True, f"Entered '{value}'"

                except:

                    pass

            return False, "Input not found."

        except Exception as e:

            return False, str(e)

    def press(self, key):

        try:

            self.page.keyboard.press(key)

            return True, f"Pressed {key}"

        except Exception as e:

            return False, str(e)

    def scroll_down(self, pixels=800):

        try:

            self.page.mouse.wheel(

                0,

                pixels

            )

            return True, "Scrolled down."

        except Exception as e:

            return False, str(e)

    def scroll_up(self, pixels=800):

        try:

            self.page.mouse.wheel(

                0,

                -pixels

            )

            return True, "Scrolled up."

        except Exception as e:

            return False, str(e)

    def select_dropdown(self, keyword, value):

        if not self.ensure_browser():
            return False, "Browser not running."

        try:

            keyword = keyword.lower()

            selects = self.page.locator("select").all()

            for sel in selects:

                try:

                    name = (sel.get_attribute("name") or "").lower()
                    aria = (sel.get_attribute("aria-label") or "").lower()

                    if keyword in name or keyword in aria:

                        try:

                            sel.select_option(label=value)

                        except:

                            sel.select_option(value=value)

                        return True, f"Selected '{value}'"

                except:
                    pass

            return False, "Dropdown not found."

        except Exception as e:

            return False, str(e)

    def check_checkbox(self, keyword):

        if not self.ensure_browser():
            return False, "Browser not running."

        try:

            keyword = keyword.lower()

            boxes = self.page.locator("input[type='checkbox']").all()

            for box in boxes:

                try:

                    name = (box.get_attribute("name") or "").lower()
                    aria = (box.get_attribute("aria-label") or "").lower()

                    if keyword in name or keyword in aria:

                        if not box.is_checked():

                            box.check()

                        return True, "Checkbox checked."

                except:
                    pass

            return False, "Checkbox not found."

        except Exception as e:

            return False, str(e)

    def uncheck_checkbox(self, keyword):

        if not self.ensure_browser():
            return False, "Browser not running."

        try:

            keyword = keyword.lower()

            boxes = self.page.locator("input[type='checkbox']").all()

            for box in boxes:

                try:

                    name = (box.get_attribute("name") or "").lower()
                    aria = (box.get_attribute("aria-label") or "").lower()

                    if keyword in name or keyword in aria:

                        if box.is_checked():

                            box.uncheck()

                        return True, "Checkbox unchecked."

                except:
                    pass

            return False, "Checkbox not found."

        except Exception as e:

            return False, str(e)

    def select_radio(self, keyword):

        if not self.ensure_browser():
            return False, "Browser not running."

        try:

            keyword = keyword.lower()

            radios = self.page.locator("input[type='radio']").all()

            for radio in radios:

                try:

                    name = (radio.get_attribute("name") or "").lower()
                    value = (radio.get_attribute("value") or "").lower()
                    aria = (radio.get_attribute("aria-label") or "").lower()

                    if keyword in name or keyword in value or keyword in aria:

                        radio.check()

                        return True, "Radio selected."

                except:
                    pass

            return False, "Radio button not found."

        except Exception as e:

            return False, str(e)

    def read_page(self):

        if not self.ensure_browser():
            return False, "Browser not running."

        try:

            return True, self.page.locator("body").inner_text()

        except Exception as e:

            return False, str(e)

    def contains_text(self, text):

        if not self.ensure_browser():
            return False, False

        try:

            body = self.page.locator("body").inner_text()

            return True, text.lower() in body.lower()

        except Exception as e:

            return False, str(e)

    def read_headings(self):

        if not self.ensure_browser():
            return False, []

        try:

            data = []

            for tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:

                items = self.page.locator(tag).all()

                for item in items:

                    text = item.inner_text().strip()

                    if text:

                        data.append(text)

            return True, data

        except Exception as e:

            return False, str(e)

    def read_tables(self):

        if not self.ensure_browser():
            return False, []

        try:

            tables = []

            all_tables = self.page.locator("table").all()

            for table in all_tables:

                rows = []

                tr_list = table.locator("tr").all()

                for tr in tr_list:

                    cols = []

                    cells = tr.locator("th,td").all()

                    for cell in cells:

                        cols.append(cell.inner_text().strip())

                    if cols:

                        rows.append(cols)

                if rows:

                    tables.append(rows)

            return True, tables

        except Exception as e:

            return False, str(e)

    def read_images(self):

        if not self.ensure_browser():
            return False, []

        try:

            data = []

            images = self.page.locator("img").all()

            for img in images:

                try:

                    data.append({

                        "alt": img.get_attribute("alt"),

                        "title": img.get_attribute("title"),

                        "src": img.get_attribute("src")

                    })

                except:
                    pass

            return True, data

        except Exception as e:

            return False, str(e)

    def get_links(self):

        if not self.ensure_browser():
            return False, []

        try:

            data = []

            links = self.page.locator("a").all()

            for link in links:

                try:

                    text = (link.inner_text() or "").strip()

                    aria = link.get_attribute("aria-label")

                    title = link.get_attribute("title")

                    href = link.get_attribute("href")

                    data.append({

                        "text": text,

                        "aria": aria,

                        "title": title,

                        "href": href

                    })

                except:
                    pass

            return True, data

        except Exception as e:

            return False, str(e)

    def get_buttons(self):

        if not self.ensure_browser():
            return False, []

        try:

            data = []

            buttons = self.page.locator("button").all()

            for btn in buttons:

                try:

                    data.append({

                        "text": (btn.inner_text() or "").strip(),

                        "aria": btn.get_attribute("aria-label"),

                        "title": btn.get_attribute("title")

                    })

                except:
                    pass

            return True, data

        except Exception as e:

            return False, str(e)

    def get_inputs(self):

        if not self.ensure_browser():
            return False, []

        try:

            data = []

            inputs = self.page.locator("input").all()

            for inp in inputs:

                try:

                    data.append({

                        "name": inp.get_attribute("name"),

                        "type": inp.get_attribute("type"),

                        "placeholder": inp.get_attribute("placeholder"),

                        "aria": inp.get_attribute("aria-label"),

                        "value": inp.input_value()

                    })

                except:
                    pass

            return True, data

        except Exception as e:

            return False, str(e)
    def wait_for_element(self, selector, timeout=10000):

        if not self.ensure_browser():
            return False, "Browser not running."

        try:

            self.page.wait_for_selector(

                selector,

                timeout=timeout

            )

            return True, "Element found."

        except Exception as e:

            return False, str(e)

    def screenshot(self, filename="browser_screenshot.png"):

        if not self.ensure_browser():
            return False, "Browser not running."

        try:

            self.page.screenshot(

                path=filename,

                full_page=True

            )

            return True, filename

        except Exception as e:

            return False, str(e)

    def download(self, selector):

        if not self.ensure_browser():
            return False, "Browser not running."

        try:

            with self.page.expect_download() as download_info:

                self.page.click(selector)

            download = download_info.value

            return True, download.path()

        except Exception as e:

            return False, str(e)

    def upload(self, selector, filepath):

        if not self.ensure_browser():
            return False, "Browser not running."

        try:

            self.page.set_input_files(

                selector,

                filepath

            )

            return True, "Uploaded."

        except Exception as e:

            return False, str(e)

    def close_browser(self):

        if not self.started:

            return True, "Browser already closed."

        try:

            if self.page is not None:

                self.page.close()

            if self.context is not None:

                self.context.close()

            if self.browser is not None:

                self.browser.close()

            if self.playwright is not None:

                self.playwright.stop()

        except Exception as e:

            return False, str(e)

        self.page = None
        self.context = None
        self.browser = None
        self.playwright = None
        self.started = False

        return True, "Browser closed."

    def wait(self, milliseconds=1000):

        if not self.ensure_browser():
            return False, "Browser not running."

        try:

            self.page.wait_for_timeout(milliseconds)

            return True, "Done."

        except Exception as e:

            return False, str(e)

    def press_enter(self):

        if not self.ensure_browser():
            return False, "Browser not running."

        try:

            self.page.keyboard.press("Enter")

            return True, "Enter pressed."

        except Exception as e:

            return False, str(e)

    def current_page_text(self):

        if not self.ensure_browser():
            return False, ""

        try:

            return True, self.page.locator("body").inner_text()

        except Exception as e:

            return False, str(e)

    def current_page_html(self):

        if not self.ensure_browser():
            return False, ""

        try:

            return True, self.page.content()

        except Exception as e:

            return False, str(e)

    def search_google_box(self, query):

        if not self.ensure_browser():
            return False, "Browser not running."

        try:

            box = self.page.locator("textarea[name='q'], input[name='q']").first

            box.fill(query)

            box.press("Enter")

            self.page.wait_for_load_state("networkidle")

            return True, f"Searched '{query}'"

        except Exception as e:

            return False, str(e)

    def search_youtube_box(self, query):

        if not self.ensure_browser():

            return False, "Browser not running."

        try:

            self.page.goto(

                "https://www.youtube.com",

                wait_until="networkidle"

            )

            self.page.wait_for_timeout(1000)

            selectors = [

                "input#search",

                "input[name='search_query']",

                "input[placeholder*='Search']"

            ]

            box = None

            for selector in selectors:

                locator = self.page.locator(selector)

                if locator.count() > 0:

                    box = locator.first

                    break

            if box is None:

                return False, "Search box not found."

            box.click()

            box.fill(query)

            box.press("Enter")

            self.page.wait_for_load_state("networkidle")

            return True, f"Searched '{query}'"

        except Exception as e:

            return False, str(e)

    def __del__(self):

        try:

            self.close_browser()

        except:

            pass