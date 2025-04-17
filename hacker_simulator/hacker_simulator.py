import time
import sys
import random
import json
import hashlib
import readline
import getpass
from dataclasses import dataclass
from typing import Dict, Callable, Optional, List
from enum import Enum

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Progress animations
PROGRESS_CHARS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

def slow_print(text: str, delay: float = 0.03, color: Optional[str] = None, newline: bool = True) -> None:
    formatted_text = f"{color}{text}{Colors.ENDC}" if color else text
    try:
        delay_value = float(delay)
        for char in formatted_text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay_value)
        if newline:
            print()
    except (ValueError, TypeError):
        print(formatted_text)
        if newline:
            print()

def animated_progress(task: str, duration: int = 3, color: Optional[str] = None) -> None:
    slow_print(task + "...", color=color, newline=False)
    start_time = time.time()
    while time.time() - start_time < duration:
        for char in PROGRESS_CHARS:
            sys.stdout.write(f'\r{task}...{char} ')
            sys.stdout.flush()
            time.sleep(0.1)
    print(f"\r{task}..." + Colors.OKGREEN + "Done!" + Colors.ENDC)

# Security components
def validate_password(password: str) -> bool:
    return len(password) >= 8 and any(c.isupper() for c in password) and any(c.isdigit() for c in password)

def generate_targets() -> List[str]:
    return [f"192.168.1.{random.randint(1, 50)}" for _ in range(random.randint(3, 6))]

# Command and Virus structures
@dataclass
class Command:
    func: Callable
    description: str
    usage: str
    args: int = 0

class VirusType(Enum):
    RANSOMWARE = "Ransomware"
    TROJAN = "Trojan"
    WORM = "Worm"
    SPYWARE = "Spyware"
    ROOTKIT = "Rootkit"

@dataclass
class Virus:
    name: str
    type: VirusType
    success_rate: float
    effect: str
    detection_chance: float = 0.3

KNOWN_VIRUSES = [
    Virus("WannaCry", VirusType.RANSOMWARE, 0.7, "Encrypts files demanding Bitcoin payment", 0.4),
    Virus("Stuxnet", VirusType.WORM, 0.9, "Targets industrial control systems", 0.1),
    Virus("Zeus", VirusType.TROJAN, 0.6, "Banking trojan stealing credentials", 0.5),
    Virus("Mirai", VirusType.WORM, 0.8, "Turns IoT devices into botnets", 0.3),
    Virus("NotPetya", VirusType.RANSOMWARE, 0.85, "Destructive wiper disguised as ransomware", 0.2),
    Virus("brogotnuked", VirusType.TROJAN, 0.6, "System destabilization", 0.3) #Added for analysis example
]

