# How to Install Environment Tools

Pre-Requirements: Make sure to have Python3.9 installed on your computer. 
If you aren't using conda, Python3.9 can be installed at: https://www.python.org/downloads/

> If you are planning on running mmrotate, you will need to install the following dependencies:
>  - VisualStudio Build Tools: [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (at least 2017)
>     - Make sure to select C++ Development tools when going through the installer.
> - Note that Linux/Mac is not recommended for mmrotate, I managed to make it work with manual editing of build files, but it was rough without knowledge of C++ and CMake.


## Conda Virtual Environment Setup Instructions

1. If you haven't already. Install Anaconda from https://www.anaconda.com/products/individual or Miniconda (preferred) from https://docs.conda.io/en/latest/miniconda.html

2. Open the integrated terminal in VSCode and run the following command: `conda create -n mighty python=3.9`

    - Alternatively, **(recommended for Windows)** you can use anaconda prompt. To do this, open the start menu and search for `anaconda prompt` and click on the option that says `Anaconda Prompt (anaconda3)`. Then run the following command: `conda create -n mighty python=3.9`

    > ## Common Error
    > There is a chance you will encounter the following error when running the above command:
    > <div style="background-color: black; color: red; font-family: monospace; padding: 10px;">
    > conda command not foound
    > </div>
    >
    > 1. **On Windows:**
    >     - Open the Start Menu and search for 'Environment Variables'.
    >     - Click on 'Edit the system environment variables'.
    >     - In the System Properties window that appears, click on 'Environment Variables'.
    >     - In the Environment Variables window, under 'System variables', find the 'Path' variable, select it, and click on 'Edit'.
    >     - In the Edit Environment Variable window, click on 'New' and add the path to your Anaconda/Miniconda installation. This is typically `C:\Users\{username}\Anaconda3\` or `C:\Users\{username}\Miniconda3\`.
    >     - Click 'OK' to close all windows.
    > 
    > 2. **On macOS and Linux:**
    >     - Open a terminal.
    >     - Use a text editor to open the `.bashrc` file for editing. If you're using nano, you can do this with `nano ~/.bashrc`.
    >     - At the end of the file, add the following line: `export PATH="/path/to/anaconda3/bin:$PATH"` or `export PATH="/path/to/miniconda3/bin:$PATH"`. Replace `/path/to/anaconda3/bin` or `/path/to/miniconda3/bin` with the actual path to your Anaconda/Miniconda installation.
    >     - Save the file and exit the text editor.
    >     - To make the changes take effect, run `source ~/.bashrc` in the terminal.

3. Once installed, you can activate the environment by using the command in the intregrated terminal: `conda activate mighty`

    You will know if you did it right if the word `(mighty)` gets appended at the beginning of the terminal line.

## Python Virtual Environment Setup Instructions

1. Open the integrated terminal in VSCode and run the following command: `pip install virtualenv` 
    - If you get an error, try running the command as an administrator. 
    - If you get a warning, you can ignore it. 
    - If you get a success message, you can move on to step 2. 

    ___ 
    > ### Note for Windows Users
    > If you get an error that says `pip is not recognized as an internal or external command`, you will need to add pip to your PATH. To do this, follow the instructions below: 
    > 
    > 1. Open the start menu and search for `environment variables` and click on the option that says `Edit the system environment variables`. 
    > 2. Click on the button that says `Environment Variables...` 
    > 3. Under the `System Variables` section, find the variable named `Path` and click on it. 
    > 4. Click on the button that says `Edit...` 
    > 5. Click on the button that says `New` 
    > 6. Paste the following into the text box: `C:\Users\{your username}\AppData\Local\Programs\Python\Python39\Scripts` 
    > 7. Click on the button that says `OK` 
    > 8. Click on the button that says `OK` 
    > 9. Click on the button that says `OK` 
    > 10. Close the terminal and reopen it. 
    > 11. Try running the command `pip install virtualenv` again.


2. Once you have successfully installed virtualenv, run the following command in the integrated terminal: 

    - For Windows: `virtualenv mighty` 
    - For Mac/Linux: `virtualenv -p python3 mighty`
___ 
3. Once installed, you can activate the environment by using the command in the intregrated terminal: 

    - For Windows: `.\mighty\Scripts\activate` 
    - For Mac/Linux: `./mighty/bin/activate`

    You will know if you did it right if the word `(mighty)` gets appended at the beginning of the terminal line.


    > ### Note for Windows Users
    > If you are using Windows, there is a chance you will encounter the following error:
    > <div style="background-color: black; color: red; font-family: monospace; padding: 10px;">
    > .\mighty\Scripts\activate : File {path_to_repository}\MightyMicros\mighty\Scripts\activate.ps1 cannot be loaded. The file {path_to_repository}\MightyMicros\mighty\Scripts\activate.ps1 is not digitally signed. You cannot run this script on the current system. For more information about running scripts and setting execution policy, see 
    > about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.
    > At line:1 char:1
    > + .\mighty\Scripts\activate
    > + ~~~~~~~~~~~~~~~~~~~~~~~~~
    >     + CategoryInfo          : SecurityError: (:) [], PSSecurityException
    >     + FullyQualifiedErrorId : UnauthorizedAccess
    > <\div>

    > If you encounter this error, you will need to change your execution policy. To do this, run the following command in the integrated terminal:
    >
    > `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`