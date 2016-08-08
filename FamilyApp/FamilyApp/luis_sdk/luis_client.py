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

import threading
from urllib.parse import quote
import http.client
import luis_response
from luis_response import LUISResponse

class LUISClient:
    '''
    This is the interface of the LUIS
    Constructs a LUISClient with the corresponding user's App Id and Subscription Keys
    Starts the prediction procedure for the user's text, and accepts a callback function
    '''
    _LUISURL = 'api.projectoxford.ai'
    _PredictMask = '/luis/v1/application%s?id=%s&subscription-key=%s&verbose=%s&q=%s'
    _ReplyMask = '/luis/v1/application%s?id=%s&subscription-key=%s&contextid=%s&verbose=%s&q=%s'

    def __init__(self, app_id, app_key, preview=False, verbose=False):
        '''
        A constructor for the LUISClient class.
        :param app_id: A string containing the application id.
        :param app_key: A string containing the subscription key.
        :param preview: A boolean to indicate whether the preview version should used or not.
        :param verbose: A boolean to indicate whether the verbose version should used or not.
        '''
        if app_id is None:
            raise TypeError('NULL App Id')
        if not app_id:
            raise ValueError('Empty App Id')
        if ' ' in app_id:
            raise ValueError('Invalid App Id')
        if app_key is None:
            raise TypeError('NULL Subscription Key')
        if not app_key:
            raise ValueError('Empty Subscription Key')
        if ' ' in app_key:
            raise ValueError('Invalid Subscription Key')

        self._app_id = app_id
        self._app_key = app_key
        self._preview = True if preview else False
        self._preview_url = '/preview' if preview else ''
        self._verbose_url = 'true' if verbose else 'false'

    def predict(self, text, response_handlers=None, daemon=False):
        '''
        Routes the prediction routine to either sync or async
        based on the presence or absence of a callback fucntion.
        :param text: the text to be analysed and predicted.
        :param response_handlers: a dictionary that contains two keys on_success and on_failure,
        whose values are two functions to be executed if async.
        :param daemon: defines whether the new thread used for async will be daemon or not.
        :return: LUISResponse if sync, thread object to give control over the thread if async.
        '''
        if response_handlers is None:
            return self.predict_sync(text)
        else:
            return self.predict_async(text, response_handlers, daemon)

    def predict_sync(self, text):
        '''
        Predicts synchronously and returns a LUISResponse.
        :param text: The text to be analysed and predicted.
        :return: A LUISResponse object containing the response data.
        '''
        if text is None:
            raise TypeError('NULL text to predict')
        if not text:
            raise ValueError('Empty text to predict')
        try:
            conn = http.client.HTTPSConnection(self._LUISURL)
            conn.request('GET', self._predict_url_gen(text))
            res = conn.getresponse()
            return LUISResponse(res.read().decode('UTF-8'))
        except Exception:
            raise

    def predict_async(self, text, response_handlers, daemon):
        '''
        Predicts asynchronously and executes a callback function at the end.
        :param text: The text to be analysed and predicted.
        :param response_handlers: A dictionary that contains two keys on_success and on_failure,
        whose values are two functions to be executed if async.
        :param daemon: Defines whether the new thread will be daemon or not.
        :return: A thread object to give control over the thread.
        '''
        if text is None:
            raise TypeError('NULL text to predict')
        if not text:
            raise ValueError('Empty text to predict')
        if 'on_success' not in response_handlers:
            raise KeyError('You have to specify the success handler with key: "on_success"')
        if 'on_failure' not in response_handlers:
            raise KeyError('You have to specify the failure handler with key: "on_failure"')
        predict_thread = threading.Thread(target=self._predict_async_helper
                                          , args=(text, response_handlers))
        predict_thread.daemon = daemon
        predict_thread.start()
        return predict_thread

    def _predict_url_gen(self, text):
        '''
        Returns the suitable LUIS API predict url.
        :param text: The text to be analysed and predicted.
        :return: LUIS API predicton url.
        '''
        return self._PredictMask%(self._preview_url, self._app_id, self._app_key
                                  , self._verbose_url, quote(text))

    def _predict_async_helper(self, text, response_handlers):
        '''
        A wrapper function to be executed asynchronously in an external thread.
        It executes the predict routine and then executes a callback function.
        :param text: The text to be analysed and predicted.
        :param response: A LUISResponse that contains the context Id.
        :param response_handlers: A dictionary that contains two keys on_success and on_failure,
        whose values are two functions to be executed if async.
        :return: None.
        '''
        res = None
        try:
            res = self.predict_sync(text)
        except Exception as exc:
            response_handlers['on_failure'](exc)
            return
        response_handlers['on_success'](res)

    def reply(self, text, response, response_handlers=None, daemon=False):
        '''
        Routes the reply routine to either sync or async
        based on the presence or absence of a callback fucntion.
        :param text: The text to be analysed and predicted.
        :param response: A LUISResponse that contains the context Id.
        :param response_handlers: A dictionary that contains two keys on_success and on_failure,
        whose values are two functions
        to be executed if async.
        :param daemon: Defines whether the new thread used for async will be daemon or not.
        :return: A LUISResponse object if sync, a thread object to control the thread if async.
        '''
        if response_handlers is None:
            return self.reply_sync(text, response)
        else:
            return self.reply_async(text, response, response_handlers, daemon)

    def reply_sync(self, text, response):
        '''
        Replies synchronously and returns a LUISResponse object.
        :param text: The text to be analysed and predicted.
        :return: A LUISResponse object containg the response data.
        '''
        if text is None:
            raise TypeError('NULL text to predict')
        if not text:
            raise ValueError('Empty text to predict')
        if not self._preview:
            raise Exception("Can't use reply unless in the preview mode")
        try:
            conn = http.client.HTTPSConnection(self._LUISURL)
            conn.request('GET', self._reply_url_gen(text, response))
            res = conn.getresponse()
            return LUISResponse(res.read().decode('UTF-8'))
        except Exception:
            raise

    def reply_async(self, text, response, response_handlers, daemon):
        '''
        Predicts asynchronously and executes a callback function at the end.
        :param text: The text to be analysed and predicted.
        :param response_handlers: A dictionary that contains two keys on_success and on_failure,
        whose values are two functions
        to be executed if async.
        :param daemon: Defines whether the new thread used will be daemon or not.
        :return: A thread object to give control over the thread.
        '''
        if text is None:
            raise TypeError('NULL text to predict')
        if not text:
            raise ValueError('Empty text to predict')

        if 'on_success' not in response_handlers:
            raise KeyError('You have to specify the success handler with key: "on_success"')
        if 'on_failure' not in response_handlers:
            raise KeyError('You have to specify the failure handler with key: "on_failure"')
        reply_thread = threading.Thread(target=self._reply_async_helper
                                        , args=(text, response, response_handlers))
        reply_thread.daemon = daemon
        reply_thread.start()
        return reply_thread

    def _reply_url_gen(self, text, response):
        '''
        Generates the suitable LUIS API reply url.
        :param text: The text to be analysed and predicted.
        :param response: A LUISResponse object that contains the context Id.
        :return: LUIS API reply url.
        '''
        return self._ReplyMask%(self._preview_url, self._app_id, self._app_key
                                , response.get_dialog().get_context_id()
                                , self._verbose_url, quote(text))

    def _reply_async_helper(self, text, response, response_handlers):
        '''
        A wrapper function to be executed asynchronously in an external thread.
        It executes the reply routine and then executes a callback function.
        :param text: The text to be analysed and predicted.
        :param response: A LUISResponse object that contains the context Id.
        :param response_handlers: A dictionary that contains two keys on_success and on_failure,
        whose values are two functions to be executed if async.
        :return: None.
        '''
        res = None
        try:
            res = self.reply_sync(text, response)
        except Exception as exc:
            response_handlers['on_failure'](exc)
            return
        response_handlers['on_success'](res)
