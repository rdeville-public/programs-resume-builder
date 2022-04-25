#!/usr/bin/env python3
"""Set of methods to manage mkdocs configuration dynamically.

Set of methods for
[mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/) Set of
which :

- Define macros usable in jinja template
- Update `env.conf`, i.e. mkdocs configuration based on variables files
- Dynamically update `env` dictionary and `nav` entries to support subrepo
  either internal subrepo, using
  [mkdocs-monorepo-plugin](https://github.com/backstage/mkdocs-monorepo-plugin),
  or external subrepo by using `online_url` of such subrepo.

This script allow to make content of `mkdocs.yml` to be templated, i.e. using
the same `mkdocs.yml` file for multiple repos and use variables files in
`docs/_data/`
"""

# pylint: disable=R0801

# JSON encoder and decoder
# https://docs.python.org/3/library/json.html
import json

# Logging facility
# https://docs.python.org/3/library/logging.html
import logging

# Miscellaneous operating system interfaces
# https://docs.python.org/3/library/os.html
import os

# Regular expression operations
# https://docs.python.org/3/library/re.html
import re

# System-specific parameters and functions
# https://docs.python.org/3/library/sys.html
import sys

# Time access and conversions
# https://docs.python.org/3/library/time.html
import time

# Python Git Library
# https://pypi.org/project/GitPython/
import git

# Python implementation of Markdown
# https://pypi.org/project/markdown/
import markdown

# YAML parser and emitter for Python
# https://pypi.org/project/PyYAML/
import yaml

# Python lib/cli for JSON/YAML schema validation
# https://pypi.org/project/pykwalify/
from pykwalify.core import Core as yamlschema

# pylint: disable=W0105
# - W0105: String statement has no effect
LOG = logging.getLogger(__name__)
"""The logger facilty."""
ERR_CLR = "\033[31m"
"""String coloring error output in red."""
INFO_CLR = "\033[32m"
"""String coloring error output in green."""
RESET_CLR = "\033[0m"
"""String reseting coloring output."""


def add_internal_to_nav(
    env: dict,
    nav: dict,
    repo_dict: dict,
    repo_parent: list,
    nav_parent: list = None,
) -> None:
    """Add internal subrepo to `nav` key of mkdocs.yml for monorepo.

    This method recursively parse `nav_parent` arguments to know where to
    include the internal subrepo into `nav` key.

    Once determined, add the subrepo as a entry to the `nav` key, with the
    format required by
    [mkdocs-monorepo-plugin](https://github.com/backstage/mkdocs-monorepo-plugin).

    Args:
        env : Environment dictionary provided by
            [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/)
        nav : Navigation dictionary (subpart of it if called
            recursively)
        repo_dict : Repo dictionary from `subrepo.yml` file in `docs/_data/`
        repo_parent : List of keys storing parent keys of the current
            `repo_dict` from `subrepo.yml` file in `docs/_data`
        nav_parent : List of keys storing parents `nav_entry` keys of the
            current `repo_dict` from `subrepo.yml` file in `docs/_data`
    """
    if nav_parent:
        for i_nav in nav:
            # "nav_entry" is a key of current parsed `nav`
            if nav_parent[0] in i_nav:
                for i_key in i_nav:
                    add_internal_to_nav(
                        env,
                        i_nav[i_key],
                        repo_dict,
                        repo_parent,
                        nav_parent[1:],
                    )
            # "nav_entry" is a subkey of current parsed `nav`
            elif nav_parent[0] in yaml.dump(i_nav):
                for i_key in i_nav:
                    add_internal_to_nav(
                        env,
                        i_nav[i_key],
                        repo_dict,
                        repo_parent,
                        nav_parent[0:],
                    )
    else:
        mkdocs_path = env.project_dir
        for i_parent in repo_parent:
            mkdocs_path = os.path.join(mkdocs_path, i_parent)
        mkdocs_path = os.path.join(mkdocs_path, repo_dict["name"])
        if "subpath" in repo_dict:
            mkdocs_path = os.path.join(mkdocs_path, repo_dict["subpath"])
        mkdocs_path = os.path.join(mkdocs_path, "mkdocs.yml")
        nav.append({repo_dict["nav_entry"]: f"!include {mkdocs_path}"})


