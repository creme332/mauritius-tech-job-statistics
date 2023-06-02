import re
from utils.dictionary import (boolean_to_int, merge_dicts)


def web_count(job_details_list):
    count = {"Svelte": False,
             "ASP.NET": False,
             "FastAPI": False,
             "React": False,
             "Vue.js": False,  # or Vue if  english job description
             "Express": False,
             "Spring": False,
             "Ruby on Rails": False,
             "Django": False,
             "Laravel": False,
             "Flask": False,
             "Gatsby": False,
             "Symfony": False,
             "jQuery": False,
             "Drupal": False,
             "Angular.js": False,
             "Angular": False
             }
    count = boolean_to_int(count)
    for job_detail in job_details_list:
        res = boolean_to_int(web_framework_check(job_detail))
        count = merge_dicts(count, res)
    return count


def web_framework_check(job_details):
    """Returns a list of web frameworks present in `job_details`

    Args:
        job_details (str): Job details scraped from website.

    Returns:
        List[str]: A list of web frameworks.
    """

    # ! LIMITATION : Cannot distinguish between the verb react
    # ! and the framework react.

    job_details = job_details.lower()

    # list of words but without special characters
    words = re.findall(r'\w+', job_details)
    is_present = {"Svelte": False,
                  "ASP.NET": False,
                  "FastAPI": False,
                  "React": False,
                  "Vue.js": False,  # or Vue if  english job description
                  "Express": False,
                  "Spring": False,
                  "Ruby on Rails": False,
                  "Django": False,
                  "Laravel": False,
                  "Flask": False,
                  "Gatsby": False,
                  "Symfony": False,
                  "jQuery": False,
                  "Drupal": False,
                  "Angular.js": False,
                  "Angular": False
                  }
    # print(is_present.keys())
    # print(','.join(is_present.keys()))

    for key in is_present:
        lang = key.lower()
        if (lang in words and lang in job_details):
            is_present[key] = True

    # corner case for angular
    foundAngular = False
    for i in range(0, len(words)):
        current_word = words[i]
        next_word = words[min(i+1, len(words)-1)]
        if (current_word == "angular" and next_word != 'js'):
            foundAngular = True
            break
    is_present['Angular'] = foundAngular

    # alternate spellings
    if ('angular.js' in job_details or 'angularjs' in job_details):
        is_present['Angular.js'] = True

    if ('asp.net' in job_details):
        is_present['ASP.NET'] = True

    if ('ruby on rails' in job_details):
        is_present['Ruby on Rails'] = True

    if ('vue.js' in job_details or 'vuejs' in job_details):
        is_present['Vue.js'] = True

    return is_present
