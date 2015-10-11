
<h1>FOR TESTING DB SCRIPTS:</h1>
<ol>
    <li>clone this branch</li>
    <li>run in terminal msql -u root -p and create database ecomap;</li>
    <li>open populate_db.py and set your msql password:</li>
    db = MySQLdb.connect("localhost", 'root', password, 'ecomap')<br>
    * if necessary change host, db_user, database_name 
    <br>
    <li>open populate_db.py and change PATH to your working directory:</li>
      (ex) PATH = '/home/padalko/ss_projects/Lv-164.UI'</li>
    <li>run python populate_db.py</li>  
</ol>

populate_db path: Lv-164.UI/ecomap/DB/ecomap/populate_db.py