def add_external_to_nav(
    env: dict, nav: dict, repo_dict: dict, repo_parent: list, nav_parent: list
) -> None:
    """Add external subrepo to `nav` key of mkdocs.yml.

    This method recursively parse `nav_parent` arguments to know where to
    include the external subrepo into `nav` key.

    Once determined, add the subrepo as a entry to the `nav` key, with the
    `online_url` key of the current subrepo defined with `repo_dict` in file
    `subrepo.yml` in `docs/_data`.

    Args:
        env : Environment dictionary provided by
            [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/)
        nav : Navigation dictionary (subpart of it if called recursively)
        repo_dict : Repo dictionary from `subrepo.yml` file in `docs/_data/`
        repo_parent : List of keys storing parent keys of the current
            `repo_dict` from `subrepo.yml` file in `docs/_data`
        nav_parent : List of keys storing parents `nav_entry` keys of the
            current `repo_dict` from `subrepo.yml` file in `docs/_data`
    """
    if nav_parent:
        for i_nav in nav:
            if nav_parent[0] in i_nav:
                for i_key in i_nav:
                    add_external_to_nav(
                        env,
                        i_nav[i_key],
                        repo_dict,
                        repo_parent,
                        nav_parent[1:],
                    )
    elif repo_dict["online_url"].startswith("/"):
        nav.append(
            {
                repo_dict["nav_entry"]: repo_dict["online_url"].replace(
                    "/", "../", 1
                )
            }
        )
    else:
        nav.append({repo_dict["nav_entry"]: repo_dict["online_url"]})


def add_nav_entry(nav: list, nav_parent: list = None) -> None:
    """Create missing entry into `nav` key of `env.conf`.

    Recursively parse list `nav_parent` and create missing entry into key `nav`
    of mkdocs.yml.

    Args:
        nav : Navigation dictionary (subpart of it if called recursively)
        nav_parent : List of keys storing parents `nav_entry` keys
    """
    entry = {}

    for i_nav in nav:
        if nav_parent[0] in i_nav:
            entry = i_nav

    if not entry:
        entry = {nav_parent[0]: []}
        nav.append(entry)

    if len(nav_parent[1:]) == 0:
        return
    add_nav_entry(entry[nav_parent[0]], nav_parent[1:])


def update_nav(
    env: dict,
    repo_dict: dict,
    repo_parent: list = None,
    nav_parent: list = None,
    first_iteration=False,
) -> None:
    """Meta method which dynamically update the `nav` key of `env.conf`.

    Recursively parse `repo_dict` (provided from `subrepo.yml` file in
    `docs/_data`), depending on the content of the keys, method will:

    - Update the list of `nav_parent` and `repo_parent`,
    - Call [add_nav_entry][plugins.add_nav_entry] to add missing entry to `nav`
      key of `mkdocs.yml`,
    - Call [add_external_to_nav][plugins.add_external_to_nav] to add external
      subrepo to `nav` key of `mkdocs.yml`,
    - Call [add_internal_to_nav][plugins.add_internal_to_nav] to add internal
      subrepo to `nav` key of `mkdocs.yml`,
    - Recursively call itself.

    Args:
        env : Environment dictionary provided by
            [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/)
        repo_dict : Repo dictionary from `subrepo.yml` file in `docs/_data/`
        repo_parent : List of keys storing parent keys of the current
            `repo_dict` from `subrepo.yml` file in `docs/_data`
        nav_parent : List of keys storing parents `nav_entry` keys of the
            current `repo_dict` from `subrepo.yml` file in `docs/_data`
        first_iteration : Simple boolean to know if it is the first recursive
            call of the method.
    """
    for i_key in repo_dict:
        if not nav_parent or first_iteration:
            nav_parent = []

        if not repo_parent or first_iteration:
            repo_parent = []

        if i_key == "nav_entry":
            nav_parent.append(repo_dict["nav_entry"])
        elif i_key == "internal":
            for i_repo in repo_dict["internal"]:
                if nav_parent[0] not in yaml.dump(env.conf["nav"]):
                    add_nav_entry(env.conf["nav"], nav_parent)
                add_internal_to_nav(
                    env, env.conf["nav"], i_repo, repo_parent, nav_parent
                )
        elif i_key == "external":
            for i_repo in repo_dict["external"]:
                if nav_parent[0] not in yaml.dump(env.conf["nav"]):
                    add_nav_entry(env.conf["nav"], nav_parent)
                add_external_to_nav(
                    env, env.conf["nav"], i_repo, repo_parent, nav_parent
                )
        else:
            repo_parent.append(i_key)
            update_nav(env, repo_dict[i_key], repo_parent, nav_parent)


