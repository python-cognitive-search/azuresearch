""" Skill
"""
import json

from azuresearch.azure_search_object import AzureSearchObject
from azuresearch.field_mapping import FieldMapping

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

        # if "inputs" not in kwargs:
        #    raise Exception("Inputs must be provided")
        self.inputs = []
        if "inputs" in kwargs:
            inputs = kwargs['inputs']
            if not isinstance(inputs[0], SkillInput):
                raise TypeError("Inputs should be of type SkillInput")
            self.inputs = inputs

        if "outputs" not in kwargs:
            raise Exception("outputs must be provided")
        outputs = kwargs['outputs']
        # TODO check all outputs type
        if not isinstance(outputs[0], SkillOutput):
            raise TypeError("Outputs should be of type SkillOutput")
        self.outputs = outputs

        if "@odata.type" in kwargs:
            self.skill_type = kwargs.get("@odata.type")
        else:
            self.skill_type = kwargs.get("skill_type")

        self.context = kwargs.get("context")

        self.params = {k: v for (k, v) in kwargs.items() if
                       k not in ['skill_type', '@odata.type', 'inputs', 'outputs', 'context']}

    def to_dict(self):
        """ to_dict
        """

        # todo: add check that object is valid, now that the context, input & output are not part
        # of the init method
        return_dict = {
            "@odata.type": self.skill_type,
            "inputs": [inp.to_dict() for inp in self.inputs] ,
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

    def get_output_field_mappings(self):
      ofm = []
      for output in self.outputs:
          multiple_suffix = ""
          if output.returns_multiple_results:
            multiple_suffix = "/*"
          ofm.append(FieldMapping("/document/" + output.target_name + multiple_suffix, output.name))
      return ofm

    def add_source(self, other, include_list=None) : 
        """
        :param other: the source skill, which its outputs will be this skill's inputs
        :param include_list: if exists, list of sources to take, otherwise, take all
        """
        # Iterate on all outputs as candidates for input
        for output in other.outputs:
            should_add = True
            # if specified explicitly which output to take, check if the current one is listed
            if include_list:
                if output.name not in include_list:
                    should_add = False

            if should_add:
                found = False
                multiple_suffix = ""
                if output.returns_multiple_results:
                  multiple_suffix = "/*"
                src = "/document/" + output.target_name + multiple_suffix
               
                for inpt in self.inputs:
                  if inpt.name == output.name:
                      found = True
                      inpt.source = src
                  
                if not found:
                    newInput = SkillInput(
                        output.name, src)
                    self.inputs.append(newInput)
        #self.context = other.context
        
    def remove_source(self, skill=None, source_name=None):
        """ remove the
        """
        if skill is None and source_name is None:
            raise Exception("please provide either a skill or a source name")
        if skill and source_name:
            raise Exception("please provide only a skill or a source name")

        if skill:
            for output in skill.outputs:
                for input in self.inputs:
                    if output.name == input.name:
                        self.inputs.remove(input)

        if source_name:
            for input in self.inputs:
                if source_name == input.name:
                    self.inputs.remove(input)

    @classmethod
    def load(cls, data):
        """ load
        """
        if data:
            if type(data) is str:
                data = json.loads(data)
            if type(data) is not dict:
                raise Exception("Failed to load JSON file with skill data")
            if "@odata.type" not in data:
                raise Exception("Please provide the skill type (@odata.type)")
            if "inputs" not in data:
                raise Exception("Please provide the skill inputs")
            if "outputs" not in data:
                raise Exception("Please provide the skill outputs")

            data['outputs'] = [SkillOutput.load(so) for so in data['outputs']]
            data['inputs'] = [SkillInput.load(so) for so in data['inputs']]

            #skill_type = data['@odata.type']
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
    :param returns_multiple_results: if true means that there are multiple results under the result name
    """
    
    def __init__(self, name, target_name, returns_multiple_results = False, **kwargs):
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
