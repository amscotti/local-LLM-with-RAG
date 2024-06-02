import ollama
from tqdm import tqdm


def __pull_model(name: str) -> None:
    current_digest, bars = "", {}
    for progress in ollama.pull(name, stream=True):
        digest = progress.get("digest", "")
        if digest != current_digest and current_digest in bars:
            bars[current_digest].close()

        if not digest:
            print(progress.get("status"))
            continue

        if digest not in bars and (total := progress.get("total")):
            bars[digest] = tqdm(
                total=total, desc=f"pulling {digest[7:19]}", unit="B", unit_scale=True
            )

        if completed := progress.get("completed"):
            bars[digest].update(completed - bars[digest].n)

        current_digest = digest


def __is_model_available_locally(model_name: str) -> bool:
    try:
        ollama.show(model_name)
        return True
    except ollama.ResponseError:
        return False


def get_list_of_models() -> list[str]:
    """
    Retrieves a list of available models from the Ollama repository.

    Returns:
        list[str]: A list of model names available in the Ollama repository.
    """
    return [model["name"] for model in ollama.list()["models"]]


def check_if_model_is_available(model_name: str) -> None:
    """
    Ensures that the specified model is available locally.
    If the model is not available, it attempts to pull it from the Ollama repository.

    Args:
        model_name (str): The name of the model to check.

    Raises:
        ollama.ResponseError: If there is an issue with pulling the model from the repository.
    """
    try:
        available = __is_model_available_locally(model_name)
    except Exception:
        raise Exception("Unable to communicate with the Ollama service")

    if not available:
        try:
            __pull_model(model_name)
        except Exception:
            raise Exception(
                f"Unable to find model '{model_name}', please check the name and try again."
            )
