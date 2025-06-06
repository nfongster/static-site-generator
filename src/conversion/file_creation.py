import re


def extract_title(markdown):
    if not re.match(r'^# ', markdown):
        raise Exception("The first line in the markdown file must start with \"# \"!")

    return markdown.split("\n\n")[0].lstrip("# ").strip()