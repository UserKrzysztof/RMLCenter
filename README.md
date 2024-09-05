RMLCenter
========
 
The Dash app (GUI) that helps set up a reinforcement learning project using a DQN agent built with PyTorch and the Gymnasium environment.

### Please, read before use

> [!WARNING]
>This is an alpha version of the app. Users may encounter bugs and unexpected behavior. Please be careful when using this software.
> 
>This app needs storage space to save data (especially recaps from episodes, approximately 1-5MB per episode) collected during agent training, so please avoid running too many episodes at once. It has been tested with maximally the 600 episodes so far. Tests are in progress.
> 
>Please remember that all data is deleted after closing the app.

>[!NOTE]
>There is an information about incomig features in the last section of this file.</dd>


Installation and First Run
=================

### Prerequisites

Ensure you have the following installed on your system:

- **Python 3.11+**
- **pip** (Python package manager)
- **Git**

### Step 1: Clone the repository

Open your terminal and clone the repository to your local machine using the following command:

```bash
git clone https://github.com/UserKrzysztof/RMLCenter.git
```

### Step 2: Navigate to the project directory

Change into the directory of the cloned repository:

```bash
cd RMLCenter
```

### Step 3: Create a virtual environment (optional but recommended)

It's a good practice to create a virtual environment to manage dependencies:

```bash
python -m venv venv
```

Acivate the virtual enviroment
* on Windows:
  ```bash
  venv\Scripts\activate
  ```
* on macOS\Linux
  ```bash
  source venv\Scripts\activate
  ```

### Step 4: Install dependencies
Install all required dependencies using the ```requirements.txt``` file:
```bash
pip install -r requirements.txt
```

### Step 5: Run the Dash app
Finally, you can run the Dash app using the following command:
```bash
python code\app.py
```

### Access the app
After running the command, the app will be available at http://127.0.0.1:8050/ in your web browser.

User Guide
=========


### Description of the main page
![main_page](https://github.com/UserKrzysztof/RMLCenter/blob/main/read_me_content/main_page.png)

1. Buttons that open modals with setup options.
2. Log. There will be printed all messages from the app.
3. Recap videos captured during episodes will be shown in this area
   3.1 Dropdown menu with available videos to be played
   3.2 Video player
4. Graph showing reward income from each episode

---
The following order of operations is recommended:

### Step 1: Set up enviroment
![env](https://github.com/UserKrzysztof/RMLCenter/blob/main/read_me_content/env.png)
First, input the environment name. If the name is correct and has specific parameters, they will appear in the designated space below the environment name input.
The input fields for the parameters of the ```gym.make()``` function will be enabled once you select the proper enviroment.<br/>
After setting up all the necessary parameters, click the "Submit" button to continue.

### Step 2: Set up DQN agent's network
Before setting up network it is good to learn about ```torch.nn``` module at https://pytorch.org/docs/stable/nn.html 
![net](https://github.com/UserKrzysztof/RMLCenter/blob/main/read_me_content/net.png)
Click the button to open a dropdown menu with all the supported layers that can be added to the agent's network.
![net2](https://github.com/UserKrzysztof/RMLCenter/blob/main/read_me_content/net2.png)
Each added layer has its own menu with parameters, which can be opened by clicking the circle button (a circle with a white arrow) on the right side of the layer's box.
You can also move and delete layers by using the controls on the right side of the layer. These controls will appear when you hover over the layer.<br/>
Once you've set up all the necessary parameters, click the "Submit" button to continue.

### Step 3: Set up learning hiperparameters
![hyper](https://github.com/UserKrzysztof/RMLCenter/blob/main/read_me_content/hyper.png)
Here, you can set additional hyperparameters for the agent, such as the number of training episodes, learning rate, and more.<br\>
Once you've set up all the necessary parameters, click the "Submit" button to continue.

### Step 4: Run calculations
<img src="https://github.com/UserKrzysztof/RMLCenter/blob/main/read_me_content/setup_done.png" width="30%">
<br/>
Once you complete the setup, you should see three green checkmarks on the main page, and the "Run" button will be enabled.
You can now click the "Run" button to follow the progress of the training process.

Tech
=======
* The agent's code is adapted from: https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
* Dash: https://dash.plotly.com
* Flask: https://flask.palletsprojects.com/en/3.0.x
* PyTorch: https://pytorch.org
* Gymnasium: https://gymnasium.farama.org

Incoming Features (Future Versions of the App)
============
- Turning off environment rendering. Render on demand.
- Overfitting alert
- Optimizing storage space requirements.
- Archiving collected data on user demand.
- Saving the agent's state to a file and loading the agent from a file.
- Support for custom environments.
- Tooltips with hints// description of the hyperparameters
- Fixing bugs in the UI.

It has not yet been determined when the first updates will be released. <br/>
The order of adding above features might change. <br/> 
I am open to ideas from the community.


