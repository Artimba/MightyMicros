# MightyMicros: Slice Manager
Live object tracking of microscopic, nanometer thin, slices off a microtome.

## How Do I Install This?

1. To install this software, you will need to install Git. You can download Git from [here](https://git-scm.com/downloads).

2. Once you have Git installed, open a terminal. Terminals can be opened by:
    - **Windows:**
        - Any Version: Press `Win + R` and type `cmd` in the box that appears.
        - Windows 10: Press `Win + X` and click on `Windows PowerShell`.
        - Windows 11: Press `Win + X` and click on `Windows Terminal`.
    - **macOS:**
        - Press `Cmd + Space` and type `terminal` in the box that appears.
    - **Linux:**
        - Press `Ctrl + Alt + T`.

3. Once you have a terminal open, navigate to the folder you want to install the software in. You can do this by typing `cd` followed by the path to the folder you want to install the software in. For example, if you want to install the software in the `Documents` folder, you would type `cd Documents`.

    > ## Note for Windows Users
    > If you want to install to a separate drive, you will need to type the drive letter followed by a colon before the path. For example, if you want to install the software in the `Documents` folder on the `D:` drive, you would type `D:` then `cd Documents`.

4. Once you are in the folder you want to install the software in, run the following command in the terminal:
    ```bash
    git clone https://github.com/Skyibis/MightyMicros.git
    ```

5. cd into the `MightyMicros` folder:
    ```bash
    cd MightyMicros
    ```

## Setup Instructions
[Virtual Environment Setup Instructions](SetupVenv.md)

Follow the instructions linked above to set up the virtual environment of your choice. Once you have set up the virtual environment, you can install the required packages by running the following command in the terminal:
```bash
pip install -v -e .
```

Ensure that you are still within the `MightyMicros` folder when you run this command.

If there is any error in the installation, please [create an issue](https://github.com/Skyibis/MightyMicros/issues/new) with the full error message/traceback. We will try to help you resolve the issue as soon as possible.


**You can verify that the installation was successful by running the following command in the terminal:**
```bash
mighty-micros
```

This will open the UI of the program.


## Using the Software

### Setup the Microtome
- Set up the microtome as usual for slicing. This includes setting up the boat and knife and loading the trimmed resin-encased sample into the microtome.

### Software Usage During Microtomy

#### Step 1: Connect Cameras
- Connect the **microtome camera** and the **external camera** to the laptop you will be running the user interface on.

#### Step 2: Open User Interface
- Open the user interface by typing `mighty micros` in your terminal.
- The microtome camera feed and the external camera feed should automatically display on the **Slicing tab**. 
  - Refer to **Section 6: Troubleshooting** if this does not happen.

#### Step 3: Start Recording
- Click on the **Start Recording** button on the **Slicing** tab to start recording both video feeds.

#### Step 4: Begin Slicing
- Start slicing with the microtome.
- The user interface will display boxes around slices on the microtome camera feed to indicate detected slices.
- The order of slices will be displayed beside each box and outputted to the console on the user interface.

#### Step 5: Collecting Slices
- Collect the slices in the boat onto grids.
- Make note of which slice numbers were picked up on the grid and store the grid in the slotted grid organizer.

#### Step 6: Manage Grids
- Click on the **Grid Management** tab.
- Click on the **Grid Management** button to open the Grid Management pop-up window.
- Enter the grid number and verify the slices picked up:
  - If correct, click **Yes**.
  - If incorrect, click **No** and enter the correct slice numbers.

#### Step 7: Stop Recording
- Click the **Stop Recording** button on the **Slicing** tab to save the recordings.

#### Step 8: Reviewing Recordings (if necessary)
- Use recordings to verify slice order.
- Access recordings via the dropdown box on the **Grid Management** tab.
- Use sliders and **Play** button to watch or skip through the recordings.

#### Step 9: Output Console Data
- Click **Write to File** on the **Slicing** tab to save console output to a text file.
- Clear the console by clicking the **Clear** button.

#### Step 10: Repeat Process
- Repeat steps 4-13 until your entire sample has been sliced and collected onto grids.

#### Step 11: Post-Processing
- Refer to the console output text files for serial 3D reconstruction of the sample.

## Troubleshooting


> # Camera Feed Not Displaying
> The displays on the UI may not display the correct external and microtome camera feeds despite the cameras being connected to your laptop. This may be due to your laptop being connected to other camera(s) (such as a webcam). To fix this issue, go to the `src/ui/head.py` file and look for `def InitializeCamera(self)`. The first few lines of code are if/else statements. 
>
>    - In these statements, change either `0` or `1` in the `if self.camera_index == 0` and `elif self.camera_index == 1` to `2` (so try `1` and `2` or `2` and `0` as the two indices) if you have 3 total cameras connected to your laptop. If you have `4` total cameras connected to your laptop, try `3`. Comment out the second elif statement (`elif self.camera_index >= 2`) and the two lines immediately below it. Start the UI and see if it displays the correct camera feeds. 

