""" Skill
"""
import json
from abc import abstractmethod

from azuresearch.azure_search_object import AzureSearchObject
from azuresearch.field_mapping import FieldMapping
from azuresearch.indexes import Field


class Skill(AzureSearchObject):
    """ An Azure search skill
    """

    def __init__(self, **kwargs):
        """
        :param skill_type: the type of skill (@odata.type)
        :param inputs: A list of objects of type SkillInput which represent the desire inputs
                       for this skill
        :param outputs: A list of objects of type SkillOutput which represent the desired outputs
                        for this skill
        :param context: Each skill should have a "context".
                        The context represents the level at which operations take place
        :param params: Additional arguments for this skill
        """
        super().__init__(**kwargs)

        self.inputs = []  ## Start with empty list of inputs, unless explicitly stated. Inputs should be either
        # defined in the constructor or using the set_inputs method
        if "inputs" in kwargs and kwargs['inputs'] is not None:
            inputs = kwargs['inputs']
            for inp in inputs:
                if not isinstance(inp, SkillInput):
                    raise TypeError("Input should be of type SkillInput. Wrong input = {}".format(inp))
            self.inputs = inputs
        else:
            self.inputs = self.get_default_inputs()

        if "outputs" in kwargs and kwargs['outputs'] is not None:
            outputs = kwargs['outputs']
            for outp in outputs:
                if not isinstance(outp, SkillOutput):
                    raise TypeError("Output should be of type SkillOutput. Wrong output = {}".format(outp))
            self.outputs = outputs
        else:
            self.set_default_outputs()

        if "@odata.type" in kwargs:
            self.skill_type = kwargs.get("@odata.type")
        else:
            self.skill_type = kwargs.get("skill_type")

        self.context = kwargs.get("context")
        if self.context is None:
            self.context = "/document"
        self.output_field_mapping = kwargs.get("output_field_mapping")
        if self.output_field_mapping is None:
            self.output_field_mapping = []

        self.params = {k: v for (k, v) in kwargs.items() if
                       k not in ['skill_type', '@odata.type',
                                 'inputs', 'outputs', 'context',
                                 'output_field_mapping']}

    @abstractmethod
    def set_inputs(self, **kwargs):
        """
        Defines the inputs this skill needs from other skills and from the document cracking phase
        :param kwargs: specific inputs required by this skill, defined by their names
        """
        pass

    @abstractmethod
    def set_default_outputs(self):
        """
        Sets the default outputs of a skill
        """
        pass

    @abstractmethod
    def get_default_inputs(self):
        """
        Returns the default inputs for this skill (the raw data source)
        :return: A list of type SkillInput
        """
        pass

    def to_dict(self):
        """ to_dict
        """

        # pylint: disable=fixme
        # todo: add check that object is valid, now that the context, input & output are not part
        # of the init method
        return_dict = {
            "@odata.type": self.skill_type,
            "inputs": [inp.to_dict() for inp in self.inputs],
            "outputs": [outp.to_dict() for outp in self.outputs],
            "context": self.context
        }
        # add additional user generated params
        return_dict.update(self.params)
        # make all params camelCase (to be sent correctly to Azure Search
        return_dict = self.to_camel_case_dict(return_dict)

        # Remove None values
        return_dict = self.remove_empty_values(return_dict)
        return return_dict

    def remove_input_by_name(self, name):
        self.inputs = [inp for inp in self.inputs if inp.name != name]

    def remove_output_by_name(self, name):
        self.outputs = [oup for oup in self.outputs if oup.name != name]

    # def add_source(self, other, include_list=None):
    #    """
    #    :param other: the source skill, which its outputs will be this skill's inputs
    #    :param include_list: if exists, list of sources to take, otherwise, take all
    #    """
    #    # Iterate on all outputs as candidates for input
    #    for output in other.outputs:
    #        should_add = True
    #        # if specified explicitly which output to take, check if the current one is listed
    #        if include_list:
    #            if output.name not in include_list:
    #                should_add = False
    #
    #        if should_add:
    #            found = False
    #            multiple_suffix = ""
    #            if output.returns_multiple_results:
    #                multiple_suffix = "/*"
    #            src = "/document/" + output.target_name + multiple_suffix
    #
    #            for inpt in self.inputs:
    #                if inpt.name == output.name:
    #                    found = True
    #                    inpt.source = src
    #
    #            if not found:
    #                newInput = SkillInput(
    #                    output.name, src)
    #                self.inputs.append(newInput)
    #    #self.context = other.context
    #
    # def remove_source(self, skill=None, source_name=None):
    #    """ remove the
    #    """
    #    if skill is None and source_name is None:
    #        raise Exception("please provide either a skill or a source name")
    #    if skill and source_name:
    #        raise Exception("please provide only a skill or a source name")
    #
    #    if skill:
    #        for output in skill.outputs:
    #            for input in self.inputs:
    #                if output.name == input.name:
    #                    self.inputs.remove(input)
    #
    #    if source_name:
    #        for input in self.inputs:
    #            if source_name == input.name:
    #                self.inputs.remove(input)

    @classmethod
    def load(cls, data):
        """ load
        """
        if data:
            if isinstance(data, str):
                data = json.loads(data)
            if not isinstance(data, dict):
                raise Exception("Failed to load JSON file with skill data")
            if "@odata.type" not in data:
                raise Exception("Please provide the skill type (@odata.type)")
            if "inputs" not in data:
                raise Exception("Please provide the skill inputs")
            if "outputs" not in data:
                raise Exception("Please provide the skill outputs")

            data['outputs'] = [SkillOutput.load(so) for so in data['outputs']]
            data['inputs'] = [SkillInput.load(so) for so in data['inputs']]

            # skill_type = data['@odata.type']
            data = cls.to_snake_case_dict(data)
            return cls(**data)
        raise Exception("data is null")