def get_repo_slug(env: dict, git_repo: git.Repo) -> str:
    """Compute the slug of the `git_repo` and ensure repo dictionary is defined.

    Compute the slug of the repo provided as `git_repo` based on the origin
    remote. If no remo, then will use the folder name.

    Then ensure the repo dictionary is defined in `docs/_data/`. If not, print
    an error and exit.

    Else, update value of `env.variables["git"]` and return the `repo_slug`.

    Arguments:
        env : Environment dictionary provided by
            [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/)
        git_repo: Git python object of the current repo.

    Returns:
        Posix path from `os.path` python library.
    """
    if git_repo.remotes:
        repo_slug = (
            git_repo.remotes.origin.url.rsplit("/")[-1]
            .split(".git")[0]
            .replace(".", "_")
        )
    else:
        repo_slug = os.path.basename(env.project_dir)

    if repo_slug not in env.variables:
        LOG.error(
            "%s[macros] - Dictionary %s is not defined.%s",
            ERR_CLR,
            repo_slug,
            RESET_CLR,
        )
        LOG.error(
            "%s[macros] - Ensure you copy docs/_data/templates/repo.tpl.yaml "
            "to docs/_data/%s.yaml.%s",
            ERR_CLR,
            repo_slug,
            RESET_CLR,
        )
        LOG.error(
            "%s[macros] - And you setup dictionary %s in docs/_data/%s.yaml.%s",
            ERR_CLR,
            repo_slug,
            repo_slug,
            RESET_CLR,
        )
        sys.exit(1)

    env.variables["git"]["repo_slug"] = repo_slug
    return repo_slug


def set_site_name(env: dict, repo_slug: str) -> None:
    """Update content of the `site_name` key in `env.conf`.

    Update the value of `site_name` keys for mkdocs documentation based on (in
    precedence order):

    - Value of `site_name` in `mkdocs.yml`,
    - Value of `site_name` in `env.variables`, from `docs/_data/vars.yml`,
    - Value of `name` in `env.variables[repo_slug]` from `docs/_data/repo.yml`.


    If `site_name` key is not defined in `mkdocs.yml` then look to
    `docs/_data/vars.yml`, if defined, else look to the the current repo
    dictionary to set value of `site_name`.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
        repo_slug: Repo slug or name of the repo folder.
    """
    if "site_name" not in env.conf or not env.conf["site_name"]:
        if "site_name" in env.variables:
            env.conf["site_name"] = env.variables["site_name"]
        else:
            env.conf["site_name"] = env.variables[repo_slug]["name"]


def set_site_desc(env: dict, repo_slug: str) -> None:
    """Update content of the `site_desc` key in `env.conf`.

    Update the value of `site_desc` keys for mkdocs configuration based on (in
    precedence order):

    - Value of `site_desc` in `mkdocs.yml`,
    - Value of `site_desc` in `env.variables`, from `docs/_data/vars.yml`,
    - Value of `desc` in `env.variables[repo_slug]` from `docs/_data/repo.yml`.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
        repo_slug: Repo slug or name of the repo folder.
    """
    if "site_desc" not in env.conf:
        if "site_desc" in env.variables:
            env.conf["site_desc"] = env.variables["site_desc"]
        else:
            env.conf["site_desc"] = env.variables[repo_slug]["desc"]


