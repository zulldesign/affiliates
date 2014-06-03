<?php
$dbhost = "localhost";   //Host of the DataBase, almost always localhost
$dbname = "proweb_TSCv4";   //DB Name
$dbuser = "proweb_admin1";   //DB user name
$dbpwd = "6021023";    //DB user password

$baseurl = "http://www.stopyourex.com/tsc/"; //URL of our site - http://www.yoursitedomain.com/tsc/  
$basepath = "/home/proweb/public_html/StopYourEx.com/tsc/"; //Base path to the root folder of our site - example - /home/somename/public_html/

$sitename= "StopYourEx.com"; //Our sitename here

$pagekeywords = ""; //Leave this blank
$pagedesc = ""; //Leave this blank
$pagetitle = ""; //Leave this blank
$pagecontent = ""; //Leave this blank

//No reply email
$noreply_mail = "noreply@noreply.com"; //This is email tag that apppears as the 'From' email address - doesn't have to be a valid email if we don't reply to mail sent back. This address will be most exploited, so use one that is SPAM-resistant.

//Service announcements - Text string that gets sent in all email communications
$serviceannouncements = <<<TXT

TXT;

//Admin email
$admin_email = "admin@stopyourex.com"; //Must be valid email here, to get admin notifications 

//Default email ad -  sent in all email communications
$email_adcode = <<<TXT

TXT;

//Banners shown on the stores. First WIDE is 480 x 60, second TALL is 120 x 600. - good to save some code like Google adsense or similar, to show on each page of store - We can directly (carefully) edit the template files to show the banners.
$b480X60 = <<<HTM
<a href="http://www.stopyourex.com" target="_blank"><img src="images/banner.gif"></a>
HTM;

$b120X600 = <<<HTM

HTM;


?>