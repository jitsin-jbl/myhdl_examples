%!PS-Adobe-3.0
%%BoundingBox: 18 36 577 806
%%Title: Enscript Output
%%Creator: GNU Enscript 1.6.5.90
%%CreationDate: Tue Nov 24 15:44:43 2015
%%Orientation: Landscape
%%Pages: (atend)
%%DocumentMedia: A4 595 842 0 () ()
%%DocumentNeededResources: (atend)
%%EndComments
%%BeginProlog
%%BeginResource: procset Enscript-Prolog 1.6.5 90
%
% Procedures.
%

/_S {	% save current state
  /_s save def
} def
/_R {	% restore from saved state
  _s restore
} def

/S {	% showpage protecting gstate
  gsave
  showpage
  grestore
} bind def

/MF {	% fontname newfontname -> -	make a new encoded font
  /newfontname exch def
  /fontname exch def

  /fontdict fontname findfont def
  /newfont fontdict maxlength dict def

  fontdict {
    exch
    dup /FID eq {
      % skip FID pair
      pop pop
    } {
      % copy to the new font dictionary
      exch newfont 3 1 roll put
    } ifelse
  } forall

  newfont /FontName newfontname put

  % insert only valid encoding vectors
  encoding_vector length 256 eq {
    newfont /Encoding encoding_vector put
  } if

  newfontname newfont definefont pop
} def

/MF_PS { % fontname newfontname -> -	make a new font preserving its enc
  /newfontname exch def
  /fontname exch def

  /fontdict fontname findfont def
  /newfont fontdict maxlength dict def

  fontdict {
    exch
    dup /FID eq {
      % skip FID pair
      pop pop
    } {
      % copy to the new font dictionary
      exch newfont 3 1 roll put
    } ifelse
  } forall

  newfont /FontName newfontname put

  newfontname newfont definefont pop
} def

/SF { % fontname width height -> -	set a new font
  /height exch def
  /width exch def

  findfont
  [width 0 0 height 0 0] makefont setfont
} def

/SUF { % fontname width height -> -	set a new user font
  /height exch def
  /width exch def

  /F-gs-user-font MF
  /F-gs-user-font width height SF
} def

/SUF_PS { % fontname width height -> -	set a new user font preserving its enc
  /height exch def
  /width exch def

  /F-gs-user-font MF_PS
  /F-gs-user-font width height SF
} def

/M {moveto} bind def
/s {show} bind def

/Box {	% x y w h -> -			define box path
  /d_h exch def /d_w exch def /d_y exch def /d_x exch def
  d_x d_y  moveto
  d_w 0 rlineto
  0 d_h rlineto
  d_w neg 0 rlineto
  closepath
} def

/bgs {	% x y height blskip gray str -> -	show string with bg color
  /str exch def
  /gray exch def
  /blskip exch def
  /height exch def
  /y exch def
  /x exch def

  gsave
    x y blskip sub str stringwidth pop height Box
    gray setgray
    fill
  grestore
  x y M str s
} def

/bgcs { % x y height blskip red green blue str -> -  show string with bg color
  /str exch def
  /blue exch def
  /green exch def
  /red exch def
  /blskip exch def
  /height exch def
  /y exch def
  /x exch def

  gsave
    x y blskip sub str stringwidth pop height Box
    red green blue setrgbcolor
    fill
  grestore
  x y M str s
} def

% Highlight bars.
/highlight_bars {	% nlines lineheight output_y_margin gray -> -
  gsave
    setgray
    /ymarg exch def
    /lineheight exch def
    /nlines exch def

    % This 2 is just a magic number to sync highlight lines to text.
    0 d_header_y ymarg sub 2 sub translate

    /cw d_output_w cols div def
    /nrows d_output_h ymarg 2 mul sub lineheight div cvi def

    % for each column
    0 1 cols 1 sub {
      cw mul /xp exch def

      % for each rows
      0 1 nrows 1 sub {
        /rn exch def
        rn lineheight mul neg /yp exch def
        rn nlines idiv 2 mod 0 eq {
	  % Draw highlight bar.  4 is just a magic indentation.
	  xp 4 add yp cw 8 sub lineheight neg Box fill
	} if
      } for
    } for

  grestore
} def

% Line highlight bar.
/line_highlight {	% x y width height gray -> -
  gsave
    /gray exch def
    Box gray setgray fill
  grestore
} def

% Column separator lines.
/column_lines {
  gsave
    .1 setlinewidth
    0 d_footer_h translate
    /cw d_output_w cols div def
    1 1 cols 1 sub {
      cw mul 0 moveto
      0 d_output_h rlineto stroke
    } for
  grestore
} def

% Column borders.
/column_borders {
  gsave
    .1 setlinewidth
    0 d_footer_h moveto
    0 d_output_h rlineto
    d_output_w 0 rlineto
    0 d_output_h neg rlineto
    closepath stroke
  grestore
} def

% Do the actual underlay drawing
/draw_underlay {
  ul_style 0 eq {
    ul_str true charpath stroke
  } {
    ul_str show
  } ifelse
} def

% Underlay
/underlay {	% - -> -
  gsave
    0 d_page_h translate
    d_page_h neg d_page_w atan rotate

    ul_gray setgray
    ul_font setfont
    /dw d_page_h dup mul d_page_w dup mul add sqrt def
    ul_str stringwidth pop dw exch sub 2 div ul_h_ptsize -2 div moveto
    draw_underlay
  grestore
} def

/user_underlay {	% - -> -
  gsave
    ul_x ul_y translate
    ul_angle rotate
    ul_gray setgray
    ul_font setfont
    0 0 ul_h_ptsize 2 div sub moveto
    draw_underlay
  grestore
} def

% Page prefeed
/page_prefeed {		% bool -> -
  statusdict /prefeed known {
    statusdict exch /prefeed exch put
  } {
    pop
  } ifelse
} def

% Wrapped line markers
/wrapped_line_mark {	% x y charwith charheight type -> -
  /type exch def
  /h exch def
  /w exch def
  /y exch def
  /x exch def

  type 2 eq {
    % Black boxes (like TeX does)
    gsave
      0 setlinewidth
      x w 4 div add y M
      0 h rlineto w 2 div 0 rlineto 0 h neg rlineto
      closepath fill
    grestore
  } {
    type 3 eq {
      % Small arrows
      gsave
        .2 setlinewidth
        x w 2 div add y h 2 div add M
        w 4 div 0 rlineto
        x w 4 div add y lineto stroke

        x w 4 div add w 8 div add y h 4 div add M
        x w 4 div add y lineto
	w 4 div h 8 div rlineto stroke
      grestore
    } {
      % do nothing
    } ifelse
  } ifelse
} def

% EPSF import.

/BeginEPSF {
  /b4_Inc_state save def    		% Save state for cleanup
  /dict_count countdictstack def	% Count objects on dict stack
  /op_count count 1 sub def		% Count objects on operand stack
  userdict begin
  /showpage { } def
  0 setgray 0 setlinecap
  1 setlinewidth 0 setlinejoin
  10 setmiterlimit [ ] 0 setdash newpath
  /languagelevel where {
    pop languagelevel
    1 ne {
      false setstrokeadjust false setoverprint
    } if
  } if
} bind def

