
### Step 3.2: Generate Populated README

#### Python Script to Populate the Template
from jinja2 import Environment, FileSystemLoader

class DocumentationGenerator:
    def __init__(self, template_dir):
        """
        Initializes the DocumentationGenerator with a directory of templates.

        Parameters:
        - template_dir: Directory containing Jinja2 templates.
        """
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate_readme(self, project_data, output_file="README.md"):
        """
        Generates a README file using the provided project data.

        Parameters:
        - project_data: Dictionary containing project details.
        - output_file: Path to save the generated README file.
        """
        template = self.env.get_template("README_template.md")
        readme_content = template.render(project_data)

        with open(output_file, "w") as file:
            file.write(readme_content)
        print(f"README generated at {output_file}")

    def generate_technical_doc(self, project_data, output_file="TECHNICAL_DOC.md"):
        """
        Generates a technical documentation file using project data.

        Parameters:
        - project_data: Dictionary containing technical details of the project.
        - output_file: Path to save the generated documentation.
        """
        template = self.env.get_template("TECHNICAL_DOC.md")
        tech_doc_content = template.render(project_data)

        with open(output_file, "w") as file:
            file.write(tech_doc_content)
        print(f"Technical Documentation generated at {output_file}")
