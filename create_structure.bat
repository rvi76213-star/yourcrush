@echo off
echo Creating YOUR CRUSH BOT folder structure...

REM Create main directories
mkdir "bot_core"
mkdir "data"
mkdir "config"
mkdir "utils"
mkdir "scripts"
mkdir "tests"
mkdir "docs"
mkdir "templates"
mkdir "examples"
mkdir "temp"
mkdir "external"

REM Create bot_core subdirectories
cd bot_core
mkdir "__pycache__"
echo. > __init__.py
echo. > master_bot.py
echo. > message_handler.py
echo. > facebook_messenger.py
echo. > cookie_manager.py
echo. > photo_delivery.py
echo. > ai_response_engine.py
echo. > learning_system.py
echo. > command_processor.py
echo. > memory_storage.py
echo. > user_manager.py
echo. > group_handler.py
echo. > media_handler.py
echo. > security_layer.py
cd ..

REM Create data subdirectories
cd data
mkdir "cookies"
mkdir "photos"
mkdir "commands"
mkdir "learning"
mkdir "json_responses"
mkdir "ai_integration"
mkdir "users"
mkdir "groups"
mkdir "logs"
mkdir "backup"

REM Create cookies subdirectories
cd cookies
echo {} > master_cookies.json
echo {} > backup_cookies.json
echo. > cookie_health.txt
cd ..

REM Create photos subdirectories
cd photos
mkdir "thumbnails"
echo. > master.jpg
echo. > master.png
echo. > photo.jpg
echo. > photo.png
echo. > own.jpg
echo. > own.png
cd ..

REM Create commands subdirectories
cd commands
mkdir "prefix"
mkdir "admin"
mkdir "nicknames"

cd prefix
mkdir "murgi"
mkdir "love"
mkdir "pick"
mkdir "dio"
mkdir "diagram"

cd murgi
echo 🐔 মুরগির ডিম পছন্দ করি! > v1.txt
echo 🍗 মুরগির রেস্তোরাঁয় যেতে চাও? >> v1.txt
echo 🏡 আমার বাড়িতে ১০টা মুরগি আছে! >> v1.txt
echo 👨‍🌾 মুরগি পালন একটা ভালো ব্যবসা! >> v1.txt
echo 🥚 প্রতিদিন মুরগির ডিম খাই! >> v1.txt
echo {"active": true, "delay": 2, "auto_continue": true} > config.json
cd ..

cd love
echo 💖 তোমাকে ভালোবাসি! > responses.txt
echo {"active": true, "romantic_level": "high"} > config.json
cd ..

cd pick
echo 🎯 আমি তোমাকে পছন্দ করি! > picks.txt
echo {"random": true, "max_picks": 10} > config.json
cd ..

cd dio
echo 🦸‍♂️ WRYYYYYYYY! > dio_lines.txt
echo {"character": "dio", "anime": "JoJo"} > config.json
cd ..

cd diagram
echo 📊 Flowchart > types.txt
echo {"types": ["flowchart", "sequence", "class"]} > config.json
cd ..

echo {} > prefix_registry.json
cd ..

cd admin
mkdir "add"
mkdir "delete"
mkdir "kick"
mkdir "out"
mkdir "start"
mkdir "stop"
mkdir "info"
mkdir "uid"

cd add
echo 👤 Adding user... > add_user.txt
echo 🎯 Adding pick... > add_pick.txt
echo 🔗 Adding URL... > add_url.txt
cd ..

cd delete
echo 👤 Deleting user... > delete_user.txt
echo {} > config.json
cd ..

cd kick
echo 👢 Kicking user... > kick_user.txt
echo {} > config.json
cd ..

cd out
echo 🚪 Leaving group... > out_group.txt
echo 👑 Admin mode leave... > out_admin.txt
echo {} > config.json
cd ..

cd start
echo 🚀 Starting live... > start_live.txt
echo {} > config.json
cd ..

cd stop
echo ⏹️ Stopping bot... > stop_bot.txt
echo {} > config.json
cd ..

cd info
echo ℹ️ User info... > user_info.txt
echo 🤖 Bot info... > bot_info.txt
echo {} > config.json
cd ..

cd uid
echo 🔢 Getting UID... > get_uid.txt
echo {} > config.json
cd ..

echo {} > admin_commands.json
cd ..

