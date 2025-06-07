import re, os
from conversion import *


TITLE_PLACEHOLDER = r"{{ Title }}"
CONTENT_PLACEHOLDER = r"{{ Content }}"


def extract_title(markdown):
    if not re.search(r'^# ', markdown):
        raise Exception("The first line in the markdown file must start with \"# \"!")
    
    # TODO: optimize so you are not splitting and re-joining the markdown
    split_md = markdown.split("\n\n")
    return split_md[0].lstrip("# ").strip(), "\n\n".join(split_md[1:]) if len(split_md) > 1 else ""



def generate_page(from_path, template_path, dest_path):
    print(F"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown, template = "", ""
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    
    title, content = extract_title(markdown)
    print(f"Title: {title}\n")
    print(f"-----Content (Original Markdown)-----\n\n{content}\n")
    node = markdown_to_html_node(content).to_html()

    print("Editing template.html with the title and HTML content above...\n")
    generated_html = template.replace(TITLE_PLACEHOLDER, title)\
                             .replace(CONTENT_PLACEHOLDER, node)
    print(generated_html)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.mkdirs(os.path.dirname(dest_path))
    with open(dest_path, "x") as file:
        file.write(generated_html)