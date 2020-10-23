__author__ = 'kashimka'

from flask import Flask
from flask import render_template
import subprocess
import telnetlib
import urllib

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }

app = Flask(__name__)

def top_menu():
    pass

def call_proc(cmd):
    output = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    return output

def filter_output(output, host):
    o_filter = ""
    for line in output.stdout.decode('cp866'):
        o_filter = o_filter+line
    return_data = str(host) + " " +  o_filter
    return return_data

@app.route('/')
def index():
    return render_template('center.html', return_data='Home Page')

@app.route('/ping/')
@app.route('/ping/<host>')
@app.route('/pong/<host>', alias=True)
def ping(host=None):
    if host is None:
        return render_template('center.html')
    else:
        cmd = "ping " + str(host)
        output = call_proc(cmd)
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)

@app.route('/tracert/')
@app.route('/traceroute/')
@app.route('/traceroute/<host>')
@app.route('/tracert/<host>', alias=True)
def traceroute(host=None):
    if host is None:
        return render_template('center.html')
    else:
        cmd = "tracert " + str(host)
        output = call_proc(cmd)
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)


@app.route('/dns-lookup/')
@app.route('/lookup/')
@app.route('/dns-lookup/<host>')
@app.route('/lookup/<host>', alias=True)
def dns_lookup(host=None):
    if host is None:
        return render_template('center.html')
    else:
        cmd = "nslookup " +str(host) + " 8.8.8.8"
        output = call_proc(cmd)
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)

@app.route('/whois/')
@app.route('/whois/<host>')
def whois(host=None):
    if host is None:
        return render_template('center.html')
    else:
        cmd = "whois " + str(host)
        output = call_proc(cmd)
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)


@app.route('/nmap/')
@app.route('/nmap/<host>')
def nmap(host=None):
    if host is None:
        return render_template('center.html')
    else:
        cmd = "nmap -v -A -T4" + str(host)
        output = call_proc(cmd)
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)

@app.route('/port-check/')
@app.route('/port-check/<host>/<int:port>')
def port_check(host=None, port=None):
    if host is None:
        render_template('center.html')
    else:
        ''' TODO: Less precise telnet test, maybe a nmap like just to see if the port is opened or closed '''
        if port == "":
            port = 23

        tn = telnetlib.Telnet(host,port, 5)
        if tn.open(host,port, 5):
            return_data = filter_output(output, host)
            tn.close()
        else:
            return_data = filter_output(output, host)
        return return_data

''' TODO: Find a better way to handle errors, since web provides more errors and seems to much work to config all ( or almost all ) '''

@app.errorhandler(403)
def forbidden():
    return render_template('center.html', return_data='Can\'t do that!' )

@app.errorhandler(404)
def page_not_found():
    return render_template('center.html', return_data='Nothing found here!')

@app.errorhandler(500)
def internal_server():
    return render_template('center.html', return_data='Something smells strange!')

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0',port=8090)