*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${glossary_title_selector} =  input#form-widgets-IBasic-title
${term_title_selector} =  input#form-widgets-title

*** Test cases ***

Test CRUD
    Enable Autologin as  Site Administrator
    Go to Homepage

    Create Glossary  The Beatles
    Create Term  The Beatles  John
    Create Term  The Beatles  Paul
    Create Term  The Beatles  George
    Create Term  The Beatles  Ringo
    Check Terms  The Beatles  John  Paul  George  Ringo
    Delete Glossary  The Beatles

*** Keywords ***

Click Add Glossary
    Open Add New Menu
    Click Link  css=a#glossary
    Page Should Contain  Add Glossary

Click Add Term
    Open Add New Menu
    Click Link  css=a#glossaryterm
    Page Should Contain  Add Glossary Term

Create Glossary
    [arguments]  ${title}

    Click Add Glossary
    Input Text  css=${glossary_title_selector}  ${title}
    Click Button  Save
    Page Should Contain  Item created

Create Term
    [arguments]  ${glossary}  ${title}

    Click Link  ${glossary}
    Click Add Term
    Input Text  css=${term_title_selector}  ${title}
    Click Button  Save
    Page Should Contain  Item created

Check Terms
    [arguments]  ${glossary}  @{terms}

    Click Link  ${glossary}
    :FOR  ${term}  IN  @{terms}
    \   Page Should Contain  ${term}

Delete Glossary
    [arguments]  ${glossary}

    Click Link  ${glossary}
    Open Action Menu
    Click Link  css=a#plone-contentmenu-actions-delete
    Click Button  Delete
    Page Should Contain  Plone site
