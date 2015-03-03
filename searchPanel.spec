==========================================================================================
container                                                         xpath         .
destination-input-label                                           xpath      //div[@class='input-holder']/preceding-sibling::label
destination-input                                                 id         q
start-date-input-label                                            xpath      id('sd-placeholder')/parent::label
start-date-input                                                  id         sd-placeholder
end-date-input-label                                              xpath      id('ed-placeholder')/parent::label
end-date-input                                                    id         ed-placeholder
guests-dropdown-label                                             xpath      id('na')/preceding-sibling::label`
guests-dropdown                                                   id         na
rooms-dropdown-label                                              xpath      id('nr')/preceding-sibling::label
rooms-dropdown                                                    id         nr
submit-button                                                     id         submit-search
start-calendar                                                    xpath      id('sd-placeholder')/parent::label::after
==========================================================================================

@ Search panel | iphone, phone
-----------------------------------------------
container
    width: ~ 95% of screen/width

destination-input
    inside: container ~8px left right
    width: ~ 95% of container/width
    centered horizontally inside: container
    aligned vertically left: destination-input-label

start-date-input
    width: ~ 45% of container/width
    aligned vertically left: destination-input
    aligned vertically left: guests-dropdown
    aligned vertically left: start-date-input-label
    aligned horizontally top: end-date-input
    near: end-date-input ~ 8px left

end-date-input
    width: ~ 46% of container/width
    aligned vertically right: destination-input
    aligned vertically right: submit-button 2px
    aligned vertically left: end-date-input-label

guests-dropdown
    aligned horizontally all: rooms-dropdown
    aligned vertically left: guests-dropdown-label

rooms-dropdown
    aligned vertically left: rooms-dropdown-label
    aligned horizontally bottom: submit-button 2px

submit-button
    inside: container ~8px right
    color scheme: ~80% #aae700


