@shard_2
Feature: CMS.Sign in
  In order to use the edX content
  As a new user
  I want to signup for a student account

  Scenario: Login with an invalid redirect
    Given I have opened a new course in Studio
    And I am not logged in
    And I visit the url "/signin?next=http://www.google.com/"
    When I fill in and submit the signin form
    And I wait for "2" seconds
    Then I should see that the path is "/home/"

  Scenario: Login with mistyped credentials
    Given I have opened a new course in Studio
    And I am not logged in
    And I visit the Studio homepage
    When I click the link with the text "Sign In"
    Then I should see that the path is "/signin"
    And I should not see a login error message
    And I fill in and submit the signin form incorrectly
    Then I should see a login error message
    And I edit the password field
    Then I should not see a login error message
    And I submit the signin form
    And I wait for "2" seconds
    Then I should see that the path is "/home/"
