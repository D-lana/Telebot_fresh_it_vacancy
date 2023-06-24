from info import dict_habr_tag, url_habr


class ErrorDict(Exception):
    def __init__(self):
        self.txt = "Error keys for dictionary tags!"


def check_correct_data(lang, grade) ->bool:
    if lang in dict_habr_tag["skills[]"] and grade in dict_habr_tag["qid"]:
        return True
    else:
        return False


def request_formation(lang, grade) ->str:    
    if lang in dict_habr_tag["skills[]"] and grade in dict_habr_tag["qid"]:
        qid = "qid=" + str(dict_habr_tag["qid"][grade])
        skills = "skills[]=" + str(dict_habr_tag["skills[]"][lang])
        sort_and_type = "sort=date&type=all"
        vacancies = "/vacancies?"
        url = url_habr + vacancies + "&".join([qid, skills, sort_and_type])
        return url
    else:
        raise ErrorDict


if __name__ == "__main__":
    lang = "python"
    grade = "junior"
    try:
        url = request_formation(lang, grade)
        print(url)
    except ErrorDict as ex:
        print(ex.txt)
