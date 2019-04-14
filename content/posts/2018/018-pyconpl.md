---
draft: true
title: "PyCon PL 2018"
description: "Summary of the of a talk I gave at PyCon PL 2018"
slug: "pyconpl-2018"
date: "2018-08-10T14:41:50+01:00"
categories:
  - learning
tags:
    - python
    - conference

featuredImage: /img/2018/020/PyConPL18.svg
featuredImageDescription: "PyConPL'18 logo. Source: [https://pl.pycon.org/2018/](https://pl.pycon.org/2018/)"
dropCap: false
---

# The good way to behave
----


# About me

* 3 years in telco compliancy testing
* 8 years in software test automation
* In love with Python for ≈4 years
* Worked for Orange, Yell, Yoyo, Arts Alliance Media & UK GOV
* Prefers to work with APIs.


```
https://medium.com/@priyank.it/bdd-best-practices-61f01098ed95
https://medium.com/@briananderson2209/best-automation-testing-tools-for-2018-top-10-reviews-8a4a19f664d2
https://behave.readthedocs.io/en/latest/practical_tips.html#seriously-don-t-test-the-user-interface
https://behave.readthedocs.io/en/latest/practical_tips.html
```

TIPS:

* list of all steps
* parameter parsers/formatter
* forcing FrontEnd devs to apply IDs to all important UI elements


Detailed abstract
Topics to 
1) Declarative vs Imperative
    * compare declarative and imperative styles of writing BDD scenarios
2) Make things easy for yourself
    * things to avoid in scenarios
    * reducing duplication by using generic parametrised steps
3) Organising your test code FTW!
    * benefits of making a step definition a one-liner
    * separating step definitions from step implementaions
    * keeping the test logic away from Page Objects (kinda MVC)
4) Dealing with complex scenarios
    * using scenario context data structure as a consistent way of passing data between steps
    * using actors in your scenarios from day one

# Declarative vs Imperative → 5 minutes

An eye opener:
* User Centred Scenarios - CukeUp 2012

```bdd
  @JIRA-003
  @contact-us
  @<selected>
  Scenario Outline: A contact confirmation email should be sent after visitor submits the contact-us form
    Given you are on the "<selected>" page

    When you click on the "Contact us" link
    And you enter "test user" in the "Name" field
    And you enter "test@example.com" in the "Email" field
    And you enter "test message" in the "Message" field
    And you tick the CAPTCHA checkbox
    And you click on the "submit" button

    Then you should be on the "Thank you for your message" page
    And you wait for "15" seconds
    And you check the inbox for the "test@example.com"
    Then you should receive a contact confirmation email from "noreply@example.com"

    Examples: selected pages
      | selected |
      | Home     |
      | Deals    |
      | Privacy  |
```

```bdd
  @JIRA-003
  @contact-us
  @<selected>
  Scenario Outline: An email should be sent after visitor submits the contact-us form
    Given "Robert" visited the "<selected>" page
    And "Robert" decided to "Contact us"

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Thank you for your message" page
    And "Robert" should receive a contact confirmation email from "noreply@example.com"

    Examples: selected pages
      | selected |
      | Home     |
      | Deals    |
      | Privacy  |
```


# Make things easy for yourself → 5 minutes
----
## things to avoid in scenarios

## reducing duplication by using generic parametrised steps


# Organising your test code FTW! → 10 minutes
----
## benefits of making a step definition a one-liner

Instead of having one long `steps.py` with implementations of all steps:
```python
from behave import given


@given('"{actor_alias}" visited the "{page_name}" page')
def given_actor_visits_page(context: Context, actor_alias: str, page_name: str):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))

    page = get_page_object(page_name)
    has_action(page, "visit")
    page.visit(context.driver)

...
```


You can move step implementation to separate file or files, and thus help to
logically organise your steps.
`given_def.py`

```python
from behave import given

from steps.when_impl import visit_page


@given('"{actor_alias}" visited the "{page_name}" page')
def given_actor_visits_page(context, actor_alias, page_name):
    visit_page(context, actor_alias, page_name)
```


```python
from behave.runner import Context


def visit_page(context: Context, actor_alias: str, page_name: str):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))

    page = get_page_object(page_name)
    has_action(page, "visit")
    page.visit(context.driver)
```


## separating step definitions from step implementaions

## keeping the test logic away from Page Objects (kinda MVC)


# Dealing with complex scenarios → 10 minutes
----
## using scenario context data structure as a consistent way of passing data between steps

## using actors in your scenarios from day one


