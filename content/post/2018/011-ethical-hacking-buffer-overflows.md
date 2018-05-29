---
draft: false
title: "Ethical Hacking - Buffer Overflow - notes"
slug: "ethical-hackin-buffer-iverflow"
date: "2018-03-20T19:20:10+01:00"
categories:
  - security
  - learning
tags:
  - notes
  - security
  - ethical hacking
  - pentesting
  - BoF
cover:
  image: /img/2018/004/ethical-hacking-wikimedia.jpg
  caption: "Source: [wikimedia.org](https://commons.wikimedia.org/wiki/File:Ethical-hacking.jpg)"
  style: normal
---

These are just my notes from the Pluralsight course: "Ethical Hacking: Buffer 
Overflows" by James Murray.


# Stack pointers

Types of stack pointers:

* `SP` → `Stack Pointer`
    * keeps track where the next element will be pushe to or poppef off of the stack
* `FP` → `Frame Pointer`
    * points to the beginning of the stack frame for the current function call
    * used to easily find inf. associated with the fucntion being executed
* `BP` → Base Pointer (different name for FP)
* `IP` → `Instruction Pointer`
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
* `Registers` → are dedicated areas of CPU memory

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

Example `c` program with a shellcode that print out "Hello, World!":

```c
unsigned char shellcode[] = "\xe9\x1e\x00\x00\x00\xb8\x04\x00\x00\x00\xbb\x01\x00\x00\x00\x59\xba\x0f\x00\x00\x00\xcd\x80\xb8\x01\x00\x00\x00\xbb\x00\x00\x00\x00\xcd\x80\xe8\xdd\xff\xff\xff\x48\x65\x6c\x6c\x6f\x2c\x20\x57\x6f\x72\x6c\x64\x21\x0d\x0a\x0";

int main()
{
    void (*func)();
    func = (void (*)())shellcode;
    (*func)();
}
```

Compile the `C` program:
```shell
gcc -g -Wall -fno-stack-protector -z execstack shelltest.c -o shelltest
```

when executed, the `shelltest` will print `Hello, World!` :)
```shell
$ ./shelltest 
Hello, World!
```


# The Heap

* Heap stores program data
* The stack is fixed in size, but the heap can grop and shrink as needed
* It's a dynamic memory
    * allocates and releases storage space as the process needs
    * user to temporarily store data for processing

```ascii
     +-----------+
     |   STACK   |
     |___________|
     |   HEAP    |
     |___________|
     |   DATA    |
     |___________|
     |   CODE    |
     +-----------+
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
necessary for the heap memory manager to step through each chunk checking if
its is allocated to a block of heap memory or not. The linkage allows blocks to 
be constructed of chunks that are not adjacent to each other in heap memory.
The heap memory can store chunks anywhehe in the memory.  

*TIP:*  
The pointers should be set to zero after the memory allocated on heap got
released.


# Exploiting Heap Overflows

* Buffers on the heap can be overflowed (same as stack buffers)
* Heap overflows can change the memory addresses stored in pointer variables,
    this can lead to:
    * redirection of the flow of program execution
    * calling the process exception handler
    * crashing the running process
* Code stored in the heap can be executed just like the one on the stack
    * this can be done by redirecting the `IP` to the code present in heap 
    * the trick is to gain accesss to heap buffer large enough to hold the
        entire exploit code and finding memory location before the first
        instruction of the code.
        * One of the techniques is to make "fake" heap chunk headers (memory 
            management structures) that actually replace the 
* prior to exploiting the BoF we need to know where the buffer is allocated.
    whether it's allocated on the `stack` or the `heap`.
* this can be established by looking at the source code or doing static/dynamic
    code analysis.
* Heap buffers are used when:
    * very large data must be stored
    * the buffer must exist for a long time
    * the size of the buffer needs to change
    * the size of the buffer is only know at run-time

Example heap overflow `c` code:
```c
int mai (in argc, char *argv[])
{
    char *buffer = (char*)malloc(16);
    strcpy(buffer, argv[1]);  // strcpy copies the string without checking how
    free(buffer);             // long the string is or even if it exists
}
```


# Heap Spray

A technique is used to make it easier to locate & execute exploit code written
(overflowed into memory) to a heap buffer.  
`Heap spray` fill the process heap with identical blocks of NOP sleds and 
exploit clode.
The paylod is executed by triggering a `BoF` vulnerability in the stack that
overwrites the function's return address with the memory location in the heap.  
When the function returns the `IP` will be directed to the overflowed memory of
the address in the heap. The `IP` will then incrementally move down the `NOP`
sled and execute the exploit code.  
`Heap spray` relieves the need to understand the structure of the `Heap` around
vulnerable buffer. It's a brute force technique that can be very effective.


## Function Pointers

* is a variable that stores the location of a function
* functions are usually called by name directly in the promogram's code
* but sometimes due to issues in the program's design, the programmer won't 
    know which function will be called ahead of time. 
* in such situation we can call a function by its memory address rather than by
    its name
* this allows to decide which function to call while a program is running
* and we don't have to hardcode the function name when the software is written

Example of a `Function poitner` (aka function callback)
```c
int function_callback(int param1)
{
    return param1;
}

