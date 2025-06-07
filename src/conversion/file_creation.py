import re, os
from conversion import *


TITLE_PLACEHOLDER = r"{{ Title }}"
CONTENT_PLACEHOLDER = r"{{ Content }}"


def extract_title(markdown):
    if not re.search(r'^# ', markdown):
        raise Exception("The first line in the markdown file must start with \"# \"!")
    
    return markdown.split("\n\n")[0].lstrip("# ").strip()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if os.path.isfile(dir_path_content):
        root, extension = os.path.splitext(dir_path_content)
        if extension == ".md":
            dest_root, _ = os.path.splitext(dest_dir_path)
            dest_file = dest_root + ".html"
            print(f"Copying {dir_path_content} ---> {dest_file}")
            generate_page(dir_path_content, template_path, dest_file, basepath)

    else:
        if not os.path.exists(dest_dir_path):
            print(f"Directory does not exist: {dest_dir_path}")
            os.mkdir(dest_dir_path)
        for item in os.listdir(dir_path_content):
            source = os.path.join(dir_path_content, item)
            destination = os.path.join(dest_dir_path, item)
            print(f"New source to destination: {source} ---> {destination}")
            generate_pages_recursive(source, template_path, destination, basepath)


def generate_page(from_path, template_path, dest_path, basepath):
    print(F"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown, template = "", ""
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    
    title = extract_title(markdown)
    # print(f"Title: {title}\n")
    # print(f"-----Content (Original Markdown)-----\n\n{markdown}\n")
    node = markdown_to_html_node(markdown).to_html()

    # print("Editing template.html with the title and HTML content above...\n")
    print(f"Replacing root dir with {basepath}")
    generated_html = template.replace(TITLE_PLACEHOLDER, title)\
                             .replace(CONTENT_PLACEHOLDER, node)\
                             .replace(r'href="/', rf'href="{basepath}')\
                             .replace(r'src="/', rf'src="{basepath}')
    # print(generated_html)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.mkdir(os.path.dirname(dest_path))
    with open(dest_path, "x") as file:
        file.write(generated_html)