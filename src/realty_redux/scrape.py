from selenium import webdriver

driver = webdriver.Chrome()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://www.realtor.com/",
    "Alt-Used": "www.realtor.com",
    "Connection": "keep-alive",
    "Cookie": '__vst=53bb0831-28b7-4265-aae3-b3a68afce768; __bot=false; AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=-1124106680%7CMCIDTS%7C20374%7CMCMID%7C05067385349617451875576096832799666454%7CMCAID%7CNONE%7CMCOPTOUT-1760377637s%7CNONE%7CvVersion%7C5.2.0; __split=32; __rdc_id=rdc-id-6a7185fe-b3ba-40c9-b3cf-d2936b23e0a2; G_ENABLED_IDPS=google; kampyleUserSession=1760370413384; kampyleSessionPageCounter=4; kampyleUserSessionsCount=57; g_state={"i_p":1760456819371,"i_l":2,"i_ll":1760370439024,"i_b":"GmNCiev4tdMbFIwHcQbI89nC4VeBO3yLkQgnBBYYA3s"}; split=n; split_tcv=162; __ssn=09454212-6102-4a04-8fdb-73ad07352823; __ssnstarttime=1760108071; AMCVS_8853394255142B6A0A4C98A4%40AdobeOrg=1; _lr_env_src_ats=false; AWSALBTG=GDD1FhMavzg+mrVRndHlF6PyK862f0kzhZe+A8B+yatfgmclv6SZc1hc56zye5NdpkKzjxZ5rEGpdVR/LME+8Kl14NnA6tlZ9A719XjHZbpp/cvXy0FNeeWAfaXcanWVF7Zg7npUarZqRG7r0ptRS70LwIQKzEjgcbPJcYLePEU7; AWSALBTGCORS=GDD1FhMavzg+mrVRndHlF6PyK862f0kzhZe+A8B+yatfgmclv6SZc1hc56zye5NdpkKzjxZ5rEGpdVR/LME+8Kl14NnA6tlZ9A719XjHZbpp/cvXy0FNeeWAfaXcanWVF7Zg7npUarZqRG7r0ptRS70LwIQKzEjgcbPJcYLePEU7; AWSALB=YC2COQp7b/TyEzyt0PUavcVhdApAv2poklpHSmhzXORkzbhh20aUs4RoXhOVE8SI8bIreYwZyMKjAQNqvlbN5B2DqDxPf/EUpf3RQc+2J28NsMiyfgvx9NMkYSYb; AWSALBCORS=YC2COQp7b/TyEzyt0PUavcVhdApAv2poklpHSmhzXORkzbhh20aUs4RoXhOVE8SI8bIreYwZyMKjAQNqvlbN5B2DqDxPf/EUpf3RQc+2J28NsMiyfgvx9NMkYSYb; criteria=city%3DAstoria%26state_id%3DNY%26zip%3D11103%26neighborhood%3D; srchID=9b5e0f03bcd644fcb404ab7ec3e5c2ba; isRVLExists=true; KP_UIDz-ssn=0dJb4AcwyGgl8o7phs39ZiawFdmUKQYD3WT6gXZowR1ogz8EGlwq8Vg8JAa9AG4KPkcbJUDkVqTLEo00qWqLHPp0DOMqsHBcSBUH3FoZjbG6Cmvdig98rvJo2f7ZJ3sBQTeROGwx6Ifxib0btJnSDxJAkj1QtRUKjpDmrxazSD4YJ8u; KP_UIDz=0dJb4AcwyGgl8o7phs39ZiawFdmUKQYD3WT6gXZowR1ogz8EGlwq8Vg8JAa9AG4KPkcbJUDkVqTLEo00qWqLHPp0DOMqsHBcSBUH3FoZjbG6Cmvdig98rvJo2f7ZJ3sBQTeROGwx6Ifxib0btJnSDxJAkj1QtRUKjpDmrxazSD4YJ8u; _lr_geo_location=US; _lr_retry_request=true; kampyleUserPercentile=19.606667469115212',
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "TE": "trailers",
}


def interceptor(request):
    request.headers.update(headers)


driver.request_interceptor = interceptor
driver.get("https://www.realtor.com/realestateandhomes-search/11103")
driver.close()
