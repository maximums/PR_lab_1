# Laborator 1
### Author: Dodi Cristian - Dumitru
#### Group: FAF - 181
## Tasks:
1. Pull a docker container (alexburlacu/pr-server) from the registry.
2. Run it on the port 5000.
3. Access the root route of the server and find a way to __/register__.
4. Put the access token from the __/register__ route in a HTTP header of the subsequent requests under the key __X-Access-Token__.
5. Extract data from routes and get links to the next ones in max 20 sec(access token timeout).
6. Convert all data to a common representation.
7. Make a concurrent TCP server, serving the fetched content, that will respond to (mandatory) a column selector message, like __selectColumn column_name__, or __selectFromColumn column_name glob_pattern__.

### Connection to TCP:<br>
![Output](https://github.com/maximums/TMPS/blob/master/img/output.png)
<br>

### TCP input and output:
![Output](https://github.com/maximums/TMPS/blob/master/img/output.png)
<br>

![Output](https://github.com/maximums/TMPS/blob/master/img/output.png)
<br>

![Output](https://github.com/maximums/TMPS/blob/master/img/output.png)



