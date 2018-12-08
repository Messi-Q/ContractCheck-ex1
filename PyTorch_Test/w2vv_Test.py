import re

ENGLISH_STOP_WORDS = "i me my myself we our ours ourselves you your yours yourself yourselves " \
                     "he him his himself she her hers herself it its itself they them their theirs themselves " \
                     "what which who whom this that these those am is are was were be been being have has had having " \
                     "do does did doing a an the and but if or because as until while of at by for with about against " \
                     "between into through during before after above below to from up down in out on off over under " \
                     "again further then once here there when where why how all any both each few more most other some " \
                     "such no nor not only own same so than too very s t can will just don should now d ll m o re ve y " \
                     "ain aren couldn didn doesn hadn hasn haven isn ma mightn mustn needn shan shouldn wasn weren won " \
                     "wouldn".strip().split()


def clean_str(string):
    string = re.sub(r"[^A-Za-z0-9]", " ", string)
    return string.strip().lower().split()


def clean_str_filter_stop(string):
    string = re.sub(r"[^A-Za-z0-9]", " ", string)
    cleaned_string = string.strip().lower().split()
    # remove stop words
    return [word for word in cleaned_string if word not in ENGLISH_STOP_WORDS]


if __name__ == '__main__':
    test_strs = '''a Dog is running
        The dog runs
        dogs-x runs'''.split('\n')

    for t in test_strs:
        print(t, '->', clean_str(t), '->', clean_str_filter_stop(t))
