*** Settings ***
Resource        lib/common.robot
Library         OperatingSystem
Library         lib.expectation
Suite Setup     Run Keywords    Bootstrap suite
...             AND             Loaddata            ${CURDIR}/fixtures/chloroform-translations.yaml
Suite Teardown  Django              flush
Test Teardown   Empty Mailbox

*** Test Cases ***
English page
    Initialize Session Lang     lang-en     en
    Navigate to         /cl/
    Should contain      ${current_page.text}        Description english
    Should contain      ${current_page.text}        Verbose name english
    Should contain      ${current_page.text}        Alternative label english

French page
    Initialize Session Lang     lang-fr     fr
    Navigate to         /cl/
    Should contain      ${current_page.text}        Description french
    Should contain      ${current_page.text}        Verbose name french
    Should contain      ${current_page.text}        Alternative label english


*** Keywords ***
Initialize Session Lang
    [arguments]     ${session_name}     ${lang}
    &{headers}=     Create Dictionary   accept-language=${lang}
    Create Session      ${session_name}             ${BASEURL}  headers=&{headers}
    Set Test Variable   ${session}                  ${session_name}
