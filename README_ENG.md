# Alexa Skill: Project MARV

## Project Description
This project aims to control a vehicle robot using voice commands via Alexa. The Alexa Skill enables the user to send various commands to the robot to control its movements and actions.

## Requirements
- Access to Alexa Developer Console
- Basic knowledge of Python
- Familiarity with AWS services (Lambda, IAM, etc.)

## Project Structure
### Skill Definition
- **Interaction Model**: Defines the intents, slots, and utterances. The data is located in the `/interactionModels/custom` folder as an exported JSON file.
- **Backend Logic**: AWS Lambda function that processes requests and generates appropriate responses. The data is located in the `/lambda/` folder. The backend logic in this project is built using Python.

## Importing the Existing Data
### Step 1: Create the Alexa Skill
1. Log in to the [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask).
2. Click on "Create Skill."
3. Choose a name for your skill and select the "Primary local language."

### Step 2: Experience, Model, Hosting Service
1. In the "Choose a type of experience" step, select "Other"
2. Choose the "Custom" model and "Alexa-hosted (Python)" as the hosting service.
3. Use an EU server as the "Hosting Region"

### Step 3: Import Git Repository
1. Click on the "Import Skill" button at the top right and enter the repository address: [MAVAlexaSkill](https://github.com/mgurdzel/MAVAlexaSkill).
2. Click on Import (the installation will take a few minutes).

### Step 4: Assign a Skill Invocation Name
1. Go to the Build section of the [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask).
2. Expand the "Invocations" tab and click on "Skill Invocation Name."
3. Assign the "Skill Invocation Name." This is needed to start the skill on Alexa.
4. Click on "Build" at the top right.

### Step 5: Test the Skill
1. Go to the Test section of the [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask).
2. Open the skill, e.g., with the command: "Hey Alexa, open {Skill Invocation Name}."
   - Replace {Skill Invocation Name} with the name assigned in Step 4.
