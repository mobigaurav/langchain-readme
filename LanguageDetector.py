from collections import Counter
import os

class LanguageDetector:
    def __init__(self, file_paths):
        """
        Initializes the LanguageDetector with the list of file paths.

        Parameters:
        - file_paths: List of file paths to analyze.
        """
        self.file_paths = file_paths

    def detect_language_by_extension(self):
        """
        Detects programming languages based on file extensions.

        Returns:
        - A dictionary with languages as keys and file paths as values.
        """
        language_extensions = {
            '.py': 'Python',
            '.java': 'Java',
            '.js': 'JavaScript',
            '.cpp': 'C++',
            '.cs': 'C#',
            '.html': 'HTML',
            '.css': 'CSS',
            '.md': 'Markdown',
            '.yml': 'YAML',
            '.yaml': 'YAML',
            '.json': 'JSON',
            '.swift': 'Swift',
        }
        languages = {}

        for file_path in self.file_paths:
            ext = os.path.splitext(file_path)[-1]
            lang = language_extensions.get(ext, 'Unknown')
            if lang not in languages:
                languages[lang] = []
            languages[lang].append(file_path)

        return languages

    def summarize_languages(self, languages):
        """
        Summarizes detected languages and their file counts.

        Parameters:
        - languages: Dictionary of languages and their file paths.

        Returns:
        - A Counter object summarizing the number of files for each language.
        """
        return Counter({lang: len(files) for lang, files in languages.items()})
