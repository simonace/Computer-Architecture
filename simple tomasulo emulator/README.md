# About this Tomasulo's algorithm Emulator

### This simple emulator written in Python implements Tomasulo's algorithm widely used to achieve dynamic scheduling and register renaming in modern processors. This simple emulator is based on the following microarchitecture settings/assumptions:

* Only two operation with different execution delays, which are sufficient to show the algorithm's ability to schedule operations dynamically
* One operation to issue in one cycle
* Unlimited reservation station, making sure one operation must be issued into the reservation in one cycle
* Tracking/encoding the operations in reservation stations and register status with unique operation name for every issued operation rather than the encoding of the reservation station the operation resides(since we have unlimited reservation stations, there is no encoding for the reservation station)
* Only 7 GPRs(r1-r7)

### The code sequence to run must be put into the file *code.txt*, the assembly-like code inside is in such format:
***OP DST,SRC1,SRC2***

(**OP**: *add* or *mul*,  **DST**, **SRC1**, **SRC2**: *r\[1-7\]*)

A golden result for the final register file values will be calculated by the program as well to check with the result done by Tomasulo's algorithm.
