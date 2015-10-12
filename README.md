
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
<h2>Setupping database</h2>
<ol>
    <li>Clone this repository to your local machine.</li>
    <li>Go to 'ecomap/DB/ecomap/' directory.</li>
    <li>Run following command - <code>mysql -u -p < CREATE_DB.sql</code>. This command will create DB - 'ecomap_db'. <br>
            To change Database name go to CREATE_DB.sql, and change 'ecomap_db' to any name you want.</li>
    <li>Run following command - <code>mysql -u -p < INSERT_DATA.sql</code> to insert basic data into table(such as admin account and etc.).</li>
    <li>Now you have working Database!</li>
</ol>
