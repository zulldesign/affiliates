<?
include_once("tsc_config.html");
include_once("tsc_funs.html");
$link = dbconnect();

$q="SELECT * FROM store_info_tab ORDER BY mem_id" ;
if($r=mysql_query($q))
{
	$scdata = mysql_fetch_array($r);
	$sc = $scdata['mem_id'];
	if($sc > 0)
	{
		header("Location: store.html?mem_id=$sc");
	}
	else
	{
		header("Location: index.html?a=signup");
	}
}
else
{
	echo mysql_error();
	exit;
}
dbclose($link);
?>