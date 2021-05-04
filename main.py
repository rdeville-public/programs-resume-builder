#!/usr/bin/env python3
#
#import jinja2
#from jinja2 import Environment, FileSystemLoader
#
import datetime
from dateutil import relativedelta
import os
import yaml
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import gettext
_ = gettext.gettext

#
#env = Environment(
#    loader=FileSystemLoader('templates')
#)
#
##
##TEMPLATE = os.path.join(BASEDIR,"templates","index.html.j2")
##J2_TEMPLATE = env.get_template("index.html.j2")
##




import jinja2
import os
from dateutil.relativedelta import relativedelta
from jinja2 import Template
from babel.support import Translations

LOCALE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),"locale")
LOCALES=["en_US","fr_FR"]

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

def compute_date(start,end,language=None,show_end=True,str_format="%b %Y"):
    start = datetime.date.fromisoformat(start)
    if show_end:
        return_string = f"{start.strftime(str_format)}\\textendash "
        if end:
            end = datetime.date.fromisoformat(end)
            return_string = f"{return_string}{end.strftime(str_format)}"
        else:
            end = datetime.datetime.now()
            return_string = f"{return_string} {_('present')}"
    else:
        return_string = f"{start.strftime(str_format)}"

    return return_string

def compute_duration(start,end,language=None):
    start = datetime.date.fromisoformat(start)
    return_string = ""

    if end:
        end = datetime.date.fromisoformat(end)
    else:
        end = datetime.datetime.now()

    duration = relativedelta(end, start)

    years = duration.years

    if duration.days > 15:
        months = duration.months + 1
    else:
        months = duration.months

    if months == 12:
        months = 0
        years = years + 1

    if years > 0:
        if years > 1:
            return_string = f"{years} {_('years')}"
        else:
            return_string = f"{years} {_('year')}"

    if months > 0:
        if months > 1:
            return_string = f"{return_string} {months} {_('months')}"
        else:
            return_string = f"{return_string} {months} {_('month')}"

    return return_string

BASEDIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASEDIR,"resume.yaml")) as config_file:
    config = yaml.load(config_file, Loader=yaml.SafeLoader)

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
    loader =
    jinja2.FileSystemLoader(os.path.join(os.path.abspath(BASEDIR),"tex","template"))
)


latex_jinja_env.install_gettext_callables(
        gettext=gettext.gettext,
        ngettext=gettext.ngettext,
        newstyle=True
)
latex_jinja_env.globals['compute_duration'] = compute_duration
latex_jinja_env.globals['compute_date'] = compute_date
latex_jinja_env.globals['location'] = location

for i_locale in LOCALES:

    # Load the translations for the current locale
    translations = Translations.load(LOCALE_PATH, [i_locale])
    latex_jinja_env.install_gettext_translations(translations)

    template = latex_jinja_env.get_template('resume.tex.j2')

    render = template.render(config)
    with open(os.path.join(BASEDIR,"tex",f"resume.{i_locale}.tex"),"w") as output_file:
        output_file.write(render)

