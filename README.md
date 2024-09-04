RLCenter
========
 
The Dash app (GUI) that helps set up a reinforcement learning project using a DQN agent built with PyTorch and the Gymnasium environment.

### Read before use

<dl>
  <dt>Notice:</dt>
  <dd>This is an alpha version of the app. Users may encounter bugs and unexpected behavior. Please be careful when using this software.
  <dd>This app needs storage space to save data (especially recaps from episodes, approximately 1-5MB per episode) collected during agent training, so please avoid running too    many episodes at once.</dd>
  <dd>Please remember that all data is deleted after closing the app.</dd>
  <dd>In the last section of this file, I have added information about the features that I am currently working on.</dd>
</dl>

Installation and First Run
=================
### Step 0: Read the notice

### Prerequisites

Ensure you have the following installed on your system:

- **Python 3.11+**
- **pip** (Python package manager)
- **Git**

### Step 1: Clone the repository

Open your terminal and clone the repository to your local machine using the following command:

```bash
git clone https://github.com/UserKrzysztof/RLCenter.git
```

### Step 2: Navigate to the project directory

Change into the directory of the cloned repository:

```bash
cd RLCenter
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
python app.py
```

### Access the app
After running the command, the app will be available at http://127.0.0.1:8050/ in your web browser.

User Guide
=========


### Description of main page

### Step 1: Set up enviromet

### Step 2: Set up DQN agent's network

### Step 3: Set up learning hiperparameters

### Step 4: Run calculations


Incoming Features (Future Versions of the App)
============

- Ability to turn off environment rendering. Render on demand.
- Optimizing storage space requirements.
- Archiving collected data on user demand.
- Saving the agent's state to a file and loading the agent from a file.
- Support for custom environments.
- Fixing bugs in the UI.

The order of adding above features might change. I am open to ideas from the community.


