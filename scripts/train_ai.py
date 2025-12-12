#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 AI Training Script - Train the bot's AI models
"""

import os
import sys
import json
import time
import random
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot_core.learning_system import LearningSystem
from utils.logger import Logger

def setup_logger():
    """Setup logger for training"""
    return Logger("ai_trainer", "data/logs", "INFO")

def load_training_data():
    """Load training data from files"""
    training_data = {
        'conversations': [],
        'patterns': [],
        'responses': []
    }
    
    # Load from conversation history
    conv_file = Path("data/learning/conversation_history.json")
    if conv_file.exists():
        try:
            with open(conv_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                training_data['conversations'] = data.get('conversations', [])
        except Exception as e:
            print(f"Error loading conversation history: {e}")
    
    # Load from user patterns
    patterns_file = Path("data/learning/user_patterns.json")
    if patterns_file.exists():
        try:
            with open(patterns_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                patterns = data.get('patterns', {})
                
                # Convert patterns to training format
                for pattern_type, pattern_info in patterns.items():
                    for example in pattern_info.get('examples', []):
                        training_data['patterns'].append({
                            'type': pattern_type,
                            'message': example.get('message', ''),
                            'user_id': example.get('user_id', ''),
                            'timestamp': example.get('timestamp', '')
                        })
        except Exception as e:
            print(f"Error loading user patterns: {e}")
    
    # Load from learned responses
    responses_file = Path("data/learning/learned_responses.json")
    if responses_file.exists():
        try:
            with open(responses_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                responses = data.get('responses', {})
                
                for response_key, response_info in responses.items():
                    for response_text in response_info.get('responses', []):
                        training_data['responses'].append({
                            'key': response_key,
                            'response': response_text,
                            'confidence': response_info.get('confidence', 0.5),
                            'usage_count': response_info.get('usage_count', 0)
                        })
        except Exception as e:
            print(f"Error loading learned responses: {e}")
    
    return training_data

def train_response_generator(training_data, logger):
    """Train response generator model"""
    logger.info("Training response generator...")
    
    # This is a simplified training process
    # In a real implementation, you would use ML libraries
    
    # Analyze conversation patterns
    conversation_count = len(training_data['conversations'])
    pattern_count = len(training_data['patterns'])
    response_count = len(training_data['responses'])
    
    logger.info(f"Training data: {conversation_count} conversations, {pattern_count} patterns, {response_count} responses")
    
    # Extract common patterns
    common_patterns = extract_common_patterns(training_data['conversations'])
    
    # Build response database
    response_db = build_response_database(training_data['responses'])
    
    # Generate training report
    report = {
        'training_date': datetime.now().isoformat(),
        'data_statistics': {
            'conversations': conversation_count,
            'patterns': pattern_count,
            'responses': response_count,
            'unique_users': count_unique_users(training_data['conversations']),
            'common_patterns': len(common_patterns)
        },
        'common_patterns': common_patterns[:10],  # Top 10
        'response_coverage': calculate_response_coverage(response_db),
        'training_duration': 0  # Will be filled later
    }
    
    return report

def extract_common_patterns(conversations):
    """Extract common conversation patterns"""
    patterns = {}
    
    for conv in conversations:
        message = conv.get('message', '').lower()
        
        # Categorize by intent
        intent = categorize_intent(message)
        
        if intent:
            if intent not in patterns:
                patterns[intent] = {
                    'count': 0,
                    'examples': [],
                    'common_words': {}
                }
            
            patterns[intent]['count'] += 1
            
            # Keep only a few examples
            if len(patterns[intent]['examples']) < 5:
                patterns[intent]['examples'].append(message[:100])
            
            # Extract words
            words = extract_words(message)
            for word in words:
                if word in patterns[intent]['common_words']:
                    patterns[intent]['common_words'][word] += 1
                else:
                    patterns[intent]['common_words'][word] = 1
    
    # Convert to list and sort by count
    pattern_list = []
    for intent, data in patterns.items():
        # Get top 5 words
        top_words = sorted(
            data['common_words'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        pattern_list.append({
            'intent': intent,
            'count': data['count'],
            'top_words': [word for word, _ in top_words],
            'examples': data['examples']
        })
    
    # Sort by frequency
    pattern_list.sort(key=lambda x: x['count'], reverse=True)
    
    return pattern_list

def categorize_intent(message):
    """Categorize message intent"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['hi', 'hello', 'হাই', 'হ্যালো', 'সালাম']):
        return 'greeting'
    elif any(word in message_lower for word in ['ছবি', 'ফটো', 'photo', 'pic']):
        return 'photo_request'
    elif '?' in message_lower:
        return 'question'
    elif any(word in message_lower for word in ['ভালোবাস', 'লাভ', 'love', 'প্রেম']):
        return 'romantic'
    elif any(word in message_lower for word in ['ধন্যবাদ', 'thank', 'থ্যাংকস']):
        return 'thanks'
    elif any(word in message_lower for word in ['বিদায়', 'বাই', 'bye', 'goodbye']):
        return 'farewell'
    elif message_lower.startswith('.murgi'):
        return 'command_murgi'
    elif message_lower.startswith('.love'):
        return 'command_love'
    elif message_lower.startswith('.pick'):
        return 'command_pick'
    else:
        return 'other'

