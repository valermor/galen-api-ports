@@ import header.spec

==========================================================================================
content                                                          id     content-wrap
search-panel                                                     id     search-form
confidence-providers                                             id     confidence
confidence-content                                               id     common-content

==========================================================================================

@ General | iphone, phone
-----------------------------------------------
content
    below: header

search-panel
    component: searchPanel.spec

confidence-providers
    below: search-panel ~15px

confidence-content
    below: confidence-providers ~13px

