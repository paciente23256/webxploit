#!/usr/bin/python
# @paciente23256

"""
webxploit 2.0.2025

@paciente23256

Melhorias realizadas (change log):

    - Uso do pathlib para paths mais seguros e legíveis.
    - Remoção de redundâncias como verificações repetidas de argumentos.
    - Modularização com funções pequenas e bem definidas
    - Evita exceções genéricas, agora indicando qual erro ocorreu.
    - Melhoria na leitura dos arquivos, usando .read_text() e .write_text() onde possível.
    - Melhoria na leitura dos logs, evitando uso de system('grep').
    - Melhoria na diversidade e formato dos relatórios.
    - Possibilidade de adicionar um alvo (ip/dns).
    - Novos modulos orientados a alvos Web.

"""


import sys
import logging
import time
import json
import argparse
import fileinput
import re
from pathlib import Path
from subprocess import run, PIPE
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        log.error(f"\033[0;31m\033[1m[!]\033[0m Cannot load configuration\nException: {e}\n")
        sys.exit(1)


def validate_module_config(modules, modules_folder):
    missing = [Path(module).name for module in modules if not (modules_folder / Path(module).name).is_file()]
    if missing:
        log.warning(f"Module(s) are missing: {', '.join(missing)}")


def generate_rcs(targets, threads, project_name, config, base_path, logs_folder):
    modules_folder = base_path / config.get('modulesfolder')
    postmodule = "spool off\n\n"
    premodule = f"spool {logs_folder}/{project_name}/"
    modules = config.get('modules')
    settings = config.get('settings', {})

    validate_module_config(modules, modules_folder)

    threads = threads or config.get('defaultthreads')

    rc_lines = []

    for target in targets:
        for module in modules:
            module_name = Path(module).name
            module_path = modules_folder / module_name
            run_module = True
            custom_settings = settings.get(module, {})

            if any(value == "CHANGEME" for value in custom_settings.values()):
                log.warning(f"No customizations have been defined for the module {module}")
                run_module = False
            else:
                log.info(f"Module settings have been customized {module}")

            if run_module and module_path.is_file():
                rc_lines.append(f"{premodule}{module_name}.log")
                rc_lines.append(f"use {module}")
                rc_lines.append(f"setg threads {threads}")
                for key, value in custom_settings.items():
                    rc_lines.append(f"set {key} {value}")
                with open(module_path, 'r') as f:
                    rc_lines.append(f.read().replace("%IP%", target))
                rc_lines.append(postmodule)

    rc_lines.append("exit -y\n")

    rc_file_path = logs_folder / project_name / 'file.rc'
    rc_file_path.write_text("\n".join(rc_lines))


def run_rcs(project_name, logs_folder):
    log.critical('\n→→→→→→→→→→ Starting msfconsole ←←←←←←←←←←')
    rc_path = logs_folder / project_name / 'file.rc'
    run(['msfconsole', '-r', str(rc_path)])
    log.info('\n→→→→→→→→→→ MFS Completed ←←←←←←←←←←\n')


def get_successful(project_name, logs_folder):
    log.critical('\n→→→→→→→→→→ Summary of findings ←←←←←←←←←←\n')
    project_path = logs_folder / project_name

    for log_file in project_path.glob("*.log"):
        log.warning(f'- Module: {log_file.stem}')
        with open(log_file, 'r') as f:
            for line in f:
                if '[+]' in line:
                    formatted = re.sub(r"\[\+\]", "\033[0;32m\033[1m[+]\033[0m", line)
                    log.critical(formatted.strip())

    log.critical('\n→→→→→→→→→→ MFS Completed ←←←←←←←←←←')


class LogFormat(logging.Formatter):
    crit_fmt = "%(msg)s"
    err_fmt = "\033[0;33m\033[1m[!]\033[0m %(msg)s"
    warn_fmt = "\033[0;34m\033[1m[*]\033[0m %(msg)s"
    info_fmt = "\033[0;32m\033[1m[+]\033[0m %(msg)s"
    dbg_fmt = "\033[0;31m\033[1m[-]\033[0m %(msg)s"

    def format(self, record):
        format_orig = self._fmt
        self._fmt = {
            logging.DEBUG: self.dbg_fmt,
            logging.INFO: self.info_fmt,
            logging.WARN: self.warn_fmt,
            logging.ERROR: self.err_fmt,
            logging.CRITICAL: self.crit_fmt,
        }.get(record.levelno, self._fmt)

        result = super().format(record)
        self._fmt = format_orig
        return result



