<?php
/**
 * 
 * @author Krios Mane
 * @version 0.1
 * @license https://opensource.org/licenses/GPL-3.0
 * 
 */
?>
<title> .: FABUI :. </title>
<?php foreach($this->meta_tags as $name => $value): ?>
<meta name="<?php echo $name ?>" content="<?php echo $value; ?>">
<?php endforeach; ?>
<meta charset="UTF-8">
<!-- Basic Styles -->
<?php if(ENVIRONMENT == 'production' && file_exists(FCPATH.'/assets/css/mandatory.css')): ?>
	<link rel="stylesheet" type="text/css" media="screen" href="/assets/css/mandatory.css?v=<?php echo FABUI_VERSION ?>">
<?php else:?>
	<?php foreach($this->css_mandatory as $css):?>
	<link rel="stylesheet" type="text/css" media="screen" href="<?php echo $css ?>?v=<?php echo FABUI_VERSION ?>">
	<?php endforeach;?>
<?php endif?>
<!-- PAGE RELATED CSS FILES -->
<?php echo $cssFiles; ?>
<!-- FAVICONS -->
<link rel="shortcut icon" href="/assets/img/favicon/favicon.ico" type="image/x-icon">
<link rel="icon"          href="/assets/img/favicon/favicon.ico" type="image/x-icon">
<!-- IE11 -->
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<!-- iOS web-app metas : hides Safari UI Components and Changes Status Bar Appearance -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<!-- HEADERD JAVASCRIPTS -->
<script src="/assets/js/libs/jquery-2.1.1.min.js?v=<?php echo FABUI_VERSION ?>"></script>
<script src="/assets/js/libs/jquery-ui-1.10.3.min.js?v=<?php echo FABUI_VERSION ?>"></script>
<style>#main{margin-left:0px !important;}</style>
<?php echo $cssInLine; ?>
