
<h1>Ecomap project (by LV-164.UI)</h1>
<h2>About this project</h2>
<p>This repository is source code of the small web project, which is named 'EcoMap'. This website allows you to publish information about ecological issues around Ukraine to dynamic map. Officials of the Ministry of Environment use this website to collect info about problems and contact with citizens, who publish info to this website. <br>
Website's url - <a href="http://ecomap.org">ecomap.org</a></p>
<h2>Dependencies</h2>
<p>We're assumming that you're using bash & you already have installed such packages: </p>
<ul>
    <li>apt-get</li>
    <ul>
        <li><code>sudo apt-get install mysql-server</code></li>
    </ul>
</ul>
<h2>Setupping database locally</h2>
<ol>
    <li>Clone this repository to your local machine</li>
    <li>Open file /etc/mysql/my.conf with following command: <code>nano /etc/mysql/my.cnf</code></li>
    <li>Add following options to this file: <br>
    <pre>
    [mysqld]
    default-character-set = utf8
    init_connect=‘SET collation_connection = utf8_unicode_ci’
    character-set-server = utf8
    collation-server = utf8_unicode_ci
    
    [client]
    default-character-set = utf8
    </pre>
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
<img src="https://raw.githubusercontent.com/lhalam/EcoMap/pagination/ecomap_db.png">
<h2>Ecomap application runs on Apache Web Server v2.4</h2>
<p>
    This is a short manual, which tells how to configure WSGI-Flask application and Apache server on your server or local        machine.
</p>
<ol>
    <li> Install Apache 2 and mod_wsgi lib:<br>
            <code>sudo apt-get install -y apache2</code><br>
            <code>sudo apt-get install libapache2-mod-wsgi</code><br>
            <code>sudo apt-get install libapache2-mod-wsgi python-dev</code><br>
    </li>
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
        Add content from apache.conf file, which is situated in - <code>ecomap/etc/apache.conf</code> to                             <code>/etc/apache2/sites-available/ecomap.conf</code>.
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
