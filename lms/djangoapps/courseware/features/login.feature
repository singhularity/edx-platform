@shard_1
Feature: LMS.Login in as a registered user
  As a registered user
  In order to access my content
  I want to be able to login in to edX

    Scenario: Logout of a signed in account
    Given I am logged in
    When I click the dropdown arrow
    And I click the link with the text "Sign out"
    Then I should see a link with the text "Sign in"
    And I should see that the path is "/"
