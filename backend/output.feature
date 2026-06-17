Feature: Password Reset

  Scenario: Successful Password Reset
    Given I am on the login page
    When I click on forgot password and enter my email
    Then I should receive a password reset email

  Scenario: Unsuccessful Password Reset
    Given I am on the login page
    When I click on forgot password and enter an invalid email
    Then I should see an error message

