Feature: registration
    Scenario Outline: Register with valid details
        Given I am on the registration page
            And I have completed the form with <email> <organisation> <password> and <passwordConfirmation>
        When I have clicked on the register button
        Then I will be logged in as <username>
            And my account will be assigned the role of <role>

            Examples:
            | email     | organisation | password  | passwordConfirmation | username  | role  |
            | usernamea | Bytes        | password1 | password1            | usernamea | Admin |
            | usernameb | Bytes        | password2 | password2            | usernameb | Admin |
            | usernamec | Bytes        | password3 | password3            | usernamec | Admin |
            | usernamed | Bytes        | password4 | password4            | usernamed | Admin |
            | usernamee | Bytes        | password5 | password5            | usernamee | Admin |