def set_site_url(env: dict, repo_slug: str) -> None:
    """Update content of the `site_url` key in `env.conf`.

    Update the value of `site_url` key for mkdocs documentation based on (in
    precedence order):

    - Value of `site_url` in `mkdocs.yml`,
    - Value of `site_url` in `env.variables`, from `docs/_data/vars.yml`,
    - Value of `site_base_url` in `env.variables`, from `docs/_data/vars.yml`,
      concatenate with `env.variables[repo_slug]["url_slug_with_namespace"]`
      from `docs/_data/repo.yml`.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
        repo_slug: Repo slug or name of the repo folder.
    """
    if "site_url" not in env.conf:
        if "site_url" in env.variables:
            env.conf["site_url"] = env.variables["site_url"]
        elif "site_base_url" in env.variables:
            site_url = (
                env.variables["site_base_url"]
                + env.variables[repo_slug]["url_slug_with_namespace"]
            )
            env.conf["site_url"] = site_url


def set_copyright(env: dict, git_repo: git.Repo) -> None:
    """Update content of the `copyright` key in `env.conf`.

    Update the value of `copyright` key for mkdocs documentation based on (in
    precedence order):

    - Value of `copyright` in `mkdocs.yml`,
    - Value of `copyright` in `env.variables`, from `docs/_data/vars.yml`, then,
      using this value:
        - Value of the year of the first commit of the repo holding the
          documentation and current year,
        - Value of the current year only,

    If no `copyright` key defined, neither in `mkdocs.yml`, nor in
    `docs/_data/vars.yml`, then not copyright will be set.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
        git_repo: Git python object of the current repo.
    """
    if (
        "copyright" not in env.conf or not env.conf["copyright"]
    ) and "copyright" in env.variables:
        if git_repo.branches and git_repo.branches.master:
            first_date = git_repo.commit(
                git_repo.branches.master.log()[0].newhexsha
            ).committed_date
            first_year = time.strftime("%Y", time.gmtime(first_date))
        else:
            first_year = time.strftime("%Y", time.localtime())
        curr_year = time.strftime("%Y", time.localtime())

        if first_year == curr_year:
            env.variables["date_copyright"] = f"Copyright &copy; {curr_year}"
        else:
            env.variables[
                "date_copyright"
            ] = f"Copyright &copy; {curr_year} - {curr_year}"

        env.conf[
            "copyright"
        ] = f"{env.variables['date_copyright']} {env.variables['copyright']}"


def set_repo_name(env: dict, repo_slug: str) -> None:
    """Update content of the `repo_name` key in `env.conf`.

    Update the value of `repo_name` key for mkdocs documentation based on (in
    precedence order):

    - Value of `repo_name` in `mkdocs.yml`,
    - Value of `repo_name` in `env.variables`, from `docs/_data/vars.yml`,
    - Value of `name` in `env.variables[repo_slug]`, from `docs/_data/repo.yml`,
      then, depending on its value:
      - If value is `!!git_platform`, then value of `repo_name` will be set to
        the value of `env.variables['git_platform']['name']`, from
        `docs/_data/vars.yml`
      - Else, value is key `name` of `env.variables[repo_slug]

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
        repo_slug: Repo slug or name of the repo folder.
    """
    if "repo_name" not in env.conf or not env.conf["repo_name"]:
        if "repo_name" in env.variables:
            env.conf["repo_name"] = env.variables["repo_name"]
        elif "name" in env.variables[repo_slug]:
            if env.variables[repo_slug]["name"] == "!!git_platform":
                env.conf["repo_name"] = env.variables["git_platform"]["name"]
            else:
                env.conf["repo_name"] = env.variables[repo_slug]["name"]