cd nicknames
mkdir "Bot"
mkdir "bow"
mkdir "Jan"
mkdir "Sona"
mkdir "Baby"

cd Bot
echo 🤖 Yes, I am Bot! > responses.txt
echo {} > config.json
cd ..

cd bow
echo 🏹 Yes boss? > responses.txt
echo {} > config.json
cd ..

cd Jan
echo 👨 Yes Jan? > responses.txt
echo {} > config.json
cd ..

cd Sona
echo 👸 Yes Sona? > responses.txt
echo {} > config.json
cd ..

cd Baby
echo 👶 Yes Baby? > responses.txt
echo {} > config.json
cd ..

echo {} > nicknames_registry.json
cd ..

echo {} > command_registry.json
echo {} > command_permissions.json
echo {} > command_stats.json
cd ..

cd learning
echo {} > user_patterns.json
echo {} > admin_knowledge.json
echo {} > bot_memories.json
echo {} > conversation_history.json
echo {} > learned_responses.json
cd ..

cd json_responses
echo {} > greetings.json
echo {} > farewells.json
echo {} > questions.json
echo {} > compliments.json
echo {} > romantic.json
echo {} > neutral.json
cd ..

cd ai_integration
mkdir "openai"
mkdir "gemini"
mkdir "deepseek"

cd openai
echo {} > config.json
echo {} > responses.json
cd ..

cd gemini
echo {} > config.json
echo {} > responses.json
cd ..

cd deepseek
echo {} > config.json
echo {} > responses.json
cd ..

echo {} > ai_config.json
cd ..

cd users
echo {} > user_profiles.json
echo {} > user_settings.json
echo {} > user_activity.json
cd ..

cd groups
echo {} > group_list.json
echo {} > group_settings.json
echo {} > group_members.json
cd ..

cd logs
echo. > bot_activity.log
echo. > error_log.log
echo. > message_log.log
echo. > command_log.log
echo. > learning_log.log
cd ..

cd backup
echo. > auto_backup.py
echo {} > backup_history.json
cd ..

cd ..
cd config
echo. > bot_config.py
echo. > facebook_config.py
echo. > ai_config.py
echo. > learning_config.py
echo. > command_config.py
echo. > photo_config.py
echo. > security_config.py
echo. > rate_limit_config.py
echo. > admin_config.py
cd ..

cd utils
echo. > __init__.py
echo. > file_handler.py
echo. > text_processor.py
echo. > encryption.py
echo. > logger.py
echo. > validator.py
echo. > backup_tool.py
echo. > proxy_manager.py
echo. > humanizer.py
echo. > formatter.py
echo. > helper_functions.py
cd ..

cd scripts
echo. > setup_bot.py
echo. > install_deps.py
echo. > extract_cookies.py
echo. > train_ai.py
echo. > backup_data.py
echo. > clean_logs.py
echo. > update_commands.py
echo. > health_check.py
echo. > start_bot.py
echo. > stop_bot.py
echo. > monitor_bot.py
cd ..

cd tests
echo. > test_bot.py
echo. > test_commands.py
echo. > test_messenger.py
echo. > test_photos.py
echo. > test_learning.py
echo. > integration_test.py
cd ..

cd docs
echo. > SETUP_GUIDE.md
echo. > COMMANDS_GUIDE.md
echo. > LEARNING_SYSTEM.md
echo. > PHOTO_SYSTEM.md
echo. > AI_INTEGRATION.md
echo. > TROUBLESHOOTING.md
echo. > FAQ.md
echo. > SECURITY_GUIDE.md
echo. > CHANGELOG.md
cd ..

cd templates
echo. > command_template.txt
echo. > response_template.json
echo. > config_template.py
echo. > photo_template.json
echo. > learning_template.json
cd ..

cd examples
mkdir "sample_commands"
mkdir "sample_responses"
mkdir "sample_configs"
mkdir "sample_photos"
cd ..

cd temp
mkdir "cache"
mkdir "downloads"
mkdir "uploads"
cd ..

cd external
echo. > openai_api.py
echo. > gemini_api.py
echo. > deepseek_api.py
echo. > telegram_api.py
cd ..

echo. > requirements.txt
echo. > requirements_ai.txt
echo. > .env.example
echo. > .gitignore
echo. > README.md
echo. > LICENSE
echo. > run.py
echo. > bot_identity.json
echo. > config.json

echo Folder structure created successfully!
pause