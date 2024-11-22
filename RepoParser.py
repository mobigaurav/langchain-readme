from github import Github
import os
from LanguageDetector import LanguageDetector
from PythonComponentExtractor import PythonComponentExtractor
from JavaParser import JavaParser
from JavaScriptParser import JavaScriptParser
from SwiftComponentExtractor import SwiftComponentExtractor
from DocumentationGenerator import DocumentationGenerator
from LLMContentGenerator import LLMContentGenerator
from langchain.prompts import PromptTemplate


class RepoParser:
    def __init__(self, github_token, repo_name, content_generator):
        """
            Handles parsing for a GitHub repository and integrates LLM for content generation.

            Parameters:
            - github_token: Token for GitHub API access.
            - repo_name: Full GitHub repo name (e.g., 'user/repo').
            - content_generator: Instance of LLMContentGenerator for generating narrative content.
            """
        self.github = Github(github_token)
        self.repo = self.github.get_repo(repo_name)
        self.content_generator = content_generator  # LLMContentGenerator instance

    def list_files(self, file_extensions=None):
        """
        Lists files in the repository with optional filtering by file extensions.

        Parameters:
        - file_extensions: List of file extensions to include (e.g., ['.py', '.md']).

        Returns:
        - A list of file paths in the repository.
        """
        files = []
        contents = self.repo.get_contents("")
        while contents:
            content_file = contents.pop(0)
            if content_file.type == "dir":
                contents.extend(self.repo.get_contents(content_file.path))
            else:
                if file_extensions is None or any(content_file.path.endswith(ext) for ext in file_extensions):
                    files.append(content_file.path)
        return files

    def categorize_files(self):
        """
        Categorizes files into 'code_files', 'config_files', and 'doc_files'.

        Returns:
        - A dictionary categorizing the repository files.
        """
        categorized_files = {
            "code_files": [],
            "config_files": [],
            "doc_files": []
        }

        for file_path in self.list_files():
            if file_path.endswith(('.py', '.js', '.java', '.cs', '.cpp', '.swift')):
                categorized_files["code_files"].append(file_path)
            elif file_path.endswith(('.yml', '.yaml', '.json', '.env', '.ini')):
                categorized_files["config_files"].append(file_path)
            elif file_path.endswith(('.md', '.rst', '.txt')):
                categorized_files["doc_files"].append(file_path)
            else:
                # Other files can be categorized if needed
                pass

        return categorized_files

    def get_file_content(self, file_path):
        """
        Fetches the content of a specific file in the repository.

        Parameters:
        - file_path: Path to the file in the repository.

        Returns:
        - The content of the file as a string.
        """
        file_content = self.repo.get_contents(file_path)
        return file_content.decoded_content.decode('utf-8')

    def get_all_files_content(self):
        """
        Fetches content for all categorized files.

        Returns:
        - A dictionary with file paths as keys and file contents as values.
        """
        categorized_files = self.categorize_files()
        all_files_content = {}

        for category, files in categorized_files.items():
            for file_path in files:
                try:
                    content = self.get_file_content(file_path)
                    all_files_content[file_path] = content
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

        return all_files_content

    def extract_all_components(languages, parser):
        """
        Extracts components from all categorized files.

        Parameters:
        - languages: Detected languages and file paths.
        - parser: RepoParser instance to fetch file contents.

        Returns:
        - A dictionary of components grouped by language.
        """
        components_by_language = {}
        for lang, files in languages.items():
            components_by_language[lang] = []
            for file_path in files:
                file_content = parser.get_file_content(file_path)
                if lang == "Python":
                    extractor = PythonComponentExtractor(file_content)
                    components = extractor.extract_components()
                    components_by_language[lang].append({
                        'file': file_path,
                        'components': components
                    })
                elif lang == "Swift":
                # Check if Swift build tools are available
                    if os.path.exists("./swift/build"):
                        # Assuming `SwiftComponentExtractor` is implemented
                        # extractor = SwiftComponentExtractor(file_content)
                        # components = extractor.extract_components()
                        components_by_language[lang].append({
                            'file': file_path,
                            'components': "Swift components extraction not implemented"
                        })
                elif lang == "Java":
                     extractor = JavaParser(file_content)
                     components = extractor.extract_components()
                     components_by_language[lang].append({
                        'file': file_path,
                        'components': components
                    })

                elif lang == "Javascript":
                     extractor = JavaScriptParser(file_content)
                     components = extractor.extract_components()
                     components_by_language[lang].append({
                        'file': file_path,
                        'components': components
                    })
                else:
                    print(f"Swift build tools not found. Skipping {file_path}.")
                # Add cases for other languages here
        return components_by_language

    def generate_content_with_llm(self):
        """
        Generates descriptive content using LLM based on repository details.
        """
        repo_name = self.repo.name
        files = parser.list_files()
        detector = LanguageDetector(files)
        primary_language = detector.detect_language_by_extension()
        language_summary = detector.summarize_languages(primary_language)

       # components_summary = f"{len(files)} files, primary language: {primary_language}"
       # components_by_language = self.extract_all_components(primary_language)

        # Generate Overview
        overview_prompt = PromptTemplate(
            input_variables=["repo_name",
                             "primary_language", "language_summary"],
            template="""
            Write a concise project overview for a README. The repository is named "{repo_name}". 
            The primary language is {primary_language}. It includes the following components: {language_summary}.
            """
        )
        overview = content_generator.generate_section(overview_prompt, {
            "repo_name": repo_name,
            "primary_language": primary_language,
            "language_summary": language_summary
        })

        # Generate Features
        features_prompt = PromptTemplate(
            input_variables=["repo_name", "primary_language"],
            template="""
            List the key features of the project "{repo_name}" written in {primary_language}.
            """
        )
        features = content_generator.generate_section(features_prompt, {
            "repo_name": repo_name,
            "primary_language": primary_language
        }).split("\n")

        code_overview_prompt = PromptTemplate(
            input_variables=["repo_name", "primary_language"],
            template="""
            Write a technical overview for the project "{repo_name}" written in {primary_language}.
            """
        )

        code_overview = content_generator.generate_section(code_overview_prompt, {
            "repo_name": repo_name,
            "primary_language": primary_language
        }).split("\n")

        installation_overview_prompt = PromptTemplate(
            input_variables=["repo_name", "primary_language"],
            template="""
             Provide Installation instruction if any for the repository "{repo_name}" written in {primary_language}.
            """
        )

        installation_instructions = content_generator.generate_section(installation_overview_prompt, {
            "repo_name": repo_name,
            "primary_language": primary_language
        }).split("\n")

        usage_prompt = PromptTemplate(
            input_variables=["repo_name", "primary_language"],
            template="""
            Provide usage examples for the repository "{repo_name}" written in {primary_language}.
            """
        )

        usage_examples = content_generator.generate_section(usage_prompt, {
            "repo_name": repo_name,
            "primary_language": primary_language
        }).split("\n")

        return {
            "overview": overview,
            "features": features,
            "files": files,
            "code_overview": code_overview,
            "usage_examples": usage_examples,
            "installation_instructions": installation_instructions

        }


api_key = "use your api key"
content_generator = LLMContentGenerator(api_key)

#repo_name = "mobigaurav/internetTV"
repo_name = "mobigaurav/langchain-readme"
#repo_name = "mobigaurav/cse571-ai"
#repo_name = "mobigaurav/Fooddelivery-clone"
#repo_name = "mobigaurav/blockchain"
github_token = "use your api key"  # optional

parser = RepoParser(github_token , repo_name,  content_generator)

# Step 3: Fetch Data and Generate LLM Content
categorized_files = parser.categorize_files()
parsed_content = parser.generate_content_with_llm()

# Output the Results
print("Categorized Files:", categorized_files)
print("Generated Content:", parsed_content)

# Generate README
# Example for README.md
project_data = {
    "project_name": parser.repo.name,
    "overview": parsed_content["overview"],
    "features": parsed_content["features"],
    "installation_instructions": parsed_content["installation_instructions"],
    "usage_examples": parsed_content["usage_examples"],
    "code_overview": parsed_content["code_overview"],
    # Replace with actual license fetched from repo if available.
    "license": parser.repo.license
}
generator = DocumentationGenerator(template_dir="templates")
generator.generate_readme(project_data)

# tech_doc_data = {
#     "project_name": parser.repo.name,
#     "overview": parsed_content["overview"],
#     "features": parsed_content["features"],
#     "installation_instructions": parsed_content["installation_instructions"],
#     "usage_examples": parsed_content["usage_examples"],
#     "code_overview": parsed_content["code_overview"],
#     # Replace with actual license fetched from repo if available.
#     "license": parser.repo.license
# }

# generator.generate_technical_doc(tech_doc_data)
