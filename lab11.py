# Intermediate programming practice: async and sockets.
#
# For EACH problem, work out your problem-solving OUTLINE first, then implement it (you
# may use an AI assistant to help - see the README). The async parts must actually run
# their work CONCURRENTLY (that's the whole point), not one after another.
#
# Do not rename the functions - the tests use these names.

import asyncio
import socket


async def gather_doubled(numbers):
    # Outline (write your plan here first):
    
    # Restate:
    #   Take a list of numbers, run an async task for each number at the same time
    #   to double it (n * 2), and return the doubled numbers in a list in the same order.

    # Example: [1, 2, 3, 4]
    #   starts 4 tasks at the same time for 1, 2, 3, and 4
    #   task 1 returns 1 * 2 = 2, task 2 returns 2 * 2 = 4, task 3 returns 3 * 2 = 6,
    #   and task 4 returns 4 * 2 = 8
    #   asyncio.gather collects all the results in order and outputs [2, 4, 6, 8]

    # Sketch the approach:
    #   first create an async helper function that takes one number n and returns n * 2
    #   next loop through all the numbers in "numbers" to create a task for each one
    #   pass all of those tasks into asyncio.gather using * so they run concurrently
    #   await asyncio.gather and return the list of doubled results
    
    # TODO (Part 1, async): run one async task per number that returns n * 2, all
    #   CONCURRENTLY with asyncio.gather, and return the results as a list in the same
    #   order as `numbers`.
    async def double_one(n):
        return n * 2

    return await asyncio.gather(*(double_one(n) for n in numbers))


async def fastest(jobs):
    # Outline:
   
    # Restate:
    #   Go through a list of (label, delay) pairs, start all of the jobs at the same time
    #   so each one waits for its delay, and return the label of whichever job finishes first.

    # Example: [("A", 0.06), ("B", 0.02), ("C", 0.04)]
    #   starts all three jobs at once: "A" waits 0.06s, "B" waits 0.02s, and "C" waits 0.04s
    #   since 0.02s is the shortest delay, "B" finishes sleeping first
    #   returns "B" right away without waiting for "A" or "C"

    # Sketch the approach:
    #   first create an async helper function that takes label and delay, runs
    #   await asyncio.sleep(delay), and returns label
    #   then create a list of tasks by looping through each (label, delay) pair in "jobs"
    #   run a for loop using asyncio.as_completed on that list to get tasks as they finish
    #   inside the loop, await and return the very first finished task's label
    
    # TODO (Part 2, async): `jobs` is a list of (label, delay) pairs. Start them all
    #   concurrently - each one just does `await asyncio.sleep(delay)` - and return the
    #   label of the FIRST job to finish. (Hint: asyncio.as_completed.)
    async def run_job(label, delay):
        await asyncio.sleep(delay)
        return label

    coros = [run_job(label, delay) for label, delay in jobs]
    for finished in asyncio.as_completed(coros):
        return await finished


def echo_once(host, port, message):
    # Outline:
    
    # Restate:
    #   Open a socket connection to a server at (host, port), send a text message
    #   as bytes, wait for the server's reply, and return that reply back as a string.

    # Example: ("127.0.0.1", 50011, "hello")
    #   creates a socket and connects to "127.0.0.1" on port 50011
    #   encodes "hello" into bytes (b"hello") and sends it to the server
    #   receives "hello" in bytes from the echo server, decodes it into "hello", and returns it

    # Sketch the approach:
    #   open a socket using a with statement 
    #   so it closes automatically when done
    #   connect the socket to (host, port) using .connect()
    #   turn "message" into bytes with .encode() and send all of it using .sendall()
    #   receive the server's response bytes using .recv(1024)
    #   finally decode the reply bytes back into a string with .decode() and return it
    
    # TODO (Part 3, sockets): open a TCP socket and connect to (host, port). Send
    #   `message` (encode it to bytes first), receive the server's reply, and return it
    #   as a string. (Hint: socket.socket, .connect, .sendall, .recv, .decode.)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message.encode())
        reply = s.recv(1024)
    return reply.decode()

def main():
    # Optional scratch space - try the async parts here, e.g.:
    # print(asyncio.run(gather_doubled([1, 2, 3, 4])))   # [2, 4, 6, 8]
    print(asyncio.run(gather_doubled([1, 2, 3, 4])))   # returns [2, 4, 6, 8])
    print(asyncio.run(fastest([("A", 0.06), ("B", 0.02), ("C", 0.04)])))   # returns "B")
    print(echo_once("127.0.0.1", 50011, "hello"))  # returns "hello"   (against an echo server))
    pass


if __name__ == "__main__":
    main()
