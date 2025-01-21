import re
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def one_hour_interval(file_path):
    # Dictionary für die 1-Stunden-Intervalle
    time_intervals = defaultdict(int)
    
    # Regex-Pattern für WhatsApp Zeitstempel
    pattern = r'\[([\d\.,\s:]+)\]'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(pattern, line)
                if match:
                    timestamp_str = match.group(1)
                    try:
                        timestamp = datetime.strptime(timestamp_str.strip(), '%d.%m.%y, %H:%M:%S')
                        
                        # Erstelle 1-Stunden-Intervall-Schlüssel
                        hour = timestamp.hour
                        interval = f"{hour:02d}:00-{(hour+1)%24:02d}:00"
                        
                        # Erhöhe Zähler für dieses Intervall
                        time_intervals[interval] += 1
                    except ValueError:
                        continue
    
        plt.figure(figsize=(12, 8))
        
        # Sortiere die Intervalle
        sorted_intervals = dict(sorted(time_intervals.items()))
        
        # Filtere Intervalle ohne Nachrichten
        filtered_intervals = {k: v for k, v in sorted_intervals.items() if v > 0}
        
        # Erstelle den Pie Chart
        plt.pie(filtered_intervals.values(), 
                labels=[f"{k}\n({v} Nachrichten)" for k, v in filtered_intervals.items()],
                autopct='%1.1f%%')
        
        plt.title('Verteilung der WhatsApp Nachrichten (1-Stunden-Intervalle)')
        plt.axis('equal')
        
        plt.savefig('whatsapp_analysis_1h.png', bbox_inches='tight', dpi=300)
        print('Saved whatsapp_analysis_1h.png')
        
        return filtered_intervals

    except Exception as e:
        print(f"Fehler beim Verarbeiten der Datei: {e}")
        return None

def messages_by_sender(file_path):
    # Dictionary für die Nachrichtenanzahl pro Person
    sender_messages = defaultdict(int)
    
    # Regex-Pattern für WhatsApp Nachrichten
    # Sucht nach Zeitstempel und Namen
    pattern = r'\[[\d\.,\s:]+\] ([^:]+): '
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(pattern, line)
                if match:
                    sender = match.group(1).strip()
                    sender_messages[sender] += 1
    
        plt.figure(figsize=(12, 8))
        
        # Sortiere nach Anzahl der Nachrichten (absteigend)
        sorted_senders = dict(sorted(sender_messages.items(), 
                                   key=lambda x: x[1], 
                                   reverse=True))
        
        # Erstelle den Pie Chart
        plt.pie(sorted_senders.values(), 
                labels=[f"{sender}\n({count} Nachrichten)" 
                       for sender, count in sorted_senders.items()],
                autopct='%1.1f%%')
        
        plt.title('Verteilung der Nachrichten pro Person')
        plt.axis('equal')
        
        plt.savefig('whatsapp_messages_by_sender.png', bbox_inches='tight', dpi=300)
        print('Saved whatsapp_messages_by_sender.png')
        
        return sorted_senders

    except Exception as e:
        print(f"Fehler beim Verarbeiten der Datei: {e}")
        return None

def analyze_word_frequency(file_path):
    # Wörter die ignoriert werden sollen
    stopwords = {
        'und', 'der', 'die', 'das', 'in', 'ist', 'für', 'von', 'mit', 'sich', 'den', 
        'zu', 'ein', 'eine', 'einen', 'dem', 'dass', 'es', 'im', 'nicht', 'auch',
        'als', 'am', 'sind', 'noch', 'wie', 'um', 'aber', 'so', 'war', 'was',
        'wenn', 'nur', 'mir', 'dir', 'mich', 'dich', 'ich', 'du', 'er', 'sie', 'wir',
        'hab', 'habe', 'haben', 'hat', 'hatte', 'dann', 'da', 'ja', 'nein', 'hier',
        'oder', 'bei', 'bis', 'war', 'wieder', 'keine', 'nach', 'schon', 'zum', 'zur',
        'was', 'wurde', 'einer', 'eines', 'einem', 'einen', 'auf', 'aus'
    }

    all_words = []
    user_words = defaultdict(list)
    
    pattern = r'\[[\d\.,\s:]+\] ([^:]+): (.+)'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(pattern, line)
                if match:
                    sender = match.group(1).strip()
                    message = match.group(2).strip().lower()
                    words = re.findall(r'\w+', message)
                    # Filtere Stopwords
                    filtered_words = [word for word in words if word not in stopwords]
                    all_words.extend(filtered_words)
                    user_words[sender].extend(filtered_words)
        
        # Zähle die häufigsten Wörter insgesamt
        word_counts = Counter(all_words)
        top_10_words = word_counts.most_common(10)
        
        # Zähle die häufigsten Wörter pro User
        user_top_words = {}
        for user, words in user_words.items():
            user_top_words[user] = Counter(words).most_common(10)
        
        # Berechne die Anzahl der Subplots
        n_users = len(user_top_words)
        n_plots = n_users + 1  # +1 für den globalen Plot
        
        # Erstelle Figure und Subplots
        fig = plt.figure(figsize=(10, 5 * n_plots))  # Breite reduziert, Höhe angepasst
        
        # Globaler Plot
        ax1 = plt.subplot(n_plots, 1, 1)
        words, counts = zip(*top_10_words)
        ax1.bar(words, counts)
        ax1.set_title('Top 10 häufigste Wörter im Chat')
        ax1.tick_params(axis='x', rotation=45)
        ax1.set_ylabel('Häufigkeit')
        
        # Plots pro User
        for idx, (user, word_counts) in enumerate(user_top_words.items(), start=2):
            words, counts = zip(*word_counts)
            ax = plt.subplot(n_plots, 1, idx)
            ax.bar(words, counts)
            ax.set_title(f'Top 10 Wörter: {user}')
            ax.tick_params(axis='x', rotation=45)
            ax.set_ylabel('Häufigkeit')
        
        plt.tight_layout()
        plt.savefig('word_frequency.png', bbox_inches='tight', dpi=300)
        print('Saved word_frequency.png')
        
        return top_10_words, user_top_words
    
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Datei: {e}")
        return None

