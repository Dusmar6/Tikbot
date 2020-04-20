# import requests
# import time
#
# EMAIL = 'emaild@gmail.com'
# PASSWORD = 'password'
# HASHTAG = 'coronatime'
#
# def encryptXOR(value, key=5):
#     b = value.encode()
#     x = []
#     for i in range(len(b)):
#         x.append(str(hex(b[i] ^ key)))
#
#     result = ''
#     for item in x:
#         result += item[2:]
#     return result
#
# def getKhronos():
#     return str(int(time.time()))
#
# user_info = {
#     'encrypted_email': encryptXOR(EMAIL),
#     'encrypted_password': encryptXOR(PASSWORD),
#     'iid': '6808596998528583430',
#     'openudid': 'bcaa82baadf2e66292e8384670ae79b89de27162',
#     'device_id': '',
#     'os_api': '18',
#     'device_platform' : 'iphone',
#     'device_type': 'iPhone11,8',
#     'os_version': '13.3.1',
#     'idfa' : '3C14945C-D647-4464-B0A9-F744A01AA757',
#     'vid' : '45124BD0-ED92-4FB2-B4D4-56F230582AF3',
#     'cdid' : '3AC64CFA-B526-4459-94EF-5F39C90E74FB',
#     'version_code' : '15.4.0'
# }
# #85701356000 02020040100355601018907221632925EFA
# #84024029000 026ac360b0e716fac677076dabc50c92bb25b26cd
# #8402e055000 0e3a49cd30591715b5c856ec426b5d8a080aa6c52
#
# session = requests.session()
#
# data = {'email': user_info['encrypted_email'], 'mix_mode': '1', 'multi_login': '1', 'password': user_info['encrypted_password']}
# headers = {'Host': 'api2-19-h2.musical.ly', 'User-Agent': 'TikTok ' + user_info['version_code'] + ' rv:154014 (iPhone; iOS 13.3.1; en_US) Cronet'}
# session.headers = headers
# response = session.post('https://api2-19-h2.musical.ly/passport/user/login/?device_id=' + user_info['device_id'] + '&residence=US&is_my_cn=0&os_version=' + user_info['os_version'] +'&iid=' + user_info['iid'] + '&app_name=musical_ly&pass-route=1&locale=en&pass-region=1&ac=WIFI&sys_region=US&version_code=' + user_info['version_code'] + '&vid=' + user_info['vid'] + '&channel=App%20Store&op_region=US&os_api=' + user_info['os_api'] + '&idfa=' + user_info['idfa'] + '&device_platform=' + user_info['device_platform'] + '&device_type=' + user_info['device_type'] + '&openudid=' + user_info['openudid'] + '&account_region=&tz_name=America/Los_Angeles&tz_offset=-25200&app_language=en&carrier_region=US&current_region=US&aid=1233&mcc_mnc=310410&screen_width=828&build_number=154014&uoo=0&language=en&cdid=' + user_info['cdid'] + '&content_language=&app_version=' + user_info['version_code'], headers=headers, data=data)
#
# print('__ATTRS__:', response.__attrs__)
# print('STATUS CODE:', response.status_code)
# print('TEXT:', response.text)
# print('COOKIES:', response.cookies)
# print('HEADERS:', response.headers)
#
# print(session.headers)
# print(session.cookies)
#
# # AFTER LOGGING IN GET OWN ACCOUNT DATA
# self_account_data = session.get('https://api2-19-h2-eagle.musical.ly/aweme/v1/user/profile/self/?device_id=' + user_info['device_id'] + '&residence=US&is_my_cn=0&os_version=' + user_info['os_version'] + '&iid=' + user_info['iid'] + '&app_name=musical_ly&pass-route=1&locale=en&pass-region=1&ac=WIFI&sys_region=US&version_code=' + user_info['version_code'] + '&vid=' + user_info['vid'] + '&channel=App%20Store&op_region=US&os_api=' + user_info['os_api'] + '&idfa=' + user_info['idfa'] + '&device_platform=' + user_info['device_platform'] + '&device_type=' + user_info['device_type'] + '&openudid=' + user_info['openudid'] + '&account_region=&tz_name=America/Los_Angeles&tz_offset=-25200&app_language=en&carrier_region=US&current_region=US&aid=1233&mcc_mnc=310410&screen_width=828&build_number=154014&uoo=0&language=en&cdid=' + user_info['cdid'] + '&content_language=&app_version=' + user_info['version_code'] + '&need_pv=1')
# print('GET self_account_data response:', self_account_data.status_code, '=', self_account_data.text)
#
# # SEARCH FOR A USERNAME
# session.headers['x-common-params-v2'] = 'pass-region=1&pass-route=1&language=en&version_code=' + user_info['version_code'] + '&app_name=musical_ly&vid=' + user_info['vid'] + '&app_version=' + user_info['version_code'] + '&carrier_region=US&is_my_cn=0&channel=App%20Store&mcc_mnc=310410&device_id=' + user_info['device_id'] + '&tz_offset=-25200&account_region=US&sys_region=US&aid=1233&residence=US&screen_width=828&uoo=0&openudid=' + user_info['openudid'] + '&os_api=' + user_info['os_api'] + '&os_version=' + user_info['os_version'] + '&app_language=en&tz_name=America/Los_Angeles&current_region=US&device_platform=' + user_info['device_platform'] + '&build_number=154014&device_type=' + user_info['device_type'] + '&iid=' + user_info['iid'] + '&idfa=' + user_info['idfa'] + '&locale=en&cdid=' + user_info['cdid'] + '&content_language='
# session.headers['X-Khronos'] = getKhronos()
# search = session.get('https://api2-19-h2.musical.ly/aweme/v1/general/search/single/?ac=WIFI&op_region=US&is_pull_refresh=0&offset=0&search_source=normal_search&is_filter_search=0&count=10&keyword=grandsoapy&hot_search=0&publish_time=0&sort_type=0&query_correct_type=1&')
# print('GET SEARCH RESPONSE', search.status_code, '=', search.text)
#
# # # BELOW RETURNS A 404 RESPONSE AND IS THE FIRST CALL THAT REQUIRES THE 'x-common-params-v2' HEADER
# # session.headers['x-common-params-v2'] = 'pass-region=1&pass-route=1&language=en&version_code=' + user_info['version_code'] + '&app_name=musical_ly&vid=' + user_info['vid'] + '&app_version=' + user_info['version_code'] + '&carrier_region=US&is_my_cn=0&channel=App%20Store&mcc_mnc=310410&device_id=' + user_info['device_id'] + '&tz_offset=-25200&account_region=US&sys_region=US&aid=1233&residence=US&screen_width=828&uoo=0&openudid=' + user_info['openudid'] + '&os_api=' + user_info['os_api'] + '&os_version=' + user_info['os_version'] + '&app_language=en&tz_name=America/Los_Angeles&current_region=US&device_platform=' + user_info['device_platform'] + '&build_number=154014&device_type=' + user_info['device_type'] + '&iid=' + user_info['iid'] + '&idfa=' + user_info['idfa'] + '&locale=en&cdid=' + user_info['cdid'] + '&content_language='
# # check_in = session.get('https://api2-16-h2.musical.ly/aweme/v1/check/in/?ac=WIFI&op_region=US&')
# # print('GET check_in response:', check_in.status_code, '=', check_in.text)
#
#
#
#
#
#
# ### ABOVE WORKING
# ### BELOW NEEDS SOME WORK
# # https://api2-19-h2.musical.ly/aweme/v2/category/list/?ac=WIFI&op_region=US&cursor=0&ad_personality_mode=1&is_complete=1&count=12&cmpl_enc=HB2-EnTn4teO-TKALBRbMDnIzaLyeaLfJXMer_VC9Cbq&
# # https://api2-19-h2.musical.ly/aweme/v2/category/list/?ac=WIFI&op_region=US&cursor=0&ad_personality_mode=1&is_complete=1&count=12&cmpl_enc=HB2-EnTn4teO-TKALBRbMDnIzaLyeaLfJXMer_VC9Cbo&
# # https://api2-19-h2.musical.ly/aweme/v2/category/list/?ac=WIFI&op_region=US&cursor=0&ad_personality_mode=1&is_complete=1&count=12&cmpl_enc=HB2-EnTn4teO-TKALBRbMDnIzaLyeaLfJXMer_VC9Cbm&
# # https://api2-19-h2.musical.ly/aweme/v2/category/list/?ac=WIFI&op_region=US&cursor=0&ad_personality_mode=1&is_complete=1&count=12&cmpl_enc=HB2-EnTn4teO-TKALBRbMDnIzaLyeaLfJXMer_VC9Cbn&
# # https://api2-19-h2.musical.ly/aweme/v2/category/list/?ac=WIFI&op_region=US&cursor=0&ad_personality_mode=1&is_complete=1&count=12&cmpl_enc=HB2-EnTn4teO-TKALBRbMDnIzaLyeaLfJXMer_VC9Cbl&
# # response = session.get('https://api2-19-h2.musical.ly/aweme/v2/category/list/?ac=WIFI&op_region=US&cursor=0&ad_personality_mode=1&is_complete=1&count=12&cmpl_enc=HB2-EnTn4teO-TKALBRbMDnIzaLyeaLfJXMer_VC9Cbe&')
#
#
#
# # ### ABOVE NEEDS TO BE CHAINED BEFORE BELOW CAN WORK
# # """
# # GET THE CHALLENGE (HASHTAG) ID
# # """
# # response = session.get('https://api2-19-h2.musical.ly/aweme/v1/challenge/aweme/?ac=WIFI&op_region=US&cursor=0&ch_id=45975747&source=challenge_video&query_type=0&count=18&pull_type=2&type=5&')
# # print('HASHTAG SEARCH STATUS CODE:', response.status_code)
# # print('HASHTAG SEARCH __ATTRS__:', response.__attrs__)
# # print('HASHTAG SEARCH _content:', response._content)
# # print('HASHTAG SEARCH TEXT:', response.text)
