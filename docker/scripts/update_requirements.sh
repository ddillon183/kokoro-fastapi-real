#!/bin/bash
cd /app
uv pip compile docs/requirements.in --universal --output-file docs/requirements.txt
