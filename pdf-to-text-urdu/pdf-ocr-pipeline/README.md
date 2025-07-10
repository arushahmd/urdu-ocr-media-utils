# Setting Up the Environment

## Option 1: Using PyCharm

### Create a New Conda Environment

1. Open PyCharm and navigate to `File` > `Settings` (or `Preferences` on macOS) > `Project` > `Project Interpreter`.
2. Click the gear icon and select `Add`.
3. Choose `Conda Environment` and follow the prompts to create a new environment.

## Option 2: Using Command Line

1. Run the following to create conda environment 
    ```bash
    conda create --name myenv python=3.8
2. Activate the environment
   ```bash
   conda activate myenv

### Install the Required Packages

In the terminal inside PyCharm, run:

```bash
pip install -r requirements.txt
