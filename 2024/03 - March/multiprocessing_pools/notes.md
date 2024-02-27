# Python Multiprocessing Pools

In this video we look at how to spread CPU-bound workloads across multiple cores on your machine using 
multiprocessing pools.

Note, that for I/O bound workloads, a much better alternative is to use asyncio (or threading). I explain this
an earlier video [here](https://youtu.be/S05-MZAJqNM).

## Example 1
In this example we have a long-running function where we use a blocking `sleep()` to simulate a CPU bound 
function - a lot of the examples I see everywhere uses that, so let's give it a shot too... Or should we? Oh well, 
let's just do it and see what happens.

This function is simple, it takes two positional arguments, sleeps a certain amount of time, and returns the sum of 
the two values.

We'll want to run this function a certain number of times with different input values. 
Then, we'll want to spread this computational workload across multiple cores. 
To do this we'll use a multiprocessing `Pool`.

So, we need to:
- spawn multiple parallel processes
- pass some values to the function
- receive a result back

In this example, our function will look for just two positional arguments.

The `Pool` instance supports passing positional arguments via a tuple for each function call, and using the `starmap` 
method to "spread" the input arguments as positional arguments - much like the `starmap` function in the `functools` 
module - Python docs [here]() (or better yet, check out my 
[Deep Dive](https://www.udemy.com/course/python-3-deep-dive-part-2/?referralCode=3E7AFEF5174F04E5C8D4) 
course that covers `starmap`, and a lot more!)

We'll start with a pool sized at 1 - this will essentially run all the function calls sequentially, so we can establish
a baseline for how long this takes to run.

Then, we'll start increasing the pool size (the max number of parallel processes), and see what we get. 

To make things a bit more realistic, the long-running function is going to sleep a variable amount of time (from 1 
to 3 seconds). To ensure repeatability, we'll set a specific seed from our `random` module.

Note that there is no guarantee of the order in which the functions are going to be called ( a consequence of the way 
we are starting the functions, later I'll show you a different method that starts the functions in a specific 
sequence) - so, in order to keep things consistent from one run to another, I will generate the random sleep 
times **outside** the called function itself.

Another important thing to understand, Python may or may not use the max number of processes available, and I do not 
think there is any guarantee of how it spreads the processes across the available cores. Also, setting a pool size
that is smaller than the number of cores on your machine does not guarantee that the load will be spread out
across that smaller number of cores only. There are ways to actually control that, but way too complex for me!
As I mentioned in a previous video 
([Distributed Computing](https://youtu.be/XCSARhkRg7g)), 
I rarely use multiprocessing and instead created a distributed computing system instead - this lets me scale beyond 
just a single machine if I need to.

Back to multiprocessing...

For testing this out, I have a Mac with 10 cores (M1Max), and here are my results, running a workload of `50`
function calls, with varying pool size:


| Pool Size | Total Time |
|-----------|------------|
| 1         | 96         |   
| 2         | 54         |
| 4         | 28         | 
| 6         | 19         |
| 8         | 16         |
| 10        | 13         |
| 12        | 12         |
| 14        | 9          |
| 18        | 8          |
| 50        | 6          |

Now these results are a bit suspicious... We definitely see a speed improvement as we increase the pool size.
But why does the time keep dropping if I am running more processes than available cores?

The problem is that my long-running function is **not actually doing any computations** - so each core that's running a 
process actually has plenty of bandwidth to run a few more at the same time.

In fact, using a `sleep()` does **NOT** simulate a CPU-bound workload!! So much for collective wisdom. In this case, 
it's OK, but only up to a point.

In the next example we'll remedy that.

## Example 2
In the previous example we saw how to set up multiprocessing. But our long running function was not truly CPU bound,
so let's change this, and once more benchmark our results.

For the computation, I'll implement a sieve of Eratosthenes - if you don't know what it is or how it works,
don't worry about it - the only thing here is we want a function that is computationally intensive.

Note that since we only need to pass a single argument to the sieve function, we no longer need to use
`starmp` to "spread out" multiple positional arguments - instead we can just use `map`.

Here are my results now, setting a job size of `100`:

| Pool Size | Total Time |
|-----------|------------|
| 1         | 55         |   
| 2         | 31         |
| 4         | 17         | 
| 6         | 12         |
| 8         | 11         |
| 10        | 9          |
| 12        | 10         |
| 14        | 10         |
| 18        | 10         |
| 50        | 11         |
| 100       | 13         | 

As you can see, going beyond the number of cores you have available does not increase performance as long as each
function call is essentially using up all the CPU resources on that core. And in fact, if you start going
way beyond your total number of cores, you'll start to see performance decreases.

Personally I usually do not set my pool size greater than my number of cores - 2. That way I don't starve the OS
for running other things, and my machine stays (somewhat) responsive.


## Example 3
One last thing I want to show you is how to pass **named** arguments when spawning your processes.

We can't use `map` or `starmap` - this will only work for positional arguments.

Instead, we can use the `apply_async` method (there is an `apply() method - but it's blocking so not very useful
in our case where we want all the work to be parallelized as much as possible).

We will also have to deal with the results a bit differently - each `apply_async` results in its own set of results, 
so we need to collect those somehow.

To implement this I won't use a Pool context manager - I need to control closing the pool and waiting for all async
results to come back (in essence similar to joining multiple threads), using the pool's `join()` method. 

Getting results back from an async result also needs to be done via a `.get()` method - the result object itself is 
an async object, so it does not contain the result value directly.

You'll notice, by the way, that the jobs are started in sequence now - simply because we are starting them that way 
(they may not complete in sequence, but they start that way). 


## Conclusion
And there you have it, how to use multiprocessing pools to speed up your workloads. Of course, you're limited to
a single machine. In large production systems, this is usually not enough, but if you really want to push your single
machine to the limit, multiprocessing can help you.

There's a lot of other options for multiprocessing, I just scratched the surface here. But honestly, this is
probably going to be the 80/20 rule.