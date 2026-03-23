# Aircraft Management

At the first stage, this project was designed for a startup that aimed to invest in renewable energy for light aircraft.

Initially, we decided to develop software for airports. However, due to time constraints in software development, it was later decided to focus on end users instead of airports. There were two main challenges. The MVP of the project could not be used directly by airports because they already rely on many different software systems, which makes step-by-step integration difficult. Therefore, the strategy was changed to a gradual integration approach, aiming to connect pilots with airports.

My partner believed that this project could be completed by AI, so I decided to publish it. The funniest part is he and his friend decided to slander me because I smoke weed. Good luck to him.

## Structure

The project consists of two layers: Flask and Spring. The database is managed by Spring because it provides greater security, ensuring that no one can access the database directly. A token must be sent to the server before accessing any endpoint.

Flask handles incoming requests. Some requests, such as OCR, do not require access to the database and are related to pilots' needs.

The most critical component is the purchasing system, as charging stations should be controlled by third-party providers. These could include airports or charging station companies, which can manage them through this framework.

## Quickstart
This guide shows how to install the Aircraft CLI and add your fist chargin station using the Python SDK.

1. Install the CLI
Download the Aircraft CLI from the official website and move the binaryto your system PATH.

Example (macOS / Linux):

'''Bash sudo mv aircraft /usr/local/bin '''

2. Login
After installing the CLI, you can log in using the command below.

'''Bash aircraft login '''

You will be logged in successfully, if you provide your company name and given password.

3. Install the Python SDK
'''Bash pip install aircraft '''

4. Add Your First Charging Station
'''Python import aircraft as ac

client = ac.Client()

client.add_station( name="Test Station", kw=150, latitude=41.0082, longitude=28.9784 )
