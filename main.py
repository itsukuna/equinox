from bot import bot
import os

if __name__ == "__main__":
    os.environ["PIPENV_VERBOSITY"] = "-1"  # Suppresses pipenv output
    # Forces pipenv to use the virtual environment
    os.environ["PIPENV_IGNORE_VIRTUALENVS"] = "1"
    # Prevents pipenv from loading .env files
    os.environ["PIPENV_DONT_LOAD_ENV"] = "1"

    # Change directory to the root of the project
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Activate the pipenv virtual environment
    os.system("pipenv shell")

    bot.run()