class SkillInput(AzureSearchObject):
    """
    Defines an input for a skill
    """

    def __init__(self, name, source, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.source = source

    def to_dict(self):
        """ to_dict
        """
        return_dict = {
            "name": self.name,
            "source": self.source
        }

        # add additional user generated params
        return_dict.update(self.params)
        # make all params camelCase (to be sent correctly to Azure Search
        return_dict = self.to_camel_case_dict(return_dict)

        # Remove None values
        return_dict = self.remove_empty_values(return_dict)
        return return_dict


class SkillOutput(AzureSearchObject):
    """
    Defines the output of a skill
    :param returns_multiple_results: if true means
                                     that there are multiple results
                                     under the result name
    """

    def __init__(self, name, target_name,
                 returns_multiple_results=False, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.target_name = target_name
        self.returns_multiple_results = returns_multiple_results

    def to_dict(self):
        """ to_dict
        """
        return_dict = {
            "name": self.name,
            "targetName": self.target_name
        }
        # add additional user generated params
        return_dict.update(self.params)
        # make all params camelCase (to be sent correctly to Azure Search
        return_dict = self.to_camel_case_dict(return_dict)

        # Remove None values
        return_dict = self.remove_empty_values(return_dict)
        return return_dict


class SkillParameter(object):
    """
    Holds the field to which this parameter maps to (e.g. in NER, organizations -> organization_field of type Field)
    """

    def __init__(self, skill, name, target=None, return_multiple=False):
        """

        :param skill: name of skill that produces this parameter
        :param name: name of (inner) field, name of parameter
        :param target: target to which output of this skill parameter is written to
        :param return_multiple: whether this skill returns an array for this parameter or a scalar.
        """
        self.skill = skill
        self.name = name
        if target:
            self.target = target
        else:
            self.target = name

        self.return_multiple = return_multiple

    @abstractmethod
    def map_to(self, field):
        if not isinstance(field, Field):
            raise Exception("field should be of type Field")

        if self.return_multiple:
            output_field_mapping = FieldMapping(
                source_field_name="{context}/{name}/*".format(context=self.skill.context,
                                                              name=self.name),
                target_field_name=field.name)
        else:
            output_field_mapping = FieldMapping(
                source_field_name="{context}/{name}".format(context=self.skill.context,
                                                            name=self.name),
                target_field_name=field.name)
        self.skill.output_field_mapping.append(output_field_mapping)

    def to_skill_output(self):
        return SkillOutput(self.name, self.name)
