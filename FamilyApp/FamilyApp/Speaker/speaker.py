""" Copyright (c) Microsoft. All rights reserved.
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
"""

import IdentificationServiceHttpClientHelper
import sys

enrollmentExcerpts = [
    { "Martin Luther King Jr" : '''I am happy to join with you today in what will go down in history as the greatest demonstration
                             for freedom in the history of our nation. Five score years ago, a great American, in whose symbolic
                             shadow we stand today, signed the Emancipation Proclamation. This momentous decree came as a great 
                             beacon light of hope to millions of Negro slaves who had been seared in the flames of withering 
                             injustice. It came as a joyous daybreak to end the long night of their captivity. But one hundred years 
                             later, the Negro still is not free.'''},
    {"Abraham Lincoln": '''Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in 
                            Liberty, and dedicated to the proposition that all men are created equal. Now we are engaged in a great 
                            civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We 
                            are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final 
                            resting place for those who here gave their lives that that nation might live. It is altogether fitting and
                            proper that we should do this.''' },
    {"William Lyon Phelps": '''The habit of reading is one of the greatest resources of mankind; and we enjoy reading books that belong 
                            to us much more than if they are borrowed. A borrowed book is like a guest in the house; it must be treated 
                            with punctiliousness, with a certain considerate formality. You must see that it sustains no damage; it must 
                            not suffer while under your roof. You cannot leave it carelessly, you cannot mark it, you cannot turn down 
                            the pages, you cannot use it familiarly. And then, some day, although this is seldom done, you really ought 
                            to return it.'''}


]
def create_profile(subscription_key, locale):
    """Creates a profile on the server.

    Arguments:
    subscription_key -- the subscription key string
    locale -- the locale string
    """
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

    creation_response = helper.create_profile(locale)
    print(creation_response.get_profile_id())
    return creation_response.get_profile_id()



def enroll_profile(subscription_key, profile_id, file_path):
    """Enrolls a profile on the server.

    Arguments:
    subscription_key -- the subscription key string
    profile_id -- the profile ID of the profile to enroll
    file_path -- the path of the file to use for enrollment
    """
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

    enrollment_response = helper.enroll_profile(profile_id, file_path)

    print('Total Enrollment Speech Time = {0}'.format(enrollment_response.get_total_speech_time()))
    print('Remaining Enrollment Time = {0}'.format(enrollment_response.get_remaining_speech_time()))
    print('Speech Time = {0}'.format(enrollment_response.get_speech_time()))
    print('Enrollment Status = {0}'.format(enrollment_response.get_enrollment_status()))
    return enrollment_response

def identify_file(subscription_key, file_path, profile_ids):
    """Identify an audio file on the server.

    Arguments:
    subscription_key -- the subscription key string
    file_path -- the audio file path for identification
    profile_ids -- an array of test profile IDs strings
    """
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)
    identification_response = helper.identify_file(file_path, profile_ids)
    
    print('Identified Speaker = {0}'.format(identification_response.get_identified_profile_id()))
    print('Confidence = {0}'.format(identification_response.get_confidence()))
    return identification_response

def print_all_profiles(subscription_key):
    """Print all the profiles for the given subscription key.

    Arguments:
    subscription_key -- the subscription key string
    """
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

    profiles = helper.get_all_profiles()

    print('Profile ID, Locale, Enrollment Speech Time, Remaining Enrollment Speech Time,'
          ' Created Date Time, Last Action Date Time, Enrollment Status')
    for profile in profiles:
        print('{0}, {1}, {2}, {3}, {4}, {5}, {6}'.format(
            profile.get_profile_id(),
            profile.get_locale(),
            profile.get_enrollment_speech_time(),
            profile.get_remaining_enrollment_time(),
            profile.get_created_date_time(),
            profile.get_last_action_date_time(),
            profile.get_enrollment_status()))