def extract_words(text):
    """Extract words from text"""
    import re
    words = re.findall(r'[\w\u0980-\u09FF]+', text.lower())
    return [word for word in words if len(word) > 1]

def build_response_database(responses):
    """Build response database from training data"""
    response_db = {}
    
    for resp in responses:
        key = resp.get('key', 'other')
        response_text = resp.get('response', '')
        confidence = resp.get('confidence', 0.5)
        
        if key not in response_db:
            response_db[key] = []
        
        response_db[key].append({
            'text': response_text,
            'confidence': confidence,
            'length': len(response_text)
        })
    
    return response_db

def calculate_response_coverage(response_db):
    """Calculate response coverage for different intents"""
    coverage = {}
    
    common_intents = ['greeting', 'photo_request', 'question', 'romantic', 
                     'thanks', 'farewell', 'command_murgi', 'command_love', 
                     'command_pick']
    
    for intent in common_intents:
        if intent in response_db:
            coverage[intent] = {
                'response_count': len(response_db[intent]),
                'has_responses': True,
                'average_confidence': sum(r['confidence'] for r in response_db[intent]) / len(response_db[intent])
            }
        else:
            coverage[intent] = {
                'response_count': 0,
                'has_responses': False,
                'average_confidence': 0
            }
    
    return coverage

def count_unique_users(conversations):
    """Count unique users in conversations"""
    user_set = set()
    
    for conv in conversations:
        user_id = conv.get('user_id', '')
        if user_id:
            user_set.add(user_id)
    
    return len(user_set)

def generate_training_examples(training_data, count=50):
    """Generate training examples for manual review"""
    examples = []
    
    # Get conversations
    conversations = training_data['conversations']
    
    if not conversations:
        return examples
    
    # Select random conversations
    selected = random.sample(
        conversations, 
        min(count, len(conversations))
    )
    
    for conv in selected:
        examples.append({
            'user_message': conv.get('message', ''),
            'bot_response': conv.get('response', ''),
            'user_id': conv.get('user_id', ''),
            'timestamp': conv.get('timestamp', ''),
            'intent': categorize_intent(conv.get('message', ''))
        })
    
    return examples

def save_training_report(report, output_file="data/learning/training_report.json"):
    """Save training report to file"""
    try:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Training report saved to {output_file}")
        
    except Exception as e:
        print(f"❌ Error saving training report: {e}")

def save_training_examples(examples, output_file="data/learning/training_examples.json"):
    """Save training examples to file"""
    try:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'example_count': len(examples),
                'examples': examples
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Training examples saved to {output_file}")
        
    except Exception as e:
        print(f"❌ Error saving training examples: {e}")

