# **craft ai** python client #

[**craft ai**](http://craft.ai) API python client

**craft ai** enables developers to create applications and services that adapt to each individual user.

> :construction: **craft ai** is currently in private beta, you can request an access at https://beta.craft.ai/signup

## Get Started! ##

**craft ai** is based around the concept of **agents**. In most use cases, one agent is created per user or per device.

An agent is an independant module that store the history of the **context** of its user or device's context, and learns which **decision** to take based on the evolution of this context in the form of a **decision tree**.

### Retrieve your credentials ###

**craft ai** agents belong to **owners**, in the current version, each identified users defines a owner, in the future we will introduce shared organization-level owners.

On top of that, calls to **craft ai** are authenticated using personal **JWT tokens**.

> :information_source: To retrieve your **owner** and **token**, visit the 'Settings' tab in the **craft ai** control center at [`https://beta.craft.ai/settings`](https://beta.craft.ai/settings).

### Install ###

### Initialize ###
```python
# TODO : write an initialization guide
```

## API ##

### Timestamp ###

As you'll see in the reference, the **craft ai** API heavily relies on `timestamps`. A `timestamp` is an instant represented as a [Unix time](https://en.wikipedia.org/wiki/Unix_time), that is to say the amount of seconds elapsed since Thursday, 1 January 1970 at midnight UTC. In most programming languages this representation is easy to retrieve, you can refer to [**this page**](https://github.com/techgaun/unix-time/blob/master/README.md) to find out how. The **craft ai** API expects integer values for `timestamps`. If your `timestamps` do not use this representation correctly, your agent will not learn properly, especially if if relies on time.

In **craft ai**, `timestamps` are used to:
1. **order** the different states of the agents, i.e. a context update occurring at a `timestamp` of _14500000**10**_ takes place **before** an update occuring at _14500000**15**_;
2. **measure** how long an agent is in a given state, i.e. if its color becomes _blue_ at a `timestamp` of _14500000**10**_, _red_ at _14500000**20**_ and again _blue_ at _14500000**25**_, between _14500000**10**_ and _14500000**25**_ it has been _blue_ twice as long as _red_.

The agents model's `time_quantum` describes, in the same representation as `timestamps`, the minimum amount of time that is meaningful for an agent. Context updates occurring faster than this quantum won't be taken into account.

### Model ###

Each agent is based upon a model, the model defines:

- the context schema, i.e. the list of property keys and their type (as defined in the following section),
- the output properties, i.e. the list of property keys on which the agent takes decisions,

> :warning: In the current version, only one output property can be provided, and must be of type `enum`.

- the [`time_quantum`](#timestamp).

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
