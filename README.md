# lichess-dgt

This is a prototype for a Python3 application to support the use of a DGT E-Board on the
lichess.org chess website. 

Although I have just found another project (wriiten in Javascript!) that does something similar,
the code is really hard to read and so I am continuing with this project for now.

This project is currently using twisted (https://twistedmatrix.org) to achieve a seamless
flow of data both from the lichess.org website and from the board itself. 

The DGT Board is (for now) being driven using the DGT Posix driver (written in 'C') with
a simple Python shim. In future this could be replaced with a native Python driver. 
The current implementation actually uses a thread to comminicate with the board itself, but
then creates a unix domain socket (half of which is returned from the Init() method) onto
which actual board change messages are published.      
 