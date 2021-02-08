fun! NeotermRunCurrentFile(command)
    exec 'botright Topen resize=' . g:term_height
    Tclear!
    exec "T " . a:command . " " . expand("%")
endf

fun! NeotermRunCommand(command)
    exec 'botright Topen resize=' . g:term_height
    Tclear!
    exec "T " . a:command
endf

