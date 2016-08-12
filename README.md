# **craft ai** API python client #

[![Build Status](https://travis-ci.org/craft-ai/craft-ai-client-python.svg?branch=master)](https://travis-ci.org/craft-ai/craft-ai-client-python) [![License](https://img.shields.io/badge/license-BSD--3--Clause-42358A.svg?style=flat-square)](LICENSE)

[**craft ai** _AI-as-a-service_](http://craft.ai) enables developers to create Apps and Things that adapt to each user. To go beyond useless dashboards and spammy notifications, **craft ai** learns how users behave to automate recurring tasks, make personalized recommendations, or detect anomalies.

## Get Started! ##

### 0 - Signup ###

If you're reading this you are probably already registered with **craft ai**, if not, head to [`https://beta.craft.ai/signup`](https://beta.craft.ai/signup).

> :construction: **craft ai** is currently in private beta, as such we validate accounts, this step should be quick.

### 1 - Retrieve your credentials ###

Once your account is setup, you need to retrieve your **owner** and **token**. Both are available in the 'Settings' tab in the **craft ai** control center at [`https://beta.craft.ai/settings`](https://beta.craft.ai/settings).

### 2 - Setup ###

#### Install ####

#### [PIP](https://pypi.python.org/pypi/pip/) / [PyPI](https://pypi.python.org/pypi) ####

Let's first install the package from pip.

```sh
pip install --upgrade craft-ai
```
Then import it in your code

```python
from craftai import client as craftai
```

#### Initialize ####

```python
config = {
    "owner": '{owner}',
    "token": '{token}'
}
client = craftai.CraftAIClient(config)
```

### 3 - Create an agent ###

**craft ai** is based on the concept of **agents**. In most use cases, one agent is created per user or per device.

An agent is an independent module that stores the history of the **context** of its user or device's context, and learns which **decision** to take based on the evolution of this context in the form of a **decision tree**.

In this example, we will create an agent that learns the **decision model** of a light bulb based on the time of the day and the number of people in the room. In practice, it means the agent's context have 4 properties:

- `peopleCount` which is a `continuous` property,
- `timeOfDay` which is a `time_of_day` property,
- `timezone`, a property of type `timezone` needed to generate proper values for `timeOfDay` (cf. the [context properties type section](#context-properties-types) for further information),
- and finally `lightbulbState` which is an `enum` property that is also the output of this model.

TODO: Write doc

Pretty straightforward to test! Open [`https://beta.craft.ai/inspector`](https://beta.craft.ai/inspector), your agent is now listed.

Now, if you run that a second time, you'll get an error: the agent `'my_first_agent'` is already existing. Let's see how we can delete it before recreating it.

TODO: Write doc

_For further information, check the ['create agent' reference documentation](#create)._

### 4 - Add context operations ###

We have now created our first agent but it is not able to do much, yet. To learn a decision model it needs to be provided with data, in **craft ai** these are called context operations.

In the following we add 8 operations:

1. The initial one sets the initial state of the agent, on July the 25th of 2016 at 5:30, in Paris, nobody is there and the light is off;
2. At 7:02, someone enters the room the light is turned on;
3. At 7:15, someone else enters the room;
4. At 7:31, the light is turned off;
5. At 8:12, everyone leaves the room;
6. At 19:23, 2 persons enter the room;
7. At 22:35, the light is turned on;
8. At 23:06, everyone leaves the room and the light is turned off.

TODO: Write doc

In real-world applications, you'll probably do the same kind of things when the agent is created and then, regularly throughout the lifetime of the agent with newer data.

_For further information, check the ['add context operations' reference documentation](#add-operations)._

### 5 - Compute the decision tree ###

The agent has acquired a context history, we can now compute a decision tree from it!

The decision tree is computed at a given timestamp, which means it will consider the context history from the creation of this agent up to this moment. Let's first try to compute the decision tree at midnight on July the 26th of 2016.

TODO: Write doc

Try to retrieve the tree at different timestamps to see how it gradually learns from the new operations. To visualize the trees, use the [inspector](https://beta.craft.ai/inspector)!

_For further information, check the ['compute decision tree' reference documentation](#compute)._

### 6 - Take a decision ###

Once the decision tree is computed it can be used to take a decision. In our case it is basically answering this type of question: "What is the anticipated **state of the lightbulb** at 7:15 if there is 2 persons in the room ?".

TODO: Write doc

_For further information, check the ['take decision' reference documentation](#take-decision)._

## API ##

### Owner ###

**craft ai** agents belong to **owners**. In the current version, each identified users defines a owner, in the future we will introduce shared organization-level owners.

### Model ###

Each agent is based upon a model, the model defines:

- the context schema, i.e. the list of property keys and their type (as defined in the following section),
- the output properties, i.e. the list of property keys on which the agent takes decisions,

> :warning: In the current version, only one output property can be provided, and must be of type `enum`.

- the `time_quantum` is the minimum amount of time, in seconds, that is meaningful for an agent; context updates occurring faster than this quantum won't be taken into account.

#### Context properties types ####

##### Base types: `enum` and `continuous` #####

`enum` and `continuous` are the two base **craft ai** types:

- `enum` properties can take any string values;
- `continuous` properties can take any real number value.

##### Time types: `timezone`, `time_of_day` and `day_of_week` #####

**craft ai** defines 3 types related to time:

- `time_of_day` properties can take any real number belonging to **[0.0; 24.0[**
representing the number of hours in the day since midnight (e.g. 13.5 means
13:30),
- `day_of_week` properties can take any integer belonging to **[0, 6]**, each
value represents a day of the week starting from Monday (0 is Monday, 6 is
Sunday).
- `timezone` properties can take string values representing the timezone as an
offset from UTC, the expected format is **±[hh]:[mm]** where `hh` represent the
hour and `mm` the minutes from UTC (eg. `+01:30`)), between `-12:00` and
`+14:00`.

> :information_source: By default, the values of `time_of_day` and `day_of_week`
> properties are > generated from the [`timestamp`](#timestamp) of an agent's
> state and the agent's current > `timezone`.
>
> If you wish to provide their value manually, add `is_generated: false` to the
> time types in your model. In this case, since you provide the values, you must
> update the context whenever one of these time values changes in a way that is
> significant for your system.

##### Examples #####

Let's take a look at the following model. It is designed to model the **color**
of a lightbulb (the `lightbulbColor` property, defined as an output) depending
on the **outside light intensity** (the `lightIntensity` property), the **time
of the day** (the `time` property) and the **day of the week** (the `day`
property).

`day` and `time` values will be generated automatically, hence the need for
`tz`, the current Time Zone, to compute their value from given
[`timestamps`](#timestamp).

The `time_quantum` is set to 100 seconds, which means that if the lightbulb
color is changed from red to blue then from blue to purple in less that 1
minutes and 40 seconds, only the change from red to purple will be taken into
account.

```json
{
  "context": {
      "lightIntensity":  {
        "type": "continuous"
      },
      "time": {
        "type": "time_of_day"
      },
      "day": {
        "type": "day_of_week"
      },
      "tz": {
        "type": "timezone"
      },
      "lightbulbColor": {
          "type": "enum"
      }
  },
  "output": ["lightbulbColor"],
  "time_quantum": 100
}
```

In this second examples, the `time` property is not generated, no property of
type `timezone` is therefore needed. However values of `time` must be manually
provided continuously.

```json
{
  "context": {
    "time": {
      "type": "time_of_day",
      "is_generated": false
    },
    "lightIntensity":  {
        "type": "continuous"
    },
    "lightbulbColor": {
        "type": "enum"
    }
  },
  "output": ["lightbulbColor"],
  "time_quantum": 100
}
```

### Timestamp ###

**craft ai** API heavily relies on `timestamps`. A `timestamp` is an instant represented as a [Unix time](https://en.wikipedia.org/wiki/Unix_time), that is to say the amount of seconds elapsed since Thursday, 1 January 1970 at midnight UTC. In most programming languages this representation is easy to retrieve, you can refer to [**this page**](https://github.com/techgaun/unix-time/blob/master/README.md) to find out how.



### Agent ###

#### Create ####

Create a new agent, and create its [model](#model).


#### Delete ####

TODO: Write doc

#### Retrieve ####

TODO: Write doc

#### List ####

TODO: Write doc



### Context ###

#### Add operations ####

TODO: Write doc

#### List operations ####

TODO: Write doc

#### Retrieve state ####

TODO: Write doc

### Decision tree ###

#### Compute ####

TODO: Write doc

#### Take Decision ####

TODO: Write doc


