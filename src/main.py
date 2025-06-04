from nodes import *

def main():
    text = "This is some anchor text"
    text_type = TextType.LINK
    url = "https://www.boot.dev"

    node = TextNode(text, text_type, url)
    print(node)


if __name__ == '__main__':
    main()