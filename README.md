<h1>Ecomap project (by LV-164.UI&LV-173.UI)</h1>
<h2>About this project</h2>
<p>This repository is source code of the small web project, which is named 'EcoMap'. This website allows you to publish information about ecological issues around Ukraine to dynamic map. Officials of the Ministry of Environment use this website to collect info about problems and contact with citizens, who publish info to this website. <br>
Website's url - <a href="http://ecomap.org">ecomap.org</a></p>
<p>Ecomap Rest Api docimentation <a href="http://lhalam.github.io/EcoMap">lhalam.github.io/EcoMap/</a></p>

<h2>Install</h2>
<p>We're assumming that you're using bash & you have to install or clone such packages: </p>
<ul>
    <li> Install MySQL server on local machine.<br>
        <code>sudo apt-get install mysql-server</code>
    </li>
    <li> Install Apache 2 and mod_wsgi lib:<br>
        <code>sudo apt-get install -y apache2</code><br>
        <code>sudo apt-get install libapache2-mod-wsgi</code><br>
        <code>sudo apt-get install libapache2-mod-wsgi python-dev</code><br>
    </li>
    <li> Install MEMCACHE on local machine.<br>
        <code>sudo apt-get install memcached</code>
    </li>
    <li>Clone this repository to your local machine.<br>
        <code>git clone https://github.com/lhalam/EcoMap.git</code>
    </li>
    <li>Go to the local copy of repository. Open terminal and run the following command<br>
        <code>sudo pip install -r requirements.txt</code>
    </li>
</ul>


<h2>Create config files for your application</h2>
<p>
    In order to run your application you need to run config builder which creates all config files.