def analyze_specific_words(file_path, target_words, excluded_users=None):
    if excluded_users is None:
        excluded_users = set()
    else:
        excluded_users = set(excluded_users)
    
    # Konvertiere alle Zielwörter zu Kleinbuchstaben
    target_words_lower = [word.lower() for word in target_words]
    
    # Zähler initialisieren
    total_counts = {word: 0 for word in target_words}
    user_counts = defaultdict(lambda: {word: 0 for word in target_words})
    
    pattern = r'\[[\d\.,\s:]+\] ([^:]+): (.+)'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(pattern, line)
                if match:
                    sender = match.group(1).strip()
                    
                    # Überspringe ausgeschlossene User
                    if sender in excluded_users:
                        continue
                        
                    message = match.group(2).lower()
                    words_in_message = re.findall(r'\b\w+\b', message)
                    
                    # Zähle Vorkommen jedes Zielworts
                    for i, target_word_lower in enumerate(target_words_lower):
                        word_count = sum(1 for word in words_in_message if word == target_word_lower)
                        total_counts[target_words[i]] += word_count
                        user_counts[sender][target_words[i]] += word_count
        
        # Visualisierung
        fig = plt.figure(figsize=(15, 10))
        
        # Gesamtzählung (oberer Plot)
        ax1 = plt.subplot(2, 1, 1)
        words = list(total_counts.keys())
        counts = list(total_counts.values())
        ax1.bar(words, counts)
        ax1.set_title('Häufigkeit der Zielwörter (Gesamt)')
        ax1.set_ylabel('Anzahl')
        plt.xticks(rotation=45)
        
        # Pro-User-Zählung (unterer Plot)
        ax2 = plt.subplot(2, 1, 2)
        users = list(user_counts.keys())
        x = np.arange(len(users))
        width = 0.8 / len(target_words)
        
        for i, word in enumerate(target_words):
            counts = [user_counts[user][word] for user in users]
            ax2.bar(x + i * width, counts, width, label=word)
        
        ax2.set_title('Häufigkeit der Zielwörter (Pro User)')
        ax2.set_xticks(x + width * (len(target_words) - 1) / 2)
        ax2.set_xticklabels(users, rotation=45)
        ax2.set_ylabel('Anzahl')
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig('specific_words_analysis.png', bbox_inches='tight', dpi=300)
        print('Saved specific_words_analysis.png')
        
        return total_counts, user_counts
    
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Datei: {e}")
        return None

def words_per_user(file_path):
    # Dictionary für die Wortanzahl pro Person
    sender_word_count = defaultdict(int)
    
    # Regex-Pattern für WhatsApp Nachrichten
    pattern = r'\[[\d\.,\s:]+\] ([^:]+): (.+)'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(pattern, line)
                if match:
                    sender = match.group(1).strip()
                    message = match.group(2).strip()
                    # Zähle die Wörter in der Nachricht
                    word_count = len(message.split())
                    sender_word_count[sender] += word_count
    
        plt.figure(figsize=(12, 8))
        
        # Sortiere nach Wortanzahl (absteigend)
        sorted_senders = dict(sorted(sender_word_count.items(), 
                                   key=lambda x: x[1], 
                                   reverse=True))
        
        plt.pie(sorted_senders.values(), 
                labels=[f"{sender}\n({count} Wörter)" 
                       for sender, count in sorted_senders.items()],
                autopct='%1.1f%%')
        
        plt.title('Verteilung der Wörter pro Person')
        plt.axis('equal')
        
        plt.savefig('whatsapp_words_per_user.png', bbox_inches='tight', dpi=300)
        print('Saved whatsapp_words_per_user.png')
        
        return sorted_senders

    except Exception as e:
        print(f"Fehler beim Verarbeiten der Datei: {e}")
        return None

