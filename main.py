#!/usr/bin/env python3
import datetime
from dateutil import relativedelta
import os
import yaml
import locale
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import gettext
import markdown

import jinja2
from jinja2 import Template
from dateutil.relativedelta import relativedelta
from babel.support import Translations

BASEDIR = os.path.dirname(os.path.realpath(__file__))
LOCALE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),"locale")
LOCALES=["en_US","fr_FR"]
_ = gettext.gettext

def location(location):
    return_string = ""
    if "city" in location and location["city"]:
        return_string = f"{location['city']}"

    if "region" in location and location["region"]:
        if return_string:
            return_string = f"{return_string}, {location['region']}"
        else:
            return_string = f"{location['region']}"

    if "country" in location and location["country"]:
        if return_string:
            return_string = f"{return_string}, {location['country']}"
        else:
            return_string = f"{location['country']}"
    return return_string


def iso_date(date):
    return datetime.date.fromisoformat(date)

def now_date():
    return datetime.datetime.now()

def format_date(date,str_format="%B %Y"):
    return date.strftime(str_format)

def relative_delta_date(end,start):
    return relativedelta(end, start)


@jinja2.contextfunction
def get_context(c):
        return c

def subs(string,context):
    return context[string]

def to_html(string):
    return markdown.markdown(string)

def to_latex(string):
    md = markdown.Markdown(extensions=['latex'])
    return md.convert(string)

def build_tex():
    latex_jinja_env = jinja2.Environment(
        extensions=['jinja2.ext.i18n','jinja2.ext.with_','jinja2.ext.loopcontrols'],
        block_start_string = '[%',
        block_end_string = '%]',
        variable_start_string = '[[',
        variable_end_string = ']]',
        comment_start_string = '[#',
        comment_end_string = '#]',
        trim_blocks = False,
        autoescape = False,
        loader = jinja2.FileSystemLoader(os.path.join(os.path.abspath(BASEDIR),"template","tex"))
    )
    latex_jinja_env.install_gettext_callables(
            gettext=gettext.gettext,
            ngettext=gettext.ngettext,
            newstyle=True
    )
    latex_jinja_env.globals['location'] = location
    latex_jinja_env.globals['format_date'] = format_date
    latex_jinja_env.globals['iso_date'] = iso_date
    latex_jinja_env.globals['now_date'] = now_date
    latex_jinja_env.globals['relative_delta_date'] = relative_delta_date
    latex_jinja_env.globals['subs'] = subs
    latex_jinja_env.globals['context'] = get_context
    latex_jinja_env.globals['to_latex'] = to_latex

    config=dict()
    curr_file = os.path.join(BASEDIR,"data","locale.yaml")
    with open(curr_file) as config_file:
        config.update(yaml.load(config_file, Loader=yaml.SafeLoader))

    for i_locale in config["locale"]:
        latex_jinja_env.globals['locale'] = i_locale["code"]
        config[i_locale["code"]] = dict()
        if os.path.isdir(os.path.join(BASEDIR,"data",i_locale)):
            for i_file in os.listdir(os.path.join(BASEDIR,"data",i_locale)):
                curr_file = os.path.join(BASEDIR,"data",i_locale,i_file)
                with open(curr_file) as config_file:
                    config[i_locale].update(yaml.load(config_file, Loader=yaml.SafeLoader))
            # Load the translations for the current locale
            translations = Translations.load(LOCALE_PATH, [i_locale])
            locale.setlocale(locale.LC_ALL, f"{i_locale}.UTF-8")
            latex_jinja_env.install_gettext_translations(translations)
            template = latex_jinja_env.get_template('resume.tex.j2')
            render = template.render(config[i_locale['code']])
            with open(os.path.join(BASEDIR,"tex",f"resume.{i_locale}.tex"),"w") as output_file:
                output_file.write(render)

def build_html():
    latex_jinja_env = jinja2.Environment(
        extensions=['jinja2.ext.i18n','jinja2.ext.with_','jinja2.ext.loopcontrols'],
        trim_blocks = False,
        autoescape = False,
        loader = jinja2.FileSystemLoader(os.path.join(os.path.abspath(BASEDIR),"template","html"))
    )
    latex_jinja_env.install_gettext_callables(
            gettext=gettext.gettext,
            ngettext=gettext.ngettext,
            newstyle=True
    )
    latex_jinja_env.globals['location'] = location
    latex_jinja_env.globals['format_date'] = format_date
    latex_jinja_env.globals['iso_date'] = iso_date
    latex_jinja_env.globals['now_date'] = now_date
    latex_jinja_env.globals['relative_delta_date'] = relative_delta_date
    latex_jinja_env.globals['subs'] = subs
    latex_jinja_env.globals['context'] = get_context
    latex_jinja_env.globals['to_html'] = to_html

    config=dict()
    all_locale = dict()
    curr_file = os.path.join(BASEDIR,"data","locale.yaml")
    with open(curr_file) as config_file:
        all_locale.update(yaml.load(config_file, Loader=yaml.SafeLoader))
    config = all_locale

    for i_locale in config["locale"]:
        latex_jinja_env.globals['locale'] = i_locale["code"]
        config[i_locale["code"]] = {
            "locale": i_locale,
            "all_locale": all_locale
        }
        output_dir = os.path.join(BASEDIR,"html",i_locale["code"])
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        if os.path.isdir(os.path.join(BASEDIR,"data",i_locale["code"])):
            for i_file in os.listdir(os.path.join(BASEDIR,"data",i_locale["code"])):
                curr_file = os.path.join(BASEDIR,"data",i_locale["code"],i_file)
                with open(curr_file) as config_file:
                    config[i_locale["code"]].update(yaml.load(config_file, Loader=yaml.SafeLoader))
            # Load the translations for the current locale
            translations = Translations.load(LOCALE_PATH, [i_locale["code"]])
            locale.setlocale(locale.LC_ALL, f"{i_locale['code']}.UTF-8")
            latex_jinja_env.install_gettext_translations(translations)
            template = latex_jinja_env.get_template('index.html.j2')
            render = template.render(config[i_locale['code']])
            with open(os.path.join(output_dir,f"index.html"),"w") as output_file:
                output_file.write(render)

            template = latex_jinja_env.get_template('404.html.j2')
            render = template.render(config[i_locale['code']])
            with open(os.path.join(output_dir,f"404.html"),"w") as output_file:
                output_file.write(render)


def main():
    #build_tex()
    build_html()

main()
