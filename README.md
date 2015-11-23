
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
    <li>Add following options to this file:
        <code>
            [mysqld]
            default-character-set = utf8
            init_connect=‘SET collation_connection = utf8_unicode_ci’
            character-set-server = utf8
            collation-server = utf8_unicode_ci

            [client]
            default-character-set = utf8
        </code>
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
