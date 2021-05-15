#!/usr/bin/perl

############################################
##                                        ##
##                 WebBBS                 ##
##           by Darryl Burgdorf           ##
##       (e-mail burgdorf@awsd.com)       ##
##                                        ##
##             version:  4.22             ##
##         last modified: 4/19/00         ##
##           copyright (c) 2000           ##
##                                        ##
##    latest version is available from    ##
##        http://awsd.com/scripts/        ##
##                                        ##
############################################

# COPYRIGHT NOTICE:
#
# Copyright 2000 Darryl C. Burgdorf.  All Rights Reserved.
#
# This program is being distributed as shareware.  It may be used and
# modified by anyone, so long as this copyright notice and the header
# above remain intact, but any usage should be registered.  (See the
# program documentation for registration information.)  Selling the
# code for this program without prior written consent is expressly
# forbidden.  Obtain permission before redistributing this program
# over the Internet or in any other medium.  In all cases copyright
# and header must remain intact.
#
# This program is distributed "as is" and without warranty of any
# kind, either express or implied.  (Some states do not allow the
# limitation or exclusion of liability for incidental or consequential
# damages, so this notice may not apply to you.)  In no event shall
# the liability of Darryl C. Burgdorf and/or Affordable Web Space
# Design for any damages, losses and/or causes of action exceed the
# total amount paid by the user for this software.

##############################################
## You MUST define the following variables! ##
##############################################

## (1) Specify the locations of your WebBBS files:

$webbbs_index = "/usgn1/usgennetorg/cgi-bin/webbbs/webbbs_index.pl";
$webbbs_read = "/usgn1/usgennetorg/cgi-bin/webbbs/webbbs_read.pl";
$webbbs_form = "/usgn1/usgennetorg/cgi-bin/webbbs/webbbs_form.pl";
$webbbs_post = "/usgn1/usgennetorg/cgi-bin/webbbs/webbbs_post.pl";
$webbbs_misc = "/usgn1/usgennetorg/cgi-bin/webbbs/webbbs_misc.pl";
$webbbs_rebuild = "/usgn1/usgennetorg/cgi-bin/webbbs/webbbs_rebuild.pl";
$webbbs_text = "/usgn1/usgennetorg/cgi-bin/webbbs/webbbs_text.pl";
$webbbs_basic = "/usgn1/usgennetorg/cgi-bin/webbbs/webbbs_basic.pl";

$dir = "/usgn1/usgennetorg/htdocs/family/smoot/webbbs/records";
$cgiurl = "/family/smoot/webbbs/records/index.cgi";

$DBMType = 0;

## (2) Define your e-mail notification features:

$mailprog = '/usr/sbin/sendmail';
$WEB_SERVER = "";
$SMTP_SERVER = "";

$admin_name = "Webmaster";
$maillist_address = "bbsadmin\@tngenweb.org";
$notification_address = "bbsadmin\@tngenweb.org";
$email_list = "";
$private_list = 1;

$HeaderOnly = 0;

# use Socket;
# use Net::SMTP;

#################################################################
## You MAY define the following variables, but do not have to! ##
#################################################################

## (3) Tailor the appearance and functionality of your BBS:

BEGIN { @AnyDBM_File::ISA = qw (DB_File) }

$MetaFile = "";
$HeaderFile = "/usgn1/usgennetorg/htdocs/family/smoot/webbbs/records/header.txt";
$FooterFile = "/usgn1/usgennetorg/htdocs/family/smoot/webbbs/records/footer.txt";
$MessageHeaderFile = "";
$MessageFooterFile = "";
$SSIRootDir = "";

$bodyspec = "BGCOLOR=\"#ffffff\" TEXT=\"#000000\"";
$fontspec = "FACE=\"Arial\"";
$navbarcolor = "cccccc";
$navbarfontspec = "FACE=\"Arial\"";
$tablecolor = "cccccc";
$tablefontspec = "FACE=\"Arial\"";

$ListBullets = 0;

@SubjectPrefixes = ();

$MessageOpenCode = "<FONT COLOR=\"#000000\">";
$MessageCloseCode = "</FONT>";

$NewOpenCode = "<EM><FONT COLOR=\"#cc0000\">NEW:</FONT></EM>";
$NewCloseCode = "";
$AdminOpenCode = "<EM><FONT COLOR=\"#990000\">ADMIN!</FONT></EM>";
$AdminCloseCode = "";

$UseLocking = 1;
$RefreshTime = 5;

$UseFrames = "";
$BBSFrame = "_parent";
$WelcomePage = "";

$Moderated = 1;
$SearchURL = "";

$TopNPosters = 0;

%Navbar_Links = ();

