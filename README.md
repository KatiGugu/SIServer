The tool for remote monitoring of some system information. Server system information runs two parallel threads. In the first thread, system information is collected and stored in the database at a specified frequency. The second thread is an http server that returns either the current system data or the data for the specified period, if they are in the database.
The Http server accepts two types of Get requests:

http://HostName:Port/current
The current system data will be returned.
and

http://HostName:Port/stat?time1={time interval start}&time2={time interval finish}
The data accumulated in the database for the specified time interval will be returned.

System information includes: RAM usage, disk space usage and network information (packets sent/received)

