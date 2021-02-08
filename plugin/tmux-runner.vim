function! SendTmuxCommand(text)
  let panes = split(system("tmux list-panes"), '\n')
  let active = filter(copy(panes), 'v:val =~ "\\(active\\)"')
  let vimPane = str2nr(active[0])
  let cmdPane = vimPane + 1
  let panes = filter(panes, 'v:val =~ "^'.cmdPane.':.*"')
  if len(panes) == 0
    call system('tmux split-window -v -l 10')
    call system('tmux select-pane -t '.vimPane)
  endif
  
  let cmd = "tmux send-keys -t ".cmdPane." ".shellescape(a:text . " && read -s -n 1 -p 'Press any key to continue . . .' && echo && exit") . " C-m"
  call system(cmd)
  call system("tmux select-pane -t " . cmdPane)
endfunction
