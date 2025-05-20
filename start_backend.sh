#!/bin/bash
cd ~/InsultMedAI
source ~/insultmedai_venv/bin/activate
export PYTHONPATH=~/InsultMedAI
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