int main()
{
    int (*callbackfunc)(int);
    callbackfunc = (int (*)())function_callback; // name of this var doesn't
                                                 // have to be same as the 
                                                 // called function
    int result = (*callbackfunc)(55);
}
```

The example above depicts that a function can be called using a memory pointer
rather than the name of the function itself.

# Other Exploitable items

Apart from Heap or Stack other items, like the ones listed below, can be 
exploited:

* Object pointers
* Virtual function tables
* Structured exception handlers (Windows OS)


## Structured Exception Handling (SEH)

`SEH` It's a Windows OS error recovery feature use to handle exceptional conditions
that might occure during the runtime.   
It might be caused by:

* hardware errors (i.e. attempts to illegally access protected memory location)
* software errors (i.e. write to read-only file)

`SEH`:

* notify of the occurence of error condition
* allows process to handle errors rather than crashing

Programs that use `__try, __except, __leave, __finally` clauses and 
`RaiseException` are explitely using `SEH`.  
If you don't use them in your programs, then `SEH` on Windows will handle
unhandled exceptions implicitely as it's present in every process.


### SEH in the Stack

The control structure used by the `SEH` is present in the stack of each thread
in the process.  
In Windows every `Stack Frame` contains a block of `SEH` information. Inside
that block there's tuple list of memory addresses called `expeption registration
records` (`ERR`).  
There's one record for each exception handler registered for the use in
function. Each record contains a memory address that points to the next record
in the list (linked list). Second memory address points to the code in the 
exception handler that is used to handle the specific exceptinal condition.  
If the function does not use `SEH` explicitely (`try - except` clause) only the
`Exception Registration Record` for the default exception handler will be 
present in the `SEH` block in the function stack frame.


## Exploiting SEH

**CodeRed's `SEH` Exploit**:
was a BoF exploit in Microsoft Index Server used by IIS written in 2001.


```html
GET/default.ida?NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN%u9090%u6858%ucb
d3%u7801%u9090%u6858%ucbd3%u7801%u9090%u6858%ucbd3%u7801%u9090%u
9090%u8190%u00c3%u0003%u8b00%u531b%u53ff%u0078%u0000%u00=a HTTP/1.0
```

* Long string of `Ns` is used to position the exploit code within the stack to
    overwrite the instruction pointer and call a function in the system
    library. 
* That call redirects back to the stack and runs the exploit code in the buffer
    (the part encoded seen as the percent encode unicode characters) 
* all of this was possible because a component from the Indexing Service did
    not perform input data validation.
* what was overwritten by the injected exploit code was the `SEH` exception
    registration records in the Index Server stack.
* Triggering exeption casused Windows to execute exploit code in the stack
    pointed to by the overwritten `SEH` record.


**NOTES:**

* http://resources.infosecinstitute.com/intro-to-fuzzing/ 
* "All input is eveil until proven otherwise" - Michael Howard, "Writing Secure
    Code"


# Mitigating BoF

In information security nomenclature, `mitigation` refers to act of reducing
the potential harmful effect of a threat. Whereas `remediation` or `disaster
recovery` is about recovering from the effects of a threat and restoring normal
operation.


**BoF - typical plans of attack:**

* Input field
* API
* Malware / Email Attachments
* Malicious insider


**BoF attack payoff:**

* Reconnaissance and surveillance of system and network operations
* Privilege escalation for the attacker
* Creation of unauthorized, privileged user accounts
* Command and control of the local system
* Multiple systems compromised and open to remote access
* Alteration, exfiltration, or destruction of critical information
* Temporary or permanent disablement of the system


**Mitigating potential BoF:**

* `BoF` vulnerabilities are easy for programmers to accidentally create
* Posiible losses due to BoF exploitation
    * System penetration and privilege escalation
    * Data alteration, exfiltration, or destruction
    * System instability and denial of service
* Active and passive mitigation
    * Active mitigation relies on detecting buffer overflow conditions
    * Passive mitiation does not rely on detection of a threat


**BoF safeguards:**

* *Safegyueards* are proactive security controls that attempt to prevent a
    threat from causing harm
* Kernel and firmware anti-BoF features
    * `DEP` - Data Execution Prevention
    * `ASLR` - Address Space Layout Randomization
    * `KASLR` - Kernel Address Space Layout Randomization
* OS and kernel security configurations
    * `EMET` - Enhanced Mitigation Experience Toolkit
* Unistall unneeded programs
* Patch all installed programs


**BoF Contermeasures:**

* *Countermeasures* are reactive security controls that attempt to mitigate the
    harm caused by an active threat
* Host-based security monitoring software: Firewalls, anti-Malware software
* Network monitoring tools: fireawall, proxies, `IDS`/`IDP`
* *Countermeasures* cannot prevent all possible loss from a threat


# Detecting BoF


**Extenal BoF Detection:**

* e.g detect BoF exploit patterns in data payload sent to web server
* `NIDS` → Network Intrustion Detection Systems
    * `NIDS` can be placed inline or in-band with the network trafiic.
        (They analyse the network traffic that passed through firewalls)
    * `NIDS` can also be placed out-of-band, where the firewall sends a copy of
        the network traffic to the `NIDS` for the inspection and reporting.
    * `NIDS` should never interfere with the flow of the network traffic
    * [SNORT](www.snort.org) is an `NIDS` that incorporates signatures into 
        the rules it uses to detect and react to attack traffic
    * If a `NIDS` detects a potential attack then it notifies `SIEM` [Security
        Information Event Management] system, like [splunk>](www.splunk.com)

**Local BoF Detection:**

* should happen on the host behind firewall and` NIDS`
* anti-virus should check:
    * files
    * email attachments
* anti-malware solutions should:
    * scan email & IM
    * look for suspicious program behaviour
    * malware running in memory
* [ClamAV](www.clamav.net) → is a freee AV for variours OSes, that can detect
    potential BoF tools and possible attacks.


**Host-based Intrusion Detection Systems (IDS):**

* HIDS are a hybrid of multiple security systems, like:
* network firewall
* web browser site & content filtering
* detect unusual or threating system behaviour
* system file changes monitoring
* periperal device monitoring
* application montoring
* [OSSEC](ossec.github.io) is a good open-source HIDS tool for many OSes


**System Event logs:**

* do you know where your system's events are logged?
* do you occasionally review those logs?
* backup your logs and secure them against alteration
* don't rely on unreliable UDP syslog protocol


# DEP - Data Execution Prevention

* `DEP` - flags a memory page as non-executable (containing just data)
* it sets the `NX` bit to true, which designates a non-executable memory page
* if a process tries to execute code in DEP-protected memory page then an
    exception is thrown and the process is terminated.
* it's a handy feature do combat stack & heap BoF 
* `DEP` is a hardware & software feature
    * Intel calls is `XD` bit (eXecuted Disabled) & `EDB` (Execute Disable Bit)
    * in IBM ARM CPUs it's called `XN` bit (eXecute Never)
    * AMD64 CPUs → `NX` bit (No eXecute) and Enhanced Virus Protection
* `DEP` can usually be toggled in `BIOS`
* Software `DEP` is supported:
    * since Windows XP SP2, Windows Server 2003 SP1
    * OS X 10.4.4 (Tiger), 10.5 (Leopard), 10.7 (Lion)
    * by Linux, UNIX - PaX (Linux), Exec Shield (Red Hat Linux), W^X (OpenBSD)
* Even if hardware DEP is not available, software counterpart can still provide
    some protection


**Defeating DEP:**

* `DEP` can be defeated by anything with administrator (root) privileges
* Most of the time attack will disable DEP only for few processes, which is
    enoug to perform it
* Prevent access to admin/root accounts
    * use complex passwords/phrases
    * 2FA
    * limit number of people with admin privileges
* Mitigate privilege escalation vulnerabilities
    * Remove unnecessary programs
    * patch & update OS/programs regularly
    * Audit system and access logs


## Set DEP in Windows 7/8/10 CLI

```shell
C:\> bcdedit.exe /set {current} nx OptIn  # default value
C:\> bcdedit.exe /set {current} nx OptOut # enable DEP for whole OS, all
                                          # processes (including kernel &
                                          # drivers)