def set_repo_url(env: dict, repo_slug: str) -> None:
    """Update content of the `repo_url` key in `env.conf`.

    Update the value of `repo_url` key for mkdocs documentation based on (in
    precedence order):

    - Value of `repo_url` in `mkdocs.yml`,
    - Value of `repo_url` in `env.variables`, from `docs/_data/vars.yml`,
    - Concatenation of the `url` of `env.variables['git_platform']`, from
      `docs/_data/vars.yml` and value `git_slug_with_namespace` in
      `env.variables[repo_slug]`, from `docs/_data/repo.yml`.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
        repo_slug: Repo slug or name of the repo folder.
    """
    if "repo_url" not in env.conf or not env.conf["repo_url"]:
        if "repo_url" in env.variables:
            env.conf["repo_url"] = env.variables["repo_url"]
        elif "repo_url" in env.conf:
            env.conf["repo_url"] = (
                f"{env.variables['git_platform']['url']}"
                + f"{env.variables[repo_slug]['git_slug_with_namespace']}"
            )


def set_nav(env: dict) -> None:
    """Update content of the `nav` key in `env.conf`.

    Update the value of `nav` key for mkdocs documentation based on (in
    precedence order):

    - Value of `nav` in `vars.yml` or `extra.yml` in `docs/_data/`, allowing
      overloading of nav for forked repo.
    - Value of `nav` in `mkdocs.yml`

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
    """
    if "nav" in env.variables and env.variables["nav"]:
        env.conf["nav"] = env.variables["nav"]


def update_theme(env: dict, repo_slug: str) -> None:
    """Update content of the `theme` key in `env.conf`.

    If `theme` key is defined in `docs/_data/vars.yml`, this override the
    content of the default `theme` key in mkdocs documentation.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
        repo_slug: Repo slug or name of the repo folder.
    """
    if "theme" in env.variables:
        for i_key in env.variables["theme"]:
            env.conf["theme"][i_key] = env.variables["theme"][i_key]

    if "logo" not in env.conf["theme"] or not env.conf["theme"]["logo"]:
        if "logo" in env.variables[repo_slug]:
            env.conf["theme"]["logo"] = env.variables[repo_slug]["logo"]
        else:
            env.conf["theme"]["logo"] = os.path.join(
                "assets", "img", "meta", f"{repo_slug}_logo.png"
            )

    if not env.conf["theme"]["icon"]:
        env.conf["theme"]["icon"] = {}

    if "icon" not in env.conf["theme"] or not env.conf["theme"]["icon"]:
        env.conf["theme"]["icon"]["repo"] = env.variables["git_platform"][
            "icon"
        ]

    if "favicon" not in env.conf["theme"] or not env.conf["theme"]["favicon"]:
        if "favicon" in env.variables[repo_slug]:
            env.conf["theme"]["favicon"] = env.variables[repo_slug]["favicon"]
        elif "logo" in env.variables[repo_slug]:
            env.conf["theme"]["favicon"] = env.variables[repo_slug]["logo"]
    else:
        env.conf["theme"]["favicon"] = os.path.join(
            "assets", "img", "meta", f"{repo_slug}_logo.png"
        )


def set_config(env: dict) -> None:
    """Dynamically update mkdocs configuration.

    Based on the `repo_slug` (or folder name) load variables in
    `docs/_data/vars.yml`, in `docs/_data/repo.yml` and update content of mkdocs
    documentation accordingly.

    Especially, if `docs/_data/subrepo.yaml` exists and define valid subrepos,
    clone these subrepo and dynamically add them to the `nav` key of the mkdocs
    configuration.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
    """
    git_repo = git.Repo(search_parent_directories=True)
    repo_slug = get_repo_slug(env, git_repo)

    set_site_name(env, repo_slug)
    set_site_desc(env, repo_slug)
    set_site_url(env, repo_slug)
    set_copyright(env, git_repo)
    set_repo_name(env, repo_slug)
    set_repo_url(env, repo_slug)
    set_nav(env)
    update_theme(env, repo_slug)

    if "subrepo" in env.variables:
        if (
            not env.variables["internal_subdoc"]
            and "monorepo" in env.conf["plugins"]
        ):
            env.conf["plugins"].pop("monorepo")
        else:
            update_nav(env, env.variables["subrepo"], first_iteration=True)