/EndEPSF {
  count op_count sub { pos } repeat	% Clean up stacks
  countdictstack dict_count sub { end } repeat
  b4_Inc_state restore
} bind def

% Check PostScript language level.
/languagelevel where {
  pop /gs_languagelevel languagelevel def
} {
  /gs_languagelevel 1 def
} ifelse
%%EndResource
%%BeginResource: procset Enscript-Encoding-88591 1.6.5 90
/encoding_vector [
/.notdef      	/.notdef      	/.notdef      	/.notdef      	
/.notdef      	/.notdef      	/.notdef      	/.notdef      	
/.notdef      	/.notdef      	/.notdef      	/.notdef      	
/.notdef      	/.notdef      	/.notdef      	/.notdef      	
/.notdef      	/.notdef      	/.notdef      	/.notdef      	
/.notdef      	/.notdef      	/.notdef      	/.notdef      	
/.notdef      	/.notdef      	/.notdef      	/.notdef      	
/.notdef      	/.notdef      	/.notdef      	/.notdef      	
/space        	/exclam       	/quotedbl     	/numbersign   	
/dollar       	/percent      	/ampersand    	/quoteright   	
/parenleft    	/parenright   	/asterisk     	/plus         	
/comma        	/hyphen       	/period       	/slash        	
/zero         	/one          	/two          	/three        	
/four         	/five         	/six          	/seven        	
/eight        	/nine         	/colon        	/semicolon    	
/less         	/equal        	/greater      	/question     	
/at           	/A            	/B            	/C            	
/D            	/E            	/F            	/G            	
/H            	/I            	/J            	/K            	
/L            	/M            	/N            	/O            	
/P            	/Q            	/R            	/S            	
/T            	/U            	/V            	/W            	
/X            	/Y            	/Z            	/bracketleft  	
/backslash    	/bracketright 	/asciicircum  	/underscore   	
/quoteleft    	/a            	/b            	/c            	
/d            	/e            	/f            	/g            	
/h            	/i            	/j            	/k            	
/l            	/m            	/n            	/o            	
/p            	/q            	/r            	/s            	
/t            	/u            	/v            	/w            	
/x            	/y            	/z            	/braceleft    	
/bar          	/braceright   	/tilde        	/.notdef      	
/.notdef      	/.notdef      	/.notdef      	/.notdef      	
/.notdef      	/.notdef      	/.notdef      	/.notdef      	
/.notdef      	/.notdef      	/.notdef      	/.notdef      	
/.notdef      	/.notdef      	/.notdef      	/.notdef      	
/.notdef      	/.notdef      	/.notdef      	/.notdef      	
/.notdef      	/.notdef      	/.notdef      	/.notdef      	
/.notdef      	/.notdef      	/.notdef      	/.notdef      	
/.notdef      	/.notdef      	/.notdef      	/.notdef      	
/space        	/exclamdown   	/cent         	/sterling     	
/currency     	/yen          	/brokenbar    	/section      	
/dieresis     	/copyright    	/ordfeminine  	/guillemotleft	
/logicalnot   	/hyphen       	/registered   	/macron       	
/degree       	/plusminus    	/twosuperior  	/threesuperior	
/acute        	/mu           	/paragraph    	/bullet       	
/cedilla      	/onesuperior  	/ordmasculine 	/guillemotright	
/onequarter   	/onehalf      	/threequarters	/questiondown 	
/Agrave       	/Aacute       	/Acircumflex  	/Atilde       	
/Adieresis    	/Aring        	/AE           	/Ccedilla     	
/Egrave       	/Eacute       	/Ecircumflex  	/Edieresis    	
/Igrave       	/Iacute       	/Icircumflex  	/Idieresis    	
/Eth          	/Ntilde       	/Ograve       	/Oacute       	
/Ocircumflex  	/Otilde       	/Odieresis    	/multiply     	
/Oslash       	/Ugrave       	/Uacute       	/Ucircumflex  	
/Udieresis    	/Yacute       	/Thorn        	/germandbls   	
/agrave       	/aacute       	/acircumflex  	/atilde       	
/adieresis    	/aring        	/ae           	/ccedilla     	
/egrave       	/eacute       	/ecircumflex  	/edieresis    	
/igrave       	/iacute       	/icircumflex  	/idieresis    	
/eth          	/ntilde       	/ograve       	/oacute       	
/ocircumflex  	/otilde       	/odieresis    	/divide       	
/oslash       	/ugrave       	/uacute       	/ucircumflex  	
/udieresis    	/yacute       	/thorn        	/ydieresis    	
] def
%%EndResource
%%EndProlog
%%BeginSetup
%%IncludeResource: font Courier-Bold
%%IncludeResource: font Courier
/HFpt_w 10 def
/HFpt_h 10 def
/Courier-Bold /HF-gs-font MF
/HF /HF-gs-font findfont [HFpt_w 0 0 HFpt_h 0 0] makefont def
/Courier /F-gs-font MF
/F-gs-font 8 8 SF
/#copies 1 def
% Pagedevice definitions:
gs_languagelevel 1 gt {
  <<
    /PageSize [595 842] 
  >> setpagedevice
} if
%%BeginResource: procset Enscript-Header-simple 1.6.5 90