C:\> bcdedit.exe /set {current} nx AlwaysOn  # same as OptOut but applies to
                                             # all running processes and all 
                                             # attempts to disable it on any 
                                             # executable will be ignored
C:\> bcdedit.exe /set {current} nx AlwaysOff # disable DEP and ignore attempts
                                             # to enable it for any executable
C:\> bcdedit.exe /enum                    # check current DEP setting
```

**NOTES:**

* any changes made via `bcdedit` will take effect after next reboot.
* `MS` provides a GUI app called `EMET` (Enhanced Mitigation Experience Toolkit) 
    to manage DEP settings


## Set DEP in Linux

To check is DEP is enabled or disable run:
```shell
# dmesg | grep NX
```

To disable software DEP emulation you'll need to set `noexec` & `noexec32` 
flags in Grub's `GRUB_CMDLINE_LINUX_DEFAULT`, e.g.:

```shell
# vim /etc/default/grub

GRUB_CMDLINE_LINUX_DEFAULT="quiet noexec noexec32"
```

To set DEP per executable file:

```shell
# execstack -s myprogram  # set the DEP bit
# execstack -1 myprogram  # check the DEP bit value
# execstack -c myprogram  # turn off DEP
```


# ASLR - Address Space Layout Randomization

`ASLR` technique randomizes the position of the stack, heap and system
resources in process memory. It makes for a BoF exploits to both find system 
resources and process memory and execute the exploit code it injects by
removing predictability from the process environment that most explots depends
on.  
`ASLR` also changes the location and the beginning of the process heap in the 
memory. By changing the heap addrress to an unpredictable random base memory 
address, the explot code won't be able to rely on predictable fixed memory 
location.  
`ASLR` Stack randomization works in the same way as above.


`ALSR` can be easily enabled with `EMET` on Windows Vista, 7, 8, 10 & Server 
2008 and later.

On `Linux` you can check it like this:
```shell
# sysctl -a | grep "kernel.randomize_va_space"
kernel.randomize_va_space = 2
```

To disable it, you'll need to change that value to `0`
```shell
# sysctl -w kernel.randomize_va_space=0
```
This change is only in memory, and will go back to `2` after the reboot.

To disable it permanently you'll need to edit `/etc/sysctl.conf`
```shell
# vim /etc/sysctl.conf 

