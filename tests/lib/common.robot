*** Settings ***
Library         lib.WsgiServer     lib.site.wsgi.application
Library         RequestsLibrary
Library         lib.Django
Library         lib.HttpClient

*** Keywords ***
Wait Email sent to
    [arguments]     ${email_addr}
    ${email}=       Wait Until Keyword Succeeds     3x      1s
    ...             Get Email Sent To               ${email_addr}
    Set Test Variable       ${email}    ${email}
    [return]        ${email}

Initialize session
    [arguments]     ${session_name}
    Create Session      ${session_name}             ${BASEURL}
    Set Test Variable   ${session}                  ${session_name}

Bootstrap Suite
    Django              Check
    Setup database
    Start Application

Navigate to
    [arguments]     ${page}
    ${resp}=    Get Request     ${session}  ${page}     allow_redirects=False
    Should be Equal As Strings  ${resp.status_code}     200
    Set Test Variable           ${current_page}         ${resp}
    [return]        ${resp}

Post Form
    [arguments]     ${submit_page}      ${data}
    ${resp}=    Post Protected Request    ${submit_page}      data=${data}
    Set Test Variable           ${current_page}         ${resp}
    Should be Equal As Strings  ${resp.status_code}     200
    [return]        ${resp}

Should be JSON Equal
    [arguments]         ${actual}       ${expected}
    ${expected}=        Evaluate        json.loads('''${expected}''')     json
    Should be Equal     ${actual}       ${expected}

Initialize Session Lang
    [arguments]     ${session_name}     ${lang}
    &{headers}=     Create Dictionary   accept-language=${lang}
    Create Session      ${session_name}             ${BASEURL}  headers=&{headers}
    Set Test Variable   ${session}                  ${session_name}
