#!/usr/bin/env python3

# Python Core Library
# -----------------------------------------------------------------------------
# https://docs.python.org/3/library/argparse.html
# Parser for command-line options, arguments and sub-commands
import argparse

# https://docs.python.org/3/library/datetime.html
# Basic date and time types
import datetime

# https://docs.python.org/3/library/gettext.html
# Multilingual internationalization services
import gettext

# https://docs.python.org/3/library/locale.html
# Internationalization services
import locale

# https://docs.python.org/3/library/logging.html
# Logging facility for Python
import logging

# https://docs.python.org/3/library/os.html
# Miscellaneous operating system interfaces
import os
import shutil
import subprocess

# Third-Party Library
# -----------------------------------------------------------------------------
# https://pypi.org/project/PyYAML/
# YAML parser and emitter for Python
import yaml
from yaml import dump, load

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader
# https://pypi.org/project/Jinja2/
# https://pypi.org/project/coloredlogs/
# Colored terminal output for Python's logging module
import coloredlogs

# A very fast and expressive template engine.
import jinja2

# https://pypi.org/project/Markdown/
# Python implementation of Markdown.
import markdown

# https://pypi.org/project/Babel/
# Internationalization utilities
from babel.support import Translations

# https://pypi.org/project/python-dateutil/
# Extensions to the standard Python datetime module
from dateutil.relativedelta import relativedelta
from jinja2 import Template

_ = gettext.gettext


