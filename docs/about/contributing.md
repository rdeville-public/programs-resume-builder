<!-- markdownlint-disable MD041 -->
{% set curr_repo=subs("TODO") %}

<!-- BEGIN MKDOCS TEMPLATE -->
<!--
WARNING, DO NOT UPDATE CONTENT BETWEEN MKDOCS TEMPLATE TAG !
Modified content will be overwritten when updating
-->

# Contributing

This project welcomes contributions from developers and users in the open source
community. Contributions can be made in a number of ways, a few examples are :

  * Code patch via pull requests
  * Documentation improvements
  * Bug reports and patch reviews
  * Proposition of new features
  * etc.

## Reporting an Issue

Please include as much details as you can when reporting an issue in the [issue
trackers][issue_tracker]. If the problem is visual (for instance, wrong
documentation rendering) please add a screenshot.

[issue_tracker]: {{ git_platform.url }}{{ curr_repo.git_slug_with_namespace }}/-/issues

## Submitting Pull Requests

Once you are happy with your changes or you are ready for some feedback, push it
to your fork and send a pull request. For a change to be accepted it will most
likely need to have tests and documentation if it is a new feature.

For more information, you can refers to the main [developers
guides][developers_guides] which is the common resources I use for all
my projects. There you will find:

  * [Syntax Guide][syntax_guide], which describe syntax guidelines per language
    to follow if you want to contribute.
  * [Contributing workflow][contributing_workflow], which provide an example
    of the workflow I used for the development.

[developers_guides]: {{ site_base_url }}/latest/dev_guides/index.html
[syntax_guide]: {{ site_base_url }}/latest/dev_guides/style_guides/index.html
[contributing_workflow]: {{ site_base_url }}/latest/dev_guides/developer_guidelines.html

## Community

Finally, every member of the community should follow this [Code of
conduct][code_of_conduct].

[code_of_conduct]: code_of_conduct.md

<!-- END MKDOCS TEMPLATE -->
