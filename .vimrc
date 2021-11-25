
" Show that a local vimrc is sources.
let g:sourced_local_vimrc=1

colorscheme happy_hacking

function Runscript(file)
    exec "!python -m swarm script -l " . a:file
endfunction

function RunDebug(...)
    exec "!python -m swarm script -l " . a:000[0] . " --debug " . a:000[1]
endfunction

command! -nargs=1 -complete=file RunScript : call Runscript(<f-args>)
command! -nargs=* -complete=file Debug : call RunDebug(<f-args>)

