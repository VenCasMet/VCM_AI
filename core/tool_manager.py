from typing import Dict, Callable, Any


class ToolManager:

    def __init__(self):

        self.tools: Dict[str, Callable] = {}

        self.categories = {}

    #########################################################
    # Register Tool
    #########################################################

    def register(

        self,

        name: str,

        func: Callable,

        category: str = "General"

    ):

        self.tools[name] = func

        if category not in self.categories:

            self.categories[category] = []

        self.categories[category].append(name)

    #########################################################
    # Remove Tool
    #########################################################

    def unregister(self, name):

        if name in self.tools:

            del self.tools[name]

        for cat in self.categories.values():

            if name in cat:

                cat.remove(name)

    #########################################################
    # Check Tool
    #########################################################

    def has_tool(self, name):

        return name in self.tools

    #########################################################
    # Execute Tool
    #########################################################

    def execute(

        self,

        tool_name,

        *args,

        **kwargs

    ):

        if tool_name not in self.tools:

            return (

                False,

                f"Tool '{tool_name}' not registered."

            )

        try:

            return self.tools[tool_name](

                *args,

                **kwargs

            )

        except Exception as e:

            return (

                False,

                str(e)

            )

    #########################################################
    # Registered Tools
    #########################################################

    def list_tools(self):

        return sorted(

            self.tools.keys()

        )

    #########################################################
    # Categories
    #########################################################

    def list_categories(self):

        return self.categories

        #########################################################
    # Tool Information
    #########################################################

    def tool_info(self, tool_name):

        if tool_name not in self.tools:

            return None

        return {

            "name": tool_name,

            "callable": self.tools[tool_name],

            "category": self.get_category(tool_name)

        }

    #########################################################
    # Get Tool Category
    #########################################################

    def get_category(self, tool_name):

        for category, tools in self.categories.items():

            if tool_name in tools:

                return category

        return "Unknown"

    #########################################################
    # Search Tool
    #########################################################

    def search_tools(self, keyword):

        keyword = keyword.lower()

        results = []

        for tool in self.tools.keys():

            if keyword in tool.lower():

                results.append(tool)

        return sorted(results)

    #########################################################
    # Execute Multiple Tools
    #########################################################

    def execute_many(self, commands):

        """
        commands = [
            ("browser.open_url", ["https://google.com"], {}),
            ("browser.google_search", ["Real Madrid"], {})
        ]
        """

        outputs = []

        for tool_name, args, kwargs in commands:

            outputs.append(

                self.execute(

                    tool_name,

                    *args,

                    **kwargs

                )

            )

        return outputs

    #########################################################
    # Clear All Tools
    #########################################################

    def clear(self):

        self.tools.clear()

        self.categories.clear()

    #########################################################
    # Total Tools
    #########################################################

    def count(self):

        return len(self.tools)

    #########################################################
    # Pretty Print
    #########################################################

    def __str__(self):

        output = []

        output.append("========== Tool Manager ==========")

        for category in sorted(self.categories.keys()):

            output.append(f"\n[{category}]")

            for tool in sorted(self.categories[category]):

                output.append(f"  • {tool}")

        output.append(

            f"\nTotal Tools : {self.count()}"

        )

        return "\n".join(output)