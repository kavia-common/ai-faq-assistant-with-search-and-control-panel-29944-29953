#!/bin/bash
cd /home/kavia/workspace/code-generation/ai-faq-assistant-with-search-and-control-panel-29944-29953/faq_bot_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

