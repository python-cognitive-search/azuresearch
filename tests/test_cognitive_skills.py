from azuresearch.indexes import CollectionField
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


def test_input_mapping_keyphrase_skill():
    keyphrases_skill = KeyPhraseExtractionSkill()
    keyphrases_field = CollectionField("keyphrases")
    keyphrases_skill.key_phrases.map_to(keyphrases_field)

    assert keyphrases_skill.output_field_mapping[0].source_field_name == "keyPhrases"
    assert keyphrases_skill.output_field_mapping[0].target_field_name == "keyphrases"


def test_keyphrase_skill_set_input():
    keyphrases_skill = KeyPhraseExtractionSkill()
    splitskill = SplitSkill()
    language_detection_skill = LanguageDetectionSkill()

    keyphrases_skill.set_inputs(text=splitskill.text_items,
                                language_code=language_detection_skill.language_code)
    assert keyphrases_skill.inputs[0].source ==  "/document/pages/*"
    assert keyphrases_skill.inputs[1].source == "/document/languageCode"
    assert len(keyphrases_skill.inputs) == 2
