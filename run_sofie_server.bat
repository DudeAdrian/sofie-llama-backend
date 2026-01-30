@echo off
title S.O.F.I.E Service (API server)

set LLAMA_SERVER=C:\llama\llama-server.exe
set MODEL=C:\llama\library\llama-model.gguf

"%LLAMA_SERVER%" ^
  -m "%MODEL%" ^
  -c 2048 ^
  --host 0.0.0.0 ^
  --port 8000 ^
  --api-key sk-dummy

echo.
echo S.O.F.I.E LLaMA server should now be listening on http://localhost:8000
echo Press Ctrl-C to stop.
pause
