from collections import OrderedDict
from json import JSONDecoder

from jinja2 import Template


def generate_readme():
    """
    This will create a README.md from the regexes.json and README.md.template file.
    """
    # render README to string
    readme_rendered = render_readme()

    # store it as README.md
    with open("README.md", "w") as output_file:
        output_file.write(readme_rendered)


def render_readme() -> str:
    with open("README.md.template") as template_file:
        template_content = template_file.read()

    regexes = read_regex_data()

    template = Template(template_content)
    return template.render(data=regexes, monster_regex=generate_monster_regex())


def generate_monster_regex() -> str:
    """
    Creates a monster regex that matches all of the profiles.
    :return: regex
    """
    regexes_qual = []
    regex_data = read_regex_data()
    for platform in regex_data:
        for type_ in regex_data[platform]:
            regex_ = regex_data[platform][type_]["regex"]
            regex_qual = "(?P<%s_%s>%s)" % (platform, type_, regex_)
            regexes_qual.append(regex_qual)
    return "\n|".join(regexes_qual)


def read_regex_data() -> dict:
    with open("regexes.json") as data_file:
        # ensure json/dict order is consistent below python 3.6
        # -> testing for correct readme won't fail
        customdecoder = JSONDecoder(object_pairs_hook=OrderedDict)
        regexes = customdecoder.decode(data_file.read())
    return regexes


if __name__ == "__main__":
    generate_readme()