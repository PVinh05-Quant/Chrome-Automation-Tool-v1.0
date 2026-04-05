import os
from selenium.webdriver.chrome.options import Options

def configure_chrome_options_with_extensions(existing_options: Options, extension_paths: list[str], headless: bool = False) -> Options:
    if not isinstance(existing_options, Options):
        raise TypeError("existing_options phải là một đối tượng selenium.webdriver.chrome.options.Options.")

    for path in extension_paths:
        if not os.path.exists(path):
            continue
        try:
            existing_options.add_extension(path)
        except Exception:
            continue

    if headless:
        headless_args = [
            "--headless=new",
            "--window-size=1920,1080",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
        
        for arg in headless_args:
            if arg not in existing_options.arguments:
                existing_options.add_argument(arg)

    return existing_options