$SepPostFormIndex = 0;
$SepPostFormRead = 0;

$DefaultType = "By Threads, Mixed";
$DefaultTime = "1 Month(s)";

$boardname = "Forum";
$shortboardname = "Forum";
$printboardname = 0;

$DateConfig = "";
$IndexEntryLines = 2;

$InputColumns = 50;
$InputRows = 10;

$HourOffset = 0;

$ArchiveOnly = 0;
$AllowHTML = 0;
$SingleLineBreaks = 0;

$AutoQuote = 0;
$AutoQuoteChar = ":";

$AutoHotlink = 0;

%SmileyCode = ();

%FormatCode = ();

$NM_Telltale = "*NM*";
$Pic_Telltale = "";

$ThreadSpacer = "";
$GuestbookSpacer = "";

$DisplayEmail = 1;
$ResolveIPs = 1;
$DisplayIPs = 0;
$DisplayViews = 1;

$UseCookies = 1;

## (4) Define your visitors' capabilities:

$MaxMessageSize = 50;
$MaxInputLength = 50;

$LockRemoteUser = 1;

$AllowUserDeletion = 0;
$AllowEmailNotices = 1;
$AllowPreview = 1;

$AllowURLs = 1;
$AllowPics = 0;

$SaveLinkInfo = 0;

$AllowUserPrefs = 1;
$AllowNewThreads = 1;
$AllowResponses = 1;

$NaughtyWords = "";
$CensorPosts = 0;

$ShowPosterIP = 1;
$BannedIPs = "";
$CompleteBan = 0;

#############################################
## Do NOT change anything in this section! ##
#############################################

require $webbbs_text;
require $webbbs_basic;

if ($BannedIPs && $CompleteBan) {
	if ($ResolveIPs) {
		if (($ENV{'REMOTE_ADDR'} =~ /\d+\.\d+\.\d+\.\d+/)
		  && (!($ENV{'REMOTE_HOST'})
		  || ($ENV{'REMOTE_HOST'} =~ /\d+\.\d+\.\d+\.\d+/))) {
			@domainbytes = split(/\./,$ENV{'REMOTE_ADDR'});
			$packaddr = pack("C4",@domainbytes);
			$resolvedip = (gethostbyaddr($packaddr, 2))[0];
			unless ($resolvedip =~
			  /^[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})$/) {
				$resolvedip = "";
			}
			if ($resolvedip) {
				$ENV{'REMOTE_HOST'} = $resolvedip;
			}
		}
	}
	else {
		$ENV{'REMOTE_HOST'} = "";
	}
	unless ($ENV{'REMOTE_HOST'}) { $ENV{'REMOTE_HOST'} = $ENV{'REMOTE_ADDR'}; }
	@bannedips = split(/ /,$BannedIPs);
	foreach $bannedip (@bannedips) {
		if (($ENV{'REMOTE_HOST'} =~ /$bannedip/i)
		  || ($ENV{'REMOTE_ADDR'} =~ /$bannedip/i)) {
			require $webbbs_read;
			&Initialize_Data;
			&Error("9520","9521");
		}
	}
}

if ($ENV{'QUERY_STRING'} =~ /noframes/i) { $UseFrames = ""; }
if ((!($UseFrames) && ($ENV{'QUERY_STRING'} =~ /review=(\d+)/i)) 
  || (!($UseFrames) && ($ENV{'QUERY_STRING'} =~ /rev=(\d+)/i)) 
  || ($ENV{'QUERY_STRING'} =~ /read=(\d+)/i)
  || ($ENV{'QUERY_STRING'} =~ /form=(\d+)/i)) {
	require $webbbs_read;
}
elsif ($ENV{'QUERY_STRING'} =~ /post/i) {
	require $webbbs_post;
}
elsif (($ENV{'QUERY_STRING'} =~ /addresslist/i)
  || ($ENV{'QUERY_STRING'} =~ /delete/i)
  || ($ENV{'QUERY_STRING'} =~ /reconfigure/i)
  || ($ENV{'QUERY_STRING'} =~ /search/i)
  || ($ENV{'QUERY_STRING'} =~ /subscribe/i)
  || ($ENV{'QUERY_STRING'} =~ /topstats/i)) {
	require $webbbs_misc;
}
else { require $webbbs_index; }

&WebBBS;

###################################################################
## If necessary, set up the WebAdverts configuration subroutine! ##
###################################################################

sub insertadvert {
	local($adzone) = @_;
	$ADVNoPrint = 1;
	if ($adzone) { $ADVQuery = "zone=$adzone"; }
	else { $ADVQuery = ""; }
	require "/usr/www/users/dburgdor/scripts/ads/ads.pl";
}
