from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

class LLMContentGenerator:
    def __init__(self, openai_api_key):
        """
        Initializes the LLMContentGenerator with an OpenAI API key.
        """
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4")
    
    def generate_section(self, prompt_template, variables):
        """
        Generates content for a documentation section.

        Parameters:
        - prompt_template: A LangChain PromptTemplate object.
        - variables: A dictionary of variables to populate the template.

        Returns:
        - Generated content as a string.
        """
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        return chain.run(variables)

    # categorized_files = parser.categorize_files()
    # print("Categorized Files:", categorized_files)

    # all_files_content = parser.get_all_files_content()
    # print("All Files Content Retrieved!")

    # # Assuming `parser` is from Step 1 and contains a list of all file paths
    # file_paths = parser.list_files()
    # detector = LanguageDetector(file_paths)

    # languages = detector.detect_language_by_extension()
    # print("Detected Languages:", languages)

    # language_summary = detector.summarize_languages(languages)
    # print("Language Summary:", language_summary)

    # components_by_language = extract_all_components(languages, parser)
    # print("Extracted Components by Language:", components_by_language)

        # # Example for TECHNICAL_DOC.md
    # tech_doc_data = {
    #     "project_name": "SwiftParser",
    #     "code_overview": code_overview,
    #     "modules": [
    #         {
    #             "name": "Parser",
    #             "description": "Handles file parsing and syntax analysis.",
    #             "functions": ["parse_file", "extract_classes", "extract_functions"]
    #         }
    #     ],
    #     "apis": [
    #         {
    #             "endpoint": "/parse",
    #             "method": "POST",
    #             "description": "Parses a Swift file.",
    #             "parameters": {"file": "Path to the Swift file to parse."}
    #         }
    #     ]
    # }

    # generate_technical_doc(tech_doc_data)