def load_yaml_file(path: str, filename: str) -> None:
    """Ensure a YAML file is valid again a schema and return its content.

    Depending on the name of the YAML file, compare its content to a schema to
    validate its content. If content is not valid, an error will be raised.
    Otherwise, its content will be returned.

    If filename is `extra.yml` or `extra.yaml`, load content of the file
    unconditionnally.

    Arguments:
        path: Base path where YAML files are.
        filename: Name of the YAML file to load.
    """
    source_file = os.path.join(path, filename)
    schema_file = os.path.join(path, "schema")
    data_type = ""

    if filename not in ("extra.yaml", "extra.yml"):
        if filename in ("subrepo.yaml", "subrepo.yml"):
            schema_file = os.path.join(schema_file, "subrepo.schema.yaml")
        elif filename in ("vars.yaml", "vars.yml"):
            schema_file = os.path.join(schema_file, "vars.schema.yaml")
        elif filename not in ("extra.yaml", "extra.yml"):
            schema_file = os.path.join(schema_file, "repo.schema.yaml")
            data_type = "repo"
        schema = yamlschema(source_file=source_file, schema_files=[schema_file])
        schema.validate(raise_exception=True)
        data_content = schema.source
    else:
        with open(source_file, encoding="UTF-8") as file:
            data_content = yaml.safe_load(file)

    return data_content, data_type


# pylint: disable=R0913
# - R0913: Too many arguments
def update_subrepo_logo_src(
    env: dict,
    curr_repo: dict,
    repo_name: str,
    subrepo_dict: dict,
    path: str,
    external: bool,
) -> None:
    """Update the content of the key `logo` and `src_path` of subrepo.

    Update value of keys `logo` and `src_path` of cloned subrepo, i.e. value
    from file `docs/_data/repo.yaml` in the cloned subrepo, relative to the main
    repo holding the documentation.

    Args:
        env : Environment dictionary provided by
            [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/)
        curr_repo : Repo dictionary from `repo.yml` file in `docs/_data/` in the
            cloned subrepo,
        repo_name: Name of the repo,
        subrepo_dict: Dictionary of the repo as defined in file `subrepo.yaml`
            in `docs/_data`,
        path: Absolute path of the location of the cloned subrepo,
        external: Boolean to know if current repo is an external subrepo.
    """
    logo_subpath = ""
    src_subpath = ""
    if external:
        logo_subpath = os.path.join(subrepo_dict["online_url"])

    src_subpath = os.path.join(
        path.replace(f"{env.project_dir}/", ""), repo_name
    )

    if "logo" not in curr_repo:
        curr_repo["logo"] = os.path.join(
            logo_subpath, "assets", "img", "meta", f"{repo_name}_logo.png"
        )
    if "src_path" in curr_repo:
        for i_src in curr_repo["src_path"]:
            i_src = os.path.join(src_subpath, i_src)
            env.conf["plugins"]["mkdocstrings"].config.data["handlers"][
                "python"
            ]["setup_commands"].append(f"sys.path.append('{i_src}')")


