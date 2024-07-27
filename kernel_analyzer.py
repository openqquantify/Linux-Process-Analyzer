import subprocess

def execute_commands(commands):
    results = {}
    for command, args, cmd_flags in commands:
        combined_flags = cmd_flags.get(command, []) + args
        result = subprocess.run([command] + combined_flags, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        results[command] = (result.stdout, result.stderr)
    return results

commands = [
    ("lscpu", [], {}),  
    ("ps", ["a", "u", "x"], {}),
    ("pidstat", ["-h"], {}),
    ("free", ["-m"], {}),
    ("vmstat", ["-a", "-s"], {}),
]

results = execute_commands(commands)
for command, (stdout, stderr) in results.items():
    print(f"{command}:\n{stdout}\n{'-'*40}\n{stderr}\n{'-'*40}")

if len(commands) > 0:
    top_command, top_args, _ = commands[-1]
    process = subprocess.Popen([top_command] + top_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        while True:
            output = process.stdout.readline()
            if not output:
                break
            print(output.strip())
    except KeyboardInterrupt:
        process.terminate()
    finally:
        process.wait()