class ResumeBuilder:
    def __init__(self, args):
        self.BASEDIR = os.path.dirname(os.path.realpath(__file__))
        self.LOCALE_PATH = os.path.join(self.BASEDIR, "locale")
        self.LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        self.redirect_build = False
        self.config = dict()
        self.output_dir = os.path.join(self.BASEDIR, args.output_dir)
        self.quiet = args.quiet
        logging.basicConfig(format=self.LOG_FORMAT)
        self.logger = logging.getLogger("ResumeBuilder")
        coloredlogs.install(
            level=set_log_verbosity(args.verbosity), logger=self.logger
        )

    @staticmethod
    def location(location: dict()) -> str:
        """Return a human readable address from a dictionary.

        Parse the dictionary provided as arguments to build a string that will
        print an adress of the form:

        ```
        city, region, country
        ```

        Args:
            location: dictionary storing address information.

        Returns:
            The location or an empty string if dictionary is empty.

        """
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

    @staticmethod
    def iso_date(date):
        return datetime.date.fromisoformat(date)

    @staticmethod
    def now_date():
        return datetime.datetime.now()

    @staticmethod
    def format_date(date, str_format="%B %Y"):
        return date.strftime(str_format)

    @staticmethod
    def relative_delta_date(end, start):
        return relativedelta(end, start)

    @staticmethod
    @jinja2.pass_context
    def get_context(c):
        return c

    @staticmethod
    def subs(string, context):
        return context[string]

    @staticmethod
    def to_html(string):
        return markdown.markdown(string)

    def parse_config(self):
        all_locale = dict()
        colors = dict()
        curr_file = os.path.join(self.BASEDIR, "data", "locale.yaml")
        with open(curr_file) as config_file:
            all_locale.update(yaml.load(config_file, Loader=yaml.SafeLoader))
        curr_file = os.path.join(self.BASEDIR, "data", "colors.yaml")
        with open(curr_file) as config_file:
            colors.update(yaml.load(config_file, Loader=yaml.SafeLoader))
        self.config = dict()
        self.config.update(all_locale)
        for i_locale in self.config["locale"]:
            self.config[i_locale["code"]] = {
                "locale": i_locale,
                "all_locale": all_locale,
            }
            self.config[i_locale["code"]].update(colors)

    def init_jinja_env(self, build_type, curr_locale):
        if build_type == "html":
            jinja_env = jinja2.Environment(
                extensions=[
                    "jinja2.ext.i18n",
                    "jinja2.ext.with_",
                    "jinja2.ext.loopcontrols",
                ],
                trim_blocks=False,
                autoescape=False,
                loader=jinja2.FileSystemLoader(
                    os.path.join(self.BASEDIR, "template", "html")
                ),
            )
        elif build_type in ["pdf","tex"]:
            jinja_env = jinja2.Environment(
                extensions=[
                    "jinja2.ext.i18n",
                    "jinja2.ext.with_",
                    "jinja2.ext.loopcontrols",
                ],
                block_start_string="[%",
                block_end_string="%]",
                variable_start_string="[[",
                variable_end_string="]]",
                comment_start_string="[#",
                comment_end_string="#]",
                trim_blocks=False,
                autoescape=False,
                loader=jinja2.FileSystemLoader(
                    os.path.join(self.BASEDIR, "template", "tex")
                ),
            )
        jinja_env.install_gettext_callables(
            gettext=gettext.gettext, ngettext=gettext.ngettext, newstyle=True
        )
        jinja_env.globals["location"] = self.location
        jinja_env.globals["format_date"] = self.format_date
        jinja_env.globals["iso_date"] = self.iso_date
        jinja_env.globals["now_date"] = self.now_date
        jinja_env.globals["relative_delta_date"] = self.relative_delta_date
        jinja_env.globals["subs"] = self.subs
        jinja_env.globals["context"] = self.get_context
        jinja_env.globals["to_html"] = self.to_html
        jinja_env.globals["locale"] = curr_locale
        # Load the translations for the current locale
        translations = Translations.load(self.LOCALE_PATH, [curr_locale])
        locale.setlocale(locale.LC_ALL, f"{curr_locale}.UTF-8")
        jinja_env.install_gettext_translations(translations)
        return jinja_env

    def compile_pdf(self, files, curr_locale):
        pdf_output_dir = os.path.join(self.output_dir, "pdf")
        html_output_dir = os.path.join(
            self.output_dir, "html", "assets", "pdf", curr_locale
        )
        if not os.path.exists(html_output_dir):
            os.makedirs(html_output_dir)
        os.chdir(pdf_output_dir)
        for i_file in files:
            i_file_tex = os.path.join(curr_locale, files[i_file])
            i_file_pdf = os.path.join(files[i_file].replace(".tex", ".pdf"))
            i_file_pdf_bw = i_file_pdf.replace(".pdf", ".bw.pdf")
            self.logger.info(f"Compiling latex PDF for locale {curr_locale}.")
            cmd = ["lualatex", i_file_tex]
            if self.quiet:
                subprocess.run(cmd, capture_output=True)
            else:
                subprocess.run(cmd)
            self.logger.info(f"Converting PDF to Black & White {curr_locale}.")
            cmd = [
                "gs",
                f"-sOutputFile={i_file_pdf_bw}",
                "-sDEVICE=pdfwrite",
                "-sColorConversionStrategy=Gray",
                "-dProcessColorModel=/DeviceGray",
                "-dCompatibilityLevel=1.4",
                "-dNOPAUSE",
                "-dBATCH",
                i_file_pdf,
            ]
            if self.quiet:
                subprocess.run(cmd, capture_output=True)
            else:
                subprocess.run(cmd)
            self.logger.info(f"Moving all PDF to the right place")
            dest_filename = (
                f"{self.config[curr_locale]['basics']['name'].replace(' ','_')}"
                + "_"
                + f"{os.path.join(files[i_file].replace('.tex','.pdf'))}"
            )
            dest_filename_bw = (
                f"{self.config[curr_locale]['basics']['name'].replace(' ','_')}"
                + "_"
                + f"{os.path.join(files[i_file].replace('.tex','.bw.pdf'))}"
            )
            shutil.copy(
                i_file_pdf,
                os.path.join(pdf_output_dir, curr_locale, dest_filename),
            )
            shutil.copy(
                i_file_pdf_bw,
                os.path.join(pdf_output_dir, curr_locale, dest_filename_bw),
            )
            shutil.move(
                i_file_pdf, os.path.join(html_output_dir, dest_filename)
            )
            shutil.move(
                i_file_pdf_bw, os.path.join(html_output_dir, dest_filename_bw)
            )

    def init_output_dir(self, build_type):
        static_dir = os.path.join(self.BASEDIR, "static", build_type)
        if not os.path.exists(os.path.join(self.output_dir, build_type)):
            os.makedirs(os.path.join(self.output_dir, build_type))
        for i_node in os.listdir(static_dir):
            src = os.path.join(static_dir, i_node)
            dest = os.path.join(self.output_dir, build_type, i_node)
            if not os.path.exists(dest):
                if os.path.isdir(src):
                    shutil.copytree(src, dest)
                else:
                    shutil.copy(src, dest)
        src = os.path.join(self.BASEDIR, "docs", "assets")
        for i_node in os.listdir(src):
            dest = os.path.join(self.output_dir, build_type, "assets", i_node)
            if not os.path.exists(dest):
                shutil.copytree(os.path.join(src, i_node), dest)

    def build_type(self, curr_locale, build_type):
        files = dict()
        if build_type in ["pdf","tex"]:
            files = {"resume.tex.j2": "resume.tex"}
        elif build_type == "html":
            files = {
                "index.html.j2": "index.html",
                "404.html.j2": "404.html",
                "style.css.j2": "../css/style.css",
            }
        self.init_output_dir(build_type)
        j2_env = self.init_jinja_env(build_type, curr_locale)

        output_dir = os.path.join(self.output_dir, build_type, curr_locale)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        for i_template in files:
            i_output = files[i_template]
            template = j2_env.get_template(i_template)
            render = template.render(self.config[curr_locale])
            with open(os.path.join(output_dir, i_output), "w") as output_file:
                output_file.write(render)

            if build_type == "pdf":
                self.compile_pdf(files, curr_locale)

        if build_type == "html" and not self.redirect_build:
            i_output = "../index.html"
            template = j2_env.get_template("redirect.html.j2")
            render = template.render(self.config[curr_locale])
            with open(os.path.join(output_dir, i_output), "w") as output_file:
                output_file.write(render)
            self.redirect_build = True


    def build(self, html=True, pdf=True, tex=True):
        self.logger.info("Compiling Translations.")
        subprocess.run(
            ["pybabel", "compile", "-d", self.LOCALE_PATH, "-f"],
            capture_output=True,
        )
        self.parse_config()

        if os.path.isdir(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)

        for i_locale in self.config["locale"]:
            locale_code = i_locale["code"]
            if os.path.isdir(os.path.join(self.BASEDIR, "data", locale_code)):
                for i_file in os.listdir(
                    os.path.join(self.BASEDIR, "data", locale_code)
                ):
                    curr_file = os.path.join(
                        self.BASEDIR, "data", locale_code, i_file
                    )
                    with open(curr_file) as config_file:
                        self.config[locale_code].update(
                            yaml.load(config_file, Loader=yaml.SafeLoader)
                        )
                if pdf or tex:
                    self.logger.info(
                        f"Building PDF resume for locale {locale_code}."
                    )
                    if pdf:
                        self.build_type(locale_code, "pdf")
                    elif tex:
                        self.build_type(locale_code, "tex")
                if html:
                    self.logger.info(
                        f"Building HTML resume for locale {locale_code}."
                    )
                    self.build_type(locale_code, "html")