def update_subrepo_info(
    env: dict, subrepo_list: dict, path: str, external: bool = False
) -> dict:
    """Clone subrepo, load repo information and update values if needed.

    Recursively clone or pull repo defined from subpart of
    `env.variables['subrepo'], load repo information from this cloned or pulled
    repo, i.e. load file `docs/_data/repo.yaml` in the subrepo, and update
    needed keys.

    Args:
        env : Environment dictionary provided by
            [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/)
        subrepo_list: List of dictionary storing subrepo dict,
        path: Absolute path of the location of the cloned subrepo,
        external: Boolean to know if current repo is an external subrepo.

    Return:
        A updating dictionary storing subrepo information
    """
    return_dict = {}
    for i_repo in subrepo_list:
        subrepo_root = os.path.join(path, i_repo["name"])

        if os.path.isdir(subrepo_root):
            print(
                f"{INFO_CLR}INFO [macros] - Pulling repo {i_repo['name']}{RESET_CLR}"
            )
            git_subrepo = git.Repo(subrepo_root)
            git_subrepo.remotes.origin.pull("master")
        else:
            print(
                f"{INFO_CLR}INFO [macros] - Cloning repo {i_repo['name']}{RESET_CLR}"
            )
            git.Repo.clone_from(i_repo["git_url"], subrepo_root)

        if "subpath" in i_repo:
            data_dir = os.path.join(
                subrepo_root, i_repo["subpath"], "docs", "_data"
            )
        else:
            data_dir = os.path.join(subrepo_root, "docs", "_data")

        data_file = os.path.join(data_dir, f"{i_repo['name']}.yaml")
        data, _ = load_yaml_file(data_dir, data_file)
        for i_repo_info in data:
            curr_repo = data[i_repo_info]
            update_subrepo_logo_src(
                env, curr_repo, i_repo_info, i_repo, path, external
            )
        return_dict.update(data)
    return return_dict


def update_subrepo(
    env: dict, subrepo_dict: dict, path: str, external: bool
) -> dict:
    """Recursively parse `env.variables['subrepo']`.

    Recursively parse dictionary `env.variables['subrepo']`, from file
    `docs/_data/subrepo.yaml`. Depending on the key:

    - `nav_entry`: Do a recursion of this method,
    - `external` or `internal`: Parse the list to update subrepo information

    Args:
        env : Environment dictionary provided by
            [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/)
        subrepo_dict: Dictionary storing subrepo,
        path: Absolute path of the location of the cloned subrepo,
        external: Boolean to know if current repo is an external subrepo.

    Returns:
        An updated dictionary of repo informations.
    """
    return_dict = {}
    for i_key in subrepo_dict:
        if isinstance(subrepo_dict[i_key], list):
            if i_key == "external":
                external = True
            elif i_key == "internal":
                env.variables["internal_subdoc"] = True
            return_dict.update(
                update_subrepo_info(env, subrepo_dict[i_key], path, external)
            )
        elif i_key not in ["nav_entry"]:
            return_dict.update(
                update_subrepo(
                    env,
                    subrepo_dict[i_key],
                    os.path.join(path, i_key),
                    external,
                )
            )
    return return_dict


def update_logo_src_repo(
    env: dict, curr_repo: dict, repo_name: str, path: str = None
) -> None:
    """Update the content of the key `logo` and `src_path` of current repo.

    Update value of keys `logo` and `src_path` of current repo holding the
    documentation.

    Args:
        env : Environment dictionary provided by
            [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/)
        curr_repo : Repo dictionary from `repo.yml` file in `docs/_data/` in the
            cloned subrepo,
        repo_name: Name of the repo,
        path: Absolute path of the location of the current repo.
    """
    subpath = ""
    if path:
        subpath = os.path.join(path.replace(env.project_dir, ""), repo_name)

    if "logo" not in curr_repo:
        curr_repo["logo"] = os.path.join(
            subpath, "assets", "img", "meta", f"{repo_name}_logo.png"
        )
    if "src_path" in curr_repo:
        for i_src in curr_repo["src_path"]:
            i_src = os.path.join(subpath, i_src)
            env.conf["plugins"]["mkdocstrings"].config.data["handlers"][
                "python"
            ]["setup_commands"].append(f"sys.path.append('{i_src}')")


def load_var_file(env: dict) -> None:
    """Load variables files in `docs/_data/`.

    Load every yaml files in `docs/_data/`, if one of the file define the
    current repo, then update keys `logo` and `src_path` for the current repo.

    Arguments:
        env : Environment dictionary provided by
            [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/)
    """
    var_dir = os.path.join(env.project_dir, "docs", "_data")

    for i_file in os.listdir(var_dir):
        if i_file.endswith((".yml", ".yaml")):
            data, data_type = load_yaml_file(var_dir, i_file)
            for i_key in data:
                if data_type == "repo":
                    update_logo_src_repo(env, data[i_key], i_key)
                env.variables[i_key] = data[i_key]


