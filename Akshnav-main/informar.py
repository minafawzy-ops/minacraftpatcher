import os
import mimetypes

# Directory to scan (run from inside Akshnav-main)
root_dir = "."

# Function to guess file purpose (same as before)
def guess_file_purpose(filename):
    if "Patch" in filename:
        return "Likely contains patching logic for Minecraft"
    if "MainWindow" in filename or "mainwindow" in filename:
        return "UI definition or code-behind for the app window"
    if "API" in filename:
        return "Handles external interactions or APIs"
    if "Settings" in filename:
        return "Configuration or settings management"
    if "AssemblyInfo" in filename:
        return "Assembly metadata (version, etc.)"
    if "ICLRRuntimeHost" in filename or "ICorRuntimeHost" in filename:
        return "CLR hosting for C++ interop"
    if filename.endswith(".csproj"):
        return "C# project file"
    if filename.endswith(".sln"):
        return "Visual Studio solution file"
    if filename == "README.md":
        return "Project documentation"
    if filename == "LICENSE":
        return "License agreement"
    return "Unknown purpose"

# Collect info from all files
output = []
for root, dirs, files in os.walk(root_dir):
    for file in files:
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, root_dir)
        
        # Basic file info
        file_info = f"File: {rel_path}\n"
        purpose = guess_file_purpose(file)
        file_info += f"Guessed Purpose: {purpose}\n"
        
        # Try to read content (all readable files)
        try:
            # Check if it's a text file
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and ("text" in mime_type or "xml" in mime_type or "json" in mime_type):
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                    # Limit content to avoid massive outputs; show full if < 10KB
                    if len(content) > 10240:  # 10KB
                        file_info += "Content (first 10KB):\n```\n" + content[:10240] + "\n[Truncated]\n```\n"
                    else:
                        file_info += "Content:\n```\n" + content + "\n```\n"
            else:
                file_info += "Content: [Binary or non-text file, skipped]\n"
        except Exception as e:
            file_info += f"Error reading content: {str(e)}\n"
        
        file_info += "-" * 50 + "\n"
        output.append(file_info)

# Write output to file
output_file = "akshnav_full_analysis.txt"
with open(output_file, "w", encoding="utf-8") as out_file:
    out_file.write("Akshnav-main Full Directory Analysis\n")
    out_file.write("=" * 40 + "\n\n")
    out_file.write("\n".join(output))

print(f"Full analysis complete! Check '{output_file}' in the directory.")
