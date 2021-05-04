% ==============================================================================
% my-resume.cls
% ==============================================================================

% A class to do stuff.
% ------------------------------------------------------------------------------

% CLASS OPTIONS
% ------------------------------------------------------------------------------
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{resume}[2020/11/17 my-resume v0.1, my own resume/CV class.]

% CLASS OPTIONS
% ------------------------------------------------------------------------------
% Option to have a single sided document, i.e. the highlight bar is always left
% or have a two sided document where the highlight bar is alternating, i.e.
% always on the same edge of the paper
\RequirePackage{ifthen}
\newboolean{@singleordouble}
\setboolean{@singleordouble}{true}
\DeclareOption{singlesided}{\setboolean{@singleordouble}{true}}
\DeclareOption{doublesided}{\setboolean{@singleordouble}{false}}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrartcl}}
\ProcessOptions*

\ifthenelse{\boolean{@singleordouble}}
    {\PassOptionsToClass{oneside}{scrartcl}}
    {\PassOptionsToClass{twoside}{scrartcl}}

\LoadClass{scrartcl}

% REQUIRED PACKAGES
% ------------------------------------------------------------------------------
% \RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{tikz}
\usetikzlibrary{arrows}
\RequirePackage[skins]{tcolorbox}       % somehow required for tikz to work at all
\RequirePackage{graphicx}
\RequirePackage{xcolor}
\RequirePackage{fontawesome5}
\RequirePackage{academicons}

% FILTER IRRELEVANT WARNINGS
% ------------------------------------------------------------------------------
\RequirePackage{silence}
% The page header is deliberately disabled in my-resume, so the warning by
% scrlayer-scrpage is invalid.
\WarningFilter{scrlayer-scrpage}{Very small head height detected!}

% DEFINE GEOMETRY
% ------------------------------------------------------------------------------
\newlength\highlightwidth
\newlength\headerheight
\newlength\marginleft
\newlength\marginright
\newlength\margintop
\newlength\marginbottom
% Default sizes, margins, ...
\setlength\highlightwidth{5.25cm}
\setlength\headerheight{3cm}
\setlength\marginleft{0.5cm}
\setlength\marginright{\marginleft}
\setlength\margintop{1cm}
\setlength\marginbottom{1cm}

\RequirePackage[
  bindingoffset=0cm,
  nomarginpar,
  noheadfoot
]{geometry}

\geometry{
  left=\marginleft,
  right=\marginright,
  top=\margintop,
  bottom=\marginbottom
}

% Minipage has an annoying af indent that must be removed
\setlength{\parindent}{0pt}