def words_per_message(file_path):
    # Dictionaries für Wort- und Nachrichtenzählung pro Person
    sender_word_count = defaultdict(int)
    sender_message_count = defaultdict(int)
    
    # Regex-Pattern für WhatsApp Nachrichten
    pattern = r'\[[\d\.,\s:]+\] ([^:]+): (.+)'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(pattern, line)
                if match:
                    sender = match.group(1).strip()
                    message = match.group(2).strip()
                    # Zähle Wörter und Nachrichten
                    word_count = len(message.split())
                    sender_word_count[sender] += word_count
                    sender_message_count[sender] += 1
        
        # Berechne durchschnittliche Wörter pro Nachricht
        words_per_message = {
            sender: round(sender_word_count[sender] / sender_message_count[sender], 2)
            for sender in sender_word_count.keys()
        }
        
        # Sortiere nach Durchschnitt (absteigend)
        sorted_averages = dict(sorted(words_per_message.items(), 
                                    key=lambda x: x[1], 
                                    reverse=True))
        
        plt.figure(figsize=(12, 8))
        plt.pie(sorted_averages.values(), 
                labels=[f"{sender}\n({avg} Wörter/Nachricht)" 
                       for sender, avg in sorted_averages.items()],
                autopct='%1.1f%%')
        
        plt.title('Durchschnittliche Wortanzahl pro Nachricht und Person')
        plt.axis('equal')
        
        plt.savefig('whatsapp_words_per_message.png', bbox_inches='tight', dpi=300)
        print('Saved whatsapp_words_per_message.png')
        
        return sorted_averages, sender_message_count, sender_word_count

    except Exception as e:
        print(f"Fehler beim Verarbeiten der Datei: {e}")
        return None

def longest_messages(file_path):
   messages = []
   pattern = r'\[[\d\.,\s:]+\] ([^:]+): (.+)'
   
   try:
       with open(file_path, 'r', encoding='utf-8') as file:
           for line in file:
               match = re.match(pattern, line)
               if match:
                   sender = match.group(1).strip()
                   message = match.group(2).strip()
                   word_count = len(message.split())
                   messages.append((sender, message, word_count))
       
       # Sortiere nach Wortanzahl und nehme top 20
       top_messages = sorted(messages, key=lambda x: x[2], reverse=True)[:20]
       
       plt.figure(figsize=(15, 10))
       
       # Erstelle die Listen in umgekehrter Reihenfolge für die Darstellung von oben nach unten
       names = [msg[0] for msg in reversed(top_messages)]
       counts = [msg[2] for msg in reversed(top_messages)]
       messages_short = [msg[1][:50] + "..." if len(msg[1]) > 50 else msg[1] 
                        for msg in reversed(top_messages)]
       
       # Erstelle horizontalen Balkendiagramm
       bars = plt.barh(range(len(counts)), counts)
       
       # Füge Beschriftungen hinzu - jetzt von oben nach unten sortiert
       plt.yticks(range(len(names)), 
                 [f"{i+1}. {name}\n{msg}" for i, (name, msg) in enumerate(zip(names, messages_short))], 
                 fontsize=8)
       plt.xlabel('Anzahl Wörter')
       plt.title('Top 20 längste Nachrichten')
       
       # Füge Werte am Ende der Balken hinzu
       for i, v in enumerate(counts):
           plt.text(v, i, f' {v}', va='center')
       
       plt.tight_layout()
       plt.savefig('whatsapp_longest_messages.png', bbox_inches='tight', dpi=300)
       print('Saved whatsapp_longest_messages.png')
       
       return top_messages

   except Exception as e:
       print(f"Fehler beim Verarbeiten der Datei: {e}")
       return None

def doAll(file_path):
    #analyze_specific_words not included
    one_hour_interval(file_path)
    messages_by_sender(file_path)
    analyze_word_frequency(file_path)
    words_per_user(file_path)
    words_per_message(file_path)
    longest_messages(file_path)

# Verwendung
if __name__ == "__main__":
   file_path = "_chat.txt"
   #analyze_specific_words(file_path, ['hä', 'kek', 'müll', 'gym', 'ti', 'mathe'])
   doAll(file_path)