---
title: "How to compile and install latest version of Vim with support for: X11 clipboard, ruby, python 2 or python 3"
description: 
date: 2013-11-19T14:19:12
slug: how-to-compile-and-install-latest-version-of-vim-with-support-for-x11-clipboard-ruby-python-2-3
draft: false
categories:
  - wordpress
  - unix
tags:
  - linux
  - vim
---

This was tested with vim 7.4.(1-398)
(Update: 2013-12-03 apparently you can't build vim with support for both python 2 and python 3, so I had to update this tutorial a bit :) )
(Update: 2014-08-09 Added three commands: "hg pull", "hg update" and "hg status" to pull the latest version of the repo) 

First of all install all the dependencies required when compiling Vim with additional options: 

```bash
sudo apt-get install \
    mercurial \
    python \
    python-dev \
    python3 \
    python3-dev \
    ruby \
    ruby-dev \
    libx11-dev \
    libxt-dev \
    libgtk2.0-dev \
    libncurses5 \
    ncurses-dev
```

Then clone official vim repo, configure it with support for: X11 clipboard, ruby, python 2 or 3 and few other cool options :) 

```bash
hg clone https://vim.googlecode.com/hg/ vim
## if you already had this repo cloned, then update it: 
hg pull 
hg update
## and then check if you definitely have the latest version: 
hg summary
parent: 6121:913d16b4904c
 Added tag v7-4-398 for changeset f62b2e76dd80 
branch: default 
commit: (clean) 
update: 52 new changesets (update) 
cd vim/src
##
## this will configure it with python 2 support
## 
./configure \
    --enable-perlinterp \
    --enable-pythoninterp \
    --enable-rubyinterp \
    --enable-cscope \
    --enable-gui=auto \
    --enable-gtk2-check \
    -enable-gnome-check \
    --with-features=huge \
    --enable-multibyte \
    --with-x \
    --with-compiledby="Senor QA <senor@qa>" \
    --with-python-config-dir=/usr/lib/python2.7/config-x86_64-linux-gnu
## 
## and this with python 3 support
## 
./configure \
    --enable-perlinterp \
    --enable-python3interp \
    --enable-rubyinterp \
    --enable-cscope \
    --enable-gui=auto \
    --enable-gtk2-check \
    --enable-gnome-check \
    --with-features=huge \
    --enable-multibyte \
    --with-x \
    --with-compiledby="Senor QA <senor@qa>" \
    --with-python3-config-dir=/usr/lib/python3.3/config-3.3m-x86_64-linux-gnu
```

Next step is to compile our setup: 
```bash
make
```

