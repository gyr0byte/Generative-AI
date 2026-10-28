from langchain.tools import tool


@tool
def get_gretting(name : str) -> str:
    """ Generate a greeting message for a user.
    """
    return f"Hello, {name}! Welcome to our platform."
    