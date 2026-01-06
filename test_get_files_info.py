from functions.get_files_info import get_files_info

result = get_files_info("calculator", ".")
print("Result for current directory:")
for line in result.split("\n"):
    if line:  # skip empty last line
        print(f"  {line}")

result = get_files_info("calculator", "pkg")
print("Result for current directory:")
for line in result.split("\n"):
    if line:  # skip empty last line
        print(f"  {line}")


result = get_files_info("calculator", "/bin")
print("Result for current directory:")
for line in result.split("\n"):
    if line:  # skip empty last line
        print(f"  {line}")


result = get_files_info("calculator", "../")
print("Result for current directory:")
for line in result.split("\n"):
    if line:  # skip empty last line
        print(f"  {line}")

