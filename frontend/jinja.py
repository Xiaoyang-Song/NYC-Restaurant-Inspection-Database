import jinja2
from icecream import ic

if __name__ == '__main__':
    ic("jinja")
    ic(__name__)
    environment = jinja2.Environment()
    template = environment.from_string("Hello, {{ name }}!")
    template.render(name="World")
