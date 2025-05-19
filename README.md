# webxploit 2.0
<p></p>
<a target="_blank" href="https://en.wikipedia.org/wiki/Python_(programming_language)">
<img src="https://img.shields.io/static/v1?label=python&message=3.10%20|%203.11&color=informational&logo=python"/>
</a>
<p></p>

**Auto Web Exploit Framework with Metasploit**
<p></p>
<p></p>
**Requirements:**

**a:** If you are using Kali distro.

        sudo apt install metasploit-framework
        
**b:** Download and Setup metasploit in other Linux distro. 
        
        curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod 755 msfinstall && ./msfinstall

You can get more information about the framework here : https://www.offsec.com/metasploit-unleashed


**SETUP and USE:**

**CLI Mode:** Download and run Webxploit in CLI. 

    sudo git clone https://github.com/paciente23256/webxploit.git
    cd webxploit
    sudo pip install -r requirements.txt
    
    sudo python3 webxploit.py -h

<p></p>

<img src="https://i.imgur.com/6PxKnKz.png" alt="Webxploit CLI" width="70%" height="70%">


**Web Interface Mode**

After clone the repository:

    cd webxploit/
    sudo python3 app.py

Then open in your browser: http://localhost:5000

<img src="https://i.imgur.com/7RWeJM1.png" alt="Webxploit Dashboard" width="50%" height="50%">


**You can follow the development of the scan (in verbose mode), in the console where you ran the flask server. At the end of the scan, you will see the results in various formats (Log, PDF, HTML, JSON) on the web interface.**

**Metasploit Modules in use:**


    "auxiliary/scanner/http/cert",
    "auxiliary/scanner/http/dir_listing",
    "auxiliary/scanner/http/dir_scanner",
    "auxiliary/scanner/http/dir_webdav_unicode_bypass",
    "auxiliary/scanner/http/enum_wayback",
    "auxiliary/scanner/http/files_dir",
    "auxiliary/scanner/http/http_login",
    "auxiliary/scanner/http/open_proxy",
    "auxiliary/scanner/http/options",
    "auxiliary/scanner/http/robots_txt",
    "auxiliary/scanner/http/ssl_version",
    "auxiliary/scanner/http/ssl",
    "auxiliary/scanner/http/http_version",
    "auxiliary/scanner/http/webdav_website_content",
    "auxiliary/fuzzers/http/http_form_field",
    "auxiliary/scanner/http/backup_file",
    "auxiliary/scanner/http/wordpress_login_enum",
    "auxiliary/scanner/http/verb_auth_bypass",
    "auxiliary/scanner/http/cgit_traversal",
    "auxiliary/scanner/http/crawler",
    "auxiliary/scanner/http/host_header_injection",
    "auxiliary/scanner/http/http_header",
    "auxiliary/scanner/http/http_hsts",
    "auxiliary/scanner/http/http_put",
    "auxiliary/scanner/http/http_traversal",
    "auxiliary/scanner/http/iis_internal_ip",
    "auxiliary/scanner/http/jboss_vulnscan",
    "auxiliary/scanner/http/log4shell_scanner",
    "auxiliary/scanner/http/lucky_punch",
    "auxiliary/scanner/http/mod_negotiation_scanner",
    "auxiliary/scanner/http/ms09_020_webdav_unicode_bypass",
    "auxiliary/scanner/http/svn_scanner",
    "auxiliary/scanner/http/tomcat_enum",
    "auxiliary/scanner/http/trace_axd",
    "auxiliary/scanner/http/trace",
    "auxiliary/scanner/http/vhost_scanner",
    "auxiliary/scanner/http/webdav_scanner",
    "auxiliary/scanner/http/xpath",
    "auxiliary/scanner/http/adobe_xml_inject",
    "auxiliary/scanner/http/apache_mod_cgi_bash_env",
    "auxiliary/scanner/http/apache_normalize_path",
    "auxiliary/scanner/http/apache_userdir_enum",
    "auxiliary/admin/http/iis_auth_bypass",
    "auxiliary/admin/http/jboss_bshdeployer",
    "auxiliary/admin/http/tomcat_utf8_traversal",
    "auxiliary/admin/http/tomcat_ghostcat",
    "auxiliary/dos/http/apache_commons_fileupload_dos",
    "auxiliary/dos/http/apache_mod_isapi",
    "exploits/multi/http/phpfilemanager_rce",
    "exploits/multi/http/php_fpm_rce",
    "exploits/multi/http/php_cgi_arg_injection",
    "exploits/multi/http/stunshell_exec",
    "exploits/multi/http/tomcat_jsp_upload_bypass",
    "exploits/multi/http/tomcat_mgr_upload",
    "exploits/multi/http/wso2_file_upload_rce",
    "exploits/multi/http/log4shell_header_injection",
    "exploits/multi/php/php_unserialize_zval_cookie",
    "exploits/multi/svn/svnserve_date",
    "exploits/windows/iis/iis_webdav_scstoragepathfromurl",
    "exploits/windows/iis/iis_webdav_upload_asp",
    "exploits/windows/http/apache_chunked",
    "exploits/windows/http/apache_modjk_overflow",
    "exploits/windows/http/apache_mod_rewrite_ldap",
    "exploits/windows/http/php_apache_request_headers_bof",
    "exploits/windows/http/tomcat_cgi_cmdlineargs"


**with poetry @paciente23256 | Enjoy.**
