let g:floaterm_runner_opened = 0

fun! FloatermRunCurrentFile(command)
    " try
    "     exec 'FloatermSend --name=yabs-runner ' . a:command . " " . expand("%")
    " catch
    "     exec 'FloatermNew! --name=yabs-runner ' . a:command . " " . expand("%")
    " endtry
    if g:floaterm_runner_opened
        exec 'FloatermSend --name=yabs-runner ' . a:command . ' ' . expand("%")
    else
        exec 'FloatermNew! --name=yabs-runner ' . a:command . ' ' . expand("%")
        let g:floaterm_runner_opened = 1
    endif
endfun

fun! FloatermRunCommand(command)
    " try
    "     exec 'FloatermSend --name=yabs-runner ' . a:command
    " catch
    "     exec 'FloatermNew! --name=yabs-runner ' . a:command
    " endtry
    if g:floaterm_runner_opened
        exec 'FloatermSend --name=yabs-runner ' . a:command
    else
        exec 'FloatermNew! --name=yabs-runner ' . a:command
        let g:floaterm_runner_opened = 1
    endif
endfun
