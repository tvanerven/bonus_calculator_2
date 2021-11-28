# Bonus calculator

A small tool to calculate a bonus, based on some factors.

# Running:

- Clone the project
- Navigate to directory
- Tests: `python -m unittest`
- Code/manual testing: Use something like IPython. This program makes no assumptions on what tooling is used here, and only uses core libraries.

# Considerations

- After the first instance of this calculator, I decided not to make the same mistake. As a result, this project has been designed with (1) testing in mind (2) only core libraries as opposed to unfamiliar stacks.
- A couple of validators are simply nice to have. Datetime objects are nice, but users will often just wish to enter dates fluidly.
- The bonus amounts are all rounded. Reason here is that I expect that people feel better getting a bonus of 260, rather than 260.4954 or something similar.The rounding is two decimals, as we're dealing with money. The raw values, however, can be easily provided by avoiding one function call. Couple of lines of change here.
- The tests are barebone, but cover both scenario's as well as account for pitfalls. While these tests can be improved by splitting individual scenario's out, the coverage (for now) appears fine.

# Pitfalls

- I initially considered making Salary a model with a start date and an end date. This makes some sense conceptually - salaries change over time, and the most clean method here would be to add a new Salary instance to provide historical logging for past salaries. However, this does complicate things for calculating a bonus for a given salary, as you need to match salaries, compare date ranges, and the like. While possible, in order to do this elegantly, the complexity exceeds the scope of this assignment. Instead, I resolved to treat Salary simple for now (without dateranges), while making a remark here to showcase my awareness of the complexity here.
- Rounding. Rounding is an interesting problem (how many decimals and where to round), and simply put, was intentionally kept isolated in the `_clean_result` function to provide one simple place to override.

# Paths not taken

- I considered going forward with using `getattr` to retrieve specific calculation functions. For instance - what if we want to use fixed amounts based on salary? It'd be nice to add a function like `getattr(f'calculate_{method}_bonus', self)`. I weighed this against the relatively low amount of lines, and decided not to do it. It's readable enough as it is, for now, but expanding it with more options in this manner is a realistic possibility in the future.

# Explanation on models

The models might require some more explanation:

- The hierarchy was followed as provided in the assignment. This is simple top-to-bottom stuff. 
- For now, I've made no assumptions on database backend. That's why Python classes were used.
- Inheritance is demonstrated by classes accepting lists of instances of other classes relating to it.
- The `Threshold` model might require some explanation. Conceptually, Thresholds define whether a calculated result is "good" or "bad" and can return a message based on that. The `value` here is intended to be the upper value. A `Dimension` can then check it's related thresholds to check what the result is, based on the cumulative value of it's related `Aspect` objects.
- As for the bonus questions:
    - Please observe the `Factor` model which are related to `Aspect`. With no further information, the model is relatively blank.
    - Please observe the `Dimension` model may also contain questions. Naturally, some logic would be required here to apply to either use the `Aspect` route or the `Questions` route. Both would be illogical (since they represent two different measurement routes) and should probably be avoided (read: blocked) for users.
