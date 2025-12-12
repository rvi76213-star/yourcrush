#!/usr/bin/env python3
"""
📊 বট মনিটরিং স্ক্রিপ্ট
এই স্ক্রিপ্টটি YOUR CRUSH AI বটের কর্মক্ষমতা এবং স্বাস্থ্য মনিটর করে
"""

import os
import sys
import json
import time
import psutil
import threading
import subprocess
from datetime import datetime, timedelta
from collections import deque
import matplotlib.pyplot as plt
import numpy as np

# প্রজেক্ট রুট ডিরেক্টরি সেট করুন
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from utils.logger import setup_logger
from utils.file_handler import read_json, write_json

class BotMonitor:
    def __init__(self):
        self.logger = setup_logger('bot_monitor')
        self.monitoring = False
        self.stats_file = 'temp/monitor_stats.json'
        self.alert_file = 'temp/monitor_alerts.json'
        
        # মনিটরিং ডেটা
        self.cpu_history = deque(maxlen=100)
        self.memory_history = deque(maxlen=100)
        self.message_history = deque(maxlen=100)
        self.error_history = deque(maxlen=50)
        
        # থ্রেশহোল্ড
        self.thresholds = {
            'cpu_warning': 80.0,
            'cpu_critical': 95.0,
            'memory_warning': 85.0,
            'memory_critical': 95.0,
            'disk_warning': 90.0,
            'disk_critical': 98.0,
            'error_threshold': 10,  # প্রতি মিনিটে এরর
            'response_time_warning': 5.0,  # সেকেন্ড
            'uptime_warning': 24 * 3600  # 24 ঘন্টা (রিস্টার্ট সুপারিশ)
        }
        
        # স্ট্যাটাস
        self.status = {
            'bot_running': False,
            'bot_pid': None,
            'bot_uptime': 0,
            'last_check': None,
            'alerts': [],
            'performance_score': 100
        }
        
        # লোড previous stats
        self.load_stats()
    
    def load_stats(self):
        """পূর্বের স্ট্যাটস লোড করুন"""
        try:
            if os.path.exists(self.stats_file):
                data = read_json(self.stats_file)
                self.cpu_history = deque(data.get('cpu_history', []), maxlen=100)
                self.memory_history = deque(data.get('memory_history', []), maxlen=100)
                self.message_history = deque(data.get('message_history', []), maxlen=100)
                self.error_history = deque(data.get('error_history', []), maxlen=50)
                self.logger.info("পূর্বের স্ট্যাটস লোড করা হয়েছে")
        except Exception as e:
            self.logger.warning(f"স্ট্যাটস লোড করতে পারেনি: {e}")
    
    def save_stats(self):
        """স্ট্যাটস সেভ করুন"""
        try:
            data = {
                'cpu_history': list(self.cpu_history),
                'memory_history': list(self.memory_history),
                'message_history': list(self.message_history),
                'error_history': list(self.error_history),
                'last_update': datetime.now().isoformat()
            }
            write_json(self.stats_file, data)
        except Exception as e:
            self.logger.error(f"স্ট্যাটস সেভ করতে পারেনি: {e}")
    
    def check_bot_process(self):
        """বট প্রক্রিয়াটির অবস্থা চেক করুন"""
        pid_file = 'temp/bot.pid'
        
        if not os.path.exists(pid_file):
            self.status['bot_running'] = False
            self.status['bot_pid'] = None
            return False
        
        try:
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            process = psutil.Process(pid)
            
            if process.is_running():
                self.status['bot_running'] = True
                self.status['bot_pid'] = pid
                self.status['bot_uptime'] = time.time() - process.create_time()
                
                # প্রক্রিয়াটির কমান্ড লাইন চেক করুন
                cmdline = ' '.join(process.cmdline())
                if 'master_bot' not in cmdline and 'start_bot' not in cmdline:
                    self.add_alert('WARNING', f"প্রক্রিয়াটি সঠিক বট নয় (PID: {pid})")
                
                return True
            else:
                self.status['bot_running'] = False
                self.status['bot_pid'] = None
                return False
                
        except (psutil.NoSuchProcess, ValueError, IOError):
            self.status['bot_running'] = False
            self.status['bot_pid'] = None
            return False
    
    def check_system_resources(self):
        """সিস্টেম রিসোর্স চেক করুন"""
        try:
            # CPU ব্যবহার
            cpu_percent = psutil.cpu_percent(interval=1)
            self.cpu_history.append(cpu_percent)
            
            if cpu_percent > self.thresholds['cpu_critical']:
                self.add_alert('CRITICAL', f"CPU ব্যবহার অত্যধিক: {cpu_percent}%")
            elif cpu_percent > self.thresholds['cpu_warning']:
                self.add_alert('WARNING', f"CPU ব্যবহার বেশি: {cpu_percent}%")
            
            # মেমোরি ব্যবহার
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            self.memory_history.append(memory_percent)
            
            if memory_percent > self.thresholds['memory_critical']:
                self.add_alert('CRITICAL', f"মেমোরি ব্যবহার অত্যধিক: {memory_percent}%")
            elif memory_percent > self.thresholds['memory_warning']:
                self.add_alert('WARNING', f"মেমোরি ব্যবহার বেশি: {memory_percent}%")
            
            # ডিস্ক ব্যবহার
            disk = psutil.disk_usage('.')
            disk_percent = disk.percent
            
            if disk_percent > self.thresholds['disk_critical']:
                self.add_alert('CRITICAL', f"ডিস্ক স্পেস অত্যধিক কম: {disk_percent}%")
            elif disk_percent > self.thresholds['disk_warning']:
                self.add_alert('WARNING', f"ডিস্ক স্পেস কম: {disk_percent}%")
            
            # নেটওয়ার্ক
            net_io = psutil.net_io_counters()
            self.status['network_sent'] = net_io.bytes_sent
            self.status['network_recv'] = net_io.bytes_recv
            
            return {
                'cpu': cpu_percent,
                'memory': memory_percent,
                'disk': disk_percent,
                'memory_available': memory.available // (1024 * 1024)  # MB
            }
            
        except Exception as e:
            self.logger.error(f"সিস্টেম রিসোর্স চেক করতে ত্রুটি: {e}")
            return None
    
    def check_bot_logs(self):
        """বট লগ চেক করুন"""
        log_file = 'logs/bot_activity.log'
        error_log = 'logs/error_log.log'
        
        stats = {
            'errors_last_hour': 0,
            'messages_last_hour': 0,
            'last_error': None,
            'last_activity': None
        }
        
        try:
            # এক ঘন্টার মধ্যে এরর সংখ্যা
            if os.path.exists(error_log):
                one_hour_ago = datetime.now() - timedelta(hours=1)
                
                with open(error_log, 'r', encoding='utf-8') as f:
                    for line in f:
                        if 'ERROR' in line:
                            try:
                                # লাইন থেকে সময় পার্স করুন
                                log_time_str = line.split(' - ')[0]
                                log_time = datetime.strptime(log_time_str, '%Y-%m-%d %H:%M:%S')
                                
                                if log_time > one_hour_ago:
                                    stats['errors_last_hour'] += 1
                                
                                stats['last_error'] = line.strip()
                            except:
                                pass
            
            # শেষ কার্যকলাপ
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines:
                        stats['last_activity'] = lines[-1].strip()
            
            # এরর থ্রেশহোল্ড চেক করুন
            if stats['errors_last_hour'] > self.thresholds['error_threshold']:
                self.add_alert('WARNING', 
                    f"প্রতি ঘণ্টায় অনেক বেশি এরর: {stats['errors_last_hour']}")
            
            self.error_history.append(stats['errors_last_hour'])
            
            return stats
            
        except Exception as e:
            self.logger.error(f"লগ চেক করতে ত্রুটি: {e}")
            return stats
    
    def check_message_activity(self):
        """মেসেজ কার্যকলাপ চেক করুন"""
        try:
            # মেসেজ লগ থেকে শেষ এক ঘণ্টার মেসেজ সংখ্যা
            log_file = 'logs/message_log.log'
            messages_last_hour = 0
            
            if os.path.exists(log_file):
                one_hour_ago = datetime.now() - timedelta(hours=1)
                
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if 'SENT:' in line or 'RECEIVED:' in line:
                            try:
                                log_time_str = line.split(' - ')[0]
                                log_time = datetime.strptime(log_time_str, '%Y-%m-%d %H:%M:%S')
                                
                                if log_time > one_hour_ago:
                                    messages_last_hour += 1
                            except:
                                pass
            
            self.message_history.append(messages_last_hour)
            
            return messages_last_hour
            
        except Exception as e:
            self.logger.error(f"মেসেজ কার্যকলাপ চেক করতে ত্রুটি: {e}")
            return 0
    
    def check_external_services(self):
        """এক্সটার্নাল সার্ভিস চেক করুন"""
        services = {
            'facebook': {'url': 'https://www.facebook.com', 'port': 443},
            'internet': {'url': 'https://www.google.com', 'port': 443},
            'api_server': {'url': 'http://localhost:5000', 'port': 5000}
        }
        
        results = {}
        
        for name, service in services.items():
            try:
                import socket
                import requests
                
                # টেস্ট কানেকশন
                socket.setdefaulttimeout(5)
                
                if service.get('url', '').startswith('http'):
                    response = requests.get(service['url'], timeout=5)
                    results[name] = response.status_code == 200
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((service['url'], service['port']))
                    sock.close()
                    results[name] = True
                    
            except Exception as e:
                results[name] = False
                if name == 'facebook':
                    self.add_alert('CRITICAL', f"ফেসবুক কানেক্টিভিটি সমস্যা: {e}")
        
        return results
    
    def calculate_performance_score(self):
        """পারফরম্যান্স স্কোর ক্যালকুলেট করুন"""
        score = 100
        
        # CPU স্কোর
        if self.cpu_history:
            avg_cpu = np.mean(list(self.cpu_history)[-10:])  # শেষ 10 রিডিং
            if avg_cpu > 90:
                score -= 30
            elif avg_cpu > 70:
                score -= 15
            elif avg_cpu > 50:
                score -= 5
        
        # মেমোরি স্কোর
        if self.memory_history:
            avg_memory = np.mean(list(self.memory_history)[-10:])
            if avg_memory > 90:
                score -= 30
            elif avg_memory > 75:
                score -= 15
            elif avg_memory > 60:
                score -= 5
        
        # এরর স্কোর
        if self.error_history:
            recent_errors = list(self.error_history)[-5:]
            avg_errors = np.mean(recent_errors)
            if avg_errors > 20:
                score -= 40
            elif avg_errors > 10:
                score -= 20
            elif avg_errors > 5:
                score -= 10
        
        # আপটাইম স্কোর
        if self.status['bot_uptime'] > self.thresholds['uptime_warning']:
            score -= 10  # দীর্ঘ সময় চললে রিস্টার্ট সুপারিশ
        
        # মেসেজ কার্যকলাপ স্কোর
        if self.message_history:
            recent_messages = list(self.message_history)[-5:]
            avg_messages = np.mean(recent_messages)
            if avg_messages == 0:
                score -= 20  # কোনো কার্যকলাপ নেই
        
        score = max(0, min(100, score))
        self.status['performance_score'] = score
        
        return score
    
    def add_alert(self, level, message):
        """অ্যালার্ট যোগ করুন"""
        alert = {
            'level': level,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        self.status['alerts'].append(alert)
        
        # লগ করুন
        if level == 'CRITICAL':
            self.logger.critical(f"অ্যালার্ট: {message}")
        elif level == 'WARNING':
            self.logger.warning(f"অ্যালার্ট: {message}")
        else:
            self.logger.info(f"অ্যালার্ট: {message}")
        
        # সর্বোচ্চ 20টি অ্যালার্ট রাখুন
        if len(self.status['alerts']) > 20:
            self.status['alerts'] = self.status['alerts'][-20:]
    
    def send_notification(self, alert):
        """অ্যালার্ট নোটিফিকেশন পাঠান"""
        # এখানে নোটিফিকেশন সিস্টেম ইমপ্লিমেন্ট করুন
        # যেমন: Telegram bot, Email, Discord webhook, etc.
        
        # উদাহরণ: কনসোলে প্রিন্ট করুন
        print(f"\n🔔 {alert['level']}: {alert['message']}")
    
    def generate_report(self):
        """মনিটরিং রিপোর্ট তৈরি করুন"""
        self.check_bot_process()
        resources = self.check_system_resources()
        log_stats = self.check_bot_logs()
        message_activity = self.check_message_activity()
        services = self.check_external_services()
        performance_score = self.calculate_performance_score()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'bot_status': {
                'running': self.status['bot_running'],
                'pid': self.status['bot_pid'],
                'uptime_hours': self.status['bot_uptime'] / 3600 if self.status['bot_uptime'] else 0
            },
            'system_resources': resources,
            'activity': {
                'messages_last_hour': message_activity,
                'errors_last_hour': log_stats.get('errors_last_hour', 0),
                'last_activity': log_stats.get('last_activity'),
                'last_error': log_stats.get('last_error')
            },
            'services': services,
            'performance': {
                'score': performance_score,
                'grade': self.get_performance_grade(performance_score)
            },
            'alerts': self.status['alerts'][-5:],  # শেষ 5টি অ্যালার্ট
            'recommendations': self.generate_recommendations()
        }
        
        return report
    
    def get_performance_grade(self, score):
        """পারফরম্যান্স স্কোর থেকে গ্রেড দিন"""
        if score >= 90:
            return 'A+ (Excellent)'
        elif score >= 80:
            return 'A (Good)'
        elif score >= 70:
            return 'B (Fair)'
        elif score >= 60:
            return 'C (Poor)'
        elif score >= 50:
            return 'D (Bad)'
        else:
            return 'F (Critical)'
    
    def generate_recommendations(self):
        """সুপারিশ তৈরি করুন"""
        recommendations = []
        
        # CPU সুপারিশ
        if self.cpu_history:
            avg_cpu = np.mean(list(self.cpu_history)[-10:])
            if avg_cpu > 90:
                recommendations.append("🚨 CPU ব্যবহার অত্যধিক বেশি। প্রক্রিয়া অপ্টিমাইজ করুন।")
            elif avg_cpu > 70:
                recommendations.append("⚠️ CPU ব্যবহার বেশি। অতিরিক্ত প্রক্রিয়া চেক করুন।")
        
        # মেমোরি সুপারিশ
        if self.memory_history:
            avg_memory = np.mean(list(self.memory_history)[-10:])
            if avg_memory > 90:
                recommendations.append("🚨 মেমোরি ব্যবহার অত্যধিক বেশি। মেমোরি লিক চেক করুন।")
            elif avg_memory > 75:
                recommendations.append("⚠️ মেমোরি ব্যবহার বেশি। ক্যাশে পরিষ্কার করুন।")
        
        # আপটাইম সুপারিশ
        if self.status['bot_uptime'] > self.thresholds['uptime_warning']:
            recommendations.append("🔄 বট দীর্ঘ সময় ধরে চলছে। রিস্টার্ট বিবেচনা করুন।")
        
        # এরর সুপারিশ
        if self.error_history:
            recent_errors = list(self.error_history)[-5:]
            avg_errors = np.mean(recent_errors)
            if avg_errors > 10:
                recommendations.append("🐛 অনেক বেশি এরর। লগ চেক করুন এবং বাগ ফিক্স করুন।")
        
        # কার্যকলাপ সুপারিশ
        if self.message_history:
            recent_messages = list(self.message_history)[-5:]
            avg_messages = np.mean(recent_messages)
            if avg_messages == 0:
                recommendations.append("🔇 কোনো মেসেজ কার্যকলাপ নেই। কানেকশন চেক করুন।")
        
        if not recommendations:
            recommendations.append("✅ সবকিছু ঠিক আছে। চমৎকার চলছে!")
        
        return recommendations
    
    def display_report(self, report):
        """রিপোর্ট প্রদর্শন করুন"""
        print("\n" + "="*70)
        print("🤖 YOUR CRUSH AI BOT - MONITORING REPORT")
        print("="*70)
        
        # বট স্ট্যাটাস
        bot_status = report['bot_status']
        print(f"\n📊 BOT STATUS:")
        print(f"   {'✅ চলছে' if bot_status['running'] else '❌ বন্ধ'}")
        if bot_status['running']:
            print(f"   PID: {bot_status['pid']}")
            print(f"   আপটাইম: {bot_status['uptime_hours']:.2f} ঘণ্টা")
        
        # পারফরম্যান্স
        perf = report['performance']
        print(f"\n⭐ PERFORMANCE:")
        print(f"   স্কোর: {perf['score']}/100")
        print(f"   গ্রেড: {perf['grade']}")
        
        # সিস্টেম রিসোর্স
        if report['system_resources']:
            res = report['system_resources']
            print(f"\n💻 SYSTEM RESOURCES:")
            print(f"   CPU: {res['cpu']:.1f}%")
            print(f"   মেমোরি: {res['memory']:.1f}% ({res.get('memory_available', 0)} MB খালি)")
            print(f"   ডিস্ক: {res['disk']:.1f}%")
        
        # কার্যকলাপ
        act = report['activity']
        print(f"\n📈 ACTIVITY:")
        print(f"   শেষ ঘণ্টার মেসেজ: {act['messages_last_hour']}")
        print(f"   শেষ ঘণ্টার এরর: {act['errors_last_hour']}")
        
        # সার্ভিস
        services = report['services']
        print(f"\n🌐 SERVICES:")
        for service, status in services.items():
            print(f"   {service}: {'✅' if status else '❌'}")
        
        # অ্যালার্ট
        if report['alerts']:
            print(f"\n🚨 ALERTS (সর্বশেষ 5টি):")
            for alert in report['alerts']:
                level_icon = '🚨' if alert['level'] == 'CRITICAL' else '⚠️'
                print(f"   {level_icon} [{alert['level']}] {alert['message']}")
        
        # সুপারিশ
        if report['recommendations']:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in report['recommendations']:
                print(f"   • {rec}")
        
        print("\n" + "="*70)
        print(f"🕒 রিপোর্ট সময়: {report['timestamp']}")
        print("="*70 + "\n")
    
    def generate_graphs(self):
        """গ্রাফ তৈরি করুন"""
        try:
            if not self.cpu_history or not self.memory_history:
                return
            
            # সময় অক্ষের জন্য ডেটা
            time_points = list(range(len(self.cpu_history)))
            
            plt.figure(figsize=(12, 8))
            
            # CPU ব্যবহার গ্রাফ
            plt.subplot(2, 2, 1)
            plt.plot(time_points, list(self.cpu_history), 'r-', linewidth=2)
            plt.title('CPU Usage (%)')
            plt.xlabel('Time')
            plt.ylabel('Percentage')
            plt.grid(True, alpha=0.3)
            plt.ylim(0, 100)
            
            # মেমোরি ব্যবহার গ্রাফ
            plt.subplot(2, 2, 2)
            plt.plot(time_points, list(self.memory_history), 'b-', linewidth=2)
            plt.title('Memory Usage (%)')
            plt.xlabel('Time')
            plt.ylabel('Percentage')
            plt.grid(True, alpha=0.3)
            plt.ylim(0, 100)
            
            # মেসেজ কার্যকলাপ গ্রাফ
            plt.subplot(2, 2, 3)
            plt.bar(range(len(self.message_history)), list(self.message_history), color='g')
            plt.title('Message Activity (per hour)')
            plt.xlabel('Hours ago')
            plt.ylabel('Message Count')
            plt.grid(True, alpha=0.3)
            
            # এরর হিস্ট্রি গ্রাফ
            plt.subplot(2, 2, 4)
            plt.bar(range(len(self.error_history)), list(self.error_history), color='orange')
            plt.title('Error History (per hour)')
            plt.xlabel('Hours ago')
            plt.ylabel('Error Count')
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # সেভ করুন
            graph_file = 'temp/monitor_graph.png'
            plt.savefig(graph_file, dpi=100)
            plt.close()
            
            self.logger.info(f"গ্রাফ সেভ করা হয়েছে: {graph_file}")
            return graph_file
            
        except Exception as e:
            self.logger.error(f"গ্রাফ তৈরি করতে ত্রুটি: {e}")
            return None
    
    def monitor_loop(self, interval=60):
        """মনিটরিং লুপ"""
        self.monitoring = True
        check_count = 0
        
        self.logger.info(f"মনিটরিং শুরু হয়েছে (ইন্টারভাল: {interval}সেকেন্ড)")
        
        try:
            while self.monitoring:
                check_count += 1
                
                # রিপোর্ট তৈরি করুন
                report = self.generate_report()
                
                # প্রতি 5ম চেকে প্রদর্শন করুন
                if check_count % 5 == 0:
                    self.display_report(report)
                
                # প্রতি 10ম চেকে গ্রাফ তৈরি করুন
                if check_count % 10 == 0:
                    self.generate_graphs()
                    self.save_stats()
                
                # গুরুতর অ্যালার্ট পাঠান
                for alert in self.status['alerts'][-3:]:  # শেষ 3টি
                    if alert['level'] in ['CRITICAL', 'WARNING']:
                        self.send_notification(alert)
                
                # অ্যালার্ট ক্লিয়ার করুন (পুরানো)
                if len(self.status['alerts']) > 20:
                    self.status['alerts'] = self.status['alerts'][-10:]
                
                # বিরতি দিন
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.logger.info("মনিটরিং বন্ধ করা হয়েছে (KeyboardInterrupt)")
        except Exception as e:
            self.logger.error(f"মনিটরিং লুপ ত্রুটি: {e}")
        finally:
            self.monitoring = False
            self.save_stats()
            self.logger.info("মনিটরিং শেষ হয়েছে")
    
    def start_monitoring(self, interval=60, duration=None):
        """মনিটরিং শুরু করুন"""
        # শেষ রিপোর্ট দেখান
        initial_report = self.generate_report()
        self.display_report(initial_report)
        
        # মনিটরিং থ্রেড শুরু করুন
        monitor_thread = threading.Thread(
            target=self.monitor_loop,
            args=(interval,),
            daemon=True
        )
        monitor_thread.start()
        
        self.logger.info(f"মনিটরিং থ্রেড শুরু হয়েছে (ইন্টারভাল: {interval}সেকেন্ড)")
        
        # নির্দিষ্ট সময়ের জন্য অপেক্ষা করুন
        if duration:
            try:
                time.sleep(duration)
                self.stop_monitoring()
            except KeyboardInterrupt:
                self.stop_monitoring()
        else:
            try:
                while self.monitoring:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop_monitoring()
    
    def stop_monitoring(self):
        """মনিটরিং বন্ধ করুন"""
        self.monitoring = False
        self.save_stats()
        self.logger.info("মনিটরিং বন্ধ করা হয়েছে")

