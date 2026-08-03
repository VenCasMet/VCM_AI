from difflib import SequenceMatcher


class BrowserAgent:

    def __init__(self, browser):

        self.browser = browser

    def similarity(self, a, b):

        if a is None:
            a = ""

        if b is None:
            b = ""

        return SequenceMatcher(

            None,

            str(a).lower(),

            str(b).lower()

        ).ratio()

    def _best_match(self, target, items, fields):

        best = None

        best_score = 0

        target = target.lower()

        for item in items:

            values = []

            for field in fields:

                value = item.get(field)

                if value:

                    values.append(str(value))

            candidate = " ".join(values)

            score = self.similarity(

                target,

                candidate

            )

            if target in candidate.lower():

                score += 0.25

            if score > best_score:

                best_score = score

                best = item

        return best

    def find_best_link(self, target):

        ok, links = self.browser.get_links()

        if not ok:

            return None

        return self._best_match(

            target,

            links,

            [

                "text",

                "aria",

                "title",

                "href"

            ]

        )

    def find_best_button(self, target):

        ok, buttons = self.browser.get_buttons()

        if not ok:

            return None

        return self._best_match(

            target,

            buttons,

            [

                "text",

                "aria",

                "title"

            ]

        )

    def find_best_input(self, target):

        ok, inputs = self.browser.get_inputs()

        if not ok:

            return None

        return self._best_match(

            target,

            inputs,

            [

                "placeholder",

                "aria",

                "name",

                "type"

            ]

        )
    def click_best_link(self, target):

        link = self.find_best_link(target)

        if link is None:

            return False, "No matching link found."

        text = link.get("text")

        if text:

            return self.browser.click_link(text)

        href = link.get("href")

        if href:

            return self.browser.goto(href)

        return False, "Unable to click link."

    def click_best_button(self, target):

        button = self.find_best_button(target)

        if button is None:

            return False, "No matching button found."

        text = button.get("text")

        if text:

            return self.browser.click_button(text)

        aria = button.get("aria")

        if aria:

            return self.browser.click_button(aria)

        return False, "Unable to click button."

    def fill_best_input(self, target, value):

        field = self.find_best_input(target)

        if field is None:

            return False, "No matching input found."

        keyword = (

            field.get("name")

            or field.get("placeholder")

            or field.get("aria")

            or ""

        )

        return self.browser.fill_best_input(

            keyword,

            value

        )

    def select_dropdown(self, target, value):

        return self.browser.select_dropdown(

            target,

            value

        )

    def check_checkbox(self, target):

        return self.browser.check_checkbox(

            target

        )

    def uncheck_checkbox(self, target):

        return self.browser.uncheck_checkbox(

            target

        )

    def select_radio(self, target):

        return self.browser.select_radio(

            target

        )

    def read_headings(self):

        return self.browser.read_headings()

    def read_tables(self):

        return self.browser.read_tables()

    def read_images(self):

        return self.browser.read_images()

    def click_first_link(self):

        ok, links = self.browser.get_links()

        if not ok or not links:

            return False, "No links found."

        text = links[0].get("text")

        if text:

            return self.browser.click_link(text)

        href = links[0].get("href")

        if href:

            return self.browser.goto(href)

        return False, "Unable to click first link."

    def click_link_index(self, index):

        ok, links = self.browser.get_links()

        if not ok:

            return False, "Unable to read links."

        if index < 0 or index >= len(links):

            return False, "Link index out of range."

        text = links[index].get("text")

        if text:

            return self.browser.click_link(text)

        href = links[index].get("href")

        if href:

            return self.browser.goto(href)

        return False, "Unable to click link."

    def click_first_button(self):

        ok, buttons = self.browser.get_buttons()

        if not ok or not buttons:

            return False, "No buttons found."

        text = buttons[0].get("text")

        if not text:

            return False, "Button has no visible text."

        return self.browser.click_button(text)

    def click_button_index(self, index):

        ok, buttons = self.browser.get_buttons()

        if not ok:

            return False, "Unable to read buttons."

        if index < 0 or index >= len(buttons):

            return False, "Button index out of range."

        text = buttons[index].get("text")

        if not text:

            return False, "Button has no visible text."

        return self.browser.click_button(text)

    def read_page(self):

        return self.browser.read_page()

    def read_links(self):

        return self.browser.get_links()

    def read_buttons(self):

        return self.browser.get_buttons()

    def read_inputs(self):

        return self.browser.get_inputs()