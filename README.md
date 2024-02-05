## How to run the program: 

NOTE: tested on mac
- Set up a conda environment that has the following libraries installed: `grpcio`, `grpcio-tools` (full list of libraries installed in conda env can be found in requirements.txt)
- Open 2 terminal windows
- run the server from one window and the client from the other:
- Server usage: ```python zkp_auth_server.py```
- Client usage: 
```python zkp_auth_client.py <action>``` where ``` action: 'register'/'reg' or 'authenticate'/'auth'```


## Thought process:

When initially presented with the assignment, I read through it and the Chaum–Pedersen Protocol description several times before diving in. I was familiar with the concept of zero knowledge proofs, but was less familiar with how such protocols function when implemented. I therefore began by studying zero knowledge proof protocols and commitments.

After this, I moved on to learning about gRPC, which I did not know anything about. I began by reading documentation and working through the tutorials on their website. Through working with the framework via tutorials and becoming familiar with gRPC concepts, I was able to create my own gRPC client server setup. I started with the proto file provided, generated the protocol buffer files, and then moved onto my client and server implementations.

Once I had figured out gRPC and had the initial structure in place, I needed to determine the values for `g`, `h`, `x`, `k`, `c`, and `q`. To do so, I moved onto a more in depth study of the Chaum Pedersen protocol. After examining the provided diagram of the protocol, I noticed I could figure out all variable values except for `q`. For this, I focused on the following sentence from the book: “We assume that `g` and `h` generate groups of prime order `q`, and we denote the common discrete logarithm by `x` ease notation.” From this, I learned about various abstract algebra concepts including groups, generators, cyclic groups, prime order, and safe primes. `q` must be chosen from a cyclic group. One such cyclic group is the multiplicative group modulo prime, meaning the group operation is multiplication mod `p`, where `p` is a safe prime (which means `(p-1)/2` is also a prime number). Namely, `(p-1)/2` is `q`. `g` and `h` can be any two values in the group. `x` is the user's "password" and therefore random; `x` is the secret that the client is proving they know without revealing its value to the server. `k` and `c` are chosen randomly.

After I got the math working, I began the process of code cleanup and documentation. During this process as I continued to manually test the code, I determined there is a programmatic error that causes authentication to succeed and fail nondeterministically when running authentication for the same user repeatedly. I suspect this could be an error in the way I'm selecting `p`, but I'm still working through determining the cause of the bug.

As extensions to my system, I would like to add a test suite for unit and integration tests using pytest. Ideally I would have set this system up while I was implementing the client and server so that I could have added tests I was performing manually and to verify changes I made didn’t break previously functioning code as I went.
