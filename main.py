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


def build_tex():
    latex_jinja_env = jinja2.Environment(
        extensions=['jinja2.ext.i18n','jinja2.ext.with_'],
        block_start_string = '[%',
        block_end_string = '%]',
        variable_start_string = '[[',
        variable_end_string = ']]',
        comment_start_string = '[#',
        comment_end_string = '#]',
        trim_blocks = False,
        autoescape = False,
        loader = jinja2.FileSystemLoader(os.path.join(os.path.abspath(BASEDIR),"tex","template"))
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

    for i_locale in LOCALES:
        config=dict()
        for i_file in os.listdir(os.path.join(BASDIR,"data",i_locale)):
            with open(i_file) as config_file:
                config.update(yaml.load(config_file, Loader=yaml.SafeLoader))
        # Load the translations for the current locale
        translations = Translations.load(LOCALE_PATH, [i_locale])
        locale.setlocale(locale.LC_ALL, f"{i_locale}.UTF-8")
        latex_jinja_env.install_gettext_translations(translations)
        template = latex_jinja_env.get_template('resume.tex.j2')
        render = template.render(config)
        with open(os.path.join(BASEDIR,"tex",f"resume.{i_locale}.tex"),"w") as output_file:
            output_file.write(render)

build_tex
