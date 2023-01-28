# Python Threading - Issues and Caveats

I often get asked to create a course (or a video) on Python multi-threading.

Creating a video I don't quite get, because threading is a complex topic, and a single video cannot possibly do it justice - threading is **hard**!

But I also often wonder **why** I get so many requests to cover multi-threading.

I think (and maybe I'm wrong, let me know in the comments below) that many people believe
that using multithreading will speed up their application.

The short answer to that is threading will not necessarily speed up your application,
and in fact may very well slow it down!

The longer answer is that whether multithreading will speed up your app **depends on the kind of 
workload** your app is performing. 

If your application workload is mainly CPU related (e.g. will your app run faster 
if you use a faster CPU?), then threading will not only not increase performance, but will likely
make things worse. This type of workload is referred to as **CPU bound**.

You have to understand that in Python, you can create as many threads as you want, but Python itself
only allows a **single** thread to run at a time - so we have concurrency (many threads can be created
and executed concurrently), but we **do not have parallelism** - threads will not run at the same time, and
the Python process is then limited to a single core.

Your Python app threads **wil not run in parallel over multiple cores**.

Python enforces this using something called the the Global Interpreter Lock (GIL). Imposing such a 
global interpreter lock provides a number of distinct advantages (see this 
[post](https://www.backblaze.com/blog/the-python-gil-past-present-and-future/) to find out more).
But this essentially makes any Python app limited to a single core - no matter how many threads you create, 
and no two threads can execute in parallel.

You could resort to multiprocessing - but as I argue in a previous video, if you need to start scaling your
computations beyond one core, you may as well bite the bullet and create a truly distributed and scalable computation 
engine. In that video I describe a very simple queue/worker approach, but there are many other, more sophisticated ways 
of doing this as well (Spark, Hadoop, etc.)

On the other hand, if your app spends a large portion of its time waiting on many I/O operations to complete (maybe 
calling an API, a database query, reading/writing files, etc), then properly implemented threading may very well 
speed up your application. This type of workload is referred to as **I/O bound**.

But if you are dealing with an I/O bound workload, then you might as well use Python's `asyncio` - it will provide 
the same performance benefits as threading would, but in a much simpler way, and far less error prone.

Creating threads in Python is easy - way too easy! The problem is not creating multi-threaded code,
the problem is writing **logically correct** multi-threaded code. Writing correct multi-threaded code is
**hard**, it is very difficult to debug, and very difficult to be absolutely sure that you don't have bugs - 
in part because those bugs may not show up all the time - just once in a while.

In this video I'm going to show you that trying to achieve certain tasks using threading has a lot of pitfalls, and that a CPU bound workload will result in worse (or equal at best) performance when switching to multi-threading.

## Problem 1
In this problem we want to calculate
```
1 + 2 + 3 + ...
```

We'll want to print the intermediate results as well, so looking for something like this

```
1 + 0 = 1
--------------------
1 + 1 = 2
--------------------
2 + 2 = 4
--------------------
4 + 3 = 7
--------------------
7 + 4 = 11
--------------------
11 + 5 = 16
--------------------
etc
```

The key here is to show how shared global state in threading can lead to issues - so I'm going to use global
variables for the counter and the cumulative sum.


### Solution 1
In this solution we use a standard non-threaded app - very easy to do. This also shows what we want our output
to look like.

### Solution 2
In this solution we create a thread for each computation, kick off all those threads, and wait for
the threads to complete.

Run this a few times, and we quickly see that we have problems.

The first things we notice is that the `----` line does not always show up in the right spot.

This is because `print` is not thread-safe - `print` actually buffers its output, and our output here is
shared amongst all the threads - so we have a shared resource (the console, or `stdout`), and writing to that output can get interrupted
by another thread, leading to this problem. This "competition" for a shared resource by different threads is
called a **race condition**.

We also see a problem with the computations themselves - again, we have a similar problem, where shared state
is being read and modified by multiple threads - again leading to a race condition.

### Solution 3
In this solution we are going to try and fix the printing problem first by creating a **lock**.

A lock is a **cooperative** concept in threading - in other words when we use locks we need to make sure that
we place those locks ourselves everywhere in our code - up to us as developers to impose these locks.

The way a lock works, we establish, or **acquire** a lock, do some work, and then **release** the lock. While the lock has been
acquired by one thread, even if the thread gets interrupted, and another thread starts running, it will not be able to
acquire that same lock, until it has been released by the previous thread - essentially we are saying "thread 2, you 
must wait until thread 1 has released its lock before you can proceed and acquire the lock" - this ensures only 
one thread can access some code at a time. It is imperative to release locks, and that we release them as 
quickly as possible. Failure to release locks will likely cause your app to simply stop running at some point.

So, we seem to have fixed our print issue, but our calculations are completely off.

### Solution 3a
Lock objects also implement a context manager, so instead of writing `acquire()` and `release()`
ourselves, we can simply use a context manager - much simpler, and saves us having to potentially handle
exceptions that could occur between the `acquire()` and `release()` (and potentially failing to release a lock).


### Solution 4
So our calculations are completely off - why?

Look at this piece of code that is being executed by **each thread**:

```python
1  global counter
2  global sum_
3
4  next_ = sum_ + counter
5  with p_lock:
6      print(f"{sum_} + {counter} = {next_}")
7      print("-" * 20)
8  sum_ = next_
9  counter = counter + 1
```

Remember that threads can be interrupted at any time mostly outside of our control (so called preemptive multi tasking).

So one thread could execute line 4 (it has read the current value of `sum_` and `counter` and calculated `next_`).
But before if can execute lines 8 and 9, another thread takes over, and reads `sum_` and `counter` as well - the same 
ones as the previous thread - and that's wrong - so our problem is that we need to make sure we put a lock around
the code that reads/updates the global state variables `counter` and `sum_`.

If we run this a few times, it looks like we get the correct final result (`5050`), but if we
run the program a few times, and look closely, the intermediate results don't appear to entirely correct.

Although we eliminated the race condition, we still have a problem where the threads are not executing
the calculations in the correct order (since we have no control on when threads run and get interrupted).

At least we are getting a correct final result. But the intermediate calculation display is off.

### Solution 5
In this solution, I want to show you a technique called **fuzzing**.

We are going to exacerbate the problem we saw in the last solution by introducing some
variability in the time it takes our `do_work` function to run.

The problem with our example, is that the amount of time take to perform each `do_work` run is about the
same, and we may therefore not see problems which may occur in "real life" situations where our
work may very well end up taking different amounts of time for each invocation, and also give more chances
for our thread to be interrupted in the middle of doing its work.

If we now run our code, we can really see the problem.

And this is not something we can solve with locks. We need to ensure that the work being done
is performed in a sequential manner somehow, and this is typically not how concurrent programming works - one
key principle in concurrent programming is that the order of execution should not matter. Indeed, for obtaining the 
final result our algorithm seems to work fine - but the intermediate calculations display is totally off.


### Solution 6
Since it looks like our calculation is actually correct, it would seem that the problem is related to
the printing of the intermediate results not being printed in the correct order.

To solve this problem, we are going to use a Queue. Instead of the thread printing directly, we are to send
the print output to a queue, and we'll have a queue watcher print out the lines one by one (FIFO).

Python provides us threadsafe queues in the `queue` module.

I'm also going to add some variability to starting the threads by fuzzing the `start()` of each thread.

So, this solution seems to work... **BUT**

I actually am not convinced this is logically correct - I may be missing something that I failed to see and
which will come back and bite me at some later point (feel free to point it out in the comments! :-)

(Personally I believe that the reason this is working is that we have essentially put a lock around 
the **entire** set of calculations - which basically blocks any other thread from interrupting the computation, 
essentially rendering our calculation flow "linear" instead of truly concurrent.)

Hopefully by now I've convinced you that multi-threading is **HARD** - way too easy to make mistakes.

### Solution 7
So, not only was multi-threading our original application hard (and not even sure it's actually fully correct),
but what about timings?

Let's time our initial single-threaded approach.

On my machine, about `0.3 seconds` for `100_000` iterations.

### Solution 8
And let's time our multi-threaded version (removing fuzzing of course)

On my machine, about `4 seconds` also for `100_000` iterations - substantially slower!


## Problem 2
The first problem we looked at was a little contrived - not just to make things simple to explain
some of the basics of multi-threading, but also to highlight some of the concurrency issues we
often face.

For this example, we're going to do something a little more practical.

We're going to calculate a definite integral of some function using simple Riemann sums.
(see [here](https://en.wikipedia.org/wiki/Riemann_sum) for info on Riemann sums)

If you are not familiar with integrals, or Riemann sums, don't worry, you don't actually need
to understand them in order to understand the solutions - basically we are going to
perform some calculations (the **order** of which will **not matter**), and arrive at some final result (we
don't actually care about the intermediate results). This problem is going to a CPU-bound workload,
and my intent is to show you here that multi-threading will **not** improve our timings, and may in fact
even slow things down (due to the overhead of context switching)

### Solution 1
This solution will just be a single-threaded approach. There are ways to simplify the code,
but I'm aiming for clarity here, not necessarily the most efficient way of doing things. As long as we use
the same technique for both the single-threaded and multi-threaded solutions, we should be able to compare 
them.

### Solution 2
We switch to a multi-threaded implementation.

You'll notice that I used a shared variable (`results`). I did not put any locks around that access since
the threads are all just appending to that list, so we should not have any race conditions here (because of the GIL!)

When we run this, we can see that as we increase the number of threads we throw at the problem, performance
actually decreases.


## Conclusion
So, in conclusion, I hope I have shown you two things:
1. multi-threading is **hard**
2. CPU-bound workloads do not benefit from multi-threading (and in fact may result in worse performance)

There are of course, other use cases for threading, even apart from I/O workloads (where I would use `asyncio` instead).

You may have a main application running, and at the same time you need some other thread to perform some unrelated work
on a periodic basis that just needs to run concurrently (e.g. a heartbeat that needs to be emitted even if 
the main code is blocking). 

But in my 15+ years of writing Python code in a business environment (APIs, data pipelines and analysis, dev ops 
type work), I have used multi-threading in production a few times only. Your mileage may very well vary of 
course, like if you are writing advanced libraries - it's just that, personally, and for the majority of the work I do, 
multi-threading is something I am extremely wary of, and only use as a last resort! :-)