Then if you want you can check if all the features were compiled properly: 
```bash
VIM - Vi IMproved 7.4 (2013 Aug 10, compiled Aug 9 2014 15:37:52) 
Included patches: 1-398 
Compiled by Me <senor@qa> 
Huge version with GTK2 GUI. 
Features included (+) or not (-):
+acl             +farsi          +mouse_netterm    +syntax
+arabic          +file_in_path   +mouse_sgr        +tag_binary
+autocmd         +find_in_path   -mouse_sysmouse   +tag_old_static
+balloon_eval    +float          +mouse_urxvt      -tag_any_white
+browse          +folding        +mouse_xterm      -tcl
++builtin_terms  -footer         +multi_byte       +terminfo
+byte_offset     +fork()         +multi_lang       +termresponse
+cindent         +gettext        -mzscheme         +textobjects
+clientserver    -hangul_input   +netbeans_intg    +title
+clipboard       +iconv          +path_extra       +toolbar
+cmdline_compl   +insert_expand  -perl             +user_commands
+cmdline_hist    +jumplist       +persistent_undo  +vertsplit
+cmdline_info    +keymap         +postscript       +virtualedit
+comments        +langmap        +printer          +visual
+conceal         +libcall        +profile          +visualextra
+cryptv          +linebreak      +python           +viminfo
+cscope          +lispindent     -python3          +vreplace
+cursorbind      +listcmds       +quickfix         +wildignore
+cursorshape     +localmap       +reltime          +wildmenu
+dialog_con_gui  -lua            +rightleft        +windows
+diff            +menu           +ruby             +writebackup
+digraphs        +mksession      +scrollbind       +X11
+dnd             +modify_fname   +signs            -xfontset
-ebcdic          +mouse          +smartindent      +xim
+emacs_tags      +mouseshape     -sniff            +xsmp_interact
+eval            +mouse_dec      +startuptime      +xterm_clipboard
+ex_extra        -mouse_gpm      +statusline       -xterm_save
+extra_search    -mouse_jsbterm  -sun_workshop     -xpm
   system vimrc file: "$VIM/vimrc"
     user vimrc file: "$HOME/.vimrc"
 2nd user vimrc file: "~/.vim/vimrc"
      user exrc file: "$HOME/.exrc"
  system gvimrc file: "$VIM/gvimrc"
    user gvimrc file: "$HOME/.gvimrc"
2nd user gvimrc file: "~/.vim/gvimrc"
    system menu file: "$VIMRUNTIME/menu.vim"
  fall-back for $VIM: "/usr/local/share/vim"
Compilation: gcc -c -I. -Iproto -DHAVE_CONFIG_H -DFEAT_GUI_GTK -pthread -I/usr/include/gtk-2.0 -I/usr/lib/x86_64-linux-gnu/gtk-2.0/include -I/usr/include/atk-1.0 -I/usr/include/cairo -I/usr/include/gdk-pixbuf-2.0 -I/usr/include/pango-1.0 -I/usr/include/gio-unix-2.0/ -I/usr/include/freetype2 -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include -I/usr/include/pixman-1 -I/usr/include/libpng12 -I/usr/include/harfbuzz -g -O2 -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=1
Linking: gcc -L. -Wl,-Bsymbolic-functions -Wl,-z,relro -L/build/buildd/ruby1.9.1-1.9.3.484/debian/lib -rdynamic -Wl,-export-dynamic -L/usr/local/lib -Wl,--as-needed -o vim -lgtk-x11-2.0 -lgdk-x11-2.0 -latk-1.0 -lgio-2.0 -lpangoft2-1.0 -lpangocairo-1.0 -lgdk_pixbuf-2.0 -lcairo -lpango-1.0 -lfontconfig -lgobject-2.0 -lglib-2.0 -lfreetype -lSM -lICE -lXt -lX11 -lXdmcp -lSM -lICE -lm -ltinfo -lnsl -ldl -L/usr/lib/python2.7/config-x86_64-linux-gnu -lpython2.7 -lpthread -ldl -lutil -lm -Xlinker -export-dynamic -Wl,-O1 -Wl,-Bsymbolic-functions -lruby-1.9.1 -lpthread -lrt -ldl -lcrypt -lm -L/usr/lib
```

Just to make sure it works as it should, launch newly compiled ./vim, and type: `:echo has("python")`  
It should return `1` if it was compiled properly :)
If you're happy with this then install it :) 

```bash
sudo make install
```

Then locate the vim command 
```bash
which vim vim is /usr/local/bin/vim vim is /usr/bin/vim
```

As you can see, there are two installed on my system.  
To make newly installed version "`/usr/local/bin/vim`" the default one, we'll use "`update-alternatives`". 

```bash
sudo update-alternatives \
    --install "/usr/bin/vim" "vim" "/usr/local/bin/vim" 1 
sudo update-alternatives \
    --install "/usr/bin/vi" "vi" "/usr/local/bin/vim" 1
```

Then use "update-alternatives" to switch between installed versions :) 

```bash
sudo update-alternatives --config vim
There are 2 choices for the alternative vim (providing /usr/bin/vim). 

Selection Path Priority Status
------------------------------------------------------------
 * 0 /usr/bin/vim.basic 30 auto mode
   1 /usr/bin/vim.basic 30 manual mode
   2 /usr/local/bin/vim 1 manual mode
Press enter to keep the current choice[*], or type selection number: 2 
```

Now let's change symbolic link for vi:
```bash
sudo update-alternatives --config vi
There are 3 choices for the alternative vi (providing /usr/bin/vi).

Selection Path Priority Status
------------------------------------------------------------
 * 0 /usr/bin/vim.basic 30 auto mode
   1 /usr/bin/vim.basic 30 manual mode
   2 /usr/bin/vim.tiny 10 manual mode
   3 /usr/local/bin/vim 1 manual mode
Press enter to keep the current choice[*], or type selection number: 3
update-alternatives: using /usr/local/bin/vim to provide /usr/bin/vi (vi) in manual mode
```


Last thing to do is to check where the /usr/bin/vim points at: 
```bash
ll /usr/bin/vim lrwxrwxrwx 1 root root 21 Jun 7 11:29 /usr/bin/vim -> /etc/alternatives/vim*
```

Then check where the `/etc/alternatives/vim` points at.  
If everything went fine, it should be pointing at: `/usr/local/bin/vim`
```bash
ll /etc/alternatives/vim
```
