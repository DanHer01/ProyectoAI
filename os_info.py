import platform
import sys
import os


def get_os_info():
    info = {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "processor": platform.processor() or "Desconocido",
        "cpu_count": str(get_cpu_count()),
        "python_executable": sys.executable,
        "hostname": platform.node(),
        "user": os.getenv('USERNAME') or os.getenv('USER') or 'Desconocido',
        "home_directory": os.path.expanduser('~'),
    }
    return info


def get_cpu_count():
    try:
        import multiprocessing

        return multiprocessing.cpu_count()
    except Exception:
        return 1


def format_os_info(info):
    lines = [
        "═" * 50,
        "📊 ESPECIFICACIONES DEL SISTEMA",
        "═" * 50,
        "",
        "🖥️  SISTEMA OPERATIVO:",
        f"   Plataforma: {info['platform']} {info['platform_release']}",
        f"   Versión: {info['platform_version']}",
        f"   Arquitectura: {info['architecture']}",
        "",
        "💻 HARDWARE:",
        f"   Procesador: {info['processor']}",
        f"   Núcleos de CPU: {info['cpu_count']}",
        "",
        "🐍 PYTHON:",
        f"   Versión: {info['python_version']}",
        f"   Ejecutable: {info['python_executable']}",
        "",
        "👤 USUARIO:",
        f"   Nombre de usuario: {info['user']}",
        f"   Hostname: {info['hostname']}",
        f"   Directorio home: {info['home_directory']}",
        "",
        "═" * 50,
    ]
    return "\n".join(lines)
