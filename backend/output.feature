Feature: Current Weather

  Scenario: Retrieve Current Weather
    Given the user is located in a valid location
    When the user requests the current weather
    Then the system displays the current weather for the user's location

