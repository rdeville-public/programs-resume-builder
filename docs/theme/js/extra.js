/* BEGIN MKDOCS TEMPLATE */
/* WARNING, DO NOT UPDATE CONTENT BETWEEN MKDOCS TEMPLATE TAG !*/
/* Modified content will be overwritten when updating.*/
/*
 * LIGHTGALLERY
 * ----------------------------------------------------------------------------
 * Lightgallery extra javascript
 * From: https://github.com/g-provost/lightgallery-markdown
 */

/*
 * Loading lightgallery
 */
var elements = document.getElementsByClassName("lightgallery");
for(var i=0; i<elements.length; i++) {
  lightGallery(elements[i]);
}

/*
 * Loading video plugins for lightgallery
 */
lightGallery(document.getElementById('html5-videos'));

/*
 * Loading parameter to auto-generate thumbnails for vimeo/youtube video
 */
lightGallery(document.getElementById('video-thumbnails'), {
    loadYoutubeThumbnail: true,
    youtubeThumbSize: 'default',
    loadVimeoThumbnail: true,
    vimeoThumbSize: 'thumbnail_medium',
});

/*
 * Table Sort
 * ----------------------------------------------------------------------------
 * Code snippet to allow sorting table
 * From: https://squidfunk.github.io/mkdocs-material/reference/data-tables/#sortable-tables
 */
document$.subscribe(function() {
  var tables = document.querySelectorAll("article table")
  tables.forEach(function(table) {
    new Tablesort(table)
  })
})


/*
 * Mermaid Configuration to support dark/light switching
 * ----------------------------------------------------------------------------
 * Table Sort
 * Optional config
 * If your document is not specifying `data-md-color-scheme` for color schemes
 * you just need to specify `default`.
 */
window.mermaidConfig = {
  "rdeville-light": {
    startOnLoad: false,
    theme: "default",
    flowchart: {
      htmlLabels: false
    },
    er: {
      useMaxWidth: false
    },
    sequence: {
      useMaxWidth: false,
      /*
       * Mermaid handles Firefox a little different. For some reason, it
       * doesn't attach font sizes to the labels in Firefox. If we specify the
       * documented defaults, font sizes are written to the labels in Firefox.
       */
      noteFontWeight: "14px",
      actorFontSize: "14px",
      messageFontSize: "16px"
    }
  },
  "rdeville-dark": {
    startOnLoad: false,
    theme: "dark",
    flowchart: {
      htmlLabels: false
    },
    er: {
      useMaxWidth: false
    },
    sequence: {
      useMaxWidth: false,
      noteFontWeight: "14px",
      actorFontSize: "14px",
      messageFontSize: "16px"
    }
  }
}
/* END MKDOCS TEMPLATE */
