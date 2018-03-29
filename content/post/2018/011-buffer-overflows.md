---
draft: true
title: "Ethical Hacking - Buffer Overflow - notes"
slug: "ethical-hackin-buffer-iverflow"
date: "2018-03-20T19:20:10+01:00"
categories:
  - security
  - learning
tags:
  - notes
  - security
  - hacking
  - pentesting
cover:
  image: /img/2018/004/ethical-hacking-wikimedia.jpg
  style: normal
---


# Stack pointers

Types of stack pointers:

* SP → Stack Pointer
    * keeps track where the next element will be pushe to or poppef off of the stack
* FP → Frame Pointer
    * points to the beginning of the stack frame for the current function call
    * used to easily find inf. associated with the fucntion being executed
* BP → Base Pointer (different name for FP)
* IP → Instruction Pointer
    * points to the location in the memory that contains next machine language
        instruction that is to be executed by the CPU. It steps through the
        program code in an incremental fashion. Causing one instruction to be
        executed at a time.
* Instruction Counter or Program Counter
    * it points to the code segment of process memory, and usually steps
        through the program code sequentially. One instruction at a time.
        Yet, when the it's set to a non-sequential memory address, then we a
        `jump` happens (caused by conditional branching, e.g.: if-else, etc.).
        For a function call to return, the IP is set to the return address of
        the funciton stack frame. This address is the location of the code 
        segment that follows the function call in the previously called
        function. 
        The key to advanced buffer overflow techninuqes is the manipulation of
        the IP. When you can set the value of the IP, then you can control what
        program instructions are executed by the CPU. And those instructions 
        don't have to be in the program code segment!
* Registers → are dedicated areas of CPU memory

# What can you do with a buffer overflow condition?

* Access memory-resident resources
* Run installed programs
* Inject and run exploit code on the computer
* Cause program instability and abormal termination

`Arbitrary code execution` -> is a condition when any executable ecode that is
injected into a program's buffer causes the buffer to overflow and forces the
program to run the injected code.


# Stages of BoF

1. Inject `exploit code` into a program's input buffer (IP) with a buffer
   overflow vulnerability. This will place the exploit's code on the program's
   stack or heap, depending on whether the program's input buffer is in the
   memory.
2. Assuming the buffer in on the program's stack, the code injection overwrites
   some or all of the stack frame of the funciton that reads the input data.
   The critical part of this overwrite is to position of the memory address in
   the beginning of exploit code in the stack to overwrite the return address
   located in the stack frame. By overwriting the return address the attacker
   can control what code instruction is executed next by the CPU.
3. When the function returns, the IP is loaded with the memory address of the
   injected code, causing the CPU to execute the exploit code.


**Predictability is the key!**

Arbitrary code exploits need a predictable execution environment, where the
memory location of needed objects is known or discoverable. 
This is usually possible due to system resources being mapped into the process'
virtual memory spaces in a predictlable way (things like ALSR can prevent
intruders from accessing such resources easily).
So this means that all processes have the same resources at the same virtual
memory locations, e.g:
* `0x7C86250D` → `kernel32.dll.WinExec()`
* `0x7C801D7B` → `kernel32.dll.LoadLibraryA()`
* `0x7C802336` → `kernel32.dll.CreateProcesW()`
* `0x7C80236B` → `kernel32.dll.CreateProcesA()`
Exploit code needs these system resources to properly run


# Egghunting

Is a technique of placing at the beginning of the exploit code an identifiable
sequence of bytes referred to as an `egg` and searching the memory for the 
location of the `egg`. For this reason the bytes used in the `egg` must be
unique enough so that it can be easily distinguished from the rest of the
process memory.  
The first intruction on the exploit code is placed immediately after the `egg`.
Search code must me pre-loaded onto the process memory in a place where it can
be easily started. Usually it's so small that it can be started from the 
buffer in the stack and the actual exploit payload containing the `egg` might 
be injected using an overflow in the heap memory.


# No Operation (NOP or NO-OP)

`NOP` is a CPU controll operation and it tell it to do notning except adnvance
the IP to the next instruction. NOP consumes one CPU cycle.  
On a 1 GHz CPU `NOP` take 1 nano second.  


# NOP Sled

NOP Sled:
* Set the `IP` to the address of the begnning of the exploit code
    * this is not always easy or possible
* The `IP` only neds to point to any place on the `OP Sled`
* The `IP` will then move down to and execute the exploit code
* a `NOP Sled` is a sequence of `NOP` intructions preceding the payload, making 
    the paylod easier to find
* The larger the Sled the more likely it'll be hit by IP.
* are easily detectable
* Psuedo-NOP Sleds (a long list of nonsensical CPU instruction) are not 
    (easily) detectable as they appear to be legit code.


# Shellcode

* creates an interaction OS shell
* executes commands on the local system via command line, script, or batch file
* can be any type of program that works as i.e. server (ssh, ftp, etc.), 
    monitor (sniffer, keylogger etc.)
* runs with the priviliges and context the process that runs it

**Shellcode types:**
* port binding (opens a port of the attacked machine)
* reverse (opens a network connection to the attacker's host)
* command executiion code
* file transfer
* find socket
* kernel space
* multistage
* process injection
* system call proxy

**Creating shellcode:**
1. write the shellcode in assembly (CPU specific) languange
2. assemble & link the assembly code to create machine code (compile)
3. convert the machine code to an escaped-byte text format

```cpp
unsigned char shellcode[] = "\xe9\x1e\x00\x00\x00\xb8\x04\x00\x00\x00\xbb\x01\x00\x00\x00\x59\xba\x0f\x00\x00\x00\xcd\x80\xb8\x01\x00\x00\x00\xbb\x00\x00\x00\x00\xcd\x80\xe8\xdd\xff\xff\xff\x48\x65\x6c\x6c\x6f\x2c\x20\x57\x6f\x72\x6c\x64\x21\x0d\x0a\x0";

int main()
{
    void (*func)();
    func = (void (*)())shellcode;
    (*func)();
}
```

Then compile the `C` program:
```shell
gcc -g -Wall -fno-stack-protector -z execstack shelltest.c -o shelltest
```

when executed, the `shelltest` will print `Hello, World!` :)
```
$ ./shelltest 
Hello, World!
```


# The Heap

* Heap stores program data
* The stack is fixed in size, but the heap can grop and shrink as needed
* It's a dynamic memory
    * allocates and releases storage space as the process needs
    * user to temporarily store data for processing

```
     _____________
     |   STACK   |
     |___________|
     |   HEAP    |
     |___________|
     |   DATA    |
     |___________|
     |   CODE    |
     |___________|
Process Address Space
```

## Structure of the heap

* process memory is filled with memory management structures called `chunks`
* `chunk` is a fixed size area of the process memory (e.g. 8 bytes in length)
    and proceeded by a chunk header.
* when a process allocates an area of memory from the heap called a `block`
    then one or more chunks are reserved to create a requested `block` of 
    heap memory
* the memory address of the beginning of the `block` is returned to the process
    so it may write & readdata to/from it and release the blocks of memory back
    to the heap when they're not longer needed. So that they can be
    re-allocated.

### Heap Chunk Header

Contains things like:
* type of chunk
* size
* memory address of previous chunk
* memory address of next chunk

The `Heap` contains a one long linked chain of `chunks`. The chaining is
necessary so that 
0206