def main():
    """মেইন ফাংশন"""
    import argparse
    
    parser = argparse.ArgumentParser(description='YOUR CRUSH AI বট মনিটর করুন')
    parser.add_argument('--interval', '-i', type=int, default=60,
                       help='চেকিং ইন্টারভাল (সেকেন্ড, ডিফল্ট: 60)')
    parser.add_argument('--duration', '-d', type=int,
                       help='মনিটরিং সময়কাল (সেকেন্ড)')
    parser.add_argument('--report', '-r', action='store_true',
                       help='শুধু একটি রিপোর্ট তৈরি করুন')
    parser.add_argument('--graph', '-g', action='store_true',
                       help='গ্রাফ তৈরি করুন')
    parser.add_argument('--alerts', '-a', action='store_true',
                       help='শুধু অ্যালার্ট দেখান')
    parser.add_argument('--export', '-e', type=str,
                       help='রিপোর্ট JSON ফাইলে এক্সপোর্ট করুন')
    
    args = parser.parse_args()
    
    monitor = BotMonitor()
    
    if args.report:
        # শুধু রিপোর্ট তৈরি করুন
        report = monitor.generate_report()
        monitor.display_report(report)
        
        if args.export:
            try:
                with open(args.export, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                print(f"✅ রিপোর্ট এক্সপোর্ট করা হয়েছে: {args.export}")
            except Exception as e:
                print(f"❌ রিপোর্ট এক্সপোর্ট করতে পারেনি: {e}")
    
    elif args.graph:
        # শুধু গ্রাফ তৈরি করুন
        graph_file = monitor.generate_graphs()
        if graph_file:
            print(f"✅ গ্রাফ তৈরি করা হয়েছে: {graph_file}")
        else:
            print("❌ গ্রাফ তৈরি করতে পারেনি")
    
    elif args.alerts:
        # শুধু অ্যালার্ট দেখান
        report = monitor.generate_report()
        if report['alerts']:
            print("\n🚨 ACTIVE ALERTS:")
            for alert in report['alerts']:
                print(f"  [{alert['level']}] {alert['message']}")
        else:
            print("\n✅ কোনো অ্যাক্টিভ অ্যালার্ট নেই")
    
    else:
        # সম্পূর্ণ মনিটরিং শুরু করুন
        print("\n" + "="*70)
        print("📊 YOUR CRUSH AI BOT - MONITORING SYSTEM")
        print("="*70)
        print(f"ইন্টারভাল: {args.interval} সেকেন্ড")
        if args.duration:
            print(f"সময়কাল: {args.duration} সেকেন্ড")
        print("Ctrl+C চাপলে বন্ধ হবে")
        print("="*70 + "\n")
        
        monitor.start_monitoring(
            interval=args.interval,
            duration=args.duration
        )

if __name__ == "__main__":
    main()