kernel.randomize_va_space = 0

# then reload that file with
# sysctl -p

# to disable ALSR for only that shell instance
# setarch `uname -m` -R /bin/bash
```


## Defeating ASLR

* ASLR renadomization occurs only at system startup
* identical randomized location applied to all process
* Know the memory location for one process and you know for them all
* Randomly chosen from a fixed set of memory locations
    * 0x1234**56**78
    * Creating `256` possible locations (0x1234**00**78 to 0x1234**FF**78)
    * Some exploit code can simply try each possible location until successful


### Missing ASLR

* ASLR is not supported by OSes older than listed below:
    * Linux (2001)
    * OpenBSD UNIX (2003)
    * Vista (Jan 2007)
    * OS X 10.5 (Leopard, Oct 2007)
    * iOS 4.3 (March 2011)
    * Android 4.0.3 (Ice Cream Sandwich, Dec 2011)


# KASLR - Kernel Address Space Layout Randomization

* Randomizes were objects are placed in kernel memory
* First added to Linux kernel in 2005 (v`2.6.12`)
* Full `KASLR` support added to Linux kernel in 20014 (v`3.14`)
* Windows Vista (Jan 2007)
* Object locations are randomized at boot time (and don't change until next
    boot)
* Memory locations discovered by brute force or memory leaks
* `KASLR` can be disabled by default (Linux especially)


# SEHOP

* Structured Exception Handling Overwripte Protection
* added to Windows to detect illicit changes in the SEH control structure
* Both `SEH` and `SEHOP` are present in all Windows processes
* `SEHOP` is controlled per process using `EMET`


## SEHOP in action

* `SEH` information is added to each stack frame
* `SEHOP` works when an exception is thrown by validating that pointers in the
    record chains are correct.
* If the linking points are correct the proper exheption handler is executed.
* If a `stack overflow` has occured the address of exception handler may have
    been replaced with memory location of some exploit code and if such
    exception is thrown the exploit code will be executed. `SEHOP` will
    validate the record chain and discover the corruption. When this happens
    the process will be terminated before exploit code can be executed.
* `SEHOP` is enabled by default on Windows.
* To check it's status you'll need to use `regedit`
* `HKEY_LOCAL_MACHINE/SYSTEM/CurrentCotrolSet/kernel/DisableExceptionChainValidation`
* you can also use `EMET`


### /SAFESEH - a Visual Studio C/C++ feature

* `/SAFESEH` is a security feature in Visual Studio C/C++
* it's an alternative protection mechanism to SEHOP
* it relocates the `SEH` block to a safe memory location outside the program
    stack
* it's enabled by default
* all modules in a program must be compiled using `/SAFESEH` flag
* it can be disabled with `/SAFESEH:NO`
* `/SAFESEH` works only with 32-bit programs

