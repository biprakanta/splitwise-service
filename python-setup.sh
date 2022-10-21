rm -rf pyenv || 1
python3.8 -m venv pyenv
pyenv/bin/pip install --upgrade pip
sudo chmod 777 `pwd` 
export POETRY_VIRTUALENVS_PATH=`pwd`/pyenv/bin/python
pyenv/bin/pip install poetry
#pyenv/bin/python -m poetry env use `pwd`/pyenv/bin/python
pyenv/bin/python -m  poetry install
source pyenv/bin/activate
mkdir -p logs