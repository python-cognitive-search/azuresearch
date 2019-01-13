import logging

from azuresearch.skills import Skill, SkillOutput, SkillInput

predefined_skills = {
    "KeyPhraseExtractionSkill": "#Microsoft.Skills.Text.KeyPhraseExtractionSkill",
    "LanguageDetectionSkill": "#Microsoft.Skills.Text.LanguageDetectionSkill",
    "EntithRecognitionSkill": "#Microsoft.Skills.Text.EntityRecognitionSkill",
    "MergeSkill": "Microsoft.Skills.Text.MergeSkill",
    "SplitSkill": "Microsoft.Skills.Text.SplitSkill",
    "SentimentSkill": "Microsoft.Skills.Text.SentimentSkill",
    "ImageAnalysisSkill": "Microsoft.Skills.Vision.ImageAnalysisSkill",
    "OCRSkill": "#Microsoft.Skills.Vision.OcrSkill",
    "ShaperSkill": "Microsoft.Skills.Util.ShaperSkill"
}


class KeyPhraseExtractionSkill(Skill):
    """
    The Key Phrase Extraction skill evaluates unstructured text, and for each record, returns a list of key phrases.
    This capability is useful if you need to quickly identify the main talking points in the record. For example, given input text "The food was delicious and there were wonderful staff", the service returns "food" and "wonderful staff".

    :param default_language_code: The language code to apply to documents that don't specify language explicitly. If the default language code is not specified, English (en) will be used as the default language code.
    See Full list of supported languages.
    :param max_key_phrase_count: The maximum number of key phrases to produce.
    """

    def __init__(self, inputs=None, outputs=None, context="/document/pages/*", default_language_code='en',
                 max_key_phrase_count=30, **kwargs):
        if inputs is None:
            inputs = self.get_default_inputs()

        if outputs is None:
            outputs = self.get_default_outputs()

        params = {"defaultLanguageCode": default_language_code,
                  "maxKeyPhraseCount": max_key_phrase_count}
        if kwargs:
            params.update(kwargs)

        super().__init__(skill_type=predefined_skills['KeyPhraseExtractionSkill'], inputs=inputs,
                       outputs=outputs, context=context, **params)

    def get_default_outputs(self):
        logging.debug("Using default outputs")
        outputs = [SkillOutput("keyPhrases", "keyPhrases")]
        return outputs

    def get_default_inputs(self):
        logging.debug("Using default inputs")

        inputs = [SkillInput("text", "/document/text"),
                  SkillInput("languageCode", "/document/languageCode")
                  ]
        return inputs


class LanguageDetectionSkill(Skill):
    """
    For up to 120 languages, the Language Detection skill detects the language of input text and reports
    a single language code for every document submitted on the request.
    The language code is paired with a score indicating the strength of the analysis.
    This capability is especially useful when you need to provide the language of the text as input to other skills
    (for example, the Sentiment Analysis skill or Text Split skill).
    """

    def __init__(self, inputs=None, outputs=None, context=None, categories=None):
        if inputs is None:
            inputs = self.get_default_inputs()

        if outputs is None:
            outputs = self.get_default_outputs()

        super(LanguageDetectionSkill, self).__init__(skills=predefined_skills['LanguageDetectionSkill'],
                                                     categories=categories, inputs=inputs, outputs=outputs,
                                                     context=context)

    def get_default_inputs(self):
        inputs = [SkillInput(name="text", source="/document/text")]
        return inputs

    def get_default_outputs(self):
        outputs = [SkillOutput(name="languageCode", target_name="myLanguageCode"),
                   SkillOutput(name="languageName", target_name="myLanguageName"),
                   SkillOutput(name="score", target_name="myLanguageScore")
                   ]
        return outputs


class EntityRecognitionSkill(Skill):
    """
    The Entity Recognition skill extracts entities of different types from text.
    """

    def __init__(self, inputs=None, outputs=None, context=None,
                 categories=["Person", "Location", "Organization", "Quantity", "Datetime", "URL", "Email"],
                 default_language_code='en',
                 minimum_precision=None, include_typeless_entities=False, **kwargs):
        if inputs is None:
            inputs = self.get_default_inputs()

        if outputs is None:
            outputs = self.get_default_outputs(categories)

        params = {"defaultLanguageCode": default_language_code,
                  "minimumPrecision": minimum_precision,
                  "includeTypelessEntities": include_typeless_entities,
                  "categories": categories
                  }
        if kwargs:
            params.update(kwargs)

        super().__init__(skills=predefined_skills['EntityRecognitionSkill'],
                         inputs=inputs, outputs=outputs,
                         context=context, **params)

    def get_default_inputs(self):
        inputs = [SkillInput(name="text", source="/document/content")]
        return inputs

    def get_default_outputs(self, categories):
        outputs = []
        for category in categories:
            so = SkillOutput(name=category.lower(), target_name=category.lower())
            outputs.append(so)
        return outputs


