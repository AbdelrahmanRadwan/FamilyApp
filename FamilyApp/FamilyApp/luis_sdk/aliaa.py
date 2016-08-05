'''
Copyright (c) Microsoft. All rights reserved.
Licensed under the MIT license.

Microsoft Cognitive Services (formerly Project Oxford): https://www.microsoft.com/cognitive-services

Microsoft Cognitive Services (formerly Project Oxford) GitHub:
https://github.com/Microsoft/ProjectOxford-ClientSDK

Copyright (c) Microsoft Corporation
All rights reserved.

MIT License:
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED ""AS IS"", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from luis_sdk import LUISClient

APPID = '06285731-8488-4da8-bb77-7f2ae52c9597'
APPKEY = '4df47277993a4f18a35dbdb8428156a5'   
TEXT = input('What do you need?\n')
CLIENT = LUISClient(APPID, APPKEY, True, True)

def on_success(res):
    '''
    A callback function that processes the luis_response object
    if the prediction succeeds.
    :param res: a luis_response object containing the response data.
    :return: None
    '''
    print('prediction successful')
    while not res.get_dialog().is_finished():
        print(res.get_dialog().get_status())
        TEXT = input(res.get_dialog().get_prompt()+': \n')
        res = CLIENT.reply(TEXT, res)
    print(res.get_dialog().get_status())
def on_failure(err):
    '''
    A callback function that processes the error object
    if the prediction fails.
    :param err: An Exception object.
    :return: None
    '''
    print(err)

CLIENT.predict(TEXT, {'on_success': on_success, 'on_failure': on_failure})
print('-------\nMain thread finishing!!\n-------')
