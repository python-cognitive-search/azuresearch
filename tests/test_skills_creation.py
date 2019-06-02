import copy

import pytest

from azuresearch.skills import Skill, SkillInput, SkillOutput, Skillset
from azuresearch.skills.predefined.cognitive_skills import KeyPhraseExtractionSkill
from azuresearch.skills.predefined.cognitive_skills import EntityRecognitionSkill
from tests.test_helpers import ordered, get_json_file

# from azuresearch.indexer import Indexer


def get_simple_skill(
    type="my_skill_type",
    input_name="name",
    input_source="source",
    output_name="name",
    output_target="target",
    context="context",
):
    skill = Skill(
        skill_type=type,
        inputs=[SkillInput(input_name, input_source)],
        outputs=[
            SkillOutput(
                EntityRecognitionSkill.SupportedTypes.EMAIL, output_target)
        ],
        context=context,
    )
    return skill


def get_simple_skill_no_inputs(type="my_skill_type", context="context"):
    skill = Skill(
        skill_type=type,
        outputs=[SkillOutput(
            EntityRecognitionSkill.SupportedTypes.LOCATION, "target")],
        context=context,
    )
    return skill


def get_simple_skill_no_inputs_two_outputs(type="my_skill_type", context="context"):
    skill = Skill(
        skill_type=type,
        outputs=[
            SkillOutput(
                EntityRecognitionSkill.SupportedTypes.PERSON, "target"),
            SkillOutput(
                KeyPhraseExtractionSkill.SupportedTypes.TEXT, "target2"),
        ],
        context=context,
    )
    return skill


def test_skill_creation():
    skill = get_simple_skill()
    assert skill.inputs[0].name == "name"
    assert skill.inputs[0].source == "source"
    assert skill.outputs[0].name == EntityRecognitionSkill.SupportedTypes.EMAIL
    assert skill.outputs[0].target_name == "target"
    assert skill.skill_type == "my_skill_type"


def test_skill_creation_no_inputs():
    skill = get_simple_skill_no_inputs()
    assert skill.skill_type == "my_skill_type"

    assert hasattr(skill, "inputs")
    assert len(skill.inputs) == 0
    assert hasattr(skill, "outputs")


# def connect_skills():
#    skill = get_simple_skill_no_inputs()
#    second_skill = get_simple_skill_no_inputs()
#
#    second_skill.add_source(skill)
#
#    return (skill, second_skill)


# def test_skills_add_source():
#    skill, second_skill = connect_skills()
#    assert hasattr(second_skill, "inputs")
#
#    assert skill.outputs[0].name == second_skill.inputs[0].name
#    assert skill.outputs[0].target_name == second_skill.inputs[0].source
#
#
# def test_skills_add_source_selective():
#    skill = get_simple_skill_no_inputs_two_outputs()
#    second_skill = get_simple_skill_no_inputs()
#
#    # take just 1
#    include_list = []
#    include_list.append(KeyPhraseExtractionSkill.SupportedTypes.TEXT)
#    second_skill.add_source(skill, include_list)
#
#    assert hasattr(second_skill, "inputs")
#
#    assert len(second_skill.inputs) == 1
#    assert second_skill.inputs[0].name == KeyPhraseExtractionSkill.SupportedTypes.TEXT
#
#
# def test_skills_remove_source():
#    skill, second_skill = connect_skills()
#    second_skill.remove_source(skill)
#    assert len(second_skill.inputs) == 0
#
#
# def test_skills_remove_source_name():
#    skill, second_skill = connect_skills()
#    second_skill.remove_source(source_name=skill.outputs[0].name)
#    assert len(second_skill.inputs) == 0


def test_skill_to_dict():
    skill = get_simple_skill()
    assert skill.context == "context"
    assert skill.to_dict()["inputs"][0]["name"] == "name"
    assert skill.to_dict()["inputs"][0]["source"] == "source"
    assert (
        skill.to_dict()["outputs"][0]["name"]
        == EntityRecognitionSkill.SupportedTypes.EMAIL
    )
    assert skill.to_dict()["outputs"][0]["targetName"] == "target"
    assert skill.to_dict()["@odata.type"] == "my_skill_type"


def test_keyphrase_extraction_skill_same_as_json():
    keyphraseExtractionSkill = KeyPhraseExtractionSkill()
    actual = keyphraseExtractionSkill.to_dict()
    expected = get_json_file("keyphrase-extraction-skill.json")

    assert ordered(actual) == ordered(expected)


#### Skillset tests ####


def test_skillset_creation_empty_skills_throws_exception():
    with pytest.raises(Exception):
        skillset = Skillset("myskillset", [])


def test_skillset_simple_skill_wrong_type_throws_exception():
    input = SkillInput("myskill", "source")
    with pytest.raises(Exception):
        skillset = Skillset("myskillset", [input])


def test_skillset_init_correct():
    skill = get_simple_skill()
    skillset = Skillset(name="my_skillset", skills=[skill], description="desc",
                        cognitive_services_key="KEY")
    skillset.name = "my_skillset"
    skillset.description = "desc"
    skillset.skills = [skill]


def test_skillset_to_dict_correct():
    skill1 = get_simple_skill("type1")
    skill2 = get_simple_skill("type2")
    skill3 = get_simple_skill("type3")
    skillset = Skillset(
        name="my_skillset", skills=[skill1, skill2, skill3], description="desc",
        cognitive_services_key="KEY"
    )
    dict = skillset.to_dict()
    assert dict["name"] == "my_skillset"
    assert dict["skills"][0]["@odata.type"] == "type1"
    assert dict["skills"][1]["@odata.type"] == "type2"
    assert dict["skills"][2]["@odata.type"] == "type3"


def test_load_to_dict_same():
    expected = get_json_file("skillset_simple.json")
    skillset_dict = copy.deepcopy(expected)

    skillset = Skillset.load(skillset_dict)
    actual = skillset.to_dict()

    assert ordered(actual) == ordered(expected)