def generate_report(project_name, logs_folder, output_formats=['json', 'html', 'pdf']):
    project_path = Path(logs_folder) / project_name
    results = []

    for logfile in project_path.glob("*.log"):
        with logfile.open("r") as f:
            lines = f.readlines()

        for line in lines:
            if '[+]' in line:
                results.append({
                    "target": logfile.stem,
                    "module": logfile.stem,
                    "status": "success",
                    "output": line.strip()
                })

    if 'json' in output_formats:
        json_path = project_path / "report.json"
        with json_path.open("w") as f:
            json.dump(results, f, indent=4)

    if 'html' in output_formats:
        html_path = project_path / "report.html"
        with html_path.open("w", encoding="utf-8") as f:
            f.write("<html><head><meta charset='UTF-8'><title>Webxploit Report</title></head><body>")
            f.write("<h1>Webxploit Report</h1><table border='1'><tr><th>Target</th><th>Module</th><th>Status</th><th>Output</th></tr>")
            for r in results:
                f.write(f"<tr><td>{r['target']}</td><td>{r['module']}</td><td>{r['status']}</td><td>{r['output']}</td></tr>")
            f.write("</table></body></html>")

    if 'pdf' in output_formats:
        pdf_path = project_path / "report.pdf"
        c = canvas.Canvas(str(pdf_path), pagesize=A4)
        width, height = A4
        c.setFont("Helvetica", 10)
        y = height - 40
        c.drawString(50, y, "Webxploit Report")
        y -= 20
        for r in results:
            line = f"Target: {r['target']} | Module: {r['module']} | Status: {r['status']} | Output: {r['output']}"
            c.drawString(50, y, line)
            y -= 15
            if y < 40:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height - 40
        c.save()




def ascii_banner():
    print(r"""
     ┓     ┓  •
┓┏┏┏┓┣┓┓┏┏┓┃┏┓┓╋
┗┻┛┗ ┗┛┛┗┣┛┗┗┛┗┗
         ┛
     With Metasploit
    """)


if __name__ == '__main__':
    base_path = Path(__file__).resolve().parent
    log_file = base_path / 'webxploit.log'
    logging.basicConfig(filename=log_file, level=logging.DEBUG)
    log = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(LogFormat())
    log.addHandler(handler)

    ascii_banner()

    config = load_config(base_path / 'config')
    logs_folder = Path(config.get('logsfolder', 'logs'))
    project_name = None
    threads = None

    parser = argparse.ArgumentParser(description="Auto Web Exploit Framework")
    parser.add_argument('-j', '--threads', type=int, help='Number of Threads')
    parser.add_argument('-p', '--project', type=str, help='Project Name')
    parser.add_argument('-f', '--folder', type=str, help='Report Path')
    parser.add_argument('-t', '--target', type=str, help='Target IP/domain')
    parser.add_argument('files', nargs='?', default='-', help='Targets file')
    args = parser.parse_args()

    targets = []
    if args.files != '-' and Path(args.files).is_file():
        with open(args.files, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
    elif args.target:
        targets.append(args.target)
    else:
        sys.exit('\n[?] Usage: python3 webxploit.py -h')

    threads = args.threads
    project_name = args.project or str(int(time.time()))
    if args.folder:
        logs_folder = Path(args.folder)

    current_run_dir = logs_folder / project_name
    try:
        current_run_dir.mkdir(parents=True, exist_ok=True)
        log.warning(f'Saving MSF logs at: {current_run_dir}')
    except Exception as e:
        sys.exit(f'\033[0;31m\033[1m[!]\033[0m Failed to create folder: {e}')

    log.critical('\n→→→→→→→→→→ Starting MSF Exploit ←←←←←←←←←←')

    generate_rcs(targets, threads, project_name, config, base_path, logs_folder)
    run_rcs(project_name, logs_folder)
    get_successful(project_name, logs_folder)

    generate_report(project_name, logs_folder, output_formats=['json', 'html', 'pdf'])
    log.critical(f'\n→→→→→→→→→→ Relatórios gerados em {logs_folder}/{project_name} ←←←←←←←←←←')