class MergeSkill(Skill):
    """
    The Text Merge skill consolidates text from a collection of fields into a single field.
    :param insert_pre_tag: String to be included before every insertion.
    The default value is " ". To omit the space, set the value to "".
    :param insert_post_tag: String to be included after every insertion.
    The default value is " ". To omit the space, set the value to "".
     """

    def __init__(self, inputs=None, outputs=None, context=None, insert_pre_tag=" ", insert_post_tag=" ", **kwargs):
        params = {"insertPreTag": insert_pre_tag,
                  "insertPostTag": insert_post_tag}
        if kwargs:
            params.update(kwargs)

        if inputs is None:
            inputs = self.get_default_inputs()

        if outputs is None:
            outputs = self.get_default_outputs()

        super(MergeSkill, self).__init__(skill_type=predefined_skills['MergeSkill'], inputs=inputs, outputs=outputs,
                                         context=context, **params)

    def get_default_inputs(self):
        inputs = [SkillInput("text", "/document/content"),
                  SkillInput("itemsToInsert", "/document/normalized_images/*/text"),
                  SkillInput("offsets", "/document/normalized_images/*/contentOffset")]
        return inputs

    def get_default_outputs(self):
        outputs = [SkillOutput("mergedText", "merged_text")]
        return outputs


class SplitSkill(Skill):
    """
    The Text Split skill breaks text into chunks of text.
    You can specify whether you want to break the text into sentences or into pages of a particular length.
    This skill is especially useful if there are maximum text length requirements in other skills downstream.
    :param text_split_mode: 	Either "pages" or "sentences"
    :param maximum_page_length: 	If textSplitMode is set to "pages", this refers to the maximum page length as measured by String.Length. The minimum value is 100. If the textSplitMode is set to "pages", the algorithm will try to split the text into chunks that are at most "maximumPageLenth" in size. In this case, the algorithm will do its best to break the sentence on a sentence boundary, so the size of the chunk may be slightly less than "maximumPageLength".
    :param default_language_code: 	(optional) One of the following language codes: da, de, en, es, fi, fr, it, ko, pt. Default is English (en). Few things to consider:

    If you pass a languagecode-countrycode format, only the languagecode part of the format is used.
    If the language is not in the previous list, the split skill breaks the text at character boundaries.
    Providing a language code is useful to avoid cutting a word in half for non-space languages such as Chinese, Japanese, and Korean.
    """

    def __init__(self, inputs=None, outputs=None, context=None, text_split_mode='pages', maximum_page_length=None,
                 default_language_code='en', **kwargs):
        params = {"testSplitMode": text_split_mode,
                  "maximumPageLength": maximum_page_length,
                  "defaultLanguageCode": default_language_code}
        if kwargs:
            params.update(kwargs)

        if inputs is None:
            inputs = self.get_default_inputs()

        if outputs is None:
            outputs = self.get_default_outputs()

        super().__init__(predefined_skills['SplitSkill'], inputs,
                         outputs, context, **params)

    def get_default_inputs(self):
        logging.debug("Using default inputs")

        inputs = [SkillInput("text", "/document/text"),
                  SkillInput("languageCode", "/document/languageCode")
                  ]
        return inputs

    def get_default_outputs(self):
        outputs = [SkillOutput("textItems", "mypages")]
        return outputs


class SentimentSkill(Skill):
    """
    The Sentiment skill evaluates unstructured text along a positive-negative continuum, and for each record, returns a numeric score between 0 and 1. Scores close to 1 indicate positive sentiment, and scores close to 0 indicate negative sentiment.

    :param default_language_code: 	(optional) One of the following language codes: da, de, en, es, fi, fr, it, ko, pt. Default is English (en). Few things to consider:

    If you pass a languagecode-countrycode format, only the languagecode part of the format is used.
    If the language is not in the previous list, the split skill breaks the text at character boundaries.
    Providing a language code is useful to avoid cutting a word in half for non-space languages such as Chinese, Japanese, and Korean.
    """

    def __init__(self, inputs=None, outputs=None, context=None, text_split_mode='pages', maximum_page_length=None,
                 default_language_code='en', **kwargs):
        params = {"defaultLanguageCode": default_language_code}
        if kwargs:
            params.update(kwargs)

        if inputs is None:
            inputs = self.get_default_inputs()

        if outputs is None:
            outputs = self.get_default_outputs()

        super().__init__(predefined_skills['SentimentSkill'], inputs, outputs, context, **params)

    def get_default_inputs(self):
        logging.debug("Using default inputs")

        inputs = [SkillInput("text", "/document/text"),
                  SkillInput("languageCode", "/document/languageCode")
                  ]
        return inputs

    def get_default_outputs(self):
        outputs = [SkillOutput("score", "mysentiment")]
        return outputs


