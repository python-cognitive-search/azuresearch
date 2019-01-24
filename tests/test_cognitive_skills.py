from azuresearch.skills.predefined.cognitive_skills import EntityRecognitionSkill, LanguageDetectionSkill, SplitSkill, \
    OCRSkill, KeyPhraseExtractionSkill
from tests.test_helpers import ordered


def test_entity_skill():
    ner_skill = EntityRecognitionSkill(categories=["Organization"])
    dict = ner_skill.to_dict()
    new_skill = EntityRecognitionSkill.load(dict)

    assert ordered(ner_skill.to_dict()) == ordered(new_skill.to_dict())


def test_language_detection_skill():
    language_detection_skill = LanguageDetectionSkill()
    dict = language_detection_skill.to_dict()
    new_skill = LanguageDetectionSkill.load(dict)

    assert ordered(language_detection_skill.to_dict()) == ordered(new_skill.to_dict())


def test_split_skill():
    split_skill = SplitSkill(maximum_page_length=4000)
    dict = split_skill.to_dict()
    new_skill = SplitSkill.load(dict)

    assert ordered(split_skill.to_dict()) == ordered(new_skill.to_dict())


def test_ocr_skill():
    ocr_skill = OCRSkill()
    dict = ocr_skill.to_dict()
    new_skill = OCRSkill.load(dict)

    assert ordered(ocr_skill.to_dict()) == ordered(new_skill.to_dict())



def test_keypharses_skill():
    keyphrases_skill = KeyPhraseExtractionSkill()
    dict = keyphrases_skill.to_dict()
    new_skill = KeyPhraseExtractionSkill.load(dict)

    assert ordered(keyphrases_skill.to_dict()) == ordered(new_skill.to_dict())
