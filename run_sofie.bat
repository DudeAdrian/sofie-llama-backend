@echo off
title S.O.F.I.E Service (Single Run)

set LLAMA_EXE=C:\llama\llama-cli.exe
set MODEL=C:\llama\models\Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
set PROMPT=C:\llama\system_prompt.txt
set INPUT=C:\llama\service\sofie_input.txt
set OUTPUT=C:\llama\service\sofie_output.txt

"%LLAMA_EXE%" -m "%MODEL%" --system-prompt-file "%PROMPT%" < "%INPUT%" > "%OUTPUT%"

echo DONE
pause
