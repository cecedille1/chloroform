*** Settings ***
Resource        lib/common.robot
Library         OperatingSystem
Library         lib.expectation
Suite Setup     Run Keywords    Bootstrap suite
...             AND             Loaddata            ${CURDIR}/fixtures/chloroform-translations.yaml
...             AND             Loaddata            ${CURDIR}/fixtures/chloroform-admin.yaml
Suite Teardown  Django              flush
Test Teardown   Empty Mailbox

*** Test Cases ***
Admin edition english
    Initialize Session Lang     lang-en     en
    Login as            admin
    Navigate to         /admin/chloroform/configuration/1/
    Should contain      ${current_page.text}        Succes-english
    Should contain      ${current_page.text}        Succes-french

Admin edition french
    Initialize Session Lang     lang-en     fr
    Login as            admin
    Navigate to         /admin/chloroform/configuration/1/
    Should contain      ${current_page.text}        Succes-english
    Should contain      ${current_page.text}        Succes-french

Admin edition ckeditor
    Initialize Session Lang     lang-en     fr
    Login as            admin
    Navigate to         /admin/chloroform/configuration/1/
    Should contain      ${current_page.text}        ckeditor

*** Keywords ***
Login as
    [arguments]         ${username}
    Navigate to         /admin/login/
    &{data}=            Create Dictionary   username=${username}    password=password
    Post Form           /admin/login/?next=/admin/  ${data}
    Should end with     ${current_page.url}         /admin/
