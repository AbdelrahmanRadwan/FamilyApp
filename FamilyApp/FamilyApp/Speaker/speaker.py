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

def create_profile(subscription_key, locale):
    """Creates a profile on the server.

    Arguments:
    subscription_key -- the subscription key string
    locale -- the locale string
    """
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

    creation_response = helper.create_profile(locale)

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

    return enrollment_response
    #print('Total Enrollment Speech Time = {0}'.format(enrollment_response.get_total_speech_time()))
    #print('Remaining Enrollment Time = {0}'.format(enrollment_response.get_remaining_speech_time()))
    #print('Speech Time = {0}'.format(enrollment_response.get_speech_time()))
    #print('Enrollment Status = {0}'.format(enrollment_response.get_enrollment_status()))


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
    return identification_response
    #print('Identified Speaker = {0}'.format(identification_response.get_identified_profile_id()))
    #print('Confidence = {0}'.format(identification_response.get_confidence()))

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