/do_header {	% print default simple header
  gsave
    d_header_x d_header_y HFpt_h 3 div add translate

    HF setfont
    user_header_p {
      5 0 moveto user_header_left_str show

      d_header_w user_header_center_str stringwidth pop sub 2 div
      0 moveto user_header_center_str show

      d_header_w user_header_right_str stringwidth pop sub 5 sub
      0 moveto user_header_right_str show
    } {
      5 0 moveto fname show
      45 0 rmoveto fmodstr show
      45 0 rmoveto pagenumstr show
    } ifelse

  grestore
} def
%%EndResource
/d_page_w 770 def
/d_page_h 559 def
/d_header_x 0 def
/d_header_y 544 def
/d_header_w 770 def
/d_header_h 15 def
/d_footer_x 0 def
/d_footer_y 0 def
/d_footer_w 770 def
/d_footer_h 0 def
/d_output_w 770 def
/d_output_h 544 def
/cols 2 def
%%EndSetup
%%Page: (1) 1
%%BeginPageSetup
_S
90 rotate
36 -577 translate
/pagenum 1 def
/fname (firfilt.ps) def
/fdir (.) def
/ftail (firfilt.ps) def
% User defined strings:
/fmodstr (Tue Nov 24 15:42:44 2015) def
/pagenumstr (1) def
/user_header_p false def
/user_footer_p false def
%%EndPageSetup
do_header
25.2 533 M (1:) s
39.6 533 M
(%!PS-Adobe-3.0) s
25.2 524 M (2:) s
39.6 524 M
(%%BoundingBox: 18 36 577 806) s
25.2 515 M (3:) s
39.6 515 M
(%%Title: Enscript Output) s
25.2 506 M (4:) s
39.6 506 M
(%%Creator: GNU Enscript 1.6.5.90) s
25.2 497 M (5:) s
39.6 497 M
(%%CreationDate: Tue Nov 24 15:42:44 2015) s
25.2 488 M (6:) s
39.6 488 M
(%%Orientation: Portrait) s
25.2 479 M (7:) s
39.6 479 M
(%%Pages: \(atend\)) s
25.2 470 M (8:) s
39.6 470 M
(%%DocumentMedia: A4 595 842 0 \(\) \(\)) s
25.2 461 M (9:) s
39.6 461 M
(%%DocumentNeededResources: \(atend\)) s
20.4 452 M (10:) s
39.6 452 M
(%%EndComments) s
20.4 443 M (11:) s
39.6 443 M
(%%BeginProlog) s
20.4 434 M (12:) s
39.6 434 M
(%%BeginResource: procset Enscript-Prolog 1.6.5 90) s
20.4 425 M (13:) s
39.6 425 M
(%) s
20.4 416 M (14:) s
39.6 416 M
(% Procedures.) s
20.4 407 M (15:) s
39.6 407 M
(%) s
20.4 398 M (16:) s
20.4 389 M (17:) s
39.6 389 M
(/_S {   % save current state) s
20.4 380 M (18:) s
39.6 380 M
(  /_s save def) s
20.4 371 M (19:) s
39.6 371 M
(} def) s
20.4 362 M (20:) s
39.6 362 M
(/_R {   % restore from saved state) s
20.4 353 M (21:) s
39.6 353 M
(  _s restore) s
20.4 344 M (22:) s
39.6 344 M
(} def) s
20.4 335 M (23:) s
20.4 326 M (24:) s
39.6 326 M
(/S {    % showpage protecting gstate) s
20.4 317 M (25:) s
39.6 317 M
(  gsave) s
20.4 308 M (26:) s
39.6 308 M
(  showpage) s
20.4 299 M (27:) s
39.6 299 M
(  grestore) s
20.4 290 M (28:) s
39.6 290 M
(} bind def) s
20.4 281 M (29:) s
20.4 272 M (30:) s
39.6 272 M
(/MF {   % fontname newfontname -> -     make a new encoded font) s
20.4 263 M (31:) s
39.6 263 M
(  /newfontname exch def) s
20.4 254 M (32:) s
39.6 254 M
(  /fontname exch def) s
20.4 245 M (33:) s
20.4 236 M (34:) s
39.6 236 M
(  /fontdict fontname findfont def) s
20.4 227 M (35:) s
39.6 227 M
(  /newfont fontdict maxlength dict def) s
20.4 218 M (36:) s
20.4 209 M (37:) s
39.6 209 M
(  fontdict {) s
20.4 200 M (38:) s
39.6 200 M
(    exch) s
20.4 191 M (39:) s
39.6 191 M
(    dup /FID eq {) s
20.4 182 M (40:) s
39.6 182 M
(      % skip FID pair) s
20.4 173 M (41:) s
39.6 173 M
(      pop pop) s
20.4 164 M (42:) s
39.6 164 M
(    } {) s
20.4 155 M (43:) s
39.6 155 M
(      % copy to the new font dictionary) s
20.4 146 M (44:) s
39.6 146 M
(      exch newfont 3 1 roll put) s
20.4 137 M (45:) s
39.6 137 M
(    } ifelse) s
20.4 128 M (46:) s
39.6 128 M
(  } forall) s
20.4 119 M (47:) s
20.4 110 M (48:) s
39.6 110 M
(  newfont /FontName newfontname put) s
20.4 101 M (49:) s
20.4 92 M (50:) s
39.6 92 M
(  % insert only valid encoding vectors) s
20.4 83 M (51:) s
39.6 83 M
(  encoding_vector length 256 eq {) s
20.4 74 M (52:) s
39.6 74 M
(    newfont /Encoding encoding_vector put) s
20.4 65 M (53:) s
39.6 65 M
(  } ) s
/Courier-Bold 8 8 SUF
0.627451 0.12549 0.941176 setrgbcolor
58.8 65 M
(if) s
/F-gs-font 8 8 SF
0 setgray
20.4 56 M (54:) s
20.4 47 M (55:) s
39.6 47 M
(  newfontname newfont definefont pop) s
20.4 38 M (56:) s
39.6 38 M
(} def) s
20.4 29 M (57:) s
20.4 20 M (58:) s
39.6 20 M
(/MF_PS { % fontname newfontname -> -    make a new font preserving its) s
5 11 M
( enc) s
20.4 2 M (59:) s
39.6 2 M
(  /newfontname exch def) s
405.4 533 M (60:) s
424.6 533 M
(  /fontname exch def) s
405.4 524 M (61:) s
405.4 515 M (62:) s
424.6 515 M
(  /fontdict fontname findfont def) s
405.4 506 M (63:) s
424.6 506 M
(  /newfont fontdict maxlength dict def) s
405.4 497 M (64:) s
405.4 488 M (65:) s
424.6 488 M
(  fontdict {) s
405.4 479 M (66:) s
424.6 479 M
(    exch) s
405.4 470 M (67:) s
424.6 470 M
(    dup /FID eq {) s
405.4 461 M (68:) s
424.6 461 M
(      % skip FID pair) s
405.4 452 M (69:) s
424.6 452 M
(      pop pop) s
405.4 443 M (70:) s
424.6 443 M
(    } {) s
405.4 434 M (71:) s
424.6 434 M
(      % copy to the new font dictionary) s
405.4 425 M (72:) s
424.6 425 M
(      exch newfont 3 1 roll put) s
405.4 416 M (73:) s
424.6 416 M
(    } ifelse) s
405.4 407 M (74:) s
424.6 407 M
(  } forall) s
405.4 398 M (75:) s
405.4 389 M (76:) s
424.6 389 M
(  newfont /FontName newfontname put) s
405.4 380 M (77:) s
405.4 371 M (78:) s
424.6 371 M
(  newfontname newfont definefont pop) s
405.4 362 M (79:) s
424.6 362 M
(} def) s
405.4 353 M (80:) s
405.4 344 M (81:) s
424.6 344 M
(/SF { % fontname width height -> -      set a new font) s
405.4 335 M (82:) s
424.6 335 M
(  /height exch def) s
405.4 326 M (83:) s
424.6 326 M
(  /width exch def) s
405.4 317 M (84:) s
405.4 308 M (85:) s
424.6 308 M
(  findfont) s
405.4 299 M (86:) s
424.6 299 M
(  [width 0 0 height 0 0] makefont setfont) s
405.4 290 M (87:) s
424.6 290 M
(} def) s
405.4 281 M (88:) s
405.4 272 M (89:) s
424.6 272 M
(/SUF { % fontname width height -> -     set a new user font) s
405.4 263 M (90:) s
424.6 263 M
(  /height exch def) s
405.4 254 M (91:) s
424.6 254 M
(  /width exch def) s
405.4 245 M (92:) s
405.4 236 M (93:) s
424.6 236 M
(  /F-gs-user-font MF) s
405.4 227 M (94:) s
424.6 227 M
(  /F-gs-user-font width height SF) s
405.4 218 M (95:) s
424.6 218 M
(} def) s
405.4 209 M (96:) s
405.4 200 M (97:) s
424.6 200 M
(/SUF_PS { % fontname width height -> -  set a new user font preserving) s
390 191 M
( its enc) s
405.4 182 M (98:) s
424.6 182 M
(  /height exch def) s
405.4 173 M (99:) s
424.6 173 M
(  /width exch def) s
400.6 164 M (100:) s
400.6 155 M (101:) s
424.6 155 M
(  /F-gs-user-font MF_PS) s
400.6 146 M (102:) s
424.6 146 M
(  /F-gs-user-font width height SF) s
400.6 137 M (103:) s
424.6 137 M
(} def) s
400.6 128 M (104:) s
400.6 119 M (105:) s
424.6 119 M
(/M {moveto} bind def) s
400.6 110 M (106:) s
424.6 110 M
(/s {show} bind def) s
400.6 101 M (107:) s
400.6 92 M (108:) s
424.6 92 M
(/Box {  % x y w h -> -                  define box path) s
400.6 83 M (109:) s
424.6 83 M
(  /d_h exch def /d_w exch def /d_y exch def /d_x exch def) s
400.6 74 M (110:) s
424.6 74 M
(  d_x d_y  moveto) s
400.6 65 M (111:) s
424.6 65 M
(  d_w 0 rlineto) s
400.6 56 M (112:) s
424.6 56 M
(  0 d_h rlineto) s
400.6 47 M (113:) s
424.6 47 M
(  d_w neg 0 rlineto) s
400.6 38 M (114:) s
424.6 38 M
(  closepath) s
400.6 29 M (115:) s
424.6 29 M
(} def) s
400.6 20 M (116:) s
400.6 11 M (117:) s
424.6 11 M
(/bgs {  % x y height blskip gray str -> -       show string with bg co) s
390 2 M
(lor) s
_R
S
%%Page: (2) 2
%%BeginPageSetup
_S
90 rotate
36 -577 translate
/pagenum 2 def
/fname (firfilt.ps) def
/fdir (.) def
/ftail (firfilt.ps) def
% User defined strings:
/fmodstr (Tue Nov 24 15:42:44 2015) def
/pagenumstr (2) def
/user_header_p false def
/user_footer_p false def
%%EndPageSetup
do_header
15.6 533 M (118:) s
39.6 533 M
(  /str exch def) s
15.6 524 M (119:) s
39.6 524 M
(  /gray exch def) s
15.6 515 M (120:) s
39.6 515 M
(  /blskip exch def) s
15.6 506 M (121:) s
39.6 506 M
(  /height exch def) s
15.6 497 M (122:) s
39.6 497 M
(  /y exch def) s
15.6 488 M (123:) s
39.6 488 M
(  /x exch def) s
15.6 479 M (124:) s
15.6 470 M (125:) s
39.6 470 M
(  gsave) s
15.6 461 M (126:) s
39.6 461 M
(    x y blskip sub str stringwidth pop height Box) s
15.6 452 M (127:) s
39.6 452 M
(    gray setgray) s
15.6 443 M (128:) s
39.6 443 M
(    fill) s
15.6 434 M (129:) s
39.6 434 M
(  grestore) s
15.6 425 M (130:) s
39.6 425 M
(  x y M str s) s
15.6 416 M (131:) s
39.6 416 M
(} def) s
15.6 407 M (132:) s
15.6 398 M (133:) s
39.6 398 M
(/bgcs { % x y height blskip red green blue str -> -  show string with ) s
5 389 M
(bg color) s
15.6 380 M (134:) s
39.6 380 M
(  /str exch def) s
15.6 371 M (135:) s
39.6 371 M
(  /blue exch def) s
15.6 362 M (136:) s
39.6 362 M
(  /green exch def) s
15.6 353 M (137:) s
39.6 353 M
(  /red exch def) s
15.6 344 M (138:) s
39.6 344 M
(  /blskip exch def) s
15.6 335 M (139:) s
39.6 335 M
(  /height exch def) s
15.6 326 M (140:) s
39.6 326 M
(  /y exch def) s
15.6 317 M (141:) s
39.6 317 M
(  /x exch def) s
15.6 308 M (142:) s
15.6 299 M (143:) s
39.6 299 M
(  gsave) s
15.6 290 M (144:) s
39.6 290 M
(    x y blskip sub str stringwidth pop height Box) s
15.6 281 M (145:) s
39.6 281 M
(    red green blue setrgbcolor) s
15.6 272 M (146:) s
39.6 272 M
(    fill) s
15.6 263 M (147:) s
39.6 263 M
(  grestore) s
15.6 254 M (148:) s
39.6 254 M
(  x y M str s) s
15.6 245 M (149:) s
39.6 245 M
(} def) s
15.6 236 M (150:) s
15.6 227 M (151:) s
39.6 227 M
(% Highlight bars.) s
15.6 218 M (152:) s
39.6 218 M
(/highlight_bars {       % nlines lineheight output_y_margin gray -> -) s
15.6 209 M (153:) s
39.6 209 M
(  gsave) s
15.6 200 M (154:) s
39.6 200 M
(    setgray) s
15.6 191 M (155:) s
39.6 191 M
(    /ymarg exch def) s
15.6 182 M (156:) s
39.6 182 M
(    /lineheight exch def) s
15.6 173 M (157:) s
39.6 173 M
(    /nlines exch def) s
15.6 164 M (158:) s
15.6 155 M (159:) s
39.6 155 M
(    % This 2 is just a magic number to sync highlight lines to text.) s
15.6 146 M (160:) s
39.6 146 M
(    0 d_header_y ymarg sub 2 sub translate) s
15.6 137 M (161:) s
15.6 128 M (162:) s
39.6 128 M
(    /cw d_output_w cols div def) s
15.6 119 M (163:) s
39.6 119 M
(    /nrows d_output_h ymarg 2 mul sub lineheight div cvi def) s
15.6 110 M (164:) s
15.6 101 M (165:) s
39.6 101 M
(    % ) s
/Courier-Bold 8 8 SUF
0.627451 0.12549 0.941176 setrgbcolor
68.4 101 M
(for) s
/F-gs-font 8 8 SF
0 setgray
82.8 101 M
( each column) s
15.6 92 M (166:) s
39.6 92 M
(    0 1 cols 1 sub {) s
15.6 83 M (167:) s
39.6 83 M
(      cw mul /xp exch def) s
15.6 74 M (168:) s
15.6 65 M (169:) s
39.6 65 M
(      % ) s
/Courier-Bold 8 8 SUF
0.627451 0.12549 0.941176 setrgbcolor
78 65 M
(for) s
/F-gs-font 8 8 SF
0 setgray
92.4 65 M
( each rows) s
15.6 56 M (170:) s
39.6 56 M
(      0 1 nrows 1 sub {) s
15.6 47 M (171:) s
39.6 47 M
(        /rn exch def) s
15.6 38 M (172:) s
39.6 38 M
(        rn lineheight mul neg /yp exch def) s
15.6 29 M (173:) s
39.6 29 M
(        rn nlines idiv 2 mod 0 eq {) s
15.6 20 M (174:) s
39.6 20 M
(          % Draw highlight bar.  4 is just a magic indentation.) s
15.6 11 M (175:) s
39.6 11 M
(          xp 4 add yp cw 8 sub lineheight neg Box fill) s
15.6 2 M (176:) s
39.6 2 M
(        } ) s
/Courier-Bold 8 8 SUF
0.627451 0.12549 0.941176 setrgbcolor
87.6 2 M
(if) s
/F-gs-font 8 8 SF
0 setgray
400.6 533 M (177:) s
424.6 533 M
(      } ) s
/Courier-Bold 8 8 SUF
0.627451 0.12549 0.941176 setrgbcolor
463 533 M
(for) s
/F-gs-font 8 8 SF
0 setgray
400.6 524 M (178:) s
424.6 524 M
(    } ) s
/Courier-Bold 8 8 SUF
0.627451 0.12549 0.941176 setrgbcolor
453.4 524 M
(for) s
/F-gs-font 8 8 SF
0 setgray
400.6 515 M (179:) s
400.6 506 M (180:) s
424.6 506 M
(  grestore) s
400.6 497 M (181:) s
424.6 497 M
(} def) s
400.6 488 M (182:) s
400.6 479 M (183:) s
424.6 479 M
(% Line highlight bar.) s
400.6 470 M (184:) s
424.6 470 M
(/line_highlight {       % x y width height gray -> -) s
400.6 461 M (185:) s
424.6 461 M
(  gsave) s
400.6 452 M (186:) s
424.6 452 M
(    /gray exch def) s
400.6 443 M (187:) s
424.6 443 M
(    Box gray setgray fill) s
400.6 434 M (188:) s
424.6 434 M
(  grestore) s
400.6 425 M (189:) s
424.6 425 M
(} def) s
400.6 416 M (190:) s
400.6 407 M (191:) s
424.6 407 M
(% Column separator lines.) s
400.6 398 M (192:) s
424.6 398 M
(/column_lines {) s
400.6 389 M (193:) s
424.6 389 M
(  gsave) s
400.6 380 M (194:) s
424.6 380 M
(    .1 setlinewidth) s
400.6 371 M (195:) s
424.6 371 M
(    0 d_footer_h translate) s
400.6 362 M (196:) s
424.6 362 M
(    /cw d_output_w cols div def) s
400.6 353 M (197:) s
424.6 353 M
(    1 1 cols 1 sub {) s
400.6 344 M (198:) s
424.6 344 M
(      cw mul 0 moveto) s
400.6 335 M (199:) s
424.6 335 M
(      0 d_output_h rlineto stroke) s
400.6 326 M (200:) s
424.6 326 M
(    } ) s
/Courier-Bold 8 8 SUF
0.627451 0.12549 0.941176 setrgbcolor
453.4 326 M
(for) s
/F-gs-font 8 8 SF
0 setgray
400.6 317 M (201:) s
424.6 317 M
(  grestore) s
400.6 308 M (202:) s
424.6 308 M
(} def) s
400.6 299 M (203:) s
400.6 290 M (204:) s
424.6 290 M
(% Column borders.) s
400.6 281 M (205:) s
424.6 281 M
(/column_borders {) s
400.6 272 M (206:) s
424.6 272 M
(  gsave) s
400.6 263 M (207:) s
424.6 263 M
(    .1 setlinewidth) s
400.6 254 M (208:) s
424.6 254 M
(    0 d_footer_h moveto) s
400.6 245 M (209:) s
424.6 245 M
(    0 d_output_h rlineto) s
400.6 236 M (210:) s
424.6 236 M
(    d_output_w 0 rlineto) s
400.6 227 M (211:) s
424.6 227 M
(    0 d_output_h neg rlineto) s
400.6 218 M (212:) s
424.6 218 M
(    closepath stroke) s
400.6 209 M (213:) s
424.6 209 M
(  grestore) s
400.6 200 M (214:) s
424.6 200 M
(} def) s
400.6 191 M (215:) s
400.6 182 M (216:) s
424.6 182 M
(% Do the actual underlay drawing) s
400.6 173 M (217:) s
424.6 173 M
(/draw_underlay {) s
400.6 164 M (218:) s
424.6 164 M
(  ul_style 0 eq {) s
400.6 155 M (219:) s
424.6 155 M
(    ul_str true charpath stroke) s
400.6 146 M (220:) s
424.6 146 M
(  } {) s
400.6 137 M (221:) s
424.6 137 M
(    ul_str show) s
400.6 128 M (222:) s
424.6 128 M
(  } ifelse) s
400.6 119 M (223:) s
424.6 119 M
(} def) s
400.6 110 M (224:) s
400.6 101 M (225:) s
424.6 101 M
(% Underlay) s
400.6 92 M (226:) s
424.6 92 M
(/underlay {     % - -> -) s
400.6 83 M (227:) s
424.6 83 M
(  gsave) s
400.6 74 M (228:) s
424.6 74 M
(    0 d_page_h translate) s
400.6 65 M (229:) s
424.6 65 M
(    d_page_h neg d_page_w atan rotate) s
400.6 56 M (230:) s
400.6 47 M (231:) s
424.6 47 M
(    ul_gray setgray) s
400.6 38 M (232:) s
424.6 38 M
(    ul_font setfont) s
400.6 29 M (233:) s
424.6 29 M
(    /dw d_page_h dup mul d_page_w dup mul add sqrt def) s
400.6 20 M (234:) s
424.6 20 M
(    ul_str stringwidth pop dw exch sub 2 div ul_h_ptsize -2 div moveto) s
400.6 11 M (235:) s
424.6 11 M
(    draw_underlay) s
400.6 2 M (236:) s
424.6 2 M
(  grestore) s
_R
S
%%Page: (3) 3
%%BeginPageSetup
_S
90 rotate
36 -577 translate
/pagenum 3 def
/fname (firfilt.ps) def
/fdir (.) def
/ftail (firfilt.ps) def
% User defined strings:
/fmodstr (Tue Nov 24 15:42:44 2015) def
/pagenumstr (3) def
/user_header_p false def
/user_footer_p false def
%%EndPageSetup
do_header
15.6 533 M (237:) s
39.6 533 M
(} def) s
15.6 524 M (238:) s
15.6 515 M (239:) s
39.6 515 M
(/user_underlay {        % - -> -) s
15.6 506 M (240:) s
39.6 506 M
(  gsave) s
15.6 497 M (241:) s
39.6 497 M
(    ul_x ul_y translate) s
15.6 488 M (242:) s
39.6 488 M
(    ul_angle rotate) s
15.6 479 M (243:) s
39.6 479 M
(    ul_gray setgray) s
15.6 470 M (244:) s
39.6 470 M
(    ul_font setfont) s
15.6 461 M (245:) s
39.6 461 M
(    0 0 ul_h_ptsize 2 div sub moveto) s
15.6 452 M (246:) s
39.6 452 M
(    draw_underlay) s
15.6 443 M (247:) s
39.6 443 M
(  grestore) s
15.6 434 M (248:) s
39.6 434 M
(} def) s
15.6 425 M (249:) s
15.6 416 M (250:) s
39.6 416 M
(% Page prefeed) s
15.6 407 M (251:) s
39.6 407 M
(/page_prefeed {         % bool -> -) s
15.6 398 M (252:) s
39.6 398 M
(  statusdict /prefeed known {) s
15.6 389 M (253:) s
39.6 389 M
(    statusdict exch /prefeed exch put) s
15.6 380 M (254:) s
39.6 380 M
(  } {) s
15.6 371 M (255:) s
39.6 371 M
(    pop) s
15.6 362 M (256:) s
39.6 362 M
(  } ifelse) s
15.6 353 M (257:) s
39.6 353 M
(} def) s
15.6 344 M (258:) s
15.6 335 M (259:) s
39.6 335 M
(% Wrapped line markers) s
15.6 326 M (260:) s
39.6 326 M
(/wrapped_line_mark {    % x y charwith charheight type -> -) s
15.6 317 M (261:) s
39.6 317 M
(  /type exch def) s
15.6 308 M (262:) s
39.6 308 M
(  /h exch def) s
15.6 299 M (263:) s
39.6 299 M
(  /w exch def) s
15.6 290 M (264:) s
39.6 290 M
(  /y exch def) s
15.6 281 M (265:) s
39.6 281 M
(  /x exch def) s
15.6 272 M (266:) s
15.6 263 M (267:) s
39.6 263 M
(  type 2 eq {) s
15.6 254 M (268:) s
39.6 254 M
(    % Black boxes \(like TeX does\)) s
15.6 245 M (269:) s
39.6 245 M
(    gsave) s
15.6 236 M (270:) s
39.6 236 M
(      0 setlinewidth) s
15.6 227 M (271:) s
39.6 227 M
(      x w 4 div add y M) s
15.6 218 M (272:) s
39.6 218 M
(      0 h rlineto w 2 div 0 rlineto 0 h neg rlineto) s
15.6 209 M (273:) s
39.6 209 M
(      closepath fill) s
15.6 200 M (274:) s
39.6 200 M
(    grestore) s
15.6 191 M (275:) s
39.6 191 M
(  } {) s
15.6 182 M (276:) s
39.6 182 M
(    type 3 eq {) s
15.6 173 M (277:) s
39.6 173 M
(      % Small arrows) s
15.6 164 M (278:) s
39.6 164 M
(      gsave) s
15.6 155 M (279:) s
39.6 155 M
(        .2 setlinewidth) s
15.6 146 M (280:) s
39.6 146 M
(        x w 2 div add y h 2 div add M) s
15.6 137 M (281:) s
39.6 137 M
(        w 4 div 0 rlineto) s
15.6 128 M (282:) s
39.6 128 M
(        x w 4 div add y lineto stroke) s
15.6 119 M (283:) s
15.6 110 M (284:) s
39.6 110 M
(        x w 4 div add w 8 div add y h 4 div add M) s
15.6 101 M (285:) s
39.6 101 M
(        x w 4 div add y lineto) s
15.6 92 M (286:) s
39.6 92 M
(        w 4 div h 8 div rlineto stroke) s
15.6 83 M (287:) s
39.6 83 M
(      grestore) s
15.6 74 M (288:) s
39.6 74 M
(    } {) s
15.6 65 M (289:) s
39.6 65 M
(      % ) s
/Courier-Bold 8 8 SUF
0.627451 0.12549 0.941176 setrgbcolor
78 65 M
(do) s
/F-gs-font 8 8 SF
0 setgray
87.6 65 M
( nothing) s
15.6 56 M (290:) s
39.6 56 M
(    } ifelse) s
15.6 47 M (291:) s
39.6 47 M
(  } ifelse) s
15.6 38 M (292:) s
39.6 38 M
(} def) s
15.6 29 M (293:) s
15.6 20 M (294:) s
39.6 20 M
(% EPSF import.) s
15.6 11 M (295:) s
15.6 2 M (296:) s
39.6 2 M
(/BeginEPSF {) s
400.6 533 M (297:) s
424.6 533 M
(  /b4_Inc_state save def                % Save state ) s
/Courier-Bold 8 8 SUF
0.627451 0.12549 0.941176 setrgbcolor
679 533 M
(for) s
/F-gs-font 8 8 SF
0 setgray
693.4 533 M
( cleanup) s
400.6 524 M (298:) s
424.6 524 M
(  /dict_count countdictstack def        % Count objects on dict stack) s
400.6 515 M (299:) s
424.6 515 M
(  /op_count count 1 sub def             % Count objects on operand sta) s
390 506 M
(ck) s
400.6 497 M (300:) s
424.6 497 M
(  userdict begin) s
400.6 488 M (301:) s
424.6 488 M
(  /showpage { } def) s
400.6 479 M (302:) s
424.6 479 M
(  0 setgray 0 setlinecap) s
400.6 470 M (303:) s
424.6 470 M
(  1 setlinewidth 0 setlinejoin) s
400.6 461 M (304:) s
424.6 461 M
(  10 setmiterlimit [ ] 0 setdash newpath) s
400.6 452 M (305:) s
424.6 452 M
(  /languagelevel where {) s
400.6 443 M (306:) s
424.6 443 M
(    pop languagelevel) s
400.6 434 M (307:) s
424.6 434 M
(    1 ne {) s
400.6 425 M (308:) s
424.6 425 M
(      false setstrokeadjust false setoverprint) s
400.6 416 M (309:) s
424.6 416 M
(    } ) s
/Courier-Bold 8 8 SUF
0.627451 0.12549 0.941176 setrgbcolor
453.4 416 M
(if) s
/F-gs-font 8 8 SF
0 setgray
400.6 407 M (310:) s
424.6 407 M
(  } ) s
/Courier-Bold 8 8 SUF
0.627451 0.12549 0.941176 setrgbcolor
443.8 407 M
(if) s
/F-gs-font 8 8 SF
0 setgray
400.6 398 M (311:) s
424.6 398 M
(} bind def) s
400.6 389 M (312:) s
400.6 380 M (313:) s
424.6 380 M
(/EndEPSF {) s
400.6 371 M (314:) s
424.6 371 M
(  count op_count sub { pos } repeat     % Clean up stacks) s
400.6 362 M (315:) s
424.6 362 M
(  countdictstack dict_count sub { end } repeat) s
400.6 353 M (316:) s
424.6 353 M
(  b4_Inc_state restore) s
400.6 344 M (317:) s
424.6 344 M
(} bind def) s
400.6 335 M (318:) s
400.6 326 M (319:) s
424.6 326 M
(% Check PostScript language level.) s
400.6 317 M (320:) s
424.6 317 M
(/languagelevel where {) s
400.6 308 M (321:) s
424.6 308 M
(  pop /gs_languagelevel languagelevel def) s
400.6 299 M (322:) s
424.6 299 M
(} {) s
400.6 290 M (323:) s
424.6 290 M
(  /gs_languagelevel 1 def) s
400.6 281 M (324:) s
424.6 281 M
(} ifelse) s
400.6 272 M (325:) s
424.6 272 M
(%%EndResource) s
400.6 263 M (326:) s
424.6 263 M
(%%BeginResource: procset Enscript-Encoding-88591 1.6.5 90) s
400.6 254 M (327:) s
424.6 254 M
(/encoding_vector [) s
400.6 245 M (328:) s
424.6 245 M
(/.notdef        /.notdef        /.notdef        /.notdef        ) s
400.6 236 M (329:) s
424.6 236 M
(/.notdef        /.notdef        /.notdef        /.notdef        ) s
400.6 227 M (330:) s
424.6 227 M
(/.notdef        /.notdef        /.notdef        /.notdef        ) s
400.6 218 M (331:) s
424.6 218 M
(/.notdef        /.notdef        /.notdef        /.notdef        ) s
400.6 209 M (332:) s
424.6 209 M
(/.notdef        /.notdef        /.notdef        /.notdef        ) s
400.6 200 M (333:) s
424.6 200 M
(/.notdef        /.notdef        /.notdef        /.notdef        ) s
400.6 191 M (334:) s
424.6 191 M
(/.notdef        /.notdef        /.notdef        /.notdef        ) s
400.6 182 M (335:) s
424.6 182 M
(/.notdef        /.notdef        /.notdef        /.notdef        ) s
400.6 173 M (336:) s
424.6 173 M
(/space          /exclam         /quotedbl       /numbersign     ) s
400.6 164 M (337:) s
424.6 164 M
(/dollar         /percent        /ampersand      /quoteright     ) s
400.6 155 M (338:) s
424.6 155 M
(/parenleft      /parenright     /asterisk       /plus           ) s
400.6 146 M (339:) s
424.6 146 M
(/comma          /hyphen         /period         /slash          ) s
400.6 137 M (340:) s
424.6 137 M
(/zero           /one            /two            /three          ) s
400.6 128 M (341:) s
424.6 128 M
(/four           /five           /six            /seven          ) s
400.6 119 M (342:) s
424.6 119 M
(/eight          /nine           /colon          /semicolon      ) s
400.6 110 M (343:) s
424.6 110 M
(/less           /equal          /greater        /question       ) s
400.6 101 M (344:) s
424.6 101 M
(/at             /A              /B              /C              ) s
400.6 92 M (345:) s
424.6 92 M
(/D              /E              /F              /G              ) s
400.6 83 M (346:) s
424.6 83 M
(/H              /I              /J              /K              ) s
400.6 74 M (347:) s
424.6 74 M
(/L              /M              /N              /O              ) s
400.6 65 M (348:) s
424.6 65 M
(/P              /Q              /R              /S              ) s
400.6 56 M (349:) s
424.6 56 M
(/T              /U              /V              /W              ) s
400.6 47 M (350:) s
424.6 47 M
(/X              /Y              /Z              /bracketleft    ) s
400.6 38 M (351:) s
424.6 38 M
(/backslash      /bracketright   /asciicircum    /underscore     ) s
400.6 29 M (352:) s
424.6 29 M
(/quoteleft      /a              /b              /c              ) s
400.6 20 M (353:) s
424.6 20 M
(/d              /e              /f              /g              ) s
400.6 11 M (354:) s
424.6 11 M
(/h              /i              /j              /k              ) s
400.6 2 M (355:) s
424.6 2 M
(/l              /m              /n              /o              ) s
_R
S
%%Page: (4) 4
%%BeginPageSetup
_S
90 rotate
36 -577 translate
/pagenum 4 def
/fname (firfilt.ps) def
/fdir (.) def
/ftail (firfilt.ps) def
% User defined strings:
/fmodstr (Tue Nov 24 15:42:44 2015) def
/pagenumstr (4) def
/user_header_p false def
/user_footer_p false def
%%EndPageSetup
do_header
15.6 533 M (356:) s
39.6 533 M
(/p              /q              /r              /s              ) s
15.6 524 M (357:) s
39.6 524 M
(/t              /u              /v              /w              ) s
15.6 515 M (358:) s
39.6 515 M
(/x              /y              /z              /braceleft      ) s
15.6 506 M (359:) s
39.6 506 M
(/bar            /braceright     /tilde          /.notdef        ) s
15.6 497 M (360:) s
39.6 497 M
(/.notdef        /.notdef        /.notdef        /.notdef        ) s
15.6 488 M (361:) s
39.6 488 M
(/.notdef        /.notdef        /.notdef        /.notdef        ) s
15.6 479 M (362:) s
39.6 479 M
(/.notdef        /.notdef        /.notdef        /.notdef        ) s
15.6 470 M (363:) s
39.6 470 M
(/.notdef        /.notdef        /.notdef        /.notdef        ) s
15.6 461 M (364:) s
39.6 461 M
(/.notdef        /.notdef        /.notdef        /.notdef        ) s
15.6 452 M (365:) s
39.6 452 M
(/.notdef        /.notdef        /.notdef        /.notdef        ) s
15.6 443 M (366:) s
39.6 443 M
(/.notdef        /.notdef        /.notdef        /.notdef        ) s
15.6 434 M (367:) s
39.6 434 M
(/.notdef        /.notdef        /.notdef        /.notdef        ) s
15.6 425 M (368:) s
39.6 425 M
(/space          /exclamdown     /cent           /sterling       ) s
15.6 416 M (369:) s
39.6 416 M
(/currency       /yen            /brokenbar      /section        ) s
15.6 407 M (370:) s
39.6 407 M
(/dieresis       /copyright      /ordfeminine    /guillemotleft  ) s
15.6 398 M (371:) s
39.6 398 M
(/logicalnot     /hyphen         /registered     /macron         ) s
15.6 389 M (372:) s
39.6 389 M
(/degree         /plusminus      /twosuperior    /threesuperior  ) s
15.6 380 M (373:) s
39.6 380 M
(/acute          /mu             /paragraph      /bullet         ) s
15.6 371 M (374:) s
39.6 371 M
(/cedilla        /onesuperior    /ordmasculine   /guillemotright ) s
15.6 362 M (375:) s
39.6 362 M
(/onequarter     /onehalf        /threequarters  /questiondown   ) s
15.6 353 M (376:) s
39.6 353 M
(/Agrave         /Aacute         /Acircumflex    /Atilde         ) s
15.6 344 M (377:) s
39.6 344 M
(/Adieresis      /Aring          /AE             /Ccedilla       ) s
15.6 335 M (378:) s
39.6 335 M
(/Egrave         /Eacute         /Ecircumflex    /Edieresis      ) s
15.6 326 M (379:) s
39.6 326 M
(/Igrave         /Iacute         /Icircumflex    /Idieresis      ) s
15.6 317 M (380:) s
39.6 317 M
(/Eth            /Ntilde         /Ograve         /Oacute         ) s
15.6 308 M (381:) s
39.6 308 M
(/Ocircumflex    /Otilde         /Odieresis      /multiply       ) s
15.6 299 M (382:) s
39.6 299 M
(/Oslash         /Ugrave         /Uacute         /Ucircumflex    ) s
15.6 290 M (383:) s
39.6 290 M
(/Udieresis      /Yacute         /Thorn          /germandbls     ) s
15.6 281 M (384:) s
39.6 281 M
(/agrave         /aacute         /acircumflex    /atilde         ) s
15.6 272 M (385:) s
39.6 272 M
(/adieresis      /aring          /ae             /ccedilla       ) s
15.6 263 M (386:) s
39.6 263 M
(/egrave         /eacute         /ecircumflex    /edieresis      ) s
15.6 254 M (387:) s
39.6 254 M
(/igrave         /iacute         /icircumflex    /idieresis      ) s
15.6 245 M (388:) s
39.6 245 M
(/eth            /ntilde         /ograve         /oacute         ) s
15.6 236 M (389:) s
39.6 236 M
(/ocircumflex    /otilde         /odieresis      /divide         ) s
15.6 227 M (390:) s
39.6 227 M
(/oslash         /ugrave         /uacute         /ucircumflex    ) s
15.6 218 M (391:) s
39.6 218 M
(/udieresis      /yacute         /thorn          /ydieresis      ) s
15.6 209 M (392:) s
39.6 209 M
(] def) s
15.6 200 M (393:) s
39.6 200 M
(%%EndResource) s
15.6 191 M (394:) s
39.6 191 M
(%%EndProlog) s
15.6 182 M (395:) s
39.6 182 M
(%%BeginSetup) s
15.6 173 M (396:) s
39.6 173 M
(%%IncludeResource: font Courier-Bold) s
15.6 164 M (397:) s
39.6 164 M
(%%IncludeResource: font Courier) s
15.6 155 M (398:) s
39.6 155 M
(/HFpt_w 10 def) s
15.6 146 M (399:) s
39.6 146 M
(/HFpt_h 10 def) s
15.6 137 M (400:) s
39.6 137 M
(/Courier-Bold /HF-gs-font MF) s
15.6 128 M (401:) s
39.6 128 M
(/HF /HF-gs-font findfont [HFpt_w 0 0 HFpt_h 0 0] makefont def) s
15.6 119 M (402:) s
39.6 119 M
(/Courier /F-gs-font MF) s
15.6 110 M (403:) s
39.6 110 M
(/F-gs-font 10 10 SF) s
15.6 101 M (404:) s
39.6 101 M
(/#copies 1 def) s
15.6 92 M (405:) s
39.6 92 M
(% Pagedevice definitions:) s
15.6 83 M (406:) s
39.6 83 M
(gs_languagelevel 1 gt {) s
15.6 74 M (407:) s
39.6 74 M
(  <<) s
15.6 65 M (408:) s
39.6 65 M
(    /PageSize [595 842] ) s
15.6 56 M (409:) s
39.6 56 M
(  >> setpagedevice) s
15.6 47 M (410:) s
39.6 47 M
(} ) s
/Courier-Bold 8 8 SUF
0.627451 0.12549 0.941176 setrgbcolor
49.2 47 M
(if) s
/F-gs-font 8 8 SF
0 setgray
15.6 38 M (411:) s
39.6 38 M
(%%BeginResource: procset Enscript-Header-simple 1.6.5 90) s
15.6 29 M (412:) s
15.6 20 M (413:) s
39.6 20 M
(/do_header {    % print ) s
/Courier-Bold 8 8 SUF
0.627451 0.12549 0.941176 setrgbcolor
154.8 20 M
(default) s
/F-gs-font 8 8 SF
0 setgray
188.4 20 M
( simple header) s
15.6 11 M (414:) s
39.6 11 M
(  gsave) s
15.6 2 M (415:) s
39.6 2 M
(    d_header_x d_header_y HFpt_h 3 div add translate) s
400.6 533 M (416:) s
400.6 524 M (417:) s
424.6 524 M
(    HF setfont) s
400.6 515 M (418:) s
424.6 515 M
(    user_header_p {) s
400.6 506 M (419:) s
424.6 506 M
(      5 0 moveto user_header_left_str show) s
400.6 497 M (420:) s
400.6 488 M (421:) s
424.6 488 M
(      d_header_w user_header_center_str stringwidth pop sub 2 div) s
400.6 479 M (422:) s
424.6 479 M
(      0 moveto user_header_center_str show) s
400.6 470 M (423:) s
400.6 461 M (424:) s
424.6 461 M
(      d_header_w user_header_right_str stringwidth pop sub 5 sub) s
400.6 452 M (425:) s
424.6 452 M
(      0 moveto user_header_right_str show) s
400.6 443 M (426:) s
424.6 443 M
(    } {) s
400.6 434 M (427:) s
424.6 434 M
(      5 0 moveto fname show) s
400.6 425 M (428:) s
424.6 425 M
(      45 0 rmoveto fmodstr show) s
400.6 416 M (429:) s
424.6 416 M
(      45 0 rmoveto pagenumstr show) s
400.6 407 M (430:) s
424.6 407 M
(    } ifelse) s
400.6 398 M (431:) s
400.6 389 M (432:) s
424.6 389 M
(  grestore) s
400.6 380 M (433:) s
424.6 380 M
(} def) s
400.6 371 M (434:) s
424.6 371 M
(%%EndResource) s
400.6 362 M (435:) s
424.6 362 M
(/d_page_w 559 def) s
400.6 353 M (436:) s
424.6 353 M
(/d_page_h 770 def) s
400.6 344 M (437:) s
424.6 344 M
(/d_header_x 0 def) s
400.6 335 M (438:) s
424.6 335 M
(/d_header_y 755 def) s
400.6 326 M (439:) s
424.6 326 M
(/d_header_w 559 def) s
400.6 317 M (440:) s
424.6 317 M
(/d_header_h 15 def) s
400.6 308 M (441:) s
424.6 308 M
(/d_footer_x 0 def) s
400.6 299 M (442:) s
424.6 299 M
(/d_footer_y 0 def) s
400.6 290 M (443:) s
424.6 290 M
(/d_footer_w 559 def) s
400.6 281 M (444:) s
424.6 281 M
(/d_footer_h 0 def) s
400.6 272 M (445:) s
424.6 272 M
(/d_output_w 559 def) s
400.6 263 M (446:) s
424.6 263 M
(/d_output_h 755 def) s
400.6 254 M (447:) s
424.6 254 M
(/cols 1 def) s
400.6 245 M (448:) s
424.6 245 M
(%%EndSetup) s
400.6 236 M (449:) s
424.6 236 M
(%%Trailer) s
400.6 227 M (450:) s
424.6 227 M
(%%Pages: 0) s
400.6 218 M (451:) s
424.6 218 M
(%%DocumentNeededResources: font Courier-Bold Courier ) s
400.6 209 M (452:) s
424.6 209 M
(%%EOF) s
_R
S
%%Trailer
%%Pages: 4
%%DocumentNeededResources: font Courier-Bold Courier 
%%EOF