% COLORS
% ------------------------------------------------------------------------------
\RequirePackage{xcolor}
% Define material UI colors
\definecolor{red_50}{RGB}{255 , 235 , 238 }
\definecolor{red_100}{RGB}{255 , 205 , 210 }
\definecolor{red_200}{RGB}{239 , 154 , 154 }
\definecolor{red_300}{RGB}{229 , 115 , 115 }
\definecolor{red_400}{RGB}{239 , 83  , 80  }
\definecolor{red_500}{RGB}{244 , 67  , 54  }
\definecolor{red_600}{RGB}{229 , 57  , 53  }
\definecolor{red_700}{RGB}{211 , 47  , 47  }
\definecolor{red_800}{RGB}{198 , 40  , 40  }
\definecolor{red_900}{RGB}{183 , 28  , 28  }
\definecolor{red_A100}{RGB}{255 , 138 , 128 }
\definecolor{red_A200}{RGB}{255 , 82  , 82  }
\definecolor{red_A400}{RGB}{255 , 23  , 68  }
\definecolor{red_A700}{RGB}{213 , 0   , 0   }
\definecolor{pink_50}{RGB}{252 , 228 , 236 }
\definecolor{pink_100}{RGB}{248 , 187 , 208 }
\definecolor{pink_200}{RGB}{244 , 143 , 177 }
\definecolor{pink_300}{RGB}{240 , 98  , 146 }
\definecolor{pink_400}{RGB}{236 , 64  , 122 }
\definecolor{pink_500}{RGB}{233 , 30  , 99  }
\definecolor{pink_600}{RGB}{216 , 27  , 96  }
\definecolor{pink_700}{RGB}{194 , 24  , 91  }
\definecolor{pink_800}{RGB}{173 , 20  , 87  }
\definecolor{pink_900}{RGB}{136 , 14  , 79  }
\definecolor{pink_A100}{RGB}{255 , 128 , 171 }
\definecolor{pink_A200}{RGB}{255 , 64  , 129 }
\definecolor{pink_A400}{RGB}{245 , 0   , 87  }
\definecolor{pink_A700}{RGB}{197 , 17  , 98  }
\definecolor{purple_50}{RGB}{243 , 229 , 245 }
\definecolor{purple_100}{RGB}{225 , 190 , 231 }
\definecolor{purple_200}{RGB}{206 , 147 , 216 }
\definecolor{purple_300}{RGB}{186 , 104 , 200 }
\definecolor{purple_400}{RGB}{171 , 71  , 188 }
\definecolor{purple_500}{RGB}{156 , 39  , 176 }
\definecolor{purple_600}{RGB}{142 , 36  , 170 }
\definecolor{purple_700}{RGB}{123 , 31  , 162 }
\definecolor{purple_800}{RGB}{106 , 27  , 154 }
\definecolor{purple_900}{RGB}{74  , 20  , 140 }
\definecolor{purple_A100}{RGB}{234 , 128 , 252 }
\definecolor{purple_A200}{RGB}{224 , 64  , 251 }
\definecolor{purple_A400}{RGB}{213 , 0   , 249 }
\definecolor{purple_A700}{RGB}{170 , 0   , 255 }
\definecolor{deep_purple_50}{RGB}{237 , 231 , 246 }
\definecolor{deep_purple_100}{RGB}{209 , 196 , 233 }
\definecolor{deep_purple_200}{RGB}{179 , 157 , 219 }
\definecolor{deep_purple_300}{RGB}{149 , 117 , 205 }
\definecolor{deep_purple_400}{RGB}{126 , 87  , 194 }
\definecolor{deep_purple_500}{RGB}{103 , 58  , 183 }
\definecolor{deep_purple_600}{RGB}{94  , 53  , 177 }
\definecolor{deep_purple_700}{RGB}{81  , 45  , 168 }
\definecolor{deep_purple_800}{RGB}{69  , 39  , 160 }
\definecolor{deep_purple_900}{RGB}{49  , 27  , 146 }
\definecolor{deep_purple_A100}{RGB}{179 , 136 , 255 }
\definecolor{deep_purple_A200}{RGB}{124 , 77  , 255 }
\definecolor{deep_purple_A400}{RGB}{101 , 31  , 255 }
\definecolor{deep_purple_A700}{RGB}{98  , 0   , 234 }
\definecolor{indigo_50}{RGB}{232 , 234 , 246 }
\definecolor{indigo_100}{RGB}{197 , 202 , 233 }
\definecolor{indigo_200}{RGB}{159 , 168 , 218 }
\definecolor{indigo_300}{RGB}{121 , 134 , 203 }
\definecolor{indigo_400}{RGB}{92  , 107 , 192 }
\definecolor{indigo_500}{RGB}{63  , 81  , 181 }
\definecolor{indigo_600}{RGB}{57  , 73  , 171 }
\definecolor{indigo_700}{RGB}{48  , 63  , 159 }
\definecolor{indigo_800}{RGB}{40  , 53  , 147 }
\definecolor{indigo_900}{RGB}{26  , 35  , 126 }
\definecolor{indigo_A100}{RGB}{140 , 158 , 255 }
\definecolor{indigo_A200}{RGB}{83  , 109 , 254 }
\definecolor{indigo_A400}{RGB}{61  , 90  , 254 }
\definecolor{indigo_A700}{RGB}{48  , 79  , 254 }
\definecolor{blue_50}{RGB}{227 , 242 , 253 }
\definecolor{blue_100}{RGB}{187 , 222 , 251 }
\definecolor{blue_200}{RGB}{144 , 202 , 249 }
\definecolor{blue_300}{RGB}{100 , 181 , 246 }
\definecolor{blue_400}{RGB}{66  , 165 , 245 }
\definecolor{blue_500}{RGB}{33  , 150 , 243 }
\definecolor{blue_600}{RGB}{30  , 136 , 229 }
\definecolor{blue_700}{RGB}{25  , 118 , 210 }
\definecolor{blue_800}{RGB}{21  , 101 , 192 }
\definecolor{blue_900}{RGB}{13  , 71  , 161 }
\definecolor{blue_A100}{RGB}{130 , 177 , 255 }
\definecolor{blue_A200}{RGB}{68  , 138 , 255 }
\definecolor{blue_A400}{RGB}{41  , 121 , 255 }
\definecolor{blue_A700}{RGB}{41  , 98  , 255 }
\definecolor{light_blue_50}{RGB}{225 , 245 , 254 }
\definecolor{light_blue_100}{RGB}{179 , 229 , 252 }
\definecolor{light_blue_200}{RGB}{129 , 212 , 250 }
\definecolor{light_blue_300}{RGB}{79  , 195 , 247 }
\definecolor{light_blue_400}{RGB}{41  , 182 , 246 }
\definecolor{light_blue_500}{RGB}{3   , 169 , 244 }
\definecolor{light_blue_600}{RGB}{3   , 155 , 229 }
\definecolor{light_blue_700}{RGB}{2   , 136 , 209 }
\definecolor{light_blue_800}{RGB}{2   , 119 , 189 }
\definecolor{light_blue_900}{RGB}{1   , 87  , 155 }
\definecolor{light_blue_A100}{RGB}{128 , 216 , 255 }
\definecolor{light_blue_A200}{RGB}{64  , 196 , 255 }
\definecolor{light_blue_A400}{RGB}{0   , 176 , 255 }
\definecolor{light_blue_A700}{RGB}{0   , 145 , 234 }
\definecolor{cyan_50}{RGB}{224 , 247 , 250 }
\definecolor{cyan_100}{RGB}{178 , 235 , 242 }
\definecolor{cyan_200}{RGB}{128 , 222 , 234 }
\definecolor{cyan_300}{RGB}{77  , 208 , 225 }
\definecolor{cyan_400}{RGB}{38  , 198 , 218 }
\definecolor{cyan_500}{RGB}{0   , 188 , 212 }
\definecolor{cyan_600}{RGB}{0   , 172 , 193 }
\definecolor{cyan_700}{RGB}{0   , 151 , 167 }
\definecolor{cyan_800}{RGB}{0   , 131 , 143 }
\definecolor{cyan_900}{RGB}{0   , 96  , 100 }
\definecolor{cyan_A100}{RGB}{132 , 255 , 255 }
\definecolor{cyan_A200}{RGB}{24  , 255 , 255 }
\definecolor{cyan_A400}{RGB}{0   , 229 , 255 }
\definecolor{cyan_A700}{RGB}{0   , 184 , 212 }
\definecolor{teal_50}{RGB}{224 , 242 , 241 }
\definecolor{teal_100}{RGB}{178 , 223 , 219 }
\definecolor{teal_200}{RGB}{128 , 203 , 196 }
\definecolor{teal_300}{RGB}{77  , 182 , 172 }
\definecolor{teal_400}{RGB}{38  , 166 , 154 }
\definecolor{teal_500}{RGB}{0   , 150 , 136 }
\definecolor{teal_600}{RGB}{0   , 137 , 123 }
\definecolor{teal_700}{RGB}{0   , 121 , 107 }
\definecolor{teal_800}{RGB}{0   , 105 , 92  }
\definecolor{teal_900}{RGB}{0   , 77  , 64  }
\definecolor{teal_A100}{RGB}{167 , 255 , 235 }
\definecolor{teal_A200}{RGB}{100 , 255 , 218 }
\definecolor{teal_A400}{RGB}{29  , 233 , 182 }
\definecolor{teal_A700}{RGB}{0   , 191 , 165 }
\definecolor{green_50}{RGB}{232 , 245 , 233 }
\definecolor{green_100}{RGB}{200 , 230 , 201 }
\definecolor{green_200}{RGB}{165 , 214 , 167 }
\definecolor{green_300}{RGB}{129 , 199 , 132 }
\definecolor{green_400}{RGB}{102 , 187 , 106 }
\definecolor{green_500}{RGB}{76  , 175 , 80  }
\definecolor{green_600}{RGB}{67  , 160 , 71  }
\definecolor{green_700}{RGB}{56  , 142 , 60  }
\definecolor{green_800}{RGB}{46  , 125 , 50  }
\definecolor{green_900}{RGB}{27  , 94  , 32  }
\definecolor{green_A100}{RGB}{185 , 246 , 202 }
\definecolor{green_A200}{RGB}{105 , 240 , 174 }
\definecolor{green_A400}{RGB}{0   , 230 , 118 }
\definecolor{green_A700}{RGB}{0   , 200 , 83  }
\definecolor{light_green_50}{RGB}{241 , 248 , 233 }
\definecolor{light_green_100}{RGB}{220 , 237 , 200 }
\definecolor{light_green_200}{RGB}{197 , 225 , 165 }
\definecolor{light_green_300}{RGB}{174 , 213 , 129 }
\definecolor{light_green_400}{RGB}{156 , 204 , 101 }
\definecolor{light_green_500}{RGB}{139 , 195 , 74  }
\definecolor{light_green_600}{RGB}{124 , 179 , 66  }
\definecolor{light_green_700}{RGB}{104 , 159 , 56  }
\definecolor{light_green_800}{RGB}{85  , 139 , 47  }
\definecolor{light_green_900}{RGB}{51  , 105 , 30  }
\definecolor{light_green_A100}{RGB}{204 , 255 , 144 }
\definecolor{light_green_A200}{RGB}{178 , 255 , 89  }
\definecolor{light_green_A400}{RGB}{118 , 255 , 3   }
\definecolor{light_green_A700}{RGB}{100 , 221 , 23  }
\definecolor{lime_50}{RGB}{249 , 251 , 231 }
\definecolor{lime_100}{RGB}{240 , 244 , 195 }
\definecolor{lime_200}{RGB}{230 , 238 , 156 }
\definecolor{lime_300}{RGB}{220 , 231 , 117 }
\definecolor{lime_400}{RGB}{212 , 225 , 87  }
\definecolor{lime_500}{RGB}{205 , 220 , 57  }
\definecolor{lime_600}{RGB}{192 , 202 , 51  }
\definecolor{lime_700}{RGB}{175 , 180 , 43  }
\definecolor{lime_800}{RGB}{158 , 157 , 36  }
\definecolor{lime_900}{RGB}{130 , 119 , 23  }
\definecolor{lime_A100}{RGB}{244 , 255 , 129 }
\definecolor{lime_A200}{RGB}{238 , 255 , 65  }
\definecolor{lime_A400}{RGB}{198 , 255 , 0   }
\definecolor{lime_A700}{RGB}{174 , 234 , 0   }
\definecolor{yellow_50}{RGB}{255 , 253 , 231 }
\definecolor{yellow_100}{RGB}{255 , 249 , 196 }
\definecolor{yellow_200}{RGB}{255 , 245 , 157 }
\definecolor{yellow_300}{RGB}{255 , 241 , 118 }
\definecolor{yellow_400}{RGB}{255 , 238 , 88  }
\definecolor{yellow_500}{RGB}{255 , 235 , 59  }
\definecolor{yellow_600}{RGB}{253 , 216 , 53  }
\definecolor{yellow_700}{RGB}{251 , 192 , 45  }
\definecolor{yellow_800}{RGB}{249 , 168 , 37  }
\definecolor{yellow_900}{RGB}{245 , 127 , 23  }
\definecolor{yellow_A100}{RGB}{255 , 255 , 141 }
\definecolor{yellow_A200}{RGB}{255 , 255 , 0   }
\definecolor{yellow_A400}{RGB}{255 , 234 , 0   }
\definecolor{yellow_A700}{RGB}{255 , 214 , 0   }
\definecolor{amber_50}{RGB}{255 , 248 , 225 }
\definecolor{amber_100}{RGB}{255 , 236 , 179 }
\definecolor{amber_200}{RGB}{255 , 224 , 130 }
\definecolor{amber_300}{RGB}{255 , 213 , 79  }
\definecolor{amber_400}{RGB}{255 , 202 , 40  }
\definecolor{amber_500}{RGB}{255 , 193 , 7   }
\definecolor{amber_600}{RGB}{255 , 179 , 0   }
\definecolor{amber_700}{RGB}{255 , 160 , 0   }
\definecolor{amber_800}{RGB}{255 , 143 , 0   }
\definecolor{amber_900}{RGB}{255 , 111 , 0   }
\definecolor{amber_A100}{RGB}{255 , 229 , 127 }
\definecolor{amber_A200}{RGB}{255 , 215 , 64  }
\definecolor{amber_A400}{RGB}{255 , 196 , 0   }
\definecolor{amber_A700}{RGB}{255 , 171 , 0   }
\definecolor{orange_50}{RGB}{255 , 243 , 224 }
\definecolor{orange_100}{RGB}{255 , 224 , 178 }
\definecolor{orange_200}{RGB}{255 , 204 , 128 }
\definecolor{orange_300}{RGB}{255 , 183 , 77  }
\definecolor{orange_400}{RGB}{255 , 167 , 38  }
\definecolor{orange_500}{RGB}{255 , 152 , 0   }
\definecolor{orange_600}{RGB}{251 , 140 , 0   }
\definecolor{orange_700}{RGB}{245 , 124 , 0   }
\definecolor{orange_800}{RGB}{239 , 108 , 0   }
\definecolor{orange_900}{RGB}{230 , 81  , 0   }
\definecolor{orange_A100}{RGB}{255 , 209 , 128 }
\definecolor{orange_A200}{RGB}{255 , 171 , 64  }
\definecolor{orange_A400}{RGB}{255 , 145 , 0   }
\definecolor{orange_A700}{RGB}{255 , 109 , 0   }
\definecolor{deep_orange_50}{RGB}{251 , 233 , 231 }
\definecolor{deep_orange_100}{RGB}{255 , 204 , 188 }
\definecolor{deep_orange_200}{RGB}{255 , 171 , 145 }
\definecolor{deep_orange_300}{RGB}{255 , 138 , 101 }
\definecolor{deep_orange_400}{RGB}{255 , 112 , 67  }
\definecolor{deep_orange_500}{RGB}{255 , 87  , 34  }
\definecolor{deep_orange_600}{RGB}{244 , 81  , 30  }
\definecolor{deep_orange_700}{RGB}{230 , 74  , 25  }
\definecolor{deep_orange_800}{RGB}{216 , 67  , 21  }
\definecolor{deep_orange_900}{RGB}{191 , 54  , 12  }
\definecolor{deep_orange_A100}{RGB}{255 , 158 , 128 }
\definecolor{deep_orange_A200}{RGB}{255 , 110 , 64  }
\definecolor{deep_orange_A400}{RGB}{255 , 61  , 0   }
\definecolor{deep_orange_A700}{RGB}{221 , 44  , 0   }
\definecolor{brown_50}{RGB}{239 , 235 , 233 }
\definecolor{brown_100}{RGB}{215 , 204 , 200 }
\definecolor{brown_200}{RGB}{188 , 170 , 164 }
\definecolor{brown_300}{RGB}{161 , 136 , 127 }
\definecolor{brown_400}{RGB}{141 , 110 , 99  }
\definecolor{brown_500}{RGB}{121 , 85  , 72  }
\definecolor{brown_600}{RGB}{109 , 76  , 65  }
\definecolor{brown_700}{RGB}{93  , 64  , 55  }
\definecolor{brown_800}{RGB}{78  , 52  , 46  }
\definecolor{brown_900}{RGB}{62  , 39  , 35  }
\definecolor{grey_50}{RGB}{250 , 250 , 250 }
\definecolor{grey_100}{RGB}{245 , 245 , 245 }
\definecolor{grey_200}{RGB}{238 , 238 , 238 }
\definecolor{grey_300}{RGB}{224 , 224 , 224 }
\definecolor{grey_400}{RGB}{189 , 189 , 189 }
\definecolor{grey_500}{RGB}{158 , 158 , 158 }
\definecolor{grey_600}{RGB}{117 , 117 , 117 }
\definecolor{grey_700}{RGB}{97  , 97  , 97  }
\definecolor{grey_800}{RGB}{66  , 66  , 66  }
\definecolor{grey_900}{RGB}{33  , 33  , 33  }
\definecolor{blue_grey_50}{RGB}{236 , 239 , 241 }
\definecolor{blue_grey_100}{RGB}{207 , 216 , 220 }
\definecolor{blue_grey_200}{RGB}{176 , 190 , 197 }
\definecolor{blue_grey_300}{RGB}{144 , 164 , 174 }
\definecolor{blue_grey_400}{RGB}{120 , 144 , 156 }
\definecolor{blue_grey_500}{RGB}{96  , 125 , 139 }
\definecolor{blue_grey_600}{RGB}{84  , 110 , 122 }
\definecolor{blue_grey_700}{RGB}{69  , 90  , 100 }
\definecolor{blue_grey_800}{RGB}{55  , 71  , 79  }
\definecolor{blue_grey_900}{RGB}{38  , 50  , 56  }
\definecolor{black}{RGB}{0   , 0   , 0   }
\definecolor{white}{RGB}{255 , 255 , 255 }
% Basic colors
\colorlet{heading}{green_900}
\colorlet{calendar}{deep_purple_900}
\colorlet{location}{brown_900}
\colorlet{company}{indigo_900}
\colorlet{body}{blue_500}
% Bar background and foreground
\colorlet{highlightbarcolor}{grey_500}
\colorlet{headerbarcolor}{grey_800}
\colorlet{headerfontcolor}{grey_200}
% Sidebar specific color
\colorlet{contact_icon}{red_500}