class ImageAnalysisSkill(Skill):
    """
    The Image Analysis skill extracts a rich set of visual features based on the image content. For example, you can generate a caption from an image, generate tags, or identify celebrities and landmarks.

    :param default_language_code: 	A string indicating the language to return. The service returns recognition results in a specified language. If this parameter is not specified, the default value is "en".
    Supported languages are:
    en - English (default)
    zh - Simplified Chinese
    :param visual_features: An array of strings indicating the visual feature types to return. Valid visual feature types include:

    categories - categorizes image content according to a taxonomy defined in the Cognitive Services documentation.
    tags - tags the image with a detailed list of words related to the image content.
    Description - describes the image content with a complete English sentence.
    Faces - detects if faces are present. If present, generates coordinates, gender, and age.
    ImageType - detects if image is clipart or a line drawing.
    Color - determines the accent color, dominant color, and whether an image is black&white.
    Adult - detects if the image is pornographic in nature (depicts nudity or a sex act). Sexually suggestive content is also detected.

    Names of visual features are case-sensitive.

    :param details: An array of strings indicating which domain-specific details to return. Valid visual feature types include:

    Celebrities - identifies celebrities if detected in the image.
    Landmarks - identifies landmarks if detected in the image.
    """

    def __init__(self, inputs=None, outputs=None, context="/document/normalized_images/*",
                 visual_features=["Tags", "Faces", "Categories", "Adult", "Description", "ImageType", "Color"],
                 details=['Celebrities', 'Landmarks'],
                 default_language_code='en', **kwargs):
        params = {"defaultLanguageCode": default_language_code, "visualFeatures": visual_features, "details": details}
        if kwargs:
            params.update(kwargs)

        if inputs is None:
            inputs = self.get_default_inputs()

        if outputs is None:
            outputs = self.get_default_outputs(visual_features)

        super().__init__(predefined_skills['ImageAnalysisSkill'], inputs, outputs, context, **params)

    def get_default_inputs(self):
        logging.debug("Using default inputs")

        inputs = [SkillInput("image", "/document/normalized_images/*")]
        return inputs

    def get_default_outputs(self, categories):
        outputs = []
        for category in categories:
            so = SkillOutput(name=category.lower(), target_name=category.lower())
            outputs.append(so)
        return outputs


class OCRSkill(Skill):
    """
    The OCR skill extracts text from image files. Supported file formats include:

    .JPEG
    .JPG
    .PNG
    .BMP
    .GIF

    :param detectOrientation: Enables autodetection of image orientation.
            Valid values: true / false.
    :param defaultLanguageCode: Language code of the input text. If the language code is unspecified or null, the language will be set to English. If the language is explicitly set to "unk", the language will be auto-detected.
    :param textExtractionAlgorithm :	"printed" or "handwritten". The "handwritten" text recognition OCR algorithm is currently in preview and only supported in English.
    """

    def __init__(self, inputs=None, outputs=None, context="/document/normalized_images/*",
                 default_language_code='en', detect_orientation=True,text_extraction_algorithm="printed", **kwargs):
        params = {"defaultLanguageCode": default_language_code,
                  "detectOrientation":detect_orientation,
                  "textExtractionAlgorithm":text_extraction_algorithm}
        if kwargs:
            params.update(kwargs)

        if inputs is None:
            inputs = self.get_default_inputs()

        if outputs is None:
            outputs = self.get_default_outputs()

        super().__init__(predefined_skills['OCRSkill'], inputs, outputs, context, **params)

    def get_default_inputs(self):
        logging.debug("Using default inputs")

        inputs = [SkillInput("image", "/document/normalized_images/*")]
        return inputs

    def get_default_outputs(self):
        outputs = [SkillOutput("text", "myText"),
                   SkillOutput("layoutText", "myLayoutText")
                   ]
        return outputs


class ShaperSkill(Skill):
    """
    The Shaper skill creates a complex type to support composite fields (also known as multipart fields). A complex type field has multiple parts but is treated as a single item in an Azure Search index. Examples of consolidated fields useful in search scenarios include combining a first and last name into a single field, city and state into a single field, or name and birthdate into a single field to establish unique identity.
    The Shaper skill allows you to essentially create a structure, define the name of the members of that structure, and assign values to each member.
    By default, this technique supports objects that are one level deep. For more complex objects, you can chain several Shaper steps.
    In the response, the output name is always "output". Internally, the pipeline can map a different name, such as "analyzedText" in the examples below to "output", but the Shaper skill itself returns "output" in the response. This might be important if you are debugging enriched documents and notice the naming discrepancy, or if you build a custom skill and are structuring the response yourself.
    """
    def __init__(self, inputs, outputs, context=None, **kwargs):

        super().__init__(predefined_skills['ShaperSkill'], inputs, outputs, context, **kwargs)