def parse_arg():
    parser = argparse.ArgumentParser(
        prog="resume",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="""
                Script which parse yaml files in `data` folder and build resume
                in html and pdf (from latex).

                Support internationalization with babel to be able to create a
                resume in multiple languages at once.
                """,
    )
    parser.add_argument(
        "--build",
        "-b",
        nargs=1,
        type=str,
        default="both",
        dest="build",
        choices=["both", "pdf", "html", "tex"],
        required=False,
        metavar="build_type",
        help="""Type of resume to build, either `both`, `html`, `pdf`, `tex`.""",
    )
    parser.add_argument(
        "--output",
        "-o",
        nargs=1,
        type=str,
        default="output",
        dest="output_dir",
        required=False,
        metavar="output_dir",
        help="""Location of the output directory where built files will be
            stored.""",
    )
    parser.add_argument(
        "--serve",
        "-s",
        default=False,
        dest="serve",
        action="store_true",
        required=False,
        help="""
                Once building of resume is done, start a python server to
                render the html pages.

                Is incompatible with option `--build pdf` as this will only build
                pdf so there is nothing to be served
                """,
    )
    parser.add_argument(
        "--verbosity",
        "-v",
        action="count",
        dest="verbosity",
        required=False,
        default="warning",
        help=""" Increase output verbosity (error, warning, info,
            debug respectively depending on the number of `v`).""",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        dest="quiet",
        required=False,
        action="store_true",
        default=False,
        help="""Do now show LaTeX and Ghostscript output""",
    )
    return parser.parse_args()


def set_log_verbosity(level):
    # If default value
    if isinstance(level, str):
        return "INFO"
    elif level == 0:
        return "ERROR"
    elif level == 1:
        return "WARNING"
    elif level == 2:
        return "INFO"
    elif level >= 3:
        return "DEBUG"
    return "ERROR"


def main():
    args = parse_arg()
    if isinstance(args.build, list):
        args.build = args.build[0]

    log_format = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    logging.basicConfig(format=log_format)
    logger = logging.getLogger("resume_builder.py")
    coloredlogs.install(level=set_log_verbosity(args.verbosity), logger=logger)

    builder = ResumeBuilder(args)

    if args.build == "pdf":
        builder.build(pdf=True, html=False, tex=False)
    elif args.build == "html":
        builder.build(pdf=False, html=True, tex=False)
    elif args.build == "tex":
        builder.build(pdf=False, html=False, tex=True)
    else:
        builder.build()

    if args.serve and args.build in ["html", "both"]:
        os.chdir(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                builder.output_dir,
                "html",
            )
        )
        subprocess.run(["python", "-m", "http.server", "8080"])


if __name__ == "__main__":
    main()