</p>
<ol>
    <li> Go to <code>'path/to/repo/ecomap/bin/</code> directory</li>
    <li> Run shell script : <code>./ecomap_config_builder.sh</code><br>
         Default logging level - DEBUG<br>
         You can run this script with two logging levels:<br>
         <code>./ecomap_config_builder.sh -v1</code> - logging level DEBUG<br>
         <code>./ecomap_config_builder.sh -v2</code> - logging level INFO<br>
         This script will run config builder in your console.
    </li>
    <li>You will have to type config values, and where it`s possible you can use default one. Example :<br>
    <pre>
    <code>[apache_project_path] Path to project for apache config [default:None]: /path/to/project/directory 
    [apache_server_admin] Admin email for apache config [default:admin@ecomap.com]: admin@gmail.com
    [apache_server_alias] Server alias for apache config [default:None]: ecomap.new
    [apache_server_name] Server name for apache config [default:None]: www.ecomap.new
    [apache_virtual_host] Virtualhost for apache config [default:None]: ecomap.new
    [db_connection_lifetime] Ecomap database ttl [default:5]: 10
    [db_connection_retries] Number of connection retry [default:3]: 5
    [db_name] Ecomap database name [default:ecomap]: ecomap_db
    [db_retry_delay] Retry delay of ecomap database [default:3]: 5
    [ecomap_admin_user_email] Email for admin user [default:admin@ecomap.com]: admin@gmail.com
    [ecomap_admin_user_password] User password for admin user [default:secre!]: adminpass      
    [ecomap_memcached_servers] List of memcahed servers [default:['127.0.0.1:11211']]: ['198.168.15.66:9000']                                             
    [ecomap_problems_cache_timeout] Cache timeout for problems [default:60]: 180
    [ecomap_secret_key] Secret key for ecomap [default:a7c268ab01141868811c070274413ea3c588733241659fcb]: 2k34knn5ny3j5mg5vm4hgb5jjk4m4v4gb3k4n5bv3hn3n3g0
    [ecomap_static_cache_timeout] Cache timeout for static files [default:86400]: 172800
    [ecomap_unknown_email] Email for unknown user [default:anonymous@ecomap.com]: anonymous@i.ua  
    [ecomap_unknown_first_name] First name for unknown user [default:anonymous]: anon
    [ecomap_unknown_last_name] Last name for unknown user [default:anonymous]: anonimovich
    [ecomap_unknown_nickname] nickname for unknown user [default:anonymous]: anonchik
    [ecomap_unknown_password] Password for unknown user [default:None]: anonpass
    [email_from_address] From email for email distribution [default:ecomaptest@gmail.com]: ecomapmail@i.ua 
    [email_server_name] SMTP server name [default:smtp.gmail.com]: smtp.i.ua
    [email_server_password] Server password for email distribution [default:ecomap_test]: emailpass
    [email_user_name] Email user name for email distribution [default:ecomaptest]: ECOMAP
    [hash_options_lifetime] Config lifetime for password restore [default:900]: 1200
    [log_logger_root_level] Logging level [default:INFO]: DEBUG
    [oauth_facebook_id] Facebook_id for facebook authentication [default:None]: 1000437473365547        
    [oauth_facebook_secret] Facebook_secret for facebook authentication [default:20b8495bdd654cde3e0be0a9ccd8a362]: 45d8d6a2fv1b79hf3f1f5sdw8o46yj61
    [ro_db_host] Read ecomap database server hostname [default:None]: localhost
    [ro_db_password] Read / write ecomap database password [default:None]: 1qaz2wsx3edc
    [ro_db_pool_size] Pool size of ecomap database [default:3]: 6
    [ro_db_port] Read ecomap database port [default:3306]: 9090
    [ro_db_user] Read ecomap database user [default:root]: cat
    [rw_db_host] Read / write ecomap database server hostname [default:None]: localhost
    [rw_db_password] Read / write ecomap database password [default:None]: k3i4i5lm6m6
    [rw_db_pool_size] Read / write pool size of ecomap database [default:3]: 5
    [rw_db_port] Read / write ecomap database port [default:3306]: 8989
    [rw_db_user] Read / write ecomap database user [default:root]: dog</code>
    </pre>
    </li>
    <li> After this it will create config files in <code>ecomap/etc/</code> directory and insert in database admin and anononymous with appropriate data.
    </li>
</ol>

<h2>Setupping database locally</h2>
<ol>
    <li>Open file /etc/mysql/my.conf with following command: <code>nano /etc/mysql/my.cnf</code></li>
    <li>Add following options to this file: <br>
    <pre>
    [mysqld]
    default-character-set = utf8
    init_connect=‘SET collation_connection = utf8_unicode_ci’
    character-set-server = utf8
    collation-server = utf8_unicode_ci
    
    [client]
    default-character-set = utf8</pre>
    </li>
    <li>Go to 'path/to/repo/ecomap/DB/ecomap/' directory</li>
    <li>Run mysql shell: <code>mysql -u -p</code></li>
    <li>Run following command: <code>CREATE DATABASE ecomap_db CHARACTER SET utf8 COLLATE utf8_unicode_ci;</code> - this command will create database if it's not created yet. Put the name you want instead of 'ecomap_db'</li>
    <li>Run following command: <code>USE ecomap_db;</code> - this command will set the database you've created earilier as current. 
        Instead of ecomap_db put the name you've chosen earlier</li>
    <li>Run following command: <code>SOURCE CREATE_DB.sql;</code> - this command will create all tables for database</li>
    <li>Run following command: <code>SOURCE INSERT_DATA.sql;</code> - this command will populate all data you need for the beginning of work</li>
    <li>Now you have working Database!</li>
</ol>
<h2>Database scheme</h2>
<img src="https://raw.githubusercontent.com/lhalam/EcoMap/dev/ecomap_db.png">

<h2>Ecomap application runs on Apache Web Server v2.4</h2>
<p>
    This is a short manual, which tells how to configure WSGI-Flask application and Apache server on your server or local        machine.
</p>
<ol>
    <li>
        Enable wsgi mod: <br>
            <code>sudo a2enmod wsgi</code>
    </li>
    <li>
        Edit your hosts file to create server name alias<br>
            <code>sudo gedit /etc/hosts</code><br>
        Add this line to th your host file: 
            <code>127.0.1.2   ecomap.new</code>
    </li>
    <li>
        Run following command: <br>
            <code>sudo gedit /etc/apache2/sites-available/ecomap.conf</code><br>
        This command will create file ecomap.conf - this is config file of your site. You can set any name you want!<br>
        Add content from apache.conf file, which is situated in - <code>ecomap/etc/_ecomap.apache.conf</code> to                             <code>/etc/apache2/sites-available/ecomap.conf</code>.
    </li>
    <li>
        Enable your site:<br>
        <code>sudo a2ensite ecomap</code>
    </li>
    <li>
        Make your own copy of ecomap.wsgi (situated in <code>ecomap/www/ecomap.wsgi</code>).
        Also read comments in that file, since they are important! This is your main wsgi script which apache will use to run         application. It has already configured for our project structure. You can set your own path to templates folder and          you'll see test site.
    </li>
    <li>
        <code>views.py</code> - this is main flask application file. All backend code will be written there. You can change          everything right now!
    </li>
</ol>

<h2> ENVIRONMENT VARIABLES </h2>
<p>insert to bashrc</p>
<ul>
<li>export PRODROOT=${PRODROOT:-/home/user/project/EcoMap/ecomap}</li>
<li>export PYSRCROOT=${PYSRCROOT:-${PRODROOT}/src/python}</li>
<li>export CONFROOT=${CONFROOT:-${PRODROOT}/etc}</li>
<li>export PYTHONPATH=${PRODROOT}/src/python</li>
<li>export PYTHON=${PYTHON:-/etc/python}</li>
<li>export PYTHON_EGG_CACHE=${PYTHON_EGG_CACHE:-/tmp/.python-eggs}</li>
<li>export STATICROOT=${STATICROOT:-${PRODROOT}/www/}</li>
</ul>