class HackingSimulator:
    def __init__(self):
        self.commands = self._initialize_commands()
        self.current_user: Optional[str] = None
        self.session_score: int = 0
        self.created_viruses: Dict[str, Virus] = {}
        self.botnet_count: int = 0

    def _initialize_commands(self) -> Dict[str, Command]:
        return {
            'analyse': Command(self.command_analyze, "Analyze malware", "analyse <virus>", 1),
            'scan': Command(self.command_scan, "Scan network", "scan"),
            'hack': Command(self.command_hack, "Hack target", "hack <target>", 1),
            'status': Command(self.command_status, "System status", "status"),
            'trace': Command(self.command_trace, "Trace route", "trace <target>", 1),
            'decrypt': Command(self.command_decrypt, "Decrypt file ", "decrypt <file>", 1),
            'help': Command(self.command_help, "Show help", "help"),
            'exit': Command(self.command_exit, "Exit program", "exit"),
            'create_virus': Command(self.command_create_virus, "Create malware", "create_virus <type> <name>", 2),
            'deploy': Command(self.command_deploy, "Deploy virus", "deploy <virus> <target>", 2),
            'port_scan': Command(self.command_port_scan, "Port scan", "port_scan <target>", 1),
            'phish': Command(self.command_phish, "Phishing attack", "phish <count>", 1),
            'analyze': Command(self.command_analyze, "Analyze malware", "analyze <virus>", 1),
            'firewall': Command(self.command_firewall, "Bypass firewall", "firewall <target>", 1),
            'ddos': Command(self.command_ddos, "DDoS attack", "ddos <target>", 1),
            'encrypt': Command(self.command_encrypt, "Ransomware", "encrypt <dir>", 1),
        }

    def load_users(self) -> Dict[str, str]:
        try:
            with open('users.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_users(self, users: Dict[str, str]) -> None:
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=2)

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(f"4ndyS4lt_{password}".encode()).hexdigest()

    def register_user(self) -> None:
        while True:
            username = input("Choose username: ").strip()
            if not username:
                slow_print("Username required!", Colors.FAIL)
                continue

            users = self.load_users()
            if username in users:
                slow_print("Username exists!", Colors.FAIL)
                continue

            while True:
                password = input("Choose password (8+ chars, 1 uppercase, 1 number): ")
                if validate_password(password):
                    users[username] = self.hash_password(password)
                    self.save_users(users)
                    slow_print("Registration successful!", Colors.OKGREEN)
                    return
                slow_print("Invalid password! Must have 8+ chars, 1 uppercase, 1 number!", Colors.FAIL)

    def login_user(self) -> None:
        while True:
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            users = self.load_users()

            if users.get(username) == self.hash_password(password):
                self.current_user = username
                slow_print("\nWelcome " + username + "! Session score: " + str(self.session_score), Colors.OKGREEN)
                return
            slow_print("Invalid credentials!", Colors.FAIL)

    def command_scan(self) -> None:
        animated_progress("Scanning network", 3, Colors.OKCYAN)
        targets = generate_targets()
        slow_print("Found targets:\n" + "\n".join(targets), Colors.OKGREEN)

    def command_hack(self, target: str) -> None:
        animated_progress("Hacking " + target, 4, Colors.WARNING)
        if random.random() < 0.4:
            self.session_score += 100
            slow_print("Breach successful! +100 points", Colors.OKGREEN)
        else:
            slow_print("Hack failed!", Colors.FAIL)

    def command_status(self) -> None:
        slow_print(
            Colors.HEADER + "=== SYSTEM STATUS ===" + Colors.ENDC + "\n" +
            f":User  {self.current_user}\n" +
            f"Score: {self.session_score}\n" +
            f"Botnet Size: {self.botnet_count}\n" +
            f"Created Malware: {len(self.created_viruses)}\n" +
            "Connection: " + ("Secure" if random.random() > 0.2 else "Compromised"),
            delay=0.01
        )

    def command_trace(self, target: str) -> None:
        animated_progress("Tracing " + target, 2, Colors.OKBLUE)
        slow_print("Trace complete to " + target, Colors.OKGREEN)

    def command_decrypt(self, filename: str) -> None:
        animated_progress("Decrypting " + filename, 3, Colors.WARNING)
        if random.random() < 0.7:
            slow_print("Decrypted " + filename + "!", Colors.OKGREEN)
        else:
            slow_print("Decryption failed!", Colors.FAIL) # error located here

    def command_create_virus(self, virus_type: str, virus_name: str) -> None:
        if virus_name in self.created_viruses:
            slow_print("Virus name already exists!", Colors.FAIL)
            return

        try:
            v_type = VirusType[virus_type.upper()]
        except KeyError:
            slow_print("Invalid type! Available: " + str([t.name for t in VirusType]), Colors.FAIL)
            return

        new_virus = Virus(
            name=virus_name,
            type=v_type,
            success_rate=random.uniform(0.4, 0.8),
            effect=random.choice([
                "Data exfiltration", "System destabilization",
                "Credential harvesting", "Destructive payload"
            ]),
            detection_chance=random.uniform(0.1, 0.6)
        )
        self.created_viruses[virus_name] = new_virus
        slow_print("Created " + v_type.value + " '" + virus_name + "'!", Colors.WARNING)

    def command_deploy(self, virus_name: str, target: str) -> None:
        matches = [name for name in self.created_viruses if name.lower() == virus_name.lower()]
        if not matches:
            slow_print(f"Unknown virus '{virus_name}'!", Colors.FAIL)
            return
        elif len(matches) > 1:
            slow_print(f"Multiple viruses found matching '{virus_name}'!", Colors.FAIL)
            return

        actual_name = matches[0]
        virus = self.created_viruses[actual_name]
        animated_progress(f"Deploying {actual_name} to {target}", 3, Colors.FAIL)

        if random.random() < virus.detection_chance:
            slow_print("Detected by security systems!", Colors.FAIL)
            return

        if random.random() < virus.success_rate:
            self.session_score += 200
            slow_print(virus.type.value + " success! " + virus.effect, Colors.OKGREEN)
            if virus.type == VirusType.WORM:
                self.botnet_count += random.randint(3, 10)
                slow_print("Botnet size: " + str(self.botnet_count), Colors.WARNING)
        else:
            slow_print("Deployment failed!", Colors.FAIL)

    def command_port_scan(self, target: str) -> None:
        animated_progress("Scanning " + target, 2, Colors.OKBLUE)
        ports = {
            80: "HTTP - Apache 2.4.52",
            443: "HTTPS - OpenSSL 3.0.7",
            22: "SSH - OpenSSH 8.9p1",
            3389: "RDP - Microsoft Terminal Services"
        }
        found = random.sample(list(ports.items()), k=3)
        slow_print("Open ports on " + target + ":", Colors.OKGREEN)
        for port, service in found:
            slow_print(f"Port {port}: {service}", Colors.OKCYAN)

    def command_phish(self, target_count: str) -> None:
        try:
            count = int(target_count)
        except ValueError:
            slow_print("Invalid number!", Colors.FAIL)
            return

        animated_progress("Sending phishing emails", 2, Colors.WARNING)
        success = sum(1 for _ in range(count) if random.random() < 0.3)
        self.session_score += success * 50
        slow_print(f"Phished {success}/{count} credentials", 
                  Colors.OKGREEN if success else Colors.FAIL)

    def command_analyze(self, virus_name: str) -> None:
        all_viruses = list(KNOWN_VIRUSES) + list(self.created_viruses.values())
        virus = next((v for v in all_viruses if v.name.lower() == virus_name.lower()), None)
        if not virus:
            slow_print("Virus not found!", Colors.FAIL)
            return

        analysis = (
            Colors.HEADER + "=== " + virus.name + " Analysis ===\n" + Colors.ENDC +
            f"Type: {virus.type.value}\n" +
            f"Success Rate: {virus.success_rate*100:.1f}%\n" +
            f"Detection: {virus.detection_chance*100:.1f}%\n" +
            f"Effect: {virus.effect}\n" +
            Colors.HEADER + "=============================" + Colors.ENDC
        )
        slow_print(analysis)

    def command_firewall(self, target: str) -> None:
        animated_progress("Bypassing " + target + " firewall", 3, Colors.WARNING)
        if random.random() < 0.6:
            slow_print("Firewall bypassed!", Colors.OKGREEN)
            self.session_score += 75
        else:
            slow_print("Bypass failed!", Colors.FAIL)

    def command_ddos(self, target: str) -> None:
        if self.botnet_count < 100:
            slow_print(f"Need 100+ bots (current: {self.botnet_count})", Colors.FAIL)
            return animated_progress("DDoSing " + target, 4, Colors.FAIL)
        if random.random() < 0.66:
            slow_print(target + " overwhelmed!", Colors.OKGREEN)
            self.session_score += 300
        else:
            slow_print("DDoS mitigated!", Colors.FAIL)

    def command_encrypt(self, directory: str) -> None:
        animated_progress("Encrypting " + directory, 5, Colors.FAIL)
        if random.random() < 0.75:
            slow_print("Ransomware deployed! 0.5 BTC demanded.", Colors.WARNING)
            self.session_score += 500
        else:
            slow_print("Encryption failed!", Colors.FAIL)

    def command_help(self) -> None:
        slow_print(Colors.HEADER + "=== COMMAND HELP ===" + Colors.ENDC)
        for cmd, details in self.commands.items():
            slow_print(Colors.BOLD + f"{details.usage:<25}" + Colors.ENDC + details.description)
        slow_print(Colors.WARNING + "\nMalware types: " + str([t.name for t in VirusType]) + Colors.ENDC)

    def command_exit(self) -> None:
        slow_print("Final score: " + str(self.session_score), Colors.HEADER)
        sys.exit(0)

    def start(self) -> None:
        slow_print("=== Welcome to CyberHackSim ===", Colors.HEADER)
        while True:
            choice = input("1) Login\n2) Register\n> ").strip()
            if choice == '1':
                self.login_user()
                break
            elif choice == '2':
                self.register_user()
            else:
                slow_print("Invalid option!", Colors.FAIL)

        while True:
            try:
                command_input = input(f"{Colors.BOLD}{self.current_user}@cyberhack> {Colors.ENDC}").strip()
                if not command_input:
                    continue
                parts = command_input.split()
                name = parts[0]
                args = parts[1:]
                if name in self.commands:
                    cmd = self.commands[name]
                    if len(args) < cmd.args:
                        slow_print("Usage: " + cmd.usage, Colors.WARNING)
                    else:
                        cmd.func(*args)
                else:
                    slow_print("Unknown command! Try 'help'", Colors.FAIL)
            except KeyboardInterrupt:
                print("\n")
                self.command_exit()
            except Exception as e:
                slow_print(f"Error: {e}", Colors.FAIL)

if __name__ == "__main__":
    sim = HackingSimulator()
    sim.start()