\colorlet{emphasis}{yellow_500}
% COLORED BARS
% ------------------------------------------------------------------------------
\RequirePackage{xpatch}
\RequirePackage{scrlayer-scrpage}
% Declare new page style using layers
\DeclareNewPageStyleByLayers{headerhighlightmain}{%
  highlightbar,
  header.bg
}
\DeclareNewPageStyleByLayers{highlightmain}{%
  highlightbar
}
\DeclareNewPageStyleByLayers{headermain}{%
  header.bg
}

% define the layer for the highlight bar on odd pages
\DeclareNewLayer[
  background,
  oddpage,
  innermargin,
  width=\highlightwidth,
  contents={\color{highlightbarcolor}\rule{\layerwidth}{\layerheight}}
]{highlightbar}

% define the layer for the header
\DeclareNewLayer[
  background,
  topmargin,
  addheight=\headerheight,
  contents={\color{headerbarcolor}\rule{\layerwidth}{\layerheight}}
]{header.bg}

% % add the layers to page style plain
% \ForEachLayerOfPageStyle*{headerhighlightmain}{%
%   \AddLayersToPageStyle{plain.scrheadings}{#1}%
% }

% remove anything that might be there (page number) from header and footer
\lehead[]{}
\cehead[]{}
\rehead[]{}
\lohead[]{}
\cohead[]{}
\rohead[]{}
\lefoot[]{}
\cefoot[]{}
\refoot[]{}
\lofoot[]{}
\cofoot[]{}
\rofoot[]{}

% convenience functions to enable/disable header or highlightbar fontawesome5
% icons
\renewcommand{\fa}[1]{
  \faIcon[solid]{#1}
}

% HEADER
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% variables for name, tag line and photo setup
\newcommand{\name}[1]{\def\@name{#1}}
\newcommand{\tagline}[1]{\def\@tagline{#1}}
\newcommand{\photo}[3][]{\def\@photo{#2}\def\@photodiameter{#3}\def\@photoformat{#1}}

% try to align the top of the written out name with the top of the photo it is
% impossible to get the actual height of a line to determine the offset between
% line top and charachter top therefore use a bad workaround by setting the
% line height to 1.5 times the character height
\newlength{\@namefontheight}
\newlength{\@namelineheight}
\settoheight{\@namefontheight}{\Huge\bfseries\MakeUppercase{A}}
\setlength\@namelineheight{1.5\@namefontheight}

% assemble the header
\newcommand{\makeheader}{% header bar is a minipage
  \begin{minipage}[t][\headerheight]{\textwidth}%
    \vspace{-1em}
    % align top of name and photo
    \vspace{\dimexpr \@namefontheight-\@namelineheight}
    % create two minipages for header text and photo if photo is given
    \ifdef{\@photodiameter}{
      % to top align name and photo add [t] here
      \begin{minipage}[t]{\dimexpr \textwidth-\@photodiameter}
        \vspace{0cm}%
      }{}
      % print the header text
        \begin{minipage}[t][2em]{\linewidth}
          {\Huge\bfseries\color{headerfontcolor}\MakeUppercase{\@name}\par}
        \end{minipage}%
        \vfill%
        \begin{minipage}[b][\dimexpr \headerheight-\marginbottom]{.85\linewidth}%
          {\large\bfseries\color{headerfontcolor}\@tagline\par}
        \end{minipage}%
    % finish the minipages for text and photo if photo is given
    \ifdef{\@photodiameter}{%
        \end{minipage}\hfil%
        % to top align name and photo add [t] here
        \begin{minipage}[t]{\@photodiameter}
          \vspace{0cm}
      % format as square or round
      \ifthenelse{\equal{\@photoformat}{square}}{%
          \includegraphics[width=\linewidth]{\@photo}%
      }{%
          \tikz\path[fill overzoom image={\@photo}]circle[radius=0.5\linewidth];
      }
    \end{minipage}%
          }{}
  \end{minipage}%
}

\newcommand{\emptyheader}{%
    \vspace*{\dimexpr \headerheight+0.5em}
}


% BODY
% ------------------------------------------------------------------------------
% Contact Info
% ------------------------------------------------------------------------------
\newcommand{\infofield}[2]{
  \fboxrule.2pt\fboxsep-.2pt
  \parbox[t]{\linewidth}{
    \parbox[t]{1.5em}{
      \centering
      \textcolor{contact_icon}{\footnotesize #1}
    }
    \parbox[t][][t]{\dimexpr \linewidth-3em}{
      \footnotesize #2
    }
  }
}

\newcommand{\email}[1]{\infofield{\fa{envelope}}{\href{mailto:#1}{#1}}}

\newcommand{\address}[1]{\infofield{\fa{at}}{#1}}

\newcommand{\location}[1]{\infofield{\fa{map-marker-alt}}{#1}}

\newcommand{\phone}[1]{\infofield{\fa{phone}}{#1}}

\newcommand{\homepage}[2]{\infofield{\fa{home}}{\href{#2}{#1}}}

\newcommand{\profile}[3]{\infofield{\lowercase{\fa{#1}}}{\href{#2}{#3}}}


% Highlight Bar
% ------------------------------------------------------------------------------
\newcommand{\highlightbar}[1]{%
  \def\@highlightbar{%
    \parbox[t]{\dimexpr \highlightwidth-\marginleft-\marginright}{%
      #1%
    }
  }
}

% Main bar
% ------------------------------------------------------------------------------
\newcommand{\mainbar}[1]{%
  \def\@mainbar{%
    \begin{minipage}[t]{\dimexpr \textwidth-\highlightwidth}
      #1%
    \end{minipage}%
  }
}

% Make body with highlight bar and main bar
% ------------------------------------------------------------------------------
\newcommand{\makebody}{%
  \@highlightbar
  \hspace{\dimexpr \marginright+\marginleft}%
  \@mainbar
}


% SECTIONS, SUBSECTIONS, AND MORE
% ------------------------------------------------------------------------------
% Redefine section in caps, bold and with rule below
\renewcommand{\section}[2][]{%
  \parbox[t]{\linewidth}{
    \vspace{1em}
    \ifstrequal{#1}{}{}{\color{heading}\large \makebox[5mm][c]{#1}\hspace{0.5em}}
    {\color{heading}\Large\bfseries\MakeUppercase{#2}}\\[-1ex]%
    {\color{heading}\rule{\linewidth}{1.0pt}\par}\smallskip
  }
}

% redefine subsection as bold
\renewcommand{\subsection}[1]{%
  \smallskip%
  {\color{emphasis}\large\bfseries{#1}\par}\medskip
}

% Format job list
% ------------------------------------------------------------------------------
\newcommand{\jobcompany}[3]{%
  % #1: Company Name
  % #2: Company URL
  % #3: Company Location
  \parbox{\linewidth}{
    \vspace{-0.25em}
    \parbox{.5\linewidth}{
      \flushleft \fa{building} \href{#2}{#1}
    }
    \parbox{.49\linewidth}{
      \scriptsize \flushright %
      \textcolor{location}{%
        \fa{map-marker-alt} #3
      }
    }
    \vspace{-1em}
  }
}

\newcommand{\jobposition}[5]{%
  % #1: Position
  % #2: Date
  % #3: Duration
  % #4: Description
  \parbox{\linewidth}{
    \parbox[t]{.75\linewidth}{
      \flushleft \textbf{#1} \\
      \vspace{0.25em}
      \footnotesize #4
      \vspace{0.5em}
      \scriptsize #5
    }
    \parbox[t]{.24\linewidth}{
      \flushright \footnotesize %
      \textcolor{calendar}{%
        \fa{calendar-alt} #2 \\
        #3
      }
    }
    \vspace{0.5em}
  }
}

% Format Volunteer list
% ------------------------------------------------------------------------------
\newcommand{\volunteerorganization}[4]{%
  % #1: Not Handled ??? DO NOT KNOW WHY
  % #2: Company Name
  % #3: Company URL
  % #4: Company Location
  \parbox{\linewidth}{
    \parbox{.5\linewidth}{
      \flushleft \fa{building} \href{#2}{#1}
    }
    \parbox{.49\linewidth}{
      \scriptsize \flushright %
      \textcolor{location}{%
        \fa{map-marker-alt} #4
      }
    }
    \footnotesize #3
    \vspace{-0.5em}
  }
}

\newcommand{\volunteerposition}[5]{%
  % #1: Not Handled ??? DO NOT KNOW WHY
  % #2: Position
  % #3: Date
  % #4: Duration
  % #5: Description
  \parbox{\linewidth}{
    \vspace{-0.5em}
    \parbox[t]{.82\linewidth}{
      \flushleft
      \scriptsize \textbullet\  #1
    }
    \parbox[t]{.17\linewidth}{
      \scriptsize \flushright
      \textcolor{calendar}{%
        \flushleft \fa{calendar-alt} #2 \\
        } %
      \textcolor{calendar}{%
         #3
      }
    }
    \vspace{-0.5em}
  }
}

% Format education list
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand{\schooldiploma[7]}{%
  % #1: Not Handled ??? DO NOT KNOW WHY
  % #2: Diploma
  % #3: Date
  % #5: Description
  \parbox{\linewidth}{
    \parbox[t]{.25\linewidth}{
      \textcolor{calendar}{%
      \footnotesize \flushleft \fa{calendar-alt} #3
      }
    }
    \parbox[t]{.74\linewidth}{
      \flushright
      \scriptsize
      \fa{school} \href{#6}{#5} \\
      \textcolor{location}{%
        \fa{map-marker-alt} #4
      }
    }
    \parbox[t]{0.75\linewidth}{
      \vspace{-0.5em}
      \footnotesize
      \textbf{#2}
    }
    \vspace{0.25em}

    \scriptsize{#7}
  }
  \vspace{0.5em}
}

\newcommand{\school}[1]{%
  \begin{minipage}[t]{\linewidth}
    #1
  \end{minipage}%
}

% skill with 5 dot bar chart
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand{\skill}[3]{%
  \parbox[t]{\linewidth}{
    \textcolor{emphasis}{\fa{#2}\textbf{#1}}
  }
  \parbox[t]{0.9\linewidth}{
    \begin{tikzpicture}
        \draw[fill=skill_bg,skill_bg] (0,0) rectangle (\linewidth,0.3);
        \draw[fill=skill_accent,skill_accent]     (0,0) rectangle (0.#3\linewidth,0.3);
    \end{tikzpicture}
  }
}

% \newcommand{\skill}[2]{%
%     \textcolor{emphasis}{\textbf{#1}}\hfill
%     \foreach \x in {1,...,5}{%
%       \space{\ifnumgreater{\x}{#2}{\color{gray}}{\color{accent}}\fa{circle}}}\par%
% }

% skill without any charts
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand{\simpleskill}[1]{%
    \textcolor{emphasis}{\textbf{#1}}\par%
}

% Sectioning of skills
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand{\skillsection}[1]{%
    \textit{\color{accent}#1}\par
}

% tag (framed word or phrase)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% adapted from AltaCV: https://github.com/liantze/AltaCV
\newcommand{\tag}[1]{%
  \tikz[baseline]\node[anchor=base,draw=body!30,rounded corners,inner
  xsep=1ex,inner ysep =0.75ex,text height=1.5ex,text depth=.25ex]{#1};
}

% wheel chart
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% adapted from AltaCV: https://github.com/liantze/AltaCV
\newcommand{\wheelchart}[4][0]{%
    \begingroup\centering
    \def\innerradius{#3}%
    \def\outerradius{#2}%
    % Calculate total
    \pgfmathsetmacro{\totalnum}{0}%
    \foreach \value/\colour/\name in {#4} {%
        \pgfmathparse{\value+\totalnum}%
        \global\let\totalnum=\pgfmathresult%
    }%
    \begin{tikzpicture}

      % Calculate the thickness and the middle line of the wheel
      \pgfmathsetmacro{\wheelwidth}{\outerradius-\innerradius}
      \pgfmathsetmacro{\midradius}{(\outerradius+\innerradius)/2}
      \pgfathsetmacro{\totalrot}{-90 + #1}

      % Rotate so we start from the top
      \begin{scope}[rotate=\totalrot]

      % Loop through each value set. \cumnum keeps track of where we are in the wheel
      \pgfmathsetmacro{\cumnum}{0}
      \foreach \value/\width/\colour/\name in {#4} {
            \pgfmathsetmacro{\newcumnum}{\cumnum + \value/\totalnum*360}

            % Calculate the percent value
            \pgfmathsetmacro{\percentage}{\value/\totalnum*100}
            % Calculate the mid angle of the colour segments to place the labels
            \pgfmathsetmacro{\midangle}{-(\cumnum+\newcumnum)/2}

            % This is necessary for the labels to align nicely
            \pgfmathparse{
               (-\midangle>180?"west":"east")
            } \edef\textanchor{\pgfmathresult}
            \pgfmathparse{
               (-\midangle>180?"flush left":"flush right")
            } \edef\textalign{\pgfmathresult}
            \pgfmathsetmacro\labelshiftdir{1-2*(-\midangle<180)}

            % Draw the color segments. Somehow, the \midrow units got lost, so
            % we add 'pt' at the end. Not nice...
            \filldraw[draw=white,fill=\colour]
              (-\cumnum:\outerradius) arc (-\cumnum:-(\newcumnum):\outerradius) --
              (-\newcumnum:\innerradius) arc (-\newcumnum:-(\cumnum):\innerradius) -- cycle;

            % Draw the data labels
            \draw  [*-,thin,emphasis] node [append after command={
              (\midangle:\midradius pt) -- (\midangle:\outerradius + 1ex) --
              (\tikzlastnode)}] at (\midangle:\outerradius + 1ex)
              [xshift=\labelshiftdir*0.5cm,inner sep=1ex, outer sep=0pt,
              text width=\width,anchor=\textanchor,align=\textalign,font=\small,
              text=body]{\name};
            % Set the old cumulated angle to the new value
            \global\let\cumnum=\newcumnum
        }
      \end{scope}
%      \draw[gray] (0,0) circle (\outerradius) circle (\innerradius);
    \end{tikzpicture}\par
    \endgroup
}

% publication
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand*{\ADS}[1]{\textcolor{awesome-skyblue}{\href{#1}{ADS}}}
\newcommand*{\arXiv}[1]{\textcolor{awesome-skyblue}{\href{#1}{arXiv}}}

\newlength{\pubdatelength}
\newlength{\pubjournallength}
\newlength{\publinklength}

% Spacings work erratically. Setting a highlight bar or not redefines
% \linewidth in a weird way which breaks the spacing and introduces line
% breaks. I have no idea what exactly causes this problem.

% helper function to set spacings that work empirically
\newcommand{\pubdefaultspacing}{%
    \setlength{\pubdatelength}{0.15\linewidth}
    \setlength{\pubjournallength}{0.65\linewidth}
    \setlength{\publinklength}{0.20\linewidth}
}

% helper function to force the publication to use the full width in normal page
% styles without highlight bar or header
\newcommand{\pubforcefullwidth}{%
    \setlength{\pubdatelength}{0.1\textwidth}
    \setlength{\pubjournallength}{0.8\textwidth}
    \setlength{\publinklength}{0.1\textwidth}
}

% \pubforcefullwidth
\pubdefaultspacing

\newcommand{\publication}[5]{%
    {\normalsize \color{emphasis}#1\par}
    \vspace{0.1em}%
    \begin{minipage}[t]{3mm}%
      \makebox[3mm][c]{\footnotesize \fa{users}}
    \end{minipage}%
    \hspace{0.5em}%
    \begin{minipage}[t]{\dimexpr \linewidth-3mm-0.5em}%
        {\footnotesize #2\par}
    \end{minipage}%
    \par%
    \vspace{0.25em}%
    \ifstrequal{#4}{}{%
        \begin{minipage}[t]{\dimexpr \pubdatelength+\pubjournallength-1.0em}%
          \footnotesize \makebox[3mm][c]{\fa{calendar-alt}} \hspace{0.25em} #3
        \end{minipage}%
    }{%
        \begin{minipage}[t]{\dimexpr \pubdatelength-1.0em}%
          \footnotesize \makebox[3mm][c]{\fa{calendar-alt}} \hspace{0.25em} #3
        \end{minipage}%
    }%
    \hspace{1.0em}
    \begin{minipage}[t]{\dimexpr \pubjournallength-1.0em}%
        \ifstrequal{#4}{}{}{%
            \begin{minipage}[t]{3mm}%
              \makebox[3mm][c]{\footnotesize \fa{book}}
            \end{minipage}%
            \hspace{0.5em}%
            \begin{minipage}[t]{\dimexpr \linewidth-3mm-0.25em}%
                {\footnotesize #4\par}
            \end{minipage}%
        }%
    \end{minipage}%
    \hspace{1.0em}
    \begin{minipage}[t]{\publinklength}%
        \ifstrequal{#5}{}{}{%
          \footnotesize \makebox[3mm][c]{\fa{link}} \hspace{0.25em} #5\par
        }%
    \end{minipage}%
    \par\normalsize
    \vspace{1.0em}
}

% achievement
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand{\achievement}[1]{%
    \begin{minipage}[t]{3mm}%
      \makebox[3mm][c]{\footnotesize \fa{trophy}}
    \end{minipage}%
    \hspace{0.5em}%
    \begin{minipage}[t]{\dimexpr \textwidth-0.5em-3mm}%
        {\normalsize #1\par}
    \end{minipage}%
    \par
    \vspace{0.5em}
}

% lists
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{enumitem}
\setlist[itemize]{noitemsep, topsep=0pt, leftmargin=1em}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% FINAL FORMATTING
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\pagestyle{headerhighlightmain}
%\RequirePackage{hyperref}

\RequirePackage[%colorlinks = true,
            linkbordercolor = green_100,
            urlbordercolor  = blue_50,
            citecolor = cyan_100]{hyperref}



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  THE END
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% vim: ft=tex.latex