def update_version(env: dict) -> None:
    """Parse every tags of the repo to build a `docs/versions.json`.

    To emulate mike version support for gitlab, this method will parse every
    tags of the current repo holding the current documentation to create a file
    `versions.json` which will be put in folder `docs`.

    This is mainly used for the CI to build a documentation per repo tags.

    Arguments:
        env : Environment dictionary provided by
            [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/)
    """
    if (
        "version" not in env.variables
        or "provider" not in env.variables["version"]
        or env.variables["version"]["provider"] != "mike"
    ):
        return
    git_repo = git.Repo(search_parent_directories=True)
    mike_version = []
    last_major = -1
    last_minor = -1
    last_patch = str(-1)
    for i_tag in git_repo.tags:
        i_tag = yaml.dump(i_tag.path)
        i_tag = re.sub(".*v", "", i_tag).split(".")
        major = int(i_tag[0])
        minor = int(i_tag[1])
        patch = str()
        for i_remain_tag in i_tag[2:]:
            if i_remain_tag and i_remain_tag not in ("", "\n"):
                i_remain_tag = i_remain_tag.replace("\n", "")
                if not patch:
                    patch = f"{i_remain_tag}"
                else:
                    patch = f"{patch}.{i_remain_tag}"
        if major > last_major:
            if last_major >= 0:
                mike_version.append(
                    {
                        "version": f"{last_major}.{last_minor}",
                        "title": f"{last_major}.{last_minor}.{last_patch}",
                        "aliases": [],
                    }
                )
            last_major = major
            last_minor = -1
        if minor > last_minor:
            if last_minor >= 0:
                mike_version.append(
                    {
                        "version": f"{last_major}.{last_minor}",
                        "title": f"{last_major}.{last_minor}.{last_patch}",
                        "aliases": [],
                    }
                )
            last_minor = minor
            last_patch = str(-1)
        if patch > last_patch:
            last_patch = str(patch)

    mike_version.append(
        {
            "version": f"{last_major}.{last_minor}",
            "title": f"{last_major}.{last_minor}.{last_patch}",
            "aliases": ["latest"],
        }
    )
    mike_version.reverse()
    with open(
        os.path.join(env.project_dir, "docs", "versions.json"),
        "w",
        encoding="UTF-8",
    ) as version_file:
        json.dump(mike_version, version_file, indent=2)


def define_env(env: dict) -> None:
    # pylint: disable=C0301
    # - C0301: Line to long
    """Hook for mkdocs-macros-plugins defining variables, macros and filters.

    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.

    See
    [https://mkdocs-macros-plugin.readthedocs.io/en/latest/](https://mkdocs-macros-plugin.readthedocs.io/en/latest/)

    This hooks also start the initialization of the dynamic configuration of
    mkdocs.

    Arguments:
        env: Mkdocs macro plugin environment dictionary.
    """
    load_var_file(env)

    if "subrepo" in env.variables:
        env.variables["internal_subdoc"] = False
        env.variables.update(
            update_subrepo(
                env, env.variables["subrepo"], env.project_dir, False
            )
        )

    set_config(env)

    update_version(env)

    @env.macro
    # pylint: disable=W0612
    # -  W0612: Unused variable (unused-variable)
    def subs(var: str) -> dict:
        """Return the content of the dictionary defined by var.

        Arguments:
            var: Key in env.variables to return.

        Returns:
            The value of `env.variables[var]` if it exists, else return None.
        """
        if var in env.variables:
            return env.variables[var]
        return None

    @env.macro
    # pylint: disable=W0612
    # -  W0612: Unused variable (unused-variable)
    def to_html(var: str) -> dict:
        """Convert the content of the markdown string into HTML.

        Arguments:
            var: Markdown string which need to be converted to HTML

        Returns:
            The content of the markdown converted to HTML
        """
        return markdown.markdown(var)


# -----------------------------------------------------------------------------
# VIM MODELINE
# vim: fdm=indent
# -----------------------------------------------------------------------------
