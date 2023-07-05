import create_model
import subprocess



result = subprocess.run(['python', 'create_model.py'], capture_output=True, text=True)

output = result.stdout

print(output)