def optimize_learning_system():
    """Optimize the learning system"""
    print("🔄 Optimizing learning system...")
    
    try:
        from bot_core.learning_system import LearningSystem
        from unittest.mock import Mock
        
        # Create mock bot for learning system
        mock_bot = Mock()
        mock_bot.logger = Mock()
        mock_bot.logger.info = print
        mock_bot.logger.error = print
        mock_bot.config = {
            'learning': {
                'enabled': True,
                'learn_from_users': True,
                'learn_from_admin': True,
                'learn_from_bot': True,
                'max_memory': 1000
            },
            'admins': []
        }
        
        # Initialize learning system
        learning_system = LearningSystem(mock_bot)
        
        # Clean up old data
        learning_system.cleanup_old_data(30)
        
        # Save all knowledge
        learning_system.save_all_knowledge()
        
        print("✅ Learning system optimized")
        
        # Get statistics
        stats = learning_system.get_learning_stats()
        print(f"\n📊 Learning System Statistics:")
        for key, value in stats.items():
            if isinstance(value, (int, float)):
                print(f"  {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error optimizing learning system: {e}")
        return False

def main():
    """Main training function"""
    print("\n" + "="*60)
    print("🧠 YOUR CRUSH AI BOT - AI TRAINING SCRIPT")
    print("="*60)
    
    # Setup logger
    logger = setup_logger()
    
    print("\n📂 Loading training data...")
    
    # Load training data
    training_data = load_training_data()
    
    if not training_data['conversations'] and not training_data['patterns']:
        print("❌ No training data found!")
        print("\n💡 Suggestions:")
        print("1. Run the bot and have some conversations")
        print("2. Check if data/learning/ directory exists")
        print("3. Make sure learning is enabled in config")
        return
    
    print(f"✅ Loaded {len(training_data['conversations'])} conversations")
    print(f"✅ Loaded {len(training_data['patterns'])} patterns")
    print(f"✅ Loaded {len(training_data['responses'])} responses")
    
    # Start training
    print("\n🚀 Starting AI training...")
    start_time = time.time()
    
    # Train response generator
    report = train_response_generator(training_data, logger)
    
    # Calculate training duration
    training_duration = time.time() - start_time
    report['training_duration'] = round(training_duration, 2)
    
    # Generate training examples
    print("\n📝 Generating training examples...")
    examples = generate_training_examples(training_data, 20)
    
    # Optimize learning system
    print("\n⚡ Optimizing learning system...")
    optimization_success = optimize_learning_system()
    
    # Save results
    print("\n💾 Saving training results...")
    save_training_report(report)
    save_training_examples(examples)
    
    # Display results
    print("\n" + "="*60)
    print("🎉 TRAINING COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    print(f"\n📊 Training Report:")
    print(f"  • Training duration: {report['training_duration']} seconds")
    print(f"  • Conversations analyzed: {report['data_statistics']['conversations']}")
    print(f"  • Unique users: {report['data_statistics']['unique_users']}")
    print(f"  • Common patterns found: {report['data_statistics']['common_patterns']}")
    
    print(f"\n🎯 Response Coverage:")
    coverage = report['response_coverage']
    for intent, stats in coverage.items():
        if stats['has_responses']:
            print(f"  • {intent}: {stats['response_count']} responses (conf: {stats['average_confidence']:.2f})")
    
    print(f"\n📝 Training Examples Generated: {len(examples)}")
    
    if optimization_success:
        print("✅ Learning system optimized")
    
    print(f"\n📁 Results saved to:")
    print("  • data/learning/training_report.json")
    print("  • data/learning/training_examples.json")
    
    print("\n" + "="*60)
    print("💡 Next steps:")
    print("1. Review training examples")
    print("2. Adjust response patterns if needed")
    print("3. Continue chatting to improve AI")
    print("4. Run training periodically")
    
    print("\n📞 Support: ranaeditz333@gmail.com")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Training interrupted by user")
    except Exception as e:
        print(f"\n❌ Training error: {e}")
        import traceback
        traceback.print_exc()