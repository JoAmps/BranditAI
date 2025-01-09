import uuid

class HelperFunctions:
    """
    A utility class for various helper functions.
    """

    @staticmethod
    def bucket_name(name):
        """
        Converts a string to a valid S3 bucket name format by:
        - Replacing spaces with hyphens.
        - Converting all letters to lowercase.
        - Appending a unique suffix for global uniqueness.

        Args:
            name (str): The input name to convert.

        Returns:
            str: The converted and uniquely suffixed bucket name.
        """
        base_name = name.strip().replace(" ", "-").lower()
        unique_suffix = uuid.uuid4().hex[:8]  # Generate a short unique code
        return f"{base_name}-{unique_suffix}"