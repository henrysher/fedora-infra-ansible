<?php
/**
 * Fedora skin
 *
 * Copied/modified from the Monobook skin
 *
 * @todo document
 * @addtogroup Skins
 */

if( !defined( 'MEDIAWIKI' ) )
	die( -1 );

/** */
require_once('includes/SkinTemplate.php');

/**
 * Inherit main code from SkinTemplate, set the CSS and template filter.
 * @todo document
 * @addtogroup Skins
 */
class SkinFedora extends SkinTemplate {
	/** Using monobook. */
	function initPage( &$out ) {
		SkinTemplate::initPage( $out );
		$this->skinname  = 'fedora';
		$this->stylename = 'fedora';
		$this->template  = 'FedoraTemplate';
	}
}

/**
 * @todo document
 * @addtogroup Skins
 */
class FedoraTemplate extends QuickTemplate {
	/**
	 * Template filter callback for Fedora skin.
	 * Takes an associative array of data set from a SkinTemplate-based
	 * class, and a wrapper for MediaWiki's localization database, and
	 * outputs a formatted page.
	 *
	 * @access private
	 */
	function execute() {
		global $wgUser;
		$skin = $wgUser->getSkin();

		// Suppress warnings to prevent notices about missing indexes in $this->data
		wfSuppressWarnings();

?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="<?php $this->text('xhtmldefaultnamespace') ?>" <?php 
	foreach($this->data['xhtmlnamespaces'] as $tag => $ns) {
		?>xmlns:<?php echo "{$tag}=\"{$ns}\" ";
	} ?>xml:lang="<?php $this->text('lang') ?>" lang="<?php $this->text('lang') ?>" dir="<?php $this->text('dir') ?>">
	<head>
		<meta http-equiv="Content-Type" content="<?php $this->text('mimetype') ?>; charset=<?php $this->text('charset') ?>" />
		<?php $this->html('headlinks') ?>
		<title><?php $this->text('pagetitle') ?></title>
		<?php $this->html('csslinks') ?>

  <link rel="stylesheet" type="text/css" media="all" href="/static/css/fedora.css" />
  <link rel="stylesheet" type="text/css" media="print" href="/static/css/print.css" />

		<style type="text/css" media="screen,projection">/*<![CDATA[*/ @import "<?php $this->text('stylepath') ?>/<?php $this->text('stylename') ?>/main.css?<?php echo $GLOBALS['wgStyleVersion'] ?>"; /*]]>*/</style>
		<link rel="stylesheet" type="text/css" <?php if(empty($this->data['printable']) ) { ?>media="print"<?php } ?> href="<?php $this->text('stylepath') ?>/common/commonPrint.css?<?php echo $GLOBALS['wgStyleVersion'] ?>" />
		<link rel="stylesheet" type="text/css" media="handheld" href="<?php $this->text('stylepath') ?>/<?php $this->text('stylename') ?>/handheld.css?<?php echo $GLOBALS['wgStyleVersion'] ?>" />
		<!--[if lt IE 5.5000]><style type="text/css">@import "<?php $this->text('stylepath') ?>/<?php $this->text('stylename') ?>/IE50Fixes.css?<?php echo $GLOBALS['wgStyleVersion'] ?>";</style><![endif]-->
		<!--[if IE 5.5000]><style type="text/css">@import "<?php $this->text('stylepath') ?>/<?php $this->text('stylename') ?>/IE55Fixes.css?<?php echo $GLOBALS['wgStyleVersion'] ?>";</style><![endif]-->
		<!--[if IE 6]><style type="text/css">@import "<?php $this->text('stylepath') ?>/<?php $this->text('stylename') ?>/IE60Fixes.css?<?php echo $GLOBALS['wgStyleVersion'] ?>";</style><![endif]-->
		<!--[if IE 7]><style type="text/css">@import "<?php $this->text('stylepath') ?>/<?php $this->text('stylename') ?>/IE70Fixes.css?<?php echo $GLOBALS['wgStyleVersion'] ?>";</style><![endif]-->
		<!--[if lt IE 7]><script type="<?php $this->text('jsmimetype') ?>" src="<?php $this->text('stylepath') ?>/common/IEFixes.js?<?php echo $GLOBALS['wgStyleVersion'] ?>"></script>
		<meta http-equiv="imagetoolbar" content="no" /><![endif]-->
		
		<?php print Skin::makeGlobalVariablesScript( $this->data ); ?>
                
		<script type="<?php $this->text('jsmimetype') ?>" src="<?php $this->text('stylepath' ) ?>/common/wikibits.js?<?php echo $GLOBALS['wgStyleVersion'] ?>"><!-- wikibits js --></script>
<?php	if($this->data['jsvarurl'  ]) { ?>
		<script type="<?php $this->text('jsmimetype') ?>" src="<?php $this->text('jsvarurl'  ) ?>"><!-- site js --></script>
<?php	}
		if($this->data['usercss'   ]) { ?>
		<style type="text/css"><?php $this->html('usercss'   ) ?></style>
<?php	}
		if($this->data['userjs'    ]) { ?>
		<script type="<?php $this->text('jsmimetype') ?>" src="<?php $this->text('userjs' ) ?>"></script>
<?php	}
		if($this->data['userjsprev']) { ?>
		<script type="<?php $this->text('jsmimetype') ?>"><?php $this->html('userjsprev') ?></script>
<?php	}
		if($this->data['trackbackhtml']) print $this->data['trackbackhtml']; ?>
		<!-- Head Scripts -->
<?php $this->html('headscripts') ?>
	</head>
<body <?php if($this->data['body_ondblclick']) { ?>ondblclick="<?php $this->text('body_ondblclick') ?>"<?php } ?>
<?php if($this->data['body_onload'    ]) { ?>onload="<?php     $this->text('body_onload')     ?>"<?php } ?>
 class="mediawiki <?php $this->text('nsclass') ?> <?php $this->text('dir') ?> <?php $this->text('pageclass') ?>">
	<div id="wrapper">
        <div id="head">
        <h1><a href="<?php echo htmlspecialchars($this->data['nav_urls']['mainpage']['href'])?>" <?php
                        foreach ($skin->tooltipAndAccesskeyAttribs('n-mainpage') as $key => $value) {
                          echo $key.'="'.$value.'" ';
                        }
            ?>>Fedora</a></h1>
	<div id="p-personal">
		<h5><?php $this->msg('personaltools') ?></h5>
			<ul>
<?php 			foreach($this->data['personal_urls'] as $key => $item) { ?>
				<li id="pt-<?php echo Sanitizer::escapeId($key) ?>"<?php
					if ($item['active']) { ?> class="active"<?php } ?>><a href="<?php
				echo htmlspecialchars($item['href']) ?>" <?php
                                  foreach ($skin->tooltipAndAccesskeyAttribs('pt-'.$key) as $attr_key => $attr_value) {
                                    echo $attr_key.'="'.$attr_value.'" ';
                                  }
                                ?><?php
				if(!empty($item['class'])) { ?> class="<?php
				echo htmlspecialchars($item['class']) ?>"<?php } ?>><?php
				echo htmlspecialchars($item['text']) ?></a></li>
<?php			} ?>
			</ul>
	</div>

<!-- Top actions bar -->
	<div id="p-cactions">
		<h5><?php $this->msg('views') ?></h5>
			<ul>
	<?php			foreach($this->data['content_actions'] as $key => $tab) { ?>
				 <li id="ca-<?php echo Sanitizer::escapeId($key) ?>"<?php
					 	if($tab['class']) { ?> class="<?php echo htmlspecialchars($tab['class']) ?>"<?php }
					 ?>><a href="<?php echo htmlspecialchars($tab['href']) ?>" <?php
                                                        foreach ($skin->tooltipAndAccesskeyAttribs('ca-'.$key) as $attr_key => $attr_value) {
                                                          echo $attr_key.'="'.$attr_value.'" ';
                                                        }
                                                     ?>><?php echo htmlspecialchars($tab['text']) ?></a></li>
	<?php			 } ?>
			</ul>
	</div>

        </div>
<div id="sidebar">
<div id="nav">
<!-- Sidebar -->
	<?php foreach ($this->data['sidebar'] as $bar => $cont) { ?>
	<div id='p-<?php echo Sanitizer::escapeId($bar) ?>'<?php echo $skin->tooltip('p-'.$bar) ?>>
		<h2><?php $out = wfMsg( $bar ); if (wfEmptyMsg($bar, $out)) echo $bar; else echo $out; ?></h2>
			<ul>
<?php 			foreach($cont as $key => $val) { ?>
				<li id="<?php echo Sanitizer::escapeId($val['id']) ?>"<?php
					if ( $val['active'] ) { ?> class="active" <?php }
				?>><a href="<?php echo htmlspecialchars($val['href']) ?>" <?php
                                              foreach($skin->tooltipAndAccesskeyAttribs($val['id']) as $attr_key => $attr_value) {
                                                echo $attr_key.'="'.$attr_value.'" ';
                                              }
                                   ?>><?php echo htmlspecialchars($val['text']) ?></a></li>
<?php			} ?>
			</ul>
	</div>
	<?php } ?>
	<div id="p-search">
		<h2><label for="searchInput"><?php $this->msg('search') ?></label></h2>
			<form action="<?php $this->text('searchaction') ?>" id="searchform"><div>
				<input id="searchInput" name="search" type="text" <?php 
                                  foreach($skin->tooltipAndAccesskeyAttribs('search') as $attr_key => $attr_value) {
                                    echo $attr_key.'="'.$attr_value.'" ';
                                  }
					if( isset( $this->data['search'] ) ) {
						?> value="<?php $this->text('search') ?>"<?php } ?> /><br />
				<input type='submit' name="go" class="searchButton" id="searchGoButton"	value="<?php $this->msg('searcharticle') ?>" />&nbsp;
				<input type='submit' name="fulltext" class="searchButton" id="mw-searchButton" value="<?php $this->msg('searchbutton') ?>" />
			</div></form>
	</div>
	<div id="p-tb">
		<h2><?php $this->msg('toolbox') ?></h2>
			<ul>
<?php
		if($this->data['notspecialpage']) { ?>
				<li id="t-whatlinkshere"><a href="<?php
				echo htmlspecialchars($this->data['nav_urls']['whatlinkshere']['href'])
				?>" <?php
                                      foreach ($skin->tooltipAndAccesskeyAttribs('t-whatlinkshere') as $attr_key => $attr_value) {
                                        echo $attr_key.'="'.$attr_value.'" ';
                                      }
                                    ?>><?php $this->msg('whatlinkshere') ?></a></li>
<?php
			if( $this->data['nav_urls']['recentchangeslinked'] ) { ?>
				<li id="t-recentchangeslinked"><a href="<?php
				echo htmlspecialchars($this->data['nav_urls']['recentchangeslinked']['href'])
				?>" <?php 
                                      foreach($skin->tooltipAndAccesskeyAttribs('t-recentchangeslinked') as $attr_key => $attr_value) {
                                        echo $attr_key.'="'.$attr_value.'" ';
                                      }
                                    ?>><?php $this->msg('recentchangeslinked') ?></a></li>
<?php 		}
		}
		if(isset($this->data['nav_urls']['trackbacklink'])) { ?>
			<li id="t-trackbacklink"><a href="<?php
				echo htmlspecialchars($this->data['nav_urls']['trackbacklink']['href'])
				?>" <?php
                                     foreach ($skin->tooltipAndAccesskeyAttribs('t-trackbacklink') as $attr_key => $attr_value) {
                                       echo $attr_key.'="'.$attr_value.'" ';
                                     }
                                   ?>><?php $this->msg('trackbacklink') ?></a></li>
<?php 	}
		if($this->data['feeds']) { ?>
			<li id="feedlinks"><?php foreach($this->data['feeds'] as $key => $feed) {
					?><span id="feed-<?php echo Sanitizer::escapeId($key) ?>"><a href="<?php
					echo htmlspecialchars($feed['href']) ?>" <?php
                                          foreach($skin->tooltipAndAccesskeyAttribs('feed-'.$key) as $attr_key => $attr_value) {
                                            echo $attr_key.'="'.$attr_value.'" ';
                                          }
                                        ?>><?php echo htmlspecialchars($feed['text'])?></a>&nbsp;</span>
					<?php } ?></li><?php
		}

		foreach( array('contributions', 'blockip', 'emailuser', 'upload', 'specialpages') as $special ) {

			if($this->data['nav_urls'][$special]) {
				?><li id="t-<?php echo $special ?>"><a href="<?php echo htmlspecialchars($this->data['nav_urls'][$special]['href'])
				?>" <?php
                                     foreach ($skin->tooltipAndAccesskeyAttribs('t-'.$special) as $attr_key => $attr_value) {
                                       echo $attr_key.'="'.$attr_value.'" ';
                                     }
                                   ?>><?php $this->msg($special) ?></a></li>
<?php		}
		}

		if(!empty($this->data['nav_urls']['print']['href'])) { ?>
				<li id="t-print"><a href="<?php echo htmlspecialchars($this->data['nav_urls']['print']['href'])
				?>"<?php
                                     foreach ($skin->tooltipAndAccesskeyAttribs('t-print') as $attr_key => $attr_value) {
                                       echo $attr_key.'="'.$attr_value.'" ';
                                     }
                                   ?>><?php $this->msg('printableversion') ?></a></li><?php
		}

		if(!empty($this->data['nav_urls']['permalink']['href'])) { ?>
				<li id="t-permalink"><a href="<?php echo htmlspecialchars($this->data['nav_urls']['permalink']['href'])
				?>"<?php
                                     foreach ($skin->tooltipAndAccesskeyAttribs('t-permalink') as $attr_key => $attr_value) {
                                       echo $attr_key.'="'.$attr_value.'" ';
                                     }
                                   ?>><?php $this->msg('permalink') ?></a></li><?php
		} elseif ($this->data['nav_urls']['permalink']['href'] === '') { ?>
				<li id="t-ispermalink"<?php echo $skin->tooltip('t-ispermalink') ?>><?php $this->msg('permalink') ?></li><?php
		}

		wfRunHooks( 'MonoBookTemplateToolboxEnd', array( &$this ) );
?>
			</ul>
	</div>
<?php
		if( $this->data['language_urls'] ) { ?>
	<div id="p-lang">
		<h2><?php $this->msg('otherlanguages') ?></h2>
			<ul>
<?php		foreach($this->data['language_urls'] as $langlink) { ?>
				<li class="<?php echo htmlspecialchars($langlink['class'])?>"><?php
				?><a href="<?php echo htmlspecialchars($langlink['href']) ?>"><?php echo $langlink['text'] ?></a></li>
<?php		} ?>
			</ul>
	</div>
<?php	} ?>
</div>
</div><!-- end of the left (by default at least) column -->

	<div id="content">
		<?php if($this->data['sitenotice']) { ?><div id="siteNotice"><?php $this->html('sitenotice') ?></div><?php } ?>
		<h2><?php $this->data['displaytitle']!=""?$this->html('title'):$this->text('title') ?></h2>
			<h3 id="siteSub"><?php $this->msg('tagline') ?></h3>
			<div id="contentSub"><?php $this->html('subtitle') ?></div>
			<?php if($this->data['undelete']) { ?><div id="contentSub2"><?php     $this->html('undelete') ?></div><?php } ?>
			<?php if($this->data['newtalk'] ) { ?><div class="usermessage"><?php $this->html('newtalk')  ?></div><?php } ?>
			<?php if($this->data['showjumplinks']) { ?><div id="jump-to-nav"><?php $this->msg('jumpto') ?> <a href="#column-one"><?php $this->msg('jumptonavigation') ?></a>, <a href="#searchInput"><?php $this->msg('jumptosearch') ?></a></div><?php } ?>
			<!-- start content -->
			<?php $this->html('bodytext') ?>
			<?php if($this->data['catlinks']) { ?><div id="catlinks"><?php       $this->html('catlinks') ?></div><?php } ?>
			<!-- end content -->
	</div>

<!-- Top login, etc. bar -->
<!-- #p-personal moved to inside #content so the text color says the same -->
	<script type="<?php $this->text('jsmimetype') ?>"> if (window.isMSIE55) fixalpha(); </script>
</div>
			<div id="bottom">
			<div id="footer">
<?php
		if($this->data['poweredbyico']) { ?>
				<div id="f-poweredbyico"><?php $this->html('poweredbyico') ?></div>
<?php 	}
		if($this->data['copyrightico']) { ?>
				<div id="f-copyrightico"><?php $this->html('copyrightico') ?></div>
<?php	}

		// Generate additional footer links
?>
      <p class="copy">
      Copyright &copy; <?php echo date('Y');?> Red Hat, Inc. and others.  All Rights Reserved.  For comments or queries, please <a href="/contact">contact us</a>.
      </p>
      <p class="disclaimer">
      The Fedora Project is maintained and driven by the community and sponsored by Red Hat.  This is a community maintained site.  Red Hat is not responsible for content.
      </p>
			<ul>
<?php
		$footerlinks = array(
			'lastmod', 'viewcount', 'numberofwatchingusers', 'credits', 'copyright',
		);
		$count = 0;
		foreach( $footerlinks as $aLink ) {
			$count++;
			$first = '';
			if ($count == 1) {
				$first = ' class="first"';
			}
			if( isset( $this->data[$aLink] ) && $this->data[$aLink] ) {
?>				<li<?php echo$first?> id="<?php echo$aLink?>"><?php $this->html($aLink) ?></li>
<?php 		}
		}
?>
			</ul>
			<ul>
<?php
		$footerlinks = array(
			'privacy', 'about', 'disclaimer', 'tagline',
		);
		$count = 0;
		foreach( $footerlinks as $aLink ) {
			$count++;
			$first = '';
			if ($count == 1) {
				$first = ' class="first"';
			}
			if( isset( $this->data[$aLink] ) && $this->data[$aLink] ) {
?>				<li<?php echo$first?> id="<?php echo$aLink?>"><?php $this->html($aLink) ?></li>
<?php 		}
		}
?>
        <li><a href="http://fedoraproject.org/en/sponsors">Sponsors</a></li>
        <li><a href="http://fedoraproject.org/wiki/Legal:Main">Legal</a></li>
        <li><a href="http://fedoraproject.org/wiki/Legal:Trademark_guidelines">Trademark Guidelines</a></li>
      </ul>
		</div>
		</div>
		
	<?php $this->html('bottomscripts'); /* JS call to runBodyOnloadHook */ ?>

  <script src="https://apps.fedoraproject.org/fedmenu/js/jquery-1.11.2.min.js"></script>
  <script src="https://apps.fedoraproject.org/fedmenu/js/fedora-libravatar.js"></script>
  <script src="https://apps.fedoraproject.org/fedmenu/js/fedmenu.js"></script>
  <script>
    fedmenu({
        'url': 'https://apps.fedoraproject.org/js/data.js',
        'mimeType': 'application/javascript',
        'position': 'bottom-right',
        <?php
            $subject = $skin->getTitle()->getInternalURL();
            $pattern = '/User:([a-zA-Z0-9]+)(\/.*)?$/';
            preg_match($pattern, $subject, $matches);
            if (sizeof($matches) >= 2):
                echo "'user': '" . strtolower($matches[1]) . "',";
            endif;
        ?>
    });
  </script>

<?php $this->html('reporttime') ?>
<?php if ( $this->data['debug'] ): ?>
<!-- Debug output:
<?php $this->text( 'debug' ); ?>

-->
<?php endif; ?>
</body></html>
<?php
	wfRestoreWarnings();
	} // end of execute() method
} // end of class
?>
