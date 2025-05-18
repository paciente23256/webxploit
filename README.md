# webxploit 2.0

<a target="_blank" href="https://en.wikipedia.org/wiki/Python_(programming_language)">
<img src="https://img.shields.io/static/v1?label=python&message=3.10%20|%203.11&color=informational&logo=python"/>
</a>

**Auto Web Exploit Framework with Metasploit**


**step 1:** Download and Setup metasploit. 
        
        curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod 755 msfinstall && ./msfinstall

**step 2:** Download and run Webxploit. 

    git clone https://github.com/paciente23256/webxploit.git
    cd webxploit
    python3 webxploit.py -h

<p></p>

<img src="https://i.imgur.com/6PxKnKz.png" alt="Webxploit CLI" width="70%" height="70%">


**Web Interface**

    python3 app.py

    open your browser http://localhost:5000

<img src="https://i.imgur.com/7RWeJM1.png" alt="Webxploit Dashboard" width="50%" height="50%">


**You can follow the development of the scan (in verbose mode), in the console where you ran the flask server. At the end of the scan, you will see the results in various formats (Log, PDF, HTML, JSON) on the web interface.**
