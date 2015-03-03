==============================================================================
header                                          id          header
logo                                            id          identity
tab-flights                                     css         li.airli
tab-carhire                                     css         li.carhi
tab-hotels                                      css         li.skhot
hamburger-dropdown                              id          toggle-touch-menu
==============================================================================

@ General | all
----------------------------------------------------------
header
    height: 104 to 110px

[flights, carhire, hotels]
tab-@
    height: 31 to 39px

[carhire, flights, hotels]
tab-@
    aligned horizontally all: tab-carhire

@ ^ | mobile
-----------------------------------------------------------
logo
    inside: header 7 to 31px top left

@ ^ | tablet, desktop
-----------------------------------------------------------
logo
    aligned vertically left: header

@ Static links behaviour | all
-----------------------------------------------
header
    contains: logo

@ ^ | mobile
----------------------------------------------------------
header
    height: 110px
    contains: hamburger-dropdown

@ ^ | tablet
----------------------------------------------------------
header
    height: 104px

@ ^ | desktop
----------------------------------------------------------
header
    height: 104px