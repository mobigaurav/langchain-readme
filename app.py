from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import zipfile
from RepoParser import RepoParser  # Ensure RepoParser is available
from LLMContentGenerator import LLMContentGenerator  # Ensure LLMContentGenerator is available
from DocumentationGenerator import DocumentationGenerator  # Ensure DocumentationGenerator is available
from urllib.parse import urlparse
from LanguageDetector import LanguageDetector
from LLMContentGenerator import LLMContentGenerator
from langchain.prompts import PromptTemplate

app = Flask(__name__)
CORS(app, origins=["*"])

def extract_username_reponame(repo_url):
    """
    Extracts the username and repository name from a GitHub URL.

    Parameters:
    - repo_url: The full GitHub repository URL.

    Returns:
    - A string in the format 'username/reponame'.
    """
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip("/").split("/")
    if len(path_parts) >= 2:
        return f"{path_parts[0]}/{path_parts[1]}"
    else:
        raise ValueError("Invalid GitHub repository URL")
    
def generate_content_with_llm(content_generator:LLMContentGenerator,
                                repo_name_user,
                                files):
    """
    Generates descriptive content using LLM based on repository details.
    """
    repo_name = repo_name_user
    print(repo_name)
    print(files)
    #files = self.list_files()
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
    
@app.route("/generate-docs", methods=["POST"])
def generate_docs():
    data = request.json
    print(data)
    repo_url = data.get("repoUrl")
    open_api_key = data.get("openApiKey")
    github_token = data.get("githubToken")

    if not all([repo_url, open_api_key, github_token]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Initialize the RepoParser and LLMContentGenerator
        content_generator = LLMContentGenerator(open_api_key)
        repo_name = extract_username_reponame(repo_url)
        repo_name_user = repo_url.split("/")[-1]
        print(repo_name)
        repo_parser = RepoParser(github_token=github_token, repo_name=extract_username_reponame(repo_url), content_generator=content_generator)

        # Parse the repository and generate content
        files = repo_parser.list_files()
        parsed_content = generate_content_with_llm(content_generator,repo_name_user,files)
        project_data = {
            "project_name": repo_parser.repo.name,
            "overview": parsed_content["overview"],
            "features": parsed_content["features"],
            "installation_instructions": parsed_content["installation_instructions"],
            "usage_examples": parsed_content["usage_examples"],
            "code_overview": parsed_content["code_overview"],
            # Replace with actual license fetched from repo if available.
            "license": repo_parser.repo.license
        }

        # Generate documentation
        generator = DocumentationGenerator(template_dir="./templates")
        readme_path = "README.md"
        #tech_doc_path = "TECHNICAL_DOC.md"
        generator.generate_readme(project_data)
        #generator.generate_technical_doc(project_data)

        # Create a ZIP file to download
        zip_filename = "downloads/docs.zip"
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            zipf.write(readme_path)
            #zipf.write(tech_doc_path)

        return jsonify({"downloadLink": f"http://localhost:5000/downloads/{zip_filename}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/downloads/docs.zip", methods=["GET"])
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
