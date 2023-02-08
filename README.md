Small tool for monitoring a system information. Starts an HTTP server and in a parallel process runs a code
that accumulates statistical information about the system in the database.
Understands two types of Get request. If the request is of the form
http://hostname/current then the current information will be returned.
If http:/hostname/stat/?time1=t1&time2=t2, then records from the database
in the "data" range between t1 and t2 will be returned if they were
previously stored there.
The current information is returned as a dictionary converted to JSON format.
Its contents may differ depending on the OS. Statistical information consists
of the same set of characteristics as information for the current moment, but
for each moment of time within the specified interval as the list.
