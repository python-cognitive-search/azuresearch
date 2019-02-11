""" Skillset
"""
import json

from azuresearch.base_api_call import BaseApiCall
from azuresearch.skills import Skill


class Skillset(BaseApiCall):
    """ Skillset
    """
    SERVICE_NAME = 'skillsets'

    def __init__(self, skills, name=None, description=None, **kwargs):
        super().__init__(service_name=Skillset.SERVICE_NAME, **kwargs)

        # pylint: disable=len-as-condition
        if skills is None or len(skills) == 0:
            raise Exception("A skillset must have at least one skill")

        if not isinstance(skills[0], Skill):
            raise Exception("Skills must be of type 'Skill'")

        self.name = name
        self.skills = skills
        self.description = description

    def to_dict(self):
        """ to_dict
        """
        return_dict = {

            'name': self.name,
            'description': self.description,
            'skills': [skill.to_dict() for skill in self.skills]
        }
        return_dict.update(self.params)
        return_dict = self.to_camel_case_dict(return_dict)

        return_dict = self.remove_empty_values(return_dict)
        return return_dict

    @classmethod
    def load(cls, data):
        """ load
        """
        if isinstance(data, str):
            data = json.loads(data)
        if not isinstance(data, dict):
            raise Exception("Failed to parse input as Dict")
        if 'skills' not in data:
            raise Exception("Skills not found")
        else:
            data['skills'] = [Skill.load(sk) for sk in data['skills']]
        if 'name' not in data:
            data['name'] = None

        if 'description' not in data:
            data['description'] = ''

        return cls(name=data['name'], skills=data['skills'], description=data['description'])

    def get_output_field_mappings(self):
        """ get_output_field_mappings
        """
        ofm = []
        for skill in self.skills:
            ofm = ofm + skill.output_field_mapping
        return ofm
