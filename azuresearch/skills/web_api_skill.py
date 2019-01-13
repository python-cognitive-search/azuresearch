from azuresearch.skills import Skill

WEBAPP_SKILL = "#Microsoft.Skills.Custom.WebApiSkill"


class WebApiSkill(Skill):

    def __init__(self, uri, inputs, outputs, context, **kwargs):
        super().__init__(skill_type=WEBAPP_SKILL, inputs=inputs, outputss=outputs, context=context, **kwargs)
        self.uri = uri

    def to_dict(self):
        return_dict = super().to_dict()
        return_dict['uri'] = self.uri
        # add additional user generated params
        return_dict.update(self.params)
        # make all params camelCase (to be sent correctly to Azure Search
        return_dict = self.to_camel_case_dict(return_dict)

        # Remove None values
        return_dict = self.remove_empty_values(return_dict)
        return return_dict
