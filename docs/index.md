---
hide:
  - navigation # Hide navigation
  - toc        # Hide table of contents
---
<!-- markdownlint-disable MD041 -->
{% set curr_repo=subs("TODO") %}

<!-- BEGIN MKDOCS TEMPLATE -->
<!--
WARNING, DO NOT UPDATE CONTENT BETWEEN MKDOCS TEMPLATE TAG !
Modified content will be overwritten when updating
-->

<div align="center">

  <!-- Project Title -->
  <a href="{{ git_platform.url }}{{ curr_repo.git_slug_with_namespace }}">
    <img src="{{ curr_repo.logo }}" width="200px">
    <h1>{{ curr_repo.name }}</h1>
  </a>

<hr>

{{ to_html(curr_repo.desc) }}

<hr>

  <b>
IMPORTANT !<br>

Main repo is on
<a href="{{ git_platform.url }}{{ curr_repo.git_slug_with_namespace }}">
  {{ git_platform.name }} - {{ curr_repo.git_name_with_namespace }}</a>.<br>
On other online git platforms, they are just mirrors of the main repo.<br>
Any issues, pull/merge requests, etc., might not be considered on those other
platforms.
  </b>

</div>

<!-- END MKDOCS TEMPLATE -->
