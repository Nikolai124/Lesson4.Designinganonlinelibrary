import json
import os


from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html') 
    with open("book_info.json", "r", encoding='utf8') as file:
        books = json.load(file)
    os.makedirs("pages", exist_ok=True)
    book_on_page = 10
    books_pages = list(chunked(books, book_on_page))
    for number, book_page in enumerate(books_pages):
        rendered_page = template.render(
            books=book_page,
            number_pages = len(books_pages),
            current_page = number + 1
        )
        with open(f'./pages/index{number + 1}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)
on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.', default_filename='./pages/index1